import os 
from streamlit import session_state as ss
import streamlit as st
from streamlit_msal import Msal

# client_id = "<your-client-id>"
# authority = "https://login.microsoftonline.com/<your-tenant-id>"


def configure():
    with st.sidebar:
        auth_data = Msal.initialize_ui(
            client_id=os.environ["MSAL_CLIENT_ID"], authority=os.environ["MSAL_AUTHORITY"],
            sign_out_label="Sign Out 🍊",
            disconnected_label="Sign In...",sign_in_label="SU Login 🍊")

    if not auth_data:
        ss["account"] = None
        ss["session_id"] = "0"

    if auth_data:
        ss["account"] = auth_data["account"]
        ss["session_id"] = ss["account"]["localAccountId"]

configure()
st.title("Authetication Testing")
st.write(ss['account'])
st.write(ss['session_id'])

