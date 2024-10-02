import streamlit as st
from msal_streamlit_authentication import msal_authentication


st.title("Authetication")
if 'login_token' in st.session_state and st.session_state.get("login_token", None) is not None:
    st.write(f"Welcome, {st.session_state.username} ({st.session_state.email})")
else:
    st.write("Please login to access the application")

login_token = msal_authentication(
    auth={
        "clientId": "f6958edd-646f-4e84-895a-ede5aa18036e",
        "authority": "https://login.microsoftonline.com/4278a402-1a9e-4eb9-8414-ffb55a5fcf1e",
        "redirectUri": "http://localhost:8501/",
        "postLogoutRedirectUri": "http://localhost:8501/"
    }, # Corresponds to the 'auth' configuration for an MSAL Instance
    cache={
        "cacheLocation": "sessionStorage",
        "storeAuthStateInCookie": False
    }, # Corresponds to the 'cache' configuration for an MSAL Instance
    login_button_text="Login SUAD", # Optional, defaults to "Login"
    logout_button_text="Logout", # Optional, defaults to "Logout"
    class_name="css_button_class_selector", # Optional, defaults to None. Corresponds to HTML class.
    html_id="html_id_for_button", # Optional, defaults to None. Corresponds to HTML id.
    key=1 # Optional if only a single instance is needed
)
if login_token and st.session_state.get("login_token", None) is None:
    st.session_state.login_token = login_token
    st.session_state.username = login_token["idTokenClaims"]["name"]
    st.session_state.email = login_token["idTokenClaims"]["preferred_username"]
    if st.button("Continue"):
        st.rerun()
elif login_token is None and st.session_state.get("login_token", None) is not None:
    st.session_state.login_token = None
    st.session_state.username = None
    st.session_state.email = None
    if st.button("Continue"):
        st.rerun()        
