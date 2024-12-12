import streamlit as st

def go_to_login():
    st.session_state.page = "login"

def go_to_register():
    st.session_state.page = "register"

