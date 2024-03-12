import requests
import os
import pandas as pd
from klaviyo_api import KlaviyoAPI

klaviyo_private_api_key = os.getenv('KLAVIYO_PRIVATE_API_KEY')

klaviyo = KlaviyoAPI(klaviyo_private_api_key, max_delay=60, max_retries=3, test_host=None)

# metrics = klaviyo.Metrics.get_metrics()
# print(metrics)

# profiles = klaviyo.Profiles.get_profiles()
# # print(profiles)

def fetch_all_profiles():
    all_profiles_data = []
    cursor = None  # Initialize the cursor for the first request
    while True:
        # Make the API call with the current cursor
        response = klaviyo.Profiles.get_profiles(page={'cursor': cursor}) if cursor else klaviyo.Profiles.get_profiles()
        profiles = response.get('data', [])
        if not profiles:
            break

    for profile in profiles:
        profile_id = profile.get('id')
        properties = profile.get('attributes', {}).get('properties', {})
        shopify_tags = properties.get('Shopify Tags', [])
        all_profiles_data.append({
            'Profile ID': profile_id,
            'Shopify Tags': ", ".join(shopify_tags) if shopify_tags else 'No tags assigned'
        })

        cursor = response.get('next', {}).get('page', {}).get('cursor')
        if not cursor:
            break

    return all_profiles_data

all_profiles_data = fetch_all_profiles()

df = pd.DataFrame(all_profiles_data)
print(df)

# result = klaviyo.Profiles.get_profile(
#     '01HQVAH8JCMQ83VPG9PV80FTDM'
#     )

# data = result['data']
# attributes = data['attributes']
# relationships = data['relationships']

# # Extracting basic information
# email = attributes.get('email', 'Email not found')
# first_name = attributes.get('first_name', 'First name not found')
# last_name = attributes.get('last_name', 'Last name not found')
# properties = attributes.get('properties',{})
# member_type = properties.get('Shopify Tags', [])
# if member_type:
#     member_type_str = ", ".join(member_type)
# else:
#     member_type_str = 'No tags assigned'

# # Extracting links
# lists_self_link = relationships['lists']['links']['self']
# lists_related_link = relationships['lists']['links']['related']
# segments_self_link = relationships['segments']['links']['self']
# segments_related_link = relationships['segments']['links']['related']

# print(f"Email: {email}")
# print(f"First Name: {first_name}")
# print(f"Last Name: {last_name}")
# print(f"Shopify Tags: {member_type_str}")

# print(result)
# print("Lists self link:", lists_self_link)
# print("Lists related link:", lists_related_link)
# print("Segments self link:", segments_self_link)
# print("Segments related link:", segments_related_link)