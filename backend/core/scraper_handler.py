
import requests
from bs4 import BeautifulSoup
import logging
import re

# Setup Logging
logger = logging.getLogger("ScraperService")

class WebScraperService:
    def __init__(self):
        self.url = "https://www.findandtrace.com/trace-mobile-number-location"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': self.url,
            'Origin': 'https://www.findandtrace.com'
        }

    def trace(self, phone_number):
        """
        Scrapes findandtrace.com for Indian numbers to get State/Circle and Carrier.
        """
        try:
            # Clean number: Expected format is 10 digits for India
            clean_num = phone_number.replace(" ", "").replace("-", "").replace("+", "")
            
            # If start with 91 and length is 12, strip 91
            if len(clean_num) == 12 and clean_num.startswith("91"):
                 clean_num = clean_num[2:]
            
            # Simple check: This specific site is best for Indian numbers (10 digits)
            if len(clean_num) != 10 or not clean_num.isdigit():
                 return {"success": False, "error": "Scraper supports 10-digit Indian numbers only."}

            logger.info(f"Scraping info for {clean_num}...")
            
            data = {
                'mobilenumber': clean_num,
                'submit': 'Track Phone Number'
            }
            
            response = requests.post(self.url, data=data, headers=self.headers, timeout=8)
            
            if response.status_code != 200:
                 return {"success": False, "error": f"Site returned {response.status_code}"}

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find Data Table
            target_table = soup.find('table', id='customers')
            if not target_table:
                 # Fallback
                 tables = soup.find_all('table')
                 if not tables:
                     return {"success": False, "error": "No data table found."}
                 target_table = tables[0]
            
            # DEBUG
            print(target_table)

            result = {}
            rows = target_table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if len(cols) < 2: continue
                
                header = cols[0].get_text(strip=True)
                val = cols[1].get_text(strip=True)
                
                if "Telecoms Circle" in header or "State" in header:
                    result['state'] = val
                elif "Original Network" in header:
                    if "carrier" not in result: 
                        result['carrier'] = val
                elif "Service Provider" in header:
                    result['carrier'] = val
                elif "Connection Status" in header:
                    result['line_type'] = val # Map status to type roughly or just extra info

            if result:
                return {
                    "success": True,
                    "state": result.get("state"),
                    "carrier": result.get("carrier"),
                    "line_type": result.get("line_type"),
                    "method": "Web Scraper (FindAndTrace)"
                }
            
            return {"success": False, "error": "Data parsing failed."}

        except Exception as e:
            logger.error(f"Scraper Error: {e}")
            return {"success": False, "error": str(e)}

# Singleton
scraper_service = WebScraperService()
