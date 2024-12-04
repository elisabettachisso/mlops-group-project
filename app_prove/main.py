import streamlit as st
from auth import login, registration
from database import initialize_db

# Inizializza il database
initialize_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if "page" not in st.session_state:
    st.session_state.page = "home"

# Funzioni per la gestione delle pagine
def go_to_login():
    st.session_state.page = "login"

def go_to_register():
    st.session_state.page = "register"

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "home"

def home_page():
    st.title("Benvenuti nella Web App")
    st.write("Seleziona un'opzione:")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Vai al Login", on_click=go_to_login)
    with col2:
        st.button("Vai alla Registrazione", on_click=go_to_register)

def main_page():
    st.title("Benvenuti nella Web App")
    st.write(f"Questa è la home page per {st.session_state.username}.")
    st.button("Logout", on_click=logout)

# Gestione principale
def main():
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
