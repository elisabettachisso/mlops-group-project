import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="MindHug",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Intestazione
st.title("🧠 MindHug")
st.subheader("Il tuo supporto per il benessere mentale")
st.write(
    "Benvenuto in **MindHug**, un'app progettata per aiutarti a monitorare il tuo benessere mentale "
    "e fornire suggerimenti personalizzati per prenderti cura di te stesso."
)


st.image("logomindhug.png", width=200)  

# Sezione di input
st.markdown("### Compila il questionario")
age = st.number_input("Quanti anni hai?", min_value=1, max_value=100, step=1)
study_hours = st.slider("Quante ore studi al giorno?", min_value=0, max_value=16, step=1)
stress_level = st.selectbox(
    "Come descriveresti il tuo livello di stress?",
    ["Basso", "Moderato", "Alto"]
)
exercise = st.selectbox(
    "Fai esercizio fisico regolarmente?",
    ["Sì", "No"]
)

# Bottone per analizzare i dati
if st.button("Calcola il tuo stato"):
    # Esempio 
    if stress_level == "Alto" or exercise == "No":
        st.error("Attenzione: il tuo livello di benessere potrebbe essere a rischio.")
        st.write("Ti consigliamo di prendere una pausa e considerare tecniche di rilassamento.")
    else:
        st.success("Ottimo! Il tuo benessere mentale sembra in buone condizioni.")
        st.write("Continua così e non dimenticare di prenderti del tempo per te stesso.")

# Sezione aggiuntiva
st.markdown("### Risorse Utili")
st.write(
    "- [Esercizi di mindfulness](https://www.headspace.com)\n"
    "- [Tecniche di gestione dello stress](https://www.helpguide.org/articles/stress/stress-management.htm)"
)

# Footer
st.markdown("---")
st.write("© 2024 MindHug. Tutti i diritti riservati.")





import streamlit as st
import sqlite3

# Connessione al database
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Funzione per verificare l'utente nel database
def check_login(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    result = c.fetchone()
    conn.close()
    return result

# Funzione per registrare un nuovo utente nel database
def register_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

# Funzione per la pagina di login
def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.page = "main"
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Funzione per la pagina di registrazione
def register():
    st.title("Register")
    username = st.text_input("New Username", key="register_username")
    password = st.text_input("New Password", type="password", key="register_password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("Registration successful! Please login.")
        else:
            st.error("Username already exists. Please try another one.")

# Funzione per la pagina principale
def main_page():
    st.title("Benvenuti nella Web App")
    st.write("Questa è la tua home page dopo il login.")

# Funzione per la pagina iniziale con le opzioni Login e Register
def home_page():
    st.title("Benvenuti nella Web App")
    st.write("Seleziona un'opzione:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Vai al Login"):
            st.session_state.page = "login"
    with col2:
        if st.button("Vai alla Registrazione"):
            st.session_state.page = "register"

# Controllo dello stato di login e della pagina attuale
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "home"

# Routing delle pagine
if st.session_state.logged_in:
    main_page()
else:
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "login":
        login()
    elif st.session_state.page == "register":
        register()
