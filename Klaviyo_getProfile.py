import requests

url = "https://a.klaviyo.com/api/profiles/01HQVAH8JCMQ83VPG9PV80FTDM/"

headers = {
    "accept": "application/json",
    "revision": "2024-02-15",
    "Authorization": "Klaviyo-API-Key pk_98a98159b54ae8eb74352839d0bf8df8e9"
}

response = requests.get(url, headers=headers)

print(response.text)