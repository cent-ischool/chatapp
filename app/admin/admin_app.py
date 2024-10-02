import streamlit as st
 
auth_title = "Logout" if 'login_token' in st.session_state else "Login"

home_page = st.Page("home.py", title="My Apps", icon=":material/home:")
logs_page = st.Page("logs.py", title="Fetch App Logs", icon=":material/assignment:")
create_page = st.Page("create.py", title="Register App", icon=":material/add_circle:")
delete_page = st.Page("delete.py", title="Delete App", icon=":material/delete:")
auth_page = st.Page("auth.py", title=auth_title, icon=":material/verified_user:")

if 'login_token' in st.session_state:
    pg = st.navigation([home_page, logs_page, create_page, delete_page,auth_page])
else:
    pg = st.navigation([auth_page])

st.set_page_config(page_title="ChatApp manager", page_icon=":material/edit:")
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