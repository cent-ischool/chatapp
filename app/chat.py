import streamlit as st
import os
import chatlogger

from openaiapi import OpenAIAPI


ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
CHAT_DEFAULT_TEXT = "Talk to me, bro."


start_timestamp = chatlogger.timestamp(as_int=True)
chatmode = st.query_params.get("chat", "True").lower() == "true"
userid = st.query_params.get("userid", f"testing-{start_timestamp}")

if 'userid' not in st.session_state:
    st.session_state.userid = userid

if 'ai' not in st.session_state:
    ai = OpenAIAPI(endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION)
    ai.system_prompt = "You are an AI assistant that helps people find information."
    st.session_state.ai = ai

st.title("Some AI Experiment")
st.caption("This is a caption for the AI experiment")
st.caption(f"User is {st.session_state.userid}")

if chatmode:
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
        
else: # Not in chat mode
    prompt = st.chat_input(CHAT_DEFAULT_TEXT)
    if prompt:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.write(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.write_stream(st.session_state.ai.stream_response(prompt, ignore_history=True))
                st.session_state.ai.record_response(response)
