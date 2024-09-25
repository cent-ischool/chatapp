from typing import Any
from openai import AzureOpenAI
import streamlit as st

class OpenAIAPI:
    def __init__(self, endpoint, api_key, api_version):
        self._client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version=api_version)
        self._messages = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]

    @property
    def system_prompt(self):
        return [m['content'] for m in self._messages if m['role'] == "system"]

    @system_prompt.setter
    def system_prompt(self, value):
        index = [i for i, m in enumerate(self._messages) if m['role'] == "system"][0]
        self._messages[index[0]]['content'] = value


def stream_response(messages: list[str]):
    response = client.chat.completions.create(
        stream=True,
        messages=messages, 
        model="gpt4o")
    
    for chunk in response:
        if len(chunk.choices) > 0:
            yield chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""


ENDPOINT = "https://ist256-openai-instance.openai.azure.com/"
API_KEY = "3cfc103aeff5407b842b277def615a1c"
API_VERSION = "2024-05-01-preview"
client = AzureOpenAI(azure_endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION)
messages = [ {
    "role": "system",
    "content": "You are an AI assistant that helps people find information."
}]

st.title("Streaming Chat Example")
st.caption("GPT 4o Model")
query = st.text_area("Query?")
button = st.button("Submit")

if query and button:
    messages.append({"role": "user", "content": query})
    with st.spinner("Thinking..."):
        assistant = st.write_stream(stream_response(messages))
        st.text(assistant)


    # for chunk in stream_response(messages):
    #     print(chunk)

    # response = client.chat.completions.create(
    #     stream=True,
    #     messages=[{"role": "user", "content": "How many different ways can one cook an egg and what are the advantages of each?"}],
    #     model="gpt4o"
    # )

    # for chunk in response:
    #     if len(chunk.choices) > 0:
    #         yield chunk.choices[0].delta.content

    