import instaloader
import os

def export_session():
    print("--- Instagram Session Repair (Free Way) ---")
    print("Since your browser's security blocked the automated tool, let's do it manually.")
    print("It only takes 30 seconds!\n")
    
    print("1. Go to Instagram in your browser (Chrome or Edge).")
    print("2. Press F12 -> Application tab -> Cookies -> www.instagram.com")
    print("3. Copy the value of the 'sessionid' cookie.")
    print("-" * 40)
    
    sessionid = input("\nPaste your Instagram 'sessionid' here: ").strip()
    username = input("Enter your Instagram username: ").strip()
    
    if not sessionid or not username:
        print("❌ Error: Both username and sessionid are required.")
        return

    L = instaloader.Instaloader()
    try:
        # Create a session manually
        L.context._session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        L.save_session_to_file(filename=f"session-{username}")
        print(f"\n✅ SUCCESS! Session file created for @{username}.")
        print("The Audit Engine will now use your human session to bypass blocks.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    export_session()
