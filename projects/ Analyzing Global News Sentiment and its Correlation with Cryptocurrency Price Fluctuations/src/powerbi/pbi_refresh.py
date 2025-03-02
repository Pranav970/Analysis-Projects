import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

POWER_BI_GROUP_ID = os.getenv("POWER_BI_GROUP_ID")  # Workspace ID
POWER_BI_DATASET_ID = os.getenv("POWER_BI_DATASET_ID")
POWER_BI_CLIENT_ID = os.getenv("POWER_BI_CLIENT_ID")
POWER_BI_CLIENT_SECRET = os.getenv("POWER_BI_CLIENT_SECRET")
POWER_BI_TENANT_ID = os.getenv("POWER_BI_TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{POWER_BI_TENANT_ID}"
RESOURCE = "https://analysis.windows.net/powerbi/api"

def get_power_bi_token():
    """
    Gets an access token from Azure Active Directory.
    """
    url = f"{AUTHORITY}/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': POWER_BI_CLIENT_ID,
        'client_secret': POWER_BI_CLIENT_SECRET,
        'resource': RESOURCE
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error getting access token: {response.status_code} - {response.text}")
        return None

def refresh_power_bi_dataset(dataset_id, group_id, access_token):
    """
    Refreshes a Power BI dataset.
    """
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 202:
        print("Power BI dataset refresh initiated successfully.")
    else:
        print(f"Error refreshing dataset: {response.status_code} - {response.text}")

if __name__ == '__main__':
    # Example usage:
    dataset_id = POWER_BI_DATASET_ID
    group_id = POWER_BI_GROUP_ID

    access_token = get_power_bi_token()
    if access_token:
        refresh_power_bi_dataset(dataset_id, group_id, access_token)
