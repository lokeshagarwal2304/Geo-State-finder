from pydantic import BaseModel
from typing import Optional, List

# Basic Response Model
class ValidationResponse(BaseModel):
    success: bool
    formatted: Optional[str] = None
    valid: bool
    country: Optional[str] = None
    code: Optional[str] = None
    carrier: Optional[str] = "N/A"
    type: Optional[str] = "Unknown"
    state: Optional[str] = "N/A"
    name: Optional[str] = "N/A"
    risk_score: Optional[float] = 0.0
    confidence: Optional[float] = 0.0
    message: Optional[str] = None
    sources: Optional[List[str]] = []

# Input Model
class PhoneInput(BaseModel):
    input: str
    deep_search: bool = False
