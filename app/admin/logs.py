
from dal.models import AppModel, LogModel
from dal.repos import AppRepository, LoggerRepository
import streamlit as st

appid = st.session_state.get("appid", None)
if appid is None:
    st.write("Missing App ID")
    st.stop()

repo = AppRepository(database=st.session_state.mongodb)
app = repo.find_one_by_id(appid)

if not app:
    st.write("This app is not registered")
    st.stop()


logs_repo = LoggerRepository(database=st.session_state.mongodb)
mylogs = logs_repo.find_by({"appid": appid})
mylogs2 = [ l.model_dump() for l in mylogs]
st.dataframe(mylogs2)

st.divider()
st.page_link("home.py", label="Return to My Apps", icon=":material/arrow_back:")