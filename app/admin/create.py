
import streamlit as st
from datetime import datetime, timezone
import uuid

from dal.models import AppModel

if 'app_form_data' not in st.session_state or st.session_state.app_form_data is None:
    app = AppModel()
    st.session_state.app_model = app
else:
    app = AppModel.model_validate(st.session_state.app_model)

st.title("Register Chat Application")
tabs = st.tabs(['⚙️ Configure','🔎 Preview','💾 Finalize Registration'])
with tabs[0]:
    with st.form("registration_form"):
        st.write("#### Settings")
        app.title = st.text_input("Enter Heading", value = app.title)
        app.caption = st.text_input("Enter Caption", value = app.caption)
        app.search_placeholder = st.text_input("Enter Search Placeholder", value=app.search_placeholder)
        app.chat_placeholder = st.text_input("Enter Chat Placeholder", value=app.chat_placeholder)
        app.system_prompt = st.text_area("Enter System Prompt. These instructions control how the model behaves.", value=app.system_prompt)
        app.temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=app.temperature)
        settings_submit = st.form_submit_button("Save Configuration")
        if settings_submit:
            pass
with tabs[1]:
    if settings_submit:
        with st.container(border=True):
            st.title(app.title)
            st.caption(app.caption)
            st.text_input("Search Box Placeholder:", placeholder=app.search_placeholder)
            st.text_input("Chat Box Placeholder:", placeholder=app.chat_placeholder)
    else:
        st.write("Go to configure and save your settings first")
with tabs[2]:
    st.write("#### Finalize")
    st.dataframe(app)
    save_submit = st.button("Save Application")
    if save_submit:
        myapps = st.session_state.get("myapps", [])
        myapps.append(app.model_dump())
        st.session_state.myapps = myapps
        st.write("Application saved!")
        st.session_state.app_form_data = None
        st.page_link("home.py", label="Return to My Apps")
