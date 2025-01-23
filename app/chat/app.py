from  add_parent_path import add_parent_path
add_parent_path(1)

import streamlit as st
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from chatlogger import ChatLogger, timestamp

from openaiapi import OpenAIAPI
from dal.models import AppModel
from dal.repos import AppRepository


CHAT_DEFAULT_TEXT = "Type a message..."
SEARCH_DEFAULT_TEXT = "Type a search query..."
USER_AVATAR = "./app/icons/person-circle.svg"
ASSISTANT_AVATAR = "./app/icons/avezgzct5.webp"

def header(app: AppModel):
    st.title(app.title)
    st.caption(app.caption)


def footer():
    with st.expander("debug", expanded=False):
        st.text(f"appid: {st.session_state.appid}, userid: {st.session_state.userid}")
    
def show_chatmode(app: AppModel):
    st.markdown(
        """
    <style>
        .st-emotion-cache-1c7y2kd {
            flex-direction: row-reverse;
            text-align: right;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    logger = ChatLogger(st.session_state.mongodb)
    header(app)

    # Display chat messages from history on app rerun
    for message in st.session_state.ai.history[1:]:
        if message["role"] == "user":
            avatar = USER_AVATAR
        else: # "assistant"
            avatar = ASSISTANT_AVATAR

        with st.chat_message(message["role"], avatar=avatar): # <-- Inject avatar here
            st.markdown(message["content"])

    # React to user input
    prompt = st.chat_input(placeholder=app.placeholder, key="chat_widget") #, r)
    if prompt:
        # Display user message in chat message container
        with st.chat_message("user", avatar=USER_AVATAR):
            st.write(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            with st.spinner("Thinking..."):
                logger.log_user_chat(st.session_state.appid, st.session_state.userid, prompt)
                response = st.write_stream(st.session_state.ai.stream_response(prompt))
                st.session_state.ai.record_response(response)
                logger.log_assistant_chat(st.session_state.appid, st.session_state.userid, response)

def show_searchmode(app: AppModel):   
    def clear_form():
        st.session_state.search_widget = ""

    logger = ChatLogger(st.session_state.mongodb)
    header(app) 
#    with st.form("search_form", clear_on_submit=False, border=False):
    col1,col2,col3 = st.columns([76,12,12], vertical_alignment="bottom")
    with col1:
        prompt = st.text_input(label="", placeholder=app.placeholder, key="search_widget", value=st.session_state.get("search_widget",None))
    with col2:
        submit = st.button("Search") #, on_click=clear_form)
    with col3:
        clear = st.button("Clear", on_click=clear_form) #, on_click=clear_form)
            
    if prompt:

        # Display assistant response in chat message container
        with st.chat_message("search_output", avatar="🔎"):
            with st.spinner("Searching..."):
                logger.log_user_search(st.session_state.appid, st.session_state.userid, prompt)
                response = st.write_stream(st.session_state.ai.stream_response(prompt, ignore_history=True))
                st.session_state.ai.record_response(response)
                logger.log_assistant_search(st.session_state.appid, st.session_state.userid, response)


def show_error(message):
    st.title("💣😢 Error 😢💣")
    st.write(message)


############################################################################
MODES = ['none', 'chat', 'search']
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")

start_timestamp = timestamp(as_int=True)
mode = st.query_params.get("mode", "none").lower()
appid = st.query_params.get("appid", None)
userid = st.query_params.get("userid", f"testing-{start_timestamp}")

if 'appid' not in st.session_state:
    client = MongoClient(os.environ.get("MONGODB_CONNSTR") , server_api=ServerApi('1'))
    db = client.get_database("chatapp")
    app_repo = AppRepository(database=db)
    app = app_repo.find_one_by_id(appid)
    if app:
        st.session_state.appid = appid
        st.session_state.app = app
        st.session_state.mongodb = db

        if 'userid' not in st.session_state:
            st.session_state.userid = userid

        if 'ai' not in st.session_state:
            logger = ChatLogger(db)
            ai = OpenAIAPI(endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION)
            ai.system_prompt = app.system_prompt
            st.session_state.ai = ai
            logger.log_system_prompt(appid, userid, app.system_prompt)
            # Initial first message
            if app.mode == "chat" and app.welcome_message and app.welcome_message.strip() != "":
                st.session_state.ai.record_response(app.welcome_message)


# Main Logic...
app = st.session_state.get("app", None)
if mode == 'chat' and app:
    show_chatmode(app)
elif mode == 'search' and app: 
    show_searchmode(app)
elif mode not in MODES:
    show_error(f"Invalid mode: `{mode}`")
else:
    show_error(f"`{appid}` is not a registered app id.")



