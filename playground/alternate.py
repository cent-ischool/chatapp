import streamlit as st

st.markdown(
    """
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

messages = [{
    "author": "user",
    "message": "hi",
}, {
    "author": "assistant",
    "message": "I'm a bot"
}] * 3

for message in messages:
    with st.chat_message(message["author"]):
        st.write(message["message"])