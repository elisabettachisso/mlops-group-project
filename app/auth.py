import streamlit as st
from database import add_user, verify_user
from route import go_to_login, go_to_register
from streamlit_cookies_controller import CookieController
import time
from datetime import datetime, timedelta

cookie_controller = CookieController()

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

def login():

    st.markdown(
        """
        <style>
        .form-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 100%;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            margin-top: 1rem;
        }
        .button-container2 {
            padding: 0.5rem 1rem;
            font-size: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Login")
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        login_button = st.form_submit_button("Login")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        back_button = st.form_submit_button("Back")
        st.markdown('</div>', unsafe_allow_html=True)
    if login_button:
        user = verify_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user[0]
            # Imposta il cookie con un parametro di scadenza
            expiration_time = datetime.utcnow() + timedelta(seconds=10)
            cookie_controller.set("user_id", st.session_state.user_id, expires=expiration_time, same_site='strict')
            st.success("Login successful")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Invalid username or password")
            return False
    if back_button:
        st.session_state.page = "home"
        st.rerun()

def registration():
   
    st.markdown(
        """
        <style>
        .form-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 100%;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            margin-top: 1rem;
        }
        .button-container2 {
            padding: 0.5rem 1rem;
            font-size: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Register")

    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    with st.form("registration_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        username = st.text_input("Username")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")

        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        register_button = st.form_submit_button("Register")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        back_button = st.form_submit_button("Back")
        st.markdown('</div>', unsafe_allow_html=True)

    def register_action():
        if password != password_confirm:
            st.error("Passwords do not match")
        elif add_user(username, name, email, password):
            st.success("Registration successful! Please login.")
            time.sleep(0.3)  
            go_to_login()
            st.rerun()
        else:
            st.error("Username already exists. Please try another one.")
    
    if register_button:
        register_action()
    if back_button:
        st.session_state.page = "home"
        st.rerun()


def logout():
    if "user_id" in st.session_state:
        cookie_controller.set("user_id", "", max_age=0)
        st.session_state.pop("user_id", None)
        st.success("Logged out successfully!")
    else:
        st.warning("You are not logged in.")
    
    time.sleep(0.5)  
    st.session_state.page = "home"
    st.rerun()


def check_session():
    user_id = cookie_controller.get("user_id")
    if user_id:
        # Verifica se il cookie è scaduto
        expiration_time = datetime.utcnow() + timedelta(seconds=10)
        if datetime.utcnow() > expiration_time:
            cookie_controller.set("user_id", "", max_age=0)  # Cancella il cookie
            st.session_state.pop("user_id", None)
            return False
        st.session_state["user_id"] = user_id
        return True
    else:
        return False




