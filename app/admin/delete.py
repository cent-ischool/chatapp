import streamlit as st

st.title("Delete Application")


if 'myapps' not in st.session_state or st.session_state.myapps is None:
    st.write("You have no apps registered")
else:
    myapps = st.session_state.myapps
    appids = [f"{app['appid']} ({app['title']})" for app in myapps]
    appid = st.selectbox("Select App to Delete", appids)
    if st.button("Delete"):
        myapps = [app for app in myapps if app['appid'] != appid.split(" ")[0]]
        st.session_state.myapps = myapps
        st.write("App deleted!")
        st.page_link("home.py", label="Return to My Apps")