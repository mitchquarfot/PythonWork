import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['XXX','XXX']).generate()

print(hashed_passwords)