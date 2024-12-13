import streamlit as st
from hashlib import sha256
from datetime import datetime, timedelta
from streamlit_cookies_controller import CookieController
from database import verify_user, add_user, get_user_last_log, get_user

# Inizializzazione del gestore dei cookie
cookie_controller = CookieController()

# Funzione per il login
def login():
    """
    Mostra il modulo di login e gestisce l'autenticazione dell'utente.
    """
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        user = verify_user(username, password)  # Verifica l'utente nel database
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user[0]

            # Imposta il cookie con una scadenza
            expiration_time = datetime.now() + timedelta(seconds=10)  # Cookie valido per 1 giorno
            cookie_controller.set("user_id", user[0], expires=expiration_time)

            # Log dell'accesso utente

            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password")
            return False

# Funzione per la registrazione
def registration():
    """
    Mostra il modulo di registrazione e registra un nuovo utente nel database.
    """
    st.title("Register")

    with st.form("registration_form"):
        username = st.text_input("Username")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        register_button = st.form_submit_button("Register")

    if register_button:
        if password != password_confirm:
            st.error("Passwords do not match")
        elif add_user(username, name, email, password):
            st.success("Registration successful! Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("Username already exists. Please try another one.")

# Funzione per il logout
def logout():
    """
    Esegue il logout dell'utente cancellando i cookie e reimpostando lo stato di sessione.
    """
    cookie_controller.remove("user_id")  # Cancella il cookie
    st.session_state.clear()  # Reimposta lo stato della sessione
    st.success("You have been logged out!")
    st.rerun()

# Funzione per verificare la sessione dell'utente
def check_session():
    """
    Controlla se l'utente ha una sessione valida tramite i cookie e aggiorna lo stato di sessione.
    """
    user_id = cookie_controller.get("user_id")
    if user_id:
        log_timestamp = get_user_last_log(user_id) 
        user = get_user(user_id)

        if log_timestamp:
            data_datetime = datetime.strptime(log_timestamp[0], '%Y-%m-%d %H:%M:%S')
            log_life = datetime.now() - data_datetime - timedelta(hours=1)
            if log_life < timedelta(minutes=1):
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = user[0][1]
            # Log ogni volta che l'utente accede alla sessione valida
                return True
            else: 
                cookie_controller.remove("user_id")
                return False
        else:
            cookie_controller.remove("user_id")
            return False
    else:
        st.session_state.logged_in = False
        st.session_state.user_id = None
        return False




