import streamlit as st
from streamlit_javascript import st_javascript

from dal.models import AppModel
from dal.repos import AppRepository

site = st_javascript("await fetch('').then(r => window.parent.location.href)")

st.title("Edit Application")

appid = st.session_state.get("appid", None)

if appid is None:
    st.write("Missing App ID")
    st.stop()

repo = AppRepository(database=st.session_state.mongodb)
app = repo.find_one_by_id(appid)

if not app:
    st.write("This app is not registered")
    st.stop()


st.title("Edit Application")
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
    st.write("URL:")
    st.code(app.build_url(site))

    save_submit = st.form_submit_button("Save App")
    if save_submit:
        repo.save(app)
        st.toast("Application Updated!")
        st.write("Application Updated!")
        st.page_link("home.py", label="Return to My Apps", icon=":material/arrow_back:")
        st.stop()



        