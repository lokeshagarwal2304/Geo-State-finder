from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
import os

API_KEY_NAME = "x-api-key"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Simple API Key storage (In real SaaS, store in DB/Redis)
API_KEYS = [
    "demo-key-123456",  # Public Demo Key
    "growth-key-abcdef",
    "enterprise-key-secure"
]

async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header in API_KEYS:
        return api_key_header
    # For now, allow requests without key for frontend demo simplicity
    # In production, raise HTTP_403_FORBIDDEN
    if not api_key_header: 
        return "public-demo"
    
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
