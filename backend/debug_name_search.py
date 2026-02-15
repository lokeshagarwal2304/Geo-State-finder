
import requests
from bs4 import BeautifulSoup
import re

def duckduckgo_search(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []
            for link in soup.find_all('a', class_='result__a'):
                title = link.get_text()
                href = link.get('href')
                results.append((title, href))
            return results
    except Exception as e:
        print(f"DDG Error: {e}")
        return []

def search_number_name(number):
    # Try multiple query variants
    queries = [
        f'"{number}" truecaller',
        f'"{number}" owner name',
        f'"{number}"'
    ]
    
    for q in queries:
        print(f"Searching for: {q}")
        results = duckduckgo_search(q)
        if not results: continue
        for title, link in results:
            print(f"Found: {title}")
            # Heuristic: Truecaller links often contain the name in title
            # e.g. "Lokesh Agarwal - Truecaller"
            
            if "truecaller" in link or "truecaller" in title.lower():
                # Extract potential name
                # Format often: "Name - Location - Phone Number"
                parts = title.split("-")
                if len(parts) > 0:
                    potential_name = parts[0].strip()
                    # Filter out generic terms
                    if "truecaller" not in potential_name.lower() and not potential_name.startswith("+"):
                        print(f"POSSIBLE NAME: {potential_name}")
                        return potential_name

if __name__ == "__main__":
    search_number_name("+919154151265")
