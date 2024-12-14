import streamlit as st
from database import verify_user, add_user
import time

def login():

    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        back_button = st.form_submit_button("Back")

    if login_button:
        user = verify_user(username, password)  
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user[0]

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

def registration():

    st.title("Register")

    with st.form("registration_form"):
        username = st.text_input("Username")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        consent = st.checkbox("I agree with the treatment of my personal data")
        register_button = st.form_submit_button("Register")
        back_button = st.form_submit_button("Back")

    if register_button:
        if password != password_confirm:
            st.error("Passwords do not match")
        if consent:
            if add_user(username, name, email, password):
                st.success("Registration successful! Please login.")
                time.sleep(0.5) 
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Username already exists. Please try another one.")
        else:
            st.error("You have to give your consent for registration")
    if back_button:
        st.session_state.page = "home"
        st.rerun()

def logout():
    st.session_state.clear()
    if "logged_in" not in st.session_state: 
        st.session_state.logged_in = False 
    if "username" not in st.session_state: 
        st.session_state.username = None 
    if "user_id" not in st.session_state: 
        st.session_state.user_id = None 
    if "page" not in st.session_state: 
        st.session_state.page = "home" 
    st.success("You have been logged out!")
    time.sleep(0.5) 
    st.rerun()







