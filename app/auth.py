import streamlit as st
from app.database import add_user, verify_user

# Login
def login():
    st.title("Login")
    username = st.text_input("Nome utente")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    if login_button:
        if verify_user(username, password):
            st.success("Login effettuato con successo!")
            st.session_state.logged_in = True
            st.session_state.username = username
            return True
        else:
            st.error("Nome utente o password errati.")
    return False

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
