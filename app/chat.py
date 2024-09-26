import streamlit as st
import os
import uuid
import chatlogger

from openaiapi import OpenAIAPI


def header():
    st.title("Some AI Experiment")
    st.caption("This is a caption for the AI experiment")
    with st.expander("debug", expanded=False):
        st.text(f"appid: {st.session_state.appid}, userid: {st.session_state.userid}")
    
def show_chatmode():
    header()
    # Display chat messages from history on app rerun
    for message in st.session_state.ai.history[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    prompt = st.chat_input(CHAT_DEFAULT_TEXT)
    if prompt:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.write(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                timestamp = chatlogger.timestamp()
                chatlogger.log(st.session_state.userid, timestamp, "user", prompt)
                response = st.write_stream(st.session_state.ai.stream_response(prompt))
                st.session_state.ai.record_response(response)
                timestamp = chatlogger.timestamp()
                chatlogger.log(st.session_state.userid, timestamp, "assistant", response)


def show_searchmode():   
    header() 
    with st.form("search_form", clear_on_submit=True, border=False):
        col1,col2 = st.columns([3,1], vertical_alignment="bottom")
        with col1:
            prompt = st.text_input("", placeholder=SEARCH_DEFAULT_TEXT, key="widget", value=st.session_state.textbox)
        with col2:
            submit = st.form_submit_button("Search") #, on_click=clear_form)
            
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                response = st.write_stream(st.session_state.ai.stream_response(prompt, ignore_history=True))
                st.session_state.ai.record_response(response)

def show_registration():
    if 'app_status' not in st.session_state:
        st.session_state.app_status = "new"

    st.title("AI Application Registration")
    tabs = st.tabs(['⚙️ Configure','🔎 Preview','💾 Submit Registration'])
    with tabs[0]:
        with st.form("registration_form"):
            st.write("#### Settings")
            title = st.text_input("Enter Heading")
            caption = st.text_input("Enter Caption")
            system_prompt = st.text_area("Enter System Prompt. These instructions control how the model behaves.", value="You are a Helpful AI Assistant")
            search_placeholder = st.text_input("Enter Search Placeholder", value=SEARCH_DEFAULT_TEXT)
            chat_placeholder = st.text_input("Enter Chat Placeholder", value=CHAT_DEFAULT_TEXT)
            settings_submit = st.form_submit_button("Save Configuration")
            if settings_submit:
                st.session_state.app_status = "configured" 
    with tabs[1]:
        if settings_submit:
            with st.container(border=True):
                st.title(title)
                st.caption(caption)
                st.text_input("Search Box Placeholder:", placeholder=search_placeholder)
                st.text_input("Chat Box Placeholder:", placeholder=chat_placeholder)
        else:
            st.write("Go to configure and save your settings first")
    with tabs[2]:
        with st.form("validation_form"):
            st.write("#### Save Settings")
            netid = st.text_input("Enter your syr.edu email", )
            passwd = st.text_input("Enter Registration Passcode", type="password")
            save_submit = st.form_submit_button("Save Settings")

        if save_submit:
            if not netid.endswith("@syr.edu"):
                st.error("Please enter a valid syr.edu email")
                st.stop()
            if not passwd == "password":
                st.error("Invalid passcode")
                st.stop()
                
            appid = uuid.uuid4()
            st.write(f"Application id is: `{appid}`")
            st.write(f'''
                     Querystring Examples: 

                       - Chat mode: (each `userid` is a separate session)   
                            `?appid={appid}&mode=chat&userid=SOMEUSER`

                       - Search mode:   
                            `?appid={appid}&mode=search&userid=SOMEUSER`
                    ''')


def show_default():
    st.title("AI Configurator")
    st.write("Welcome to the AI Experiment!")

############################################################################
MODES = ['none', 'chat', 'search', 'register']
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
CHAT_DEFAULT_TEXT = "Ask me something."
SEARCH_DEFAULT_TEXT = "Search for something."

start_timestamp = chatlogger.timestamp(as_int=True)
mode = st.query_params.get("mode", "none").lower()
appid = st.query_params.get("appid", "none")
userid = st.query_params.get("userid", f"testing-{start_timestamp}")

if 'appid' not in st.session_state:
    st.session_state.appid = appid

if 'userid' not in st.session_state:
    st.session_state.userid = userid

if 'ai' not in st.session_state:
    ai = OpenAIAPI(endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION)
    ai.system_prompt = "You are an AI assistant that helps people find information. You speak like a pirate."
    st.session_state.ai = ai

if mode == 'chat':
    show_chatmode()
elif mode == 'search': 
    show_searchmode()
elif mode == 'register':
    show_registration()
else:
    show_default()



