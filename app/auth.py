import streamlit as st
from app.database import verify_user

# Login
def login():
    st.title("Login")
    username = st.text_input("Nome utente")
    password = st.text_input("Password", type="password")
    
    if "login_attempted" not in st.session_state:
        st.session_state.login_attempted = False

    if st.button("Login") or st.session_state.login_attempted:
        if not st.session_state.login_attempted:
            st.session_state.login_attempted = True

        if verify_user(username, password):
            st.success("Login effettuato con successo!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "main"
            st.experimental_rerun()  # Reindirizza immediatamente
        else:
            st.error("Nome utente o password errati.")
            st.session_state.login_attempted = False

# Registrazione
def registration():
    st.title("Registrazione")
    username = st.text_input("Nome utente")
    password = st.text_input("Password", type="password")
    register_button = st.button("Registrati")
    if register_button:
        try:
            add_user(username, password)
            st.success("Registrazione completata con successo! Vai al login.")
            st.button("Vai al Login", on_click=lambda: st.session_state.update({"page": "login"}))
        except ValueError as e:
            st.error(str(e))
