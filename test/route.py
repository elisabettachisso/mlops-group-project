import streamlit as st

def go_to_login():
    st.session_state.page = "login"

def go_to_register():
    st.session_state.page = "register"

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "home"
    st.session_state.user_id = None