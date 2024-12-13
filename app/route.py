import streamlit as st

def go_to_login():
    st.session_state.page = "login"
    st.rerun()

def go_to_register():
    st.session_state.page = "register"
    st.rerun()

