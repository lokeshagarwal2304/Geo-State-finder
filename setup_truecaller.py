
"""
Truecaller Setup Tool (Final Robust Version)

This script helps you log in to Truecaller. 
It auto-cleans your phone number to prevent format errors.
"""

import asyncio
import json
import os
import sys
import re

# Try to import truecallerpy, install if missing
try:
    import truecallerpy
    from truecallerpy import login, verify_otp
except ImportError:
    import subprocess
    print("Installing truecallerpy...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "truecallerpy"])
    from truecallerpy import login, verify_otp

async def main():
    print("=========================================")
    print("   Truecaller Login Setup")
    print("=========================================")
    print("NOTE: You do NOT need a VPN. Just use your standard connection.")
    print("If this fails, you can still use the app for Carrier/State detection!")
    print("=========================================\n")
    
    raw_input = input("Enter your full phone number (e.g. +91 999 999 9999): ").strip()
    
    # 1. Heavy Cleaning (Remove all non-numeric except +)
    # This turns "+91 9154-151 265" into "+919154151265"
    phone_number = "+" + "".join(filter(str.isdigit, raw_input))
    
    # Ensure it looks right
    print(f"\nProcessing Number: {phone_number}")
    
    if len(phone_number) < 10:
        print("Error: Number looks too short. Please try again.")
        return

    print(f"Requesting OTP...")
    
    try:
        # Step 1: Login (Send OTP)
        otp_response = await login(phone_number)
        
        # Parse Response
        data = otp_response.get('data', {}) if isinstance(otp_response, dict) else otp_response
        
        # Check Success
        if (data and (data.get("status") == 1 or data.get("status") == 9 or str(data.get("status")) == "1")):
             print("\n[SUCCESS] OTP Sent Successfully!")
             print("Check your SMS.")
             
             # Step 2: Verify OTP
             otp = input("Enter the 6-digit OTP: ").strip()
             
             print("Verifying...")
             verify_response = await verify_otp(phone_number, data, otp)
             verify_data = verify_response.get('data', {}) if isinstance(verify_response, dict) else verify_response
             
             if not verify_data.get("suspended") and "installationId" in verify_data:
                 token_data = {
                     "installationId": verify_data["installationId"],
                     "phone": phone_number
                 }
                 
                 os.makedirs("backend", exist_ok=True)
                 path = "backend/truecaller_auth.json"
                 
                 with open(path, "w") as f:
                     json.dump(token_data, f)
                 
                 print(f"\n[SUCCESS] Logged in.")
                 print("Restart the backend to see Names.")
             else:
                 print("\n[FAIL] OTP Verification Failed.")
                 print(f"Server Message: {verify_data.get('message', 'Unknown')}")
        
        else:
             print("\n[FAIL] Failed to send OTP.")
             msg = data.get('message', 'Unknown Error')
             print(f"Server Message: {msg}")
             
             if "limit" in msg.lower() or "verification failed" in msg.lower():
                 print("\n[INFO] Tip: Truecaller is strictly limiting new logins from this IP.")
                 print("SUGGESTION: Skip this step. The app still works for Carrier & State detection!")

    except Exception as e:
         print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
