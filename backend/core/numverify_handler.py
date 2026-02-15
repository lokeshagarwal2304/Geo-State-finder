
import requests
import os
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NumverifyService")

class NumverifyService:
    def __init__(self, api_key=None):
        # API Key management
        self.api_key = api_key or os.getenv("NUMVERIFY_API_KEY") 
        self.base_url = "http://apilayer.net/api/validate"

    def validate(self, phone_number):
        """
        Fetches details from Numverify API.
        """
        if not self.api_key:
            logger.warning("Numverify API Key not set.")
            return {"success": False, "error": "API Key Missing"}

        # Format number (Numverify prefers international format without + often, or with +? 
        # Documentation usually creates URL with number=1415... (no plus).
        # But let's try strict digits.
        clean_number = phone_number.replace("+", "").strip()

        params = {
            'access_key': self.api_key,
            'number': clean_number,
            'country_code': '', 
            'format': 1
        }

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()

            if "success" in data and not data["success"]:
                # API returned an error (e.g. invalid key, limit reached)
                error_msg = data.get("error", {}).get("info", "Unknown Error")
                logger.error(f"Numverify Error: {error_msg}")
                return {"success": False, "error": error_msg}

            if data.get("valid"):
                return {
                    "success": True,
                    "country": data.get("country_name"),
                    "location": data.get("location"),  # This is usually the State/City
                    "carrier": data.get("carrier"),
                    "line_type": data.get("line_type"),
                    "local_format": data.get("local_format"),
                    "international_format": data.get("international_format")
                }
            else:
                 return {
                     "success": False,
                     "error": "Number invalid per Numverify" 
                 }

        except Exception as e:
            logger.error(f"Numverify Exception: {e}")
            return {"success": False, "error": str(e)}

# Singleton
nv_service = NumverifyService()
