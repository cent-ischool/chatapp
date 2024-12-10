import streamlit as st

from dal.models import AppModel
from dal.repos import AppRepository


appid = st.session_state.get("appid", None)

if appid is None:
    st.title("Preview Application")
    st.write("Missing App ID")
    st.stop()

repo = AppRepository(database=st.session_state.mongodb)
app = repo.find_one_by_id(appid)

if not app:
    st.title("Preview Application")
    st.write("This app is not registered")
    st.stop()


st.title(f"Preview {app.mode.title()} Application")
st.divider()
st.write(f"# {app.title}")
st.caption(f"{app.caption}")
messages = [
        {
            "role": "user",
            "content": "Why is the sky blue?"
        },
        {
            "role": "assistant",
            "content": "Ours is not to question why...."
        }
]

if app.mode == "chat":
    if app.welcome_message  or app.welcome_message != "":
        messages.insert(0,
            {
                "role": "assistant",
                "content": app.welcome_message
            }
        )

    st.markdown(
        """
    <style>
        .st-emotion-cache-janbn0 {
            flex-direction: row-reverse;
            text-align: right;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )    
    for message in messages:
        if message["role"] == "user":
            avatar = app.user_avatar
        else:
            avatar = app.assistant_avatar
        with st.chat_message(message["role"], avatar=avatar): 
            st.markdown(message["content"])
    st.chat_input(placeholder=app.placeholder)
else: # mode=="search"
    with st.form("search_form", clear_on_submit=True, border=False):
        col1,col2 = st.columns([3,1], vertical_alignment="bottom")
        with col1:
            prompt = st.text_input(label="", placeholder=app.placeholder, key="search_widget")
        with col2:
            submit = st.form_submit_button("Search") 
            
    for message in messages:
        if message["role"] == "user":
            avatar = app.user_avatar
        else:
            avatar = app.assistant_avatar
        with st.chat_message(message["role"], avatar=avatar): 
            st.markdown(message["content"])


st.divider()
st.page_link("home.py", label="Return to My Apps", icon=":material/arrow_back:")
