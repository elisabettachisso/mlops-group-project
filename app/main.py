import streamlit as st
from auth import login, registration, logout, check_session
from pages import main_page, home_page

# Inizializzazione dello stato
if "logged_in" not in st.session_state: 
    st.session_state.logged_in = False 
if "username" not in st.session_state: 
    st.session_state.username = None 
if "user_id" not in st.session_state: 
    st.session_state.user_id = None 
if "page" not in st.session_state: 
    st.session_state.page = "home"

# Funzione principale
def main():
    st.set_page_config(
        page_title="Welcome to Mindhug",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Controllo della sessione
    if check_session():
        st.session_state.logged_in = True
        st.session_state.page = "main"

    # Navigazione tra le pagine
    if st.session_state.logged_in and st.session_state.page == "main":
        main_page()
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
