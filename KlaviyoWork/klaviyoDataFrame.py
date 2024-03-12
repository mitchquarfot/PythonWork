import os
import pandas as pd
from klaviyo_api import KlaviyoAPI

klaviyo_private_api_key = os.getenv('KLAVIYO_PRIVATE_API_KEY')
klaviyo = KlaviyoAPI(klaviyo_private_api_key, max_delay=60, max_retries=3, test_host=None)

def fetch_all_profiles():
    all_profiles_data = []
    cursor = None
    while True:
        response = klaviyo.Profiles.get_profiles(page={'cursor': cursor}) if cursor else klaviyo.Profiles.get_profiles()
        profiles = response.get('data', [])
        if not profiles:
            break
        
        for profile in profiles:
            attributes = profile.get('attributes', {})
            profile_id = profile.get('id')
            first_name = attributes.get('first_name', 'First name not found')
            last_name = attributes.get('last_name', 'Last name not found')
            properties = profile.get('attributes', {}).get('properties', {})
            shopify_tags = properties.get('Shopify Tags', [])
            if shopify_tags:
                all_profiles_data.append({
                    'Profile ID': profile_id,
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Shopify Tags': ", ".join(shopify_tags) if shopify_tags else 'No tags assigned'
            })

        cursor = response.get('next', {}).get('page', {}).get('cursor')
        if not cursor:
            break

    return all_profiles_data

# Fetch all profiles and their Shopify Tags
all_profiles_data = fetch_all_profiles()

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(all_profiles_data)

# Print or display the DataFrame
print(df)