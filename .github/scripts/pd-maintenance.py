#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta, UTC
import json
import os
import sys

def create_maintenance_window(service_id):
    url = "https://api.pagerduty.com/maintenance_windows"
    headers = {
        "Authorization": f"Token token={os.environ.get('CLEVERTAP_SNE_PD_AUTHORIZATION_TOKEN')}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    start_time = datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')
    end_time = (datetime.now(UTC) + timedelta(minutes=30)).isoformat(timespec='seconds').replace('+00:00', 'Z')
    data = {
        "maintenance_window": {
            "type": "service",
            "description": "Scheduled maintenance",
            "start_time": start_time,
            "end_time": end_time,
            "services": service_id
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to create maintenance window: {e}")
        return None

def get_services_id():
    url = "https://api.pagerduty.com/services"
    headers = {
        "Authorization": f"Token token={os.environ.get('CLEVERTAP_SNE_PD_AUTHORIZATION_TOKEN')}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch service IDs: {e}")
        return None

if __name__ == "__main__":
    services_response = get_services_id()
    if services_response and 'services' in services_response:
        try:
            service_data = [{"id": s['id'], "type": "service"} for s in services_response['services']]
            maintenance_window = create_maintenance_window(service_data)
            if maintenance_window:
                print("Maintenance window created:", json.dumps(maintenance_window, indent=2))
            else:
                print("[ERROR] Could not create maintenance window.")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
    else:
        print("[ERROR] No services found or failed to retrieve service data.")
        sys.exit(1)
