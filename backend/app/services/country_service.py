import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CountryService:
    def __init__(self):
        # Scraping headers if needed
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    async def get_country_info(self, phone: str):
        default_resp = {
            "success": False, "valid": False, "country": "Unknown", "code": "", 
            "carrier": "Unknown Carrier", "line_type": "Unknown", "formatted": phone,
            "region": "Unknown"
        }
        
        try:
            # 1. Parse with Google Libphonenumber
            try:
                z = phonenumbers.parse(phone, None)
            except phonenumbers.NumberParseException:
                # Try simple cleaning
                 clean = "+" + re.sub(r'[^0-9]', '', phone)
                 try:
                     z = phonenumbers.parse(clean, None)
                 except:
                     return default_resp
            
            if not phonenumbers.is_valid_number(z):
                return {**default_resp, "message": "Invalid Number Format"}

            # 2. Extract Data
            country = geocoder.description_for_number(z, "en")
            carrier_name = carrier.name_for_number(z, "en")
            tz = timezone.time_zones_for_number(z)
            formatted = phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            e164 = phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.E164)
            
            # Simple Type Logic
            import phonenumbers.number_type_map
            type_code = phonenumbers.number_type(z) # 1=Mobile, 2=Fixed, etc
            line_type = "Fixed Line"
            if type_code == 1: line_type = "Mobile"
            elif type_code == 2: line_type = "Fixed Line"
            elif type_code == 3: line_type = "Toll Free"
            elif type_code == 4: line_type = "VoIP"
            
            # Scrape Override for India (Since Google Lib is generic for India states)
            state = "Entire Country"
            if z.country_code == 91:
                # Simple mapping based on Circle codes (heuristic) or just use geocoder
                # Actually google lib gives 'India' only.
                # Let's try to get more detail if carrier is present
                if not carrier_name:
                     carrier_name = "Unknown (India)"
                
                # Mock refined state for demo if strictly +91
                # In real app, we use HLR lookup API here
                pass
            else:
                state = country # For USA it returns 'CA' etc.

            return {
                "success": True,
                "valid": True,
                "country": country,
                "code": f"+{z.country_code}",
                "formatted": formatted,
                "carrier": carrier_name or "Unknown Carrier",
                "line_type": line_type,
                "state": state,
                "timezone": list(tz)[0] if tz else "UTC"
            }

        except Exception as e:
            logger.error(f"Error in CountryService: {e}")
            return default_resp
