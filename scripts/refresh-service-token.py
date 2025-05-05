import os
import requests

API_BASE = "https://api.cloudflare.com/client/v4/accounts"
API_BASE = f"{API_BASE}/{os.environ['CLOUDFLARE_ACCOUNT_ID']}/access/service_tokens"
HEADERS = {
    "Authorization": f"Bearer {os.environ['CLOUDFLARE_API_AUTHORIZATION_TOKEN']}",
    "Content-Type": "application/json",
    "X-Auth-Email": "nidhi.chaudhary@clevertap.com"
}

def refresh_token(token_id):
    response = requests.post(f"{API_BASE}/{token_id}/refresh", headers=HEADERS)
    if response.status_code == 200:
        print(f"🔄 Refreshed token {token_id}")
    else:
        print(f"❌ Failed to refresh token {token_id}: {response.status_code} - {response.text}")

def main():
    try:
        with open("/tmp/expiring_tokens.txt", "r") as f:
            token_ids = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("✅ No expiring tokens to refresh.")
        return

    for token_id in token_ids:
        refresh_token(token_id)

if __name__ == "__main__":
    main()
