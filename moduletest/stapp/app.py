from  add_parent_path import add_parent_path
add_parent_path(1)
import os
import sys

import streamlit as st

from testmod.mod import mod_function

st.title("Streamlit Module Test")

# st.write(libpath)
st.write(os.getcwd())
st.write(sys.path)
st.write(mod_function())
