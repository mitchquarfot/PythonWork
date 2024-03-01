from klaviyo_api import KlaviyoAPI

klaviyo = KlaviyoAPI("pk_98a98159b54ae8eb74352839d0bf8df8e9", max_delay=60, max_retries=3, test_host=None)

# metrics = klaviyo.Metrics.get_metrics()
# print(metrics)

profiles = klaviyo.Profiles.get_profiles()
# print(profiles)

result = klaviyo.Profiles.get_profile(
    '01HQVAH8JCMQ83VPG9PV80FTDM'
    )

data = result['data']
attributes = data['attributes']
relationships = data['relationships']

# Extracting basic information
email = attributes.get('email', 'Email not found')
first_name = attributes.get('first_name', 'First name not found')
last_name = attributes.get('last_name', 'Last name not found')

# Extracting links
lists_self_link = relationships['lists']['links']['self']
lists_related_link = relationships['lists']['links']['related']
segments_self_link = relationships['segments']['links']['self']
segments_related_link = relationships['segments']['links']['related']

print(f"Email: {email}")
print(f"First Name: {first_name}")
print(f"Last Name: {last_name}")
# print("Lists self link:", lists_self_link)
# print("Lists related link:", lists_related_link)
# print("Segments self link:", segments_self_link)
# print("Segments related link:", segments_related_link)