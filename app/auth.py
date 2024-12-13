import streamlit as st
from datetime import datetime, timedelta
from database import verify_user, add_user, get_user_last_log, get_user
import time 


# Inizializzazione del gestore dei cookie

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
        back_button = st.form_submit_button("Back")


    if login_button:
        user = verify_user(username, password)  # Verifica l'utente nel database
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user[0]
            # Log dell'accesso utente
            st.success("Login successful!")
            time.sleep(0.5) 
            st.rerun()
            return True
        else:
            st.error("Invalid username or password")
            return False
    if back_button:
        st.session_state.page = "home"
        st.rerun()

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
        back_button = st.form_submit_button("Back")

    if register_button:
        if password != password_confirm:
            st.error("Passwords do not match")
        elif add_user(username, name, email, password):
            st.success("Registration successful! Please login.")
            time.sleep(0.5) 
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("Username already exists. Please try another one.")
    if back_button:
        st.session_state.page = "home"
        st.rerun()
# Funzione per il logout
def logout():
    """
    Esegue il logout dell'utente cancellando i cookie e reimpostando lo stato di sessione.
    """  
    st.session_state.clear()
    if "logged_in" not in st.session_state: 
        st.session_state.logged_in = False 
    if "username" not in st.session_state: 
        st.session_state.username = None 
    if "user_id" not in st.session_state: 
        st.session_state.user_id = None 
    if "page" not in st.session_state: 
        st.session_state.page = "home"  # Reimposta lo stato della sessione
    st.success("You have been logged out!")
    time.sleep(0.5) 
    st.rerun()

# Funzione per verificare la sessione dell'utente
# def check_session():
#     """
#     Controlla se l'utente ha una sessione valida tramite i cookie e aggiorna lo stato di sessione.
#     """
    
#     if user_id:
#         log_timestamp = get_user_last_log(user_id) 
#         user = get_user(user_id)

#         if log_timestamp:
#             data_datetime = datetime.strptime(log_timestamp[0], '%Y-%m-%d %H:%M:%S')
#             log_life = datetime.now() - data_datetime - timedelta(hours=1)
#             if log_life < timedelta(minutes=1):
#                 st.sessiotime.sleep(0.5) n_state.clear()
#                 if "logged_in" not in st.session_state: 
#                     st.session_state.logged_in = True
#                 if "username" not in st.session_state: 
#                     st.session_state.username = user[0][1]
#                 if "user_id" not in st.session_state: 
#                     st.session_state.user_id = user_id
#                 if "page" not in st.session_state: 
#                     st.session_state.page = "main"
#             # Log ogni volta che l'utente accede alla sessione valida
#                 return True
#             else: 
#                 st.session_state.clear()
#                 if "logged_in" not in st.session_state: 
#                     st.session_state.logged_in = False 
#                 if "username" not in st.session_state: 
#                     st.session_state.username = None 
#                 if "user_id" not in st.session_state: 
#                     st.session_state.user_id = None 
#                 if "page" not in st.session_state: 
#                     st.session_state.page = "home"
#                 return False
#         else:
#             st.session_state.clear()
#             if "logged_in" not in st.session_state: 
#                 st.session_state.logged_in = False 
#             if "username" not in st.session_state: 
#                 st.session_state.username = None 
#             if "user_id" not in st.session_state: 
#                 st.session_state.user_id = None 
#             if "page" not in st.session_state: 
#                 st.session_state.page = "home"
#             return False
#     else:
#         st.session_state.logged_in = False
#         st.session_state.user_id = None
#         return False




