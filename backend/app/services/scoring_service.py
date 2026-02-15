from .truecaller_handler import TruecallerService
from .country_service import CountryService
import logging
from typing import Dict, Any

# Configure Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ScoringEngine")

class ScoringEngine:
    """
    Advanced AI Intelligence Layer (Prompt #7)
    Aggregates data from multiple sources and calculates a confidence score (0-100).
    """

    def __init__(self):
        self.country_service = CountryService()
        self.truecaller_service = TruecallerService()

    async def analyze(self, phone: str, deep_search: bool = False) -> Dict[str, Any]:
        """
        Main Intelligence Function.
        Orchestrates calls to CountryService (Numverify/Scrapers) and Truecaller.
        """
        logger.info(f"Analyzing {phone} (Deep: {deep_search})")
        
        # 1. Base Validation
        base_data = await self.country_service.get_country_info(phone)
        if not base_data.get("valid"):
            return {
                "success": False,
                "message": base_data.get("message", "Invalid Number"),
                "confidence": 0.0
            }

        final_data = base_data.copy()
        sources_used = ["ValidationEngine"]
        
        # 2. Risk Scoring Logic (Simple Heuristic for now)
        risk_score = 0.0
        confidence = 0.8  # Start high for valid numbers
        
        # If Carrier is unknown, lower confidence
        if base_data.get("carrier") == "Unknown Carrier":
            confidence -= 0.2
            risk_score += 0.3
        
        # If Line Type is VoIP, increase risk
        if base_data.get("line_type") == "VoIP":
            risk_score += 0.6
            confidence -= 0.1

        # 3. Deep Search (Truecaller)
        if deep_search:
            tc_data = await self.truecaller_service.identify(phone, base_data.get("country"))
            
            if tc_data.get("success"):
                sources_used.append("TruecallerAI")
                # Merge Truecaller Data
                if tc_data.get("name"):
                    final_data["name"] = tc_data["name"]
                    confidence += 0.15 # Verified Name boosts confidence
                    
                if tc_data.get("carrier"):
                    final_data["carrier"] = tc_data["carrier"] # Prefer TC carrier
                
                # Check for Spam Score in TC data (mock logic if not provided)
                if tc_data.get("spam_score", 0) > 10:
                    risk_score += 0.8
                    final_data["spam_level"] = "High"
            else:
                # If TC fails, check if we have a verified manual override (e.g. Lokesh)
                # This logic is already inside country_service somewhat, but let's be sure.
                pass
        
        # Normalize Scores
        final_data["confidence"] = min(confidence, 1.0)
        final_data["risk_score"] = min(risk_score, 1.0)
        final_data["success"] = True
        final_data["sources"] = sources_used

        return final_data
