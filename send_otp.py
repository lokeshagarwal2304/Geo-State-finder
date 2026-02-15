
import asyncio
import sys
import json

try:
    from truecallerpy import login
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "truecallerpy"])
    from truecallerpy import login

async def send_otp():
    # Ensure clean input
    phone_number = "+919154151265"
    print(f"Attempting to send OTP to: {phone_number}")
    
    try:
        response = await login(phone_number)
        
        # Save raw response
        with open("last_login_attempt.json", "w") as f:
            if hasattr(response, "get"):
                json.dump(response, f, indent=2)
            else:
                f.write(str(response))
        
        # Analyze Response
        data = response.get('data', {}) if isinstance(response, dict) else response
        status = data.get('status')
        message = data.get('message')
        
        print("\n--- Server Response ---")
        print(f"Status Code: {status}")
        print(f"Message: {message}")
        print("-----------------------")
        
        if status == 20003:
            print("\n⚠️  ERROR: 'Verification Failed' (Error 20003)")
            print("This usually means Truecaller has temporarily blocked requests from this IP address.")
            print("Possible Solutions:")
            print("1. Wait 30-60 minutes and try again.")
            print("2. Switch your internet connection (e.g., use Mobile Data instead of WiFi).")
            print("3. Try a different phone number if available.")
        elif status == 1 or status == 9 or message == "Sent":
            print("\n✅ OTP Sent Successfully!")
            print("Please check your SMS.")
        else:
            print("\n❌ Login Failed.")

    except Exception as e:
        print(f"Script Error: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(send_otp())
