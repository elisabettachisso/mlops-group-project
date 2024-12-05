import streamlit as st
from auth import login, registration
from pages import main_page, home_page
from database import initialize_database


if "logged_in" not in st.session_state: 
    st.session_state.logged_in = False 
if "username" not in st.session_state: 
    st.session_state.username = None 
if "user_id" not in st.session_state: 
    st.session_state.user_id = None 
if "page" not in st.session_state: 
    st.session_state.page = "home"

def main():
    if st.session_state.logged_in:
        main_page()
    else:
        if st.session_state.page == "home":
            home_page()
        elif st.session_state.page == "login":
            if login():
                st.session_state.page = "main"
                st.rerun()
        elif st.session_state.page == "register":
            registration()


if __name__ == "__main__":
    main()