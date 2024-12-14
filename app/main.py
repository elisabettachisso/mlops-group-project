import streamlit as st
from auth import login, registration, logout
from pages import home_page, main_page_analyst, main_page_admin , main_page_users

if "logged_in" not in st.session_state: 
    st.session_state.logged_in = False 
if "username" not in st.session_state: 
    st.session_state.username = None 
if "user_id" not in st.session_state: 
    st.session_state.user_id = None 
if "page" not in st.session_state: 
    st.session_state.page = "home"


def main():
    st.set_page_config(
        page_title="Welcome to Mindhug",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    if st.session_state.logged_in == True:
        st.session_state.page = "main"

    if st.session_state.logged_in and st.session_state.page == "main":
        if st.session_state.username == "dataanalyst":
            main_page_analyst()
        elif st.session_state.username == "admin":
            main_page_admin()
        else:
            main_page_users()
    elif st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "login":
        if login():
            st.session_state.page = "main"
            st.session_state.logged_in = True
            st.rerun()
    elif st.session_state.page == "register":
        registration()
    elif st.session_state.page == "logout":
        logout()
        st.session_state.page = "home"
        st.session_state.logged_in = False
        st.rerun()
# Entry point
if __name__ == "__main__":
    main()
