from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import streamlit as st
from streamlit_javascript import st_javascript
import os

from dal.models import AppModel
from dal.repos import AppRepository

site = st_javascript("await fetch('').then(r => window.parent.location.href)")



col = st.columns([1,1], vertical_alignment="bottom")
with col[0]:
    st.title("My Apps")

with col[1]:
    st.page_link("create.py", label="Create App", icon=":material/add_circle:")


app_repo = AppRepository(database=st.session_state.mongodb)
email = st.session_state.auth_model.email 

myapps = app_repo.find_by({"auth_email" : email})
myapps2 = [ a.model_dump() for a in myapps]

appids = [f"{app['id']} ({app['title']})" for app in myapps2]
select_appid = st.selectbox("Select App:", appids)
if select_appid :
    appid = select_appid.split(" ")[0]
    st.session_state.appid = appid
    app = [a for a in myapps2 if a['id'] == appid][0]

    am = AppModel(**app)
    st.code(am.build_url(site))
    st.table(app)
    cols = st.columns(4)
    with cols[0]:
        st.page_link("edit.py", label="Edit App", icon=":material/edit:")
    with cols[1]:
         st.page_link("preview.py", label="Preview App", icon=":material/preview:")
    with cols[2]:        
        st.page_link("logs.py",label="Fetch App Logs", icon=":material/assignment:")
    with cols[3]:
        st.page_link("delete.py", label="Delete App", icon=":material/delete:")
