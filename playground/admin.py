import streamlit as st

home_page = st.Page("home.py", title="App Home", icon=":material/settings:")
create_page = st.Page("create.py", title="Create App", icon=":material/add_circle:")
delete_page = st.Page("delete.py", title="Delete App", icon=":material/delete:")

pg = st.navigation([home_page, create_page, delete_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()


# from msal_streamlit_authentication import msal_authentication

# if st.query_params.get("mode") == "admin":
#     st.title("Chatapp Administration")
#     login_token = msal_authentication(
#         auth={
#             "clientId": "f6958edd-646f-4e84-895a-ede5aa18036e",
#             "authority": "https://login.microsoftonline.com/4278a402-1a9e-4eb9-8414-ffb55a5fcf1e",
#             "redirectUri": "http://localhost:8501/",
#             "postLogoutRedirectUri": "http://localhost:8501/"
#         }, # Corresponds to the 'auth' configuration for an MSAL Instance
#         cache={
#             "cacheLocation": "sessionStorage",
#             "storeAuthStateInCookie": False
#         }, # Corresponds to the 'cache' configuration for an MSAL Instance
#         login_button_text="Login SUAD", # Optional, defaults to "Login"
#         logout_button_text="Logout", # Optional, defaults to "Logout"
#         class_name="css_button_class_selector", # Optional, defaults to None. Corresponds to HTML class.
#         html_id="html_id_for_button", # Optional, defaults to None. Corresponds to HTML id.
#         #key=1 # Optional if only a single instance is needed
#     )
#     if login_token:
#         st.write("Recevied login token:", login_token)
#         pages = st.navigation([st.Page("home.py"), st.Page("1_page.py")])
#         pages.run()
#     else:
#         st.write("No login token received.")

# else: 
#     st.write("Show the Chat interface here")






















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