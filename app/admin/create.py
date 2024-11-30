
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

app.auth_email = st.session_state.auth_model.email

st.title("Create Application")
app.mode = st.selectbox("Select Mode", ["chat", "search"], index=0 if app.mode == "chat" else 1)
mode = app.mode.title()
with st.form("registration_form"):

    st.write("#### User Interface")
    app.title = st.text_input("Enter Heading", value = app.title, placeholder="Title of the app.")
    app.caption = st.text_area("Enter Caption", value = app.caption, placeholder="Description of the app or any user instructions.")
    app.placeholder = st.text_input(f"Enter {mode} Placeholder", value=app.placeholder, placeholder=f"What's inside the empty {mode} box. e.g. Type something.")
    app.user_avatar = st.text_input(f"{mode} User Avatar", value=app.user_avatar, placeholder="Enter an Emoji or URL to a picture for the user.")
    app.assistant_avatar = st.text_input(f"{mode} AI Avatar", value=app.assistant_avatar, placeholder="Enter an Emoji or URL to a picture for the AI.")

    st.write("#### AI Behavior")
    app.system_prompt = st.text_area("Enter System Prompt. These instructions control how the model behaves.", value=app.system_prompt)
    app.temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=app.temperature)
    if app.mode == "chat":
        app.welcome_message = st.text_area(f"{mode} Welcome Message", value=app.welcome_message, placeholder="This message will output from the AI, when they first open the app.")

    st.write("#### Settings")
    st.text_input("App ID", value=app.id, key="app_id", disabled=True)
    st.text_input("Created", value=app.created, key="created", disabled=True)
    st.text_input("Auth Email", value=app.auth_email, key="auth_email", disabled=True)
    st.write("Query String:")
    st.code(app.build_querystring())

    save_submit = st.form_submit_button("Save App")
    
    if save_submit:
        repo = AppRepository(database=st.session_state.mongodb)
        repo.save(app)
        st.session_state.app_model = None
        st.write("Application saved!")
        st.page_link("home.py", label="Return to My Apps")
