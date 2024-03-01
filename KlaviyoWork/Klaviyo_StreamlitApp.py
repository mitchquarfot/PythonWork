from secrets import secrets
import streamlit as st
from klaviyo_api import KlaviyoAPI

klaviyo_private_api_key = secrets.get('klaviyo_private_api_key')

klaviyo = KlaviyoAPI(klaviyo_private_api_key, max_delay=60, max_retries=3, test_host=None)

# Streamlit app title
st.title('Klaviyo Profile and Segment Details Viewer')

# User input for profile ID
profile_id = st.text_input('Enter Profile ID:', '')

# Button to trigger the API call
if st.button('Get Profile Details'):
    if profile_id:
        try:
            # API call to get profile details
            result = klaviyo.Profiles.get_profile(profile_id)
            
            if result:
                data = result['data']
                attributes = data['attributes']
                relationships = data['relationships']
                
                # Extracting basic information
                email = attributes.get('email', 'Email not found')
                first_name = attributes.get('first_name', 'First name not found')
                last_name = attributes.get('last_name', 'Last name not found')
                
                # Displaying the information
                st.write(f"Email: {email}")
                st.write(f"First Name: {first_name}")
                st.write(f"Last Name: {last_name}")
                
                # Extracting and displaying links
                lists_self_link = relationships['lists']['links']['self']
                lists_related_link = relationships['lists']['links']['related']
                segments_self_link = relationships['segments']['links']['self']
                segments_related_link = relationships['segments']['links']['related']
                
                st.write(f"Lists Self Link: {lists_self_link}")
                st.write(f"Lists Related Link: {lists_related_link}")
                st.write(f"Segments Self Link: {segments_self_link}")
                st.write(f"Segments Related Link: {segments_related_link}")
                
            else:
                st.error('Profile not found. Please check the Profile ID and try again.')
        except Exception as e:
            st.error(f'An error occurred: {e}')
    else:
        st.error('Please enter a Profile ID.')
