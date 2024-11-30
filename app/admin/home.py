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

# if 'myapps' not in st.session_state or st.session_state.myapps is None:
#     st.write("You have no apps registered")
#     st.write(st.session_state.auth_data)
# else:
#     myapps = st.session_state.myapps
#     st.dataframe(myapps)


# # Create a new client and connect to the server
# client = MongoClient(os.environ.get("MONGODB_CONNSTR") , server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
