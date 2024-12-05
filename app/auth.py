import streamlit as st
import streamlit_authenticator as stauth
from database import add_user, get_users

def load_users():
    users = get_users()  # Ottieni gli utenti dal database
    credentials = {"usernames": {}}
    for user in users:
        username, name, email, password = user
        credentials["usernames"][username] = {
            "email": email,
            "name": name,
            "password": password
        }
        #st.write("Loaded credentials:", credentials) 
    return credentials

def login():

    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    credentials = load_users()
    if st.button("Login"):
        authenticator = stauth.Authenticate(
            credentials,
            "app_cookie",
            "random_key",
            cookie_expiry_days=30
        )
 # Controllo del valore restituito
        result = authenticator.login()
        if result is None:
            st.error("Authentication failed: login returned None")
            return None

        name, authentication_status, username = None, None, None # Inizializza le variabili 
        try: 
            name, authentication_status, username = authenticator.login("Login", "main") 
        except ValueError as e:
            st.error(f"An error occurred: {e}") 
            return None

        if authentication_status:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome {name}")
            st.session_state.page = "main"
        elif authentication_status is False:
            st.error("Username/password is incorrect")
        elif authentication_status is None:
            st.warning("Please enter your username and password")
    
        return authentication_status



def registration():
    username = st.text_input("Username")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm Password", type="password")

    def register_action():
        if password != password_confirm:
            st.error("Passwords do not match")
        elif add_user(username, name, email, password):
            st.success("Registration successful! Please login.")
        else:
            st.error("Username already exists. Please try another one.")

    st.button("Register", on_click=register_action)
