import streamlit as st

from dal.models import AppModel
from dal.repos import AppRepository

st.title("Delete Application")

repo = AppRepository(database=st.session_state.mongodb)
email = st.session_state.auth_model.email 
myapps = repo.find_by({"auth_email" : email})
myapps2 = [ a.model_dump() for a in myapps]

if len(myapps2) == 0:
    st.write("You have no apps registered")
    st.stop()

if st.session_state.get("delete_confirm_clicked", False):
    st.write("App Deleted!")
    st.page_link("home.py", label="Return to My Apps")
    st.stop()

appids = [f"{app['id']} ({app['title']})" for app in myapps2]
delete_appid = st.selectbox("Select App to Delete", appids)
if delete_appid and st.button("Show App Details"):
    st.session_state.delete_confirm_clicked = False
    st.write("App Details:")
    appid = delete_appid.split(" ")[0]
    app = repo.find_one_by_id(appid)
    st.dataframe(app)
    if st.button("Confirm Delete"):
        print(f"Deleting app {appid}")
        repo.delete_by_id(appid)
        st.session_state.delete_confirm_clicked = True
        st.toast("App deleted!")
        st.page_link("home.py", label="Return to My Apps")
        st.stop()



