import requests
import os
from klaviyo_api import KlaviyoAPI

klaviyo_private_api_key = os.getenv('KLAVIYO_PRIVATE_API_KEY')

url = "https://a.klaviyo.com/api/profiles/01HQVAH8JCMQ83VPG9PV80FTDM/"

headers = {
    "accept": "application/json",
    "revision": "2024-02-15",
    "Authorization": f"Klaviyo-API-Key {klaviyo_private_api_key}"
}

response = requests.get(url, headers=headers)

print(response.text)