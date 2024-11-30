from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import streamlit as st
import os

from dal.models import AppModel
from dal.repos import AppRepository

st.title("My Apps")

app_repo = AppRepository(database=st.session_state.mongodb)
email = st.session_state.auth_model.email 

myapps = app_repo.find_by({"auth_email" : email})
myapps2 = [ a.model_dump() for a in myapps]
st.dataframe(myapps2)

