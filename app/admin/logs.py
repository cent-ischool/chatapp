
from dal.models import AppModel, LogModel
from dal.repos import AppRepository, LoggerRepository
import streamlit as st

st.title("Fetch ChatApp Logs")

app_repo = AppRepository(database=st.session_state.mongodb)
email = st.session_state.auth_model.email 
myapps = app_repo.find_by({"auth_email" : email})

if myapps is None:
    st.write("You have no apps registered")
else:
    myapp_names = sorted([ f"{a.title} | {a.id}"  for a in myapps])
    appname_and_id = st.selectbox("Select App To Fetch Logs", myapp_names)
    if appname_and_id:
        appname, appid = [a.strip() for a in appname_and_id.split("|")]
        st.write(appid)
        logs_repo = LoggerRepository(database=st.session_state.mongodb)
        mylogs = logs_repo.find_by({"appid": appid})
        mylogs2 = [ l.model_dump() for l in mylogs]
        st.dataframe(mylogs2)
