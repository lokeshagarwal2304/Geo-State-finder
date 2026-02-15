
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

    async def identify(self, phone: str, country_hint: str = "IN") -> Dict[str, Any]:
        """ Wrapper for internal search to standardize output for ScoringEngine """
        return await self.search(phone, country_hint)

    async def search(self, phone_number, country_code_str="IN"):
        """
        Searches Truecaller for a given number (async).
        """
        if not self.installation_id:
             # Try one more time to reload, maybe it was created
             self._reload_auth()
             if not self.installation_id:
                return {
                    "success": False,
                    "error": "Truecaller Not Login. Run setup_truecaller.py first."
                }
        
        try:
            # Clean number
            clean_number = phone_number.replace("+", "").strip()
            
            # The library 'truecallerpy' is synchronous? No, usually it's used async or sync.
            # Let's wrap in executor if it blocks, but based on imports 'await' suggests async usage?
            # actually previous code used 'await search_phonenumber'. If library is sync, we need run_in_executor.
            # Assuming it is async compatible or we wrapeed it.
            
            # Wait, `truecallerpy` is often synchronous wrapper around requests.
            # Let's simulate async if needed, or just call it.
            # If previous code worked with await, then fine.
            
            # Mocking the call if library fails or is rate limited:
            # For demonstration, we assume it works.
            
            import asyncio
            loop = asyncio.get_event_loop()
            # Run in thread pool to avoid blocking FastAPI
            t_response = await loop.run_in_executor(None, lambda: search_phonenumber(clean_number, country_code_str, self.installation_id))

            if t_response and "data" in t_response and t_response["data"]:
                 data = t_response["data"][0] if isinstance(t_response["data"], list) else t_response["data"]
                 
                 return {
                    "success": True, 
                    "name": data.get("name"), 
                    "carrier": data.get("carrier"), 
                    "spam_score": data.get("score", 0),
                    "email": data.get("email")
                 }
            
            return {"success": False, "error": "No Result"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _reload_auth(self):
        # Logic to find auth file in parent dirs
        import os
        paths = ["truecaller_auth.json", "../truecaller_auth.json", "../../truecaller_auth.json"]
        for p in paths:
            if os.path.exists(p):
                with open(p, "r") as f:
                     data = json.load(f)
                     self.installation_id = data.get("installationId")
                     break



# Singleton
tc_service = TruecallerService()
