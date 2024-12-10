from  add_parent_path import add_parent_path
add_parent_path(1)
import sys
import os

import streamlit as st
from streamlit_msal import Msal
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dal.models import AuthModel


def configure():
    with st.sidebar:
        auth_data = Msal.initialize_ui(
            client_id=os.environ["MSAL_CLIENT_ID"], authority=os.environ["MSAL_AUTHORITY"],
            sign_out_label="Sign Out 🍊",
            disconnected_label="Sign In...",sign_in_label="SU Login 🍊")

    if not auth_data:
        st.session_state.auth_data = None
        st.session_state.auth_model = None

    if auth_data:
        st.session_state.auth_data = auth_data
        st.session_state.auth_model = AuthModel.from_auth_data(auth_data)
        st.session_state.mongodb = MongoClient(os.environ.get("MONGODB_CONNSTR") , server_api=ServerApi('1')).get_database("chatapp")

st.set_page_config(page_title="ChatApp manager", page_icon=":material/edit:")

not_logged_in_page = st.Page("not_logged_in.py", title="Welcome to the ChatApp Manager", icon=":material/home:")
home_page = st.Page("home.py", title="My Apps", icon=":material/home:")
logs_page = st.Page("logs.py", title="Fetch Logs", icon=":material/assignment:")
create_page = st.Page("create.py", title="Create App", icon=":material/add_circle:")
preview_page = st.Page("preview.py", title="Preview App", icon=":material/preview:")
edit_page = st.Page("edit.py", title="Edit App", icon=":material/edit:")
delete_page = st.Page("delete.py", title="Delete App", icon=":material/delete:")
info_page = st.Page("info.py", title="Auth Info", icon=":material/info:")

configure()
if 'auth_data'in st.session_state and st.session_state.auth_data is not None:
    pg = st.navigation([home_page, create_page, preview_page, edit_page, logs_page, delete_page, info_page]) 
else:
    pg = st.navigation([not_logged_in_page])

pg.run()






















# import streamlit as st
# from streamlit_msal import Msal

# with st.sidebar:
#     token = Msal.initialize_ui(
#         client_id=client_id,
#         authority=authority,
#         scopes=[], # Optional
#         # Customize (Default values):
#         connecting_label="Connecting",
#         disconnected_label="Disconnected",
#         sign_in_label="Sign in",
#         sign_out_label="Sign out"
#     )

# if not token:
#     st.write("Authenticate to access protected content")
#     st.stop()

# account = token["account"]

# name = account["name"]

# st.text(f"TOKEN: {auth_data}")
# st.write(f"Hello {name}!")
# st.write("Protected content available")