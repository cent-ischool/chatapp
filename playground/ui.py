import streamlit as st

args = st.query_params

if 'count' not in st.session_state:
    st.session_state.count = 1
else:
    st.session_state.count += 1

st.button("Increment")

st.write(st.session_state.count)
st.write(args)