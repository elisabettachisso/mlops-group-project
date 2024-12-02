import streamlit as st
from app.database import add_user, verify_user
from app.utils import hash_password

def login():
    st.subheader("Login")
    username = st.text_input("Nome utente", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Accedi"):
        if username and password:
            user = verify_user(username, password)
            if user:
                st.success(f"Benvenuto, {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                return True
            else:
                st.error("Nome utente o password errati.")
        else:
            st.warning("Per favore, completa tutti i campi.")
    return False

def registration():
    st.subheader("Registrati")
    username = st.text_input("Nome utente")
    password = st.text_input("Password", type="password")
    if st.button("Registrati"):
        if username and password:
            try:
                hashed_password = hash_password(password)
                add_user(username, hashed_password)
                st.success("Registrazione completata! Ora puoi effettuare il login.")
            except ValueError as e:
                st.error(str(e))
        else:
            st.warning("Per favore, completa tutti i campi.")