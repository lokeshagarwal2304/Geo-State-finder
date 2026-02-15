
import json
import logging
from truecallerpy import search_phonenumber
import asyncio

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TruecallerService")

class TruecallerService:
    def __init__(self, installation_id=None):
        self.installation_id = installation_id
        # Try to load ID from a local file if not provided
        if not self.installation_id:
            try:
                # Assuming the file is in backend/ as it was saved there.
                with open("truecaller_auth.json", "r") as f:
                    data = json.load(f)
                    self.installation_id = data.get("installationId")
                    logger.info("Truecaller Auth Token Loaded Successfully.")
            except FileNotFoundError:
                try: 
                    # Try looking parent dir if running from subfolder
                    with open("../truecaller_auth.json", "r") as f:
                        data = json.load(f)
                        self.installation_id = data.get("installationId")
                        logger.info("Truecaller Auth Token Loaded Successfully (Parent Dir).")
                except:
                    logger.warning("Truecaller Auth File NOT FOUND. Creating empty service.")
                    self.installation_id = None

    async def search(self, phone_number, country_code_str="IN"):
        """
        Searches Truecaller for a given number (async).
        """
        if not self.installation_id:
            return {
                "success": False,
                "error": "Truecaller Not Login. Run setup_truecaller.py first."
            }

        try:
            # Clean number: if it starts with +, strip it.
            clean_number = phone_number.replace("+", "").strip()
            
            # Use Library - AWAIT!
            # search_phonenumber(phone_number, country_code, installation_id)
            t_response = await search_phonenumber(clean_number, country_code_str, self.installation_id)
            
            # Check if valid JSON response or error object
            if t_response and "data" in t_response and t_response["data"]:
                data = t_response["data"][0] # Usually a list
                
                return {
                    "success": True,
                    "name": data.get("name", "Unknown Name"),
                    "carrier": data.get("carrier", "Unknown Carrier"),
                    "email": data.get("email", None),
                    "city": data.get("city", None),
                    "address": data.get("address", None),
                    "score": data.get("score", 0),
                    "image": data.get("image", None),
                    "source": "Truecaller API"
                }

            return {"success": False, "error": f"No data found. Resp: {t_response.get('error') or 'Empty'}"}

        except Exception as e:
            logger.error(f"Truecaller API Error: {e}")
            return {"success": False, "error": str(e)}

# Singleton
tc_service = TruecallerService()
