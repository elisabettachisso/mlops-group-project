import streamlit as st
from database import add_user, verify_user
from route import go_to_login, go_to_register
from streamlit_cookies_controller import CookieController
import time

cookie_controller = CookieController()

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = verify_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user[0]
            cookie_controller.set("user_id", st.session_state.user_id)
            time.sleep(0.5)  # Pause briefly before rerun
            st.rerun()
        else:
            st.error("Invalid username or password")
            return False

def registration():
    st.title("Register")
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
            time.sleep(0.5)  # Pause briefly before rerun
            go_to_login()
        else:
            st.error("Username already exists. Please try another one.")

    st.button("Register", on_click=register_action)


def logout():
    # Clear cookie by setting it to an empty value with a past expiration
        cookie_controller.set("user_id", "", max_age=0)
        st.session_state.pop("user_id", None)
        st.success("Logged out successfully!")
        time.sleep(0.5)  # Pause briefly before rerun
        st.rerun()
        return True  # Rerun to clear the interface

def check_session():
    # Check if the user_id cookie exists
    user_id = cookie_controller.get("user_id")
    if user_id:
        # Restore session
        st.session_state["user_id"] = user_id
        return True
    else:
        return False
