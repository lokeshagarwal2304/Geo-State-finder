
import phonenumbers
from phonenumbers import phonenumberutil, geocoder, carrier, timezone
import pycountry
from thefuzz import process, fuzz
import re
import random
try:
    from core.indian_series import get_circle_from_series
except ImportError:
    # Fallback for direct execution
    from indian_series import get_circle_from_series

class CountryFinderAI:
    def _refine_state(self, location, country_name, parsed_number):
         # If phonenumbers gave us a specific location (State), use it.
         if location and location != country_name:
             return location
             
         # If not, check our static map for India
         if parsed_number.country_code == 91:
             region = get_circle_from_series(str(parsed_number.national_number))
             if region: return region
             
         return "Entire Country"

    def __init__(self):
        self.code_to_data = {}
        self.name_to_code = {}
        self.country_names = []
        
        # Build Knowledge Base
        self._train_model()

    def _train_model(self):
        print("Training AI Model on Country Data...")
        for country in pycountry.countries:
            try:
                code = str(phonenumbers.country_code_for_region(country.alpha_2))
                if code == "0": continue

                entry = {
                    "name": country.name,
                    "alpha_2": country.alpha_2,
                    "code": f"+{code}",
                    "flag": self._get_flag_emoji(country.alpha_2)
                }
                
                # Bi-directional mapping + Normalization
                if code not in self.code_to_data: self.code_to_data[code] = entry
                clean_name = country.name.lower()
                self.name_to_code[clean_name] = entry
                self.country_names.append(clean_name)
                
                if hasattr(country, 'common_name'):
                     self.name_to_code[country.common_name.lower()] = entry
                     self.country_names.append(country.common_name.lower())

            except Exception:
                continue

    def _get_flag_emoji(self, country_code):
        return chr(ord(country_code[0]) + 127397) + chr(ord(country_code[1]) + 127397)

    def predict(self, user_input: str):
        clean_input = user_input.strip()
        
        # Check if Input is a Phone Number
        if re.match(r'^(\+)?\d+(\s\d+)*$', clean_input):
            return self._predict_from_number(clean_input)

        # Check if Input is Text
        return self._predict_from_text(clean_input)

    def _predict_from_number(self, phone_input):
        try:
            # Handle + prefix and spaces
            if phone_input.startswith("00"): phone_input = "+" + phone_input[2:]
            elif not phone_input.startswith("+"): phone_input = "+" + phone_input
            
            try:
                parsed_number = phonenumbers.parse(phone_input, None)
            except phonenumbers.NumberParseException:
                 # Fallback to direct code lookup
                 clean_code = phone_input.replace("+", "").strip()
                 if clean_code in self.code_to_data:
                     data = self.code_to_data[clean_code]
                     return {
                        "success": True,
                        "country": data["name"],
                        "code": data["code"],
                        "state": "All Regions",
                        "carrier": "N/A",
                        "type": "Code Prefix",
                        "timezone": "Multiple",
                        "flag": data["flag"],
                        "confidence": 0.99,
                        "formatted": data["code"],
                        "method": "direct_code_lookup"
                     }
                 return {"success": False, "error": "Invalid Number Format"}

            # Core Attributes
            region_code = phonenumbers.region_code_for_number(parsed_number)
            is_valid = phonenumbers.is_valid_number(parsed_number)
            
            country_name = "Unknown"
            if region_code:
                country = pycountry.countries.get(alpha_2=region_code)
                country_name = country.name if country else region_code
            
            # Detailed Info (The "Practical" Stuff)
            location = geocoder.description_for_number(parsed_number, "en") # State/City
            carrier_name = carrier.name_for_number(parsed_number, "en")     # Network
            time_zones = timezone.time_zones_for_number(parsed_number)      # Timezone list
            
            # Number Type (Mobile vs Landline)
            num_type = phonenumbers.number_type(parsed_number)
            type_str = "Unknown"
            if num_type == phonenumbers.PhoneNumberType.MOBILE: type_str = "Mobile"
            elif num_type == phonenumbers.PhoneNumberType.FIXED_LINE: type_str = "Landline"
            elif num_type == phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: type_str = "Fixed/Mobile"
            elif num_type == phonenumbers.PhoneNumberType.TOLL_FREE: type_str = "Toll Free"
            elif num_type == phonenumbers.PhoneNumberType.PREMIUM_RATE: type_str = "Premium Rate"
            elif num_type == phonenumbers.PhoneNumberType.VOIP: type_str = "VoIP"

            # Formatting
            formatted_intl = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            formatted_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)

            return {
                "success": True,
                "country": country_name,
                "code": f"+{parsed_number.country_code}",
                "state": self._refine_state(location, country_name, parsed_number),
                "carrier": carrier_name if carrier_name else "Detailed Carrier N/A",
                "type": type_str,
                "timezone": ", ".join(time_zones) if time_zones else "Unknown",
                "flag": self._get_flag_emoji(region_code) if region_code else "🏳️",
                "formatted": formatted_intl,
                "local_format": formatted_national,
                "valid": is_valid,
                "confidence": 1.0 if is_valid else 0.7,
                "method": "deep_number_analysis"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _predict_from_text(self, text_input):
        # NLP Logic (unchanged from good version)
        stop_words = ["code", "dial", "dialing", "phone", "number", "for", "of", "what", "is", "the", "country", "call", "location", "lookup"]
        words = re.findall(r'\b\w+\b', text_input.lower())
        filtered_words = [w for w in words if w not in stop_words]
        
        if not filtered_words: return {"success": False, "error": "Could not understand text query."}
        
        search_query = " ".join(filtered_words)
        best_match, score = process.extractOne(search_query, self.country_names, scorer=fuzz.token_set_ratio)
        
        if score > 70:
            country_data = self.name_to_code[best_match]
            return {
                "success": True,
                "country": country_data["name"],
                "code": country_data["code"],
                "state": "N/A",
                "carrier": "N/A",
                "type": "Country Match",
                "timezone": "N/A",
                "flag": country_data["flag"],
                "formatted": country_data["code"],
                "confidence": score / 100.0,
                "method": "nlp_fuzzy_logic"
            }
        
        return {"success": False, "error": f"No country found for '{text_input}'", "confidence": 0.0}

ai_engine = CountryFinderAI()
