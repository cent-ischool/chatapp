import streamlit as st
from datetime import datetime
import uuid

CHAT_DEFAULT_TEXT = "Ask me something."
SEARCH_DEFAULT_TEXT = "Search for something."
SYSTEM_PROMPT_DEFAULT = "You are a Helpful AI Assistant"

if 'app_form_data' not in st.session_state or st.session_state.app_form_data is None:
    appid = str(uuid.uuid4())
    app = {
        "created" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "appid": appid,
        "title": "",
        "caption": "",
        "owner": st.session_state.email,
        "system_prompt": SYSTEM_PROMPT_DEFAULT ,
        "search_placeholder": SEARCH_DEFAULT_TEXT,
        "chat_placeholder": CHAT_DEFAULT_TEXT,
        "chat_mode_querystring": f"?appid={appid}&mode=chat&userid=SOMEUSER",
        "search_mode_querystring": f"?appid={appid}&mode=search&userid=SOMEUSER"
    }
    st.session_state.app_form_data = app
else:
    app = st.session_state.app_form_data

st.title("Register Chat Application")
tabs = st.tabs(['⚙️ Configure','🔎 Preview','💾 Finalize Registration'])
with tabs[0]:
    with st.form("registration_form"):
        st.write("#### Settings")
        app['title'] = st.text_input("Enter Heading", value = app['title'])
        app['caption'] = st.text_input("Enter Caption", value = app['caption'])
        app['system_prompt'] = st.text_area("Enter System Prompt. These instructions control how the model behaves.", value=app['system_prompt'])
        app['search_placeholder'] = st.text_input("Enter Search Placeholder", value=app['search_placeholder'])
        app['chat_placeholder'] = st.text_input("Enter Chat Placeholder", value=app['chat_placeholder'])
        settings_submit = st.form_submit_button("Save Configuration")
        if settings_submit:
            pass
with tabs[1]:
    if settings_submit:
        with st.container(border=True):
            st.title(app['title'])
            st.caption(app['caption'])
            st.text_input("Search Box Placeholder:", placeholder=app['search_placeholder'])
            st.text_input("Chat Box Placeholder:", placeholder=app['chat_placeholder'])
    else:
        st.write("Go to configure and save your settings first")
with tabs[2]:
    st.write("#### Finalize")
    st.dataframe(app)
    save_submit = st.button("Save Application")
    if save_submit:
        myapps = st.session_state.get("myapps", [])
        myapps.append(app)
        st.session_state.myapps = myapps
        st.write("Application saved!")
        st.session_state.app_form_data = None
        st.page_link("home.py", label="Return to My Apps")
