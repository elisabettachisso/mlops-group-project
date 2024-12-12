import streamlit as st
from database import add_user, verify_user
from route import go_to_login, go_to_register
from streamlit_cookies_controller import CookieController
import time

cookie_controller = CookieController()

def login():

    st.set_page_config(page_title="Login", layout="centered")

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
            cookie_controller.set("user_id", st.session_state.user_id)
            st.success("Login successful")
            time.sleep(0.5)  # Pause briefly before rerun
            st.rerun()
        else:
            st.error("Invalid username or password")
            return False
    if back_button:
        st.session_state.page = "home"
        st.rerun()

def registration():
    st.set_page_config(page_title="Register", layout="centered")

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
            time.sleep(0.3)  # Pause briefly before rerun
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
    # Clear cookie by setting it to an empty value with a past expiration
        cookie_controller.set("user_id", "", max_age=0)
        st.session_state.pop("user_id", None)
        st.success("Logged out successfully!")
        time.sleep(0.5)  # Pause briefly before rerun
        st.session_state.page = "home"
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






