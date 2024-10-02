import streamlit as st

st.title("My Apps")


if 'myapps' not in st.session_state or st.session_state.myapps is None:
    st.write("You have no apps registered")
else:
    myapps = st.session_state.myapps
    st.dataframe(myapps)
