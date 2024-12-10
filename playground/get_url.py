import streamlit as st
from streamlit_javascript import st_javascript

url = st_javascript("await fetch('').then(r => window.parent.location.href)")

st.write(f"The URL of the running Streamlit app is: {url}")
