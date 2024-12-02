import streamlit as st
import sys
import os

# Aggiungi la directory principale al percorso
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth import login, registration
from app.database import initialize_db

initialize_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

def main():
    st.title("Sistema di Login con Streamlit")
    
    if st.session_state.logged_in:
        st.success(f"Sei loggato come: {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.experimental_rerun()
    else:
        option = st.sidebar.selectbox("Scegli un'opzione", ["Login", "Registrazione"])
        if option == "Login":
            if login():
                st.experimental_rerun()
        elif option == "Registrazione":
            registration()

if __name__ == "__main__":
    main()