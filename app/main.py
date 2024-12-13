import streamlit as st
from auth import login, registration, logout, check_session
from pages import main_page, home_page

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

    st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    if check_session():
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
        elif logout():
            st.session_state.page = "home"
            home_page()
            st.rerun

        


if __name__ == "__main__":
    main()
