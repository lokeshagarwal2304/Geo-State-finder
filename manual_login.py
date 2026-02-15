
import asyncio
from truecallerpy import login, verify_otp
import json
import os

async def manual_login():
    print("Manual Truecaller Login")
    print("-----------------------")
    phone = input("Enter Phone Number (e.g. +919999999999): ").strip()
    
    print("Sending OTP...")
    try:
        res = await login(phone)
        print("Response:", res)
        
        if res['status'] == 1 or res['status'] == 9:
            print("OTP Sent!")
            otp = input("Enter OTP: ").strip()
            v_res = await verify_otp(phone, res['data'], otp)
            print("Verify Result:", v_res)
            
            if not v_res['data']['suspended']:
                print("Success! Saving token...")
                with open("backend/truecaller_auth.json", "w") as f:
                    token_data = {
                        "installationId": v_res['data']['installationId'],
                        "phone": phone
                    }
                    json.dump(token_data, f)
                print("Token saved to backend/truecaller_auth.json")
            else:
                print("Account Suspended!")
        else:
            print("Failed to send OTP. Try again later.")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(manual_login())
