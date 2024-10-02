import streamlit as st

st.title("Fetch ChatApp Logs")

if 'myapps' not in st.session_state or st.session_state.myapps is None:
    st.write("You have no apps registered")
else:
    myapps = st.session_state.myapps
    appids = [f"{app['appid']} ({app['title']})" for app in myapps]
    appid = st.selectbox("Select App", appids)
    app = [app for app in myapps if app['appid'] == appid.split(" ")[0]][0]
    st.dataframe(app.get('logs', {}))
    st.page_link("home.py", label="Return to My Apps")