import streamlit as st
import os

st.title("Auth Info")

if 'auth_data' not in st.session_state or st.session_state.auth_data is None:
    st.write("Not Logged in")
else:
    st.write(st.session_state.auth_data)

