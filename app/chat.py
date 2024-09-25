import streamlit as st
import os

from openaiapi import OpenAIAPI
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")

if 'ai' not in st.session_state:
    ai = OpenAIAPI(endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION)
    ai.system_prompt = "You are an AI assistant that helps people find information, but you talk in jive."
    st.session_state.ai = ai

st.title("Chat Example")
st.caption("GPT 4o Model")

# Display chat messages from history on app rerun
for message in st.session_state.ai.history[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("What is up?")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(st.session_state.ai.stream_response(prompt))
        st.session_state.ai.record_response(response)
    