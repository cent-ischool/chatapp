import streamlit as st

import os

st.title('Hello World!')
st.write('This is a simple Streamlit app.')
st.write(os.environ['OPENAI_ENDPOINT'])