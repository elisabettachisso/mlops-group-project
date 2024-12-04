import streamlit as st
from app.auth import login, registration
from app.database import initialize_db

# Inizializza il database
initialize_db()

# Stato iniziale
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# Funzioni per navigazione
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "home"
    st.experimental_rerun()

def home_page():
    st.title("Benvenuti nella Web App")
    st.write("Seleziona un'opzione:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Vai al Login"):
            st.session_state.page = "login"
            st.experimental_rerun()
    with col2:
        if st.button("Vai alla Registrazione"):
            st.session_state.page = "register"
            st.experimental_rerun()

def main_page():
    st.title("Benvenuti nella Web App")
    st.write(f"Questa è la home page per {st.session_state.username}.")
    st.button("Logout", on_click=logout)

# Gestione principale
def main():
    # Controlla lo stato di login
    if st.session_state.logged_in:
        main_page()
    else:
        if st.session_state.page == "home":
            home_page()
        elif st.session_state.page == "login":
            login()
        elif st.session_state.page == "register":
            registration()

if __name__ == "__main__":
    main()
