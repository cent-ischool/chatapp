import streamlit as st
import os

from openai import OpenAIAPI
ENDPOINT = os.environ.get("OPENAI_ENDPOINT")
API_KEY = os.environ.get("OPENAI_API_KEY")

if 'ai' not in st.session_state:
    ai = OpenAIAPI(ENDPOINT, API_KEY)
    ai.system_text = "You are a helpful AI assistant who speaks like a pirate."
    ai.start_conversation()
    st.session_state.ai = ai

# def generate_ai_response(prompt):
#     response = ai.generate_response(prompt)
#     return response 

st.title("Chat Example")
st.caption("GPT 4o Model")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("What is up?")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.session_state.ai.generate_response(prompt)
        st.write(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})