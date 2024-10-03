import streamlit as st
import os
import chatlogger

from openaiapi import OpenAIAPI

CHAT_DEFAULT_TEXT = "Type a message..."
SEARCH_DEFAULT_TEXT = "Type a search query..."

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



def show_default():
    st.title("AI Configurator")
    st.write("Welcome to the AI Experiment!")

############################################################################
MODES = ['none', 'chat', 'search']
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")

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
else:
    show_default()



