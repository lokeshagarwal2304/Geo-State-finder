from fastapi import FastAPI, Depends, HTTPException, Body
# from app.api.v1 import endpoints
from app.services.scoring_service import ScoringEngine
# from app.core.security import get_api_key
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Initialize App
app = FastAPI(
    title="CountryFinder AI",
    description="Global Phone Number Validation & Identity API",
    version="2.1.0"
)

# CORS (Frontend Access)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
scoring_engine = ScoringEngine()

# --- ROUTES ---

@app.post("/predict")
async def predict(
    payload: dict = Body(...),
    # api_key: str = Depends(get_api_key) # Disabled for local demo ease
):
    """
    Main Validation Endpoint.
    Uses Scoring Engine to return verified data + confidence scores.
    """
    input_text = payload.get("input")
    deep_search = payload.get("deep_search", False)
    
    if not input_text:
        raise HTTPException(status_code=400, detail="Input is required")

    result = await scoring_engine.analyze(input_text, deep_search)
    return result

@app.post("/contact")
async def contact(payload: dict = Body(...)):
    """ Contact Form Stub """
    print(f"📧 New Contact: {payload}")
    return {"status": "sent"}

# --- RUNNER ---
if __name__ == "__main__":
    import uvicorn
    # Run directly
    uvicorn.run(app, host="0.0.0.0", port=8000)
