import streamlit as st
import os
import pandas as pd
from klaviyo_api import KlaviyoAPI

def initialize_klaviyo():
    klaviyo_private_api_key = os.getenv('KLAVIYO_PRIVATE_API_KEY')
    return KlaviyoAPI(klaviyo_private_api_key, max_delay=60, max_retries=3, test_host=None)

def fetch_profiles_by_member_type(selected_member_type):
    klaviyo = initialize_klaviyo()
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
            if selected_member_type in shopify_tags:
                all_profiles_data.append({
                    'Profile ID': profile_id,
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Shopify Tags': ", ".join(shopify_tags) if shopify_tags else 'No tags assigned'
            })

        cursor = response.get('next', {}).get('page', {}).get('cursor')
        if not cursor:
            break

    return pd.DataFrame(all_profiles_data)

st.title('Greyson Membership Customer List')
member_types = [
    'Black Wolf Member',
    'Crimson Wolf Member',
    'Spirit Wolf Member',
    'Silver Wolf Member'
]
# Application formatting
klaviyo_logo_url = 'https://images.ctfassets.net/lzny33ho1g45/2y8TzsQ1uuOzjGXZgbqmZS/664ebbf2f55885c92de263f112eb4827/add-klaviyo-subscribers-for-shopify-purchases-00-hero.jpg?w=1520&fm=jpg&q=30&fit=thumb&h=760'
greyson_logo_url = 'https://media.licdn.com/dms/image/C4E03AQEITDf6pUQZ8w/profile-displayphoto-shrink_800_800/0/1580833996476?e=2147483647&v=beta&t=Hp1b4tFiMPnCPqJx-qQUkG3NY9c3s-gTKF6Gl7z87JI'
# st.image(klaviyo_logo_url, width=250)
st.image(greyson_logo_url, width=500)

# Application interaction
selected_member_type = st.selectbox('Select Member Type:', member_types)

if st.button('Fetch Profiles'):
    df = fetch_profiles_by_member_type(selected_member_type)
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No profiles found for selected member type.")