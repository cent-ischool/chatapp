import streamlit as st

from dal.models import AppModel
from dal.repos import AppRepository

st.title("Delete Application")

appid = st.session_state.get("appid", None)
if appid is None:
    st.write("Missing App ID")
    st.stop()

repo = AppRepository(database=st.session_state.mongodb)
app = repo.find_one_by_id(appid)

if not app:
    st.write("This app is not registered")
    st.stop()

st.table(app)
if st.button("Confirm Delete"):
    repo.delete_by_id(appid)
    st.toast("Application deleted!")
    st.write("Application deleted!")
    st.page_link("home.py", label="Return to My Apps", icon=":material/arrow_back:")
    st.stop()