from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import streamlit as st
import os

st.title("My Apps")


if 'myapps' not in st.session_state or st.session_state.myapps is None:
    st.write("You have no apps registered")
    st.write(st.session_state.auth_data)
else:
    myapps = st.session_state.myapps
    st.dataframe(myapps)


# Create a new client and connect to the server
client = MongoClient(os.environ.get("MONGODB_CONNSTR") , server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
