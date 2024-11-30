
import streamlit as st
from datetime import datetime, timezone
from bson import ObjectId

from dal.models import AppModel
from dal.repos import AppRepository

if 'app_model' not in st.session_state or st.session_state.app_model is None:
    app = AppModel(id=ObjectId().__str__(), created=datetime.now().isoformat())
    st.session_state.app_model = app
else:
    app = AppModel.model_validate(st.session_state.app_model)

st.title("Register Chat Application")
tabs = st.tabs(['⚙️ Configure','🔎 Preview','💾 Finalize Registration'])
with tabs[0]:
    with st.form("registration_form"):
        st.write("#### Settings")
        st.text_input("App ID", value=app.id, key="app_id", disabled=True)
        st.text_input("Created", value=app.created, key="created", disabled=True)
        app.title = st.text_input("Enter Heading", value = app.title)
        app.caption = st.text_input("Enter Caption", value = app.caption)
        app.search_placeholder = st.text_input("Enter Search Placeholder", value=app.search_placeholder)
        app.chat_placeholder = st.text_input("Enter Chat Placeholder", value=app.chat_placeholder)
        app.system_prompt = st.text_area("Enter System Prompt. These instructions control how the model behaves.", value=app.system_prompt)
        app.temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=app.temperature)
        app.auth_email = st.session_state.auth_model.email
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
    save_submit = st.button("Save Application", disabled=st.session_state.app_model is None)
    if save_submit:
        repo = AppRepository(database=st.session_state.mongodb)
        repo.save(app)
        st.session_state.app_model = None
        st.write("Application saved!")
        st.page_link("home.py", label="Return to My Apps")
