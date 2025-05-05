import os
import requests
from datetime import datetime, timedelta

API_BASE = "https://api.cloudflare.com/client/v4/accounts"
API_BASE = f"{API_BASE}/{os.environ['CLOUDFLARE_ACCOUNT_ID']}/access/service_tokens"
HEADERS = {
    "Authorization": f"Bearer {os.environ['CLOUDFLARE_API_AUTHORIZATION_TOKEN']}",
    "Content-Type": "application/json",
    "X-Auth-Email": "nidhi.chaudhary@clevertap.com"
}

def get_tokens():
    response = requests.get(f"{API_BASE}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def is_expiring_soon(expiry_date_str):
    expiry_date = datetime.fromisoformat(expiry_date_str)
    return expiry_date <= datetime.utcnow() + timedelta(days=30)

def main():
    tokens = get_tokens()
    print(t for t in tokens)
    expiring = [t for t in tokens if is_expiring_soon(t["expires_at"])]
    if not expiring:
        print("✅ No tokens expiring in the next 30 days.")
    else:
        print("⚠️ Tokens expiring in the next 30 days:")
        for t in expiring:
            print(f" - {t['name']} (ID: {t['id']}, Expires: {t['expires_at']})")

        # Write to a temporary file so the next script can read it
        with open("/tmp/expiring_tokens.txt", "w") as f:
            for t in expiring:
                f.write(f"{t['id']}\n")
                print(f"🔄 Token ID {t['id']} written to /tmp/expiring_tokens.txt")

if __name__ == "__main__":
    main()
# This script lists all service tokens and checks if any are expiring in the next 30 days.