import streamlit as st
from database import add_user, verify_user
from route import go_to_login, go_to_register, logout

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
            go_to_login()
        else:
            st.error("Username already exists. Please try another one.")

    st.button("Register", on_click=register_action)

