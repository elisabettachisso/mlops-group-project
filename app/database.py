import sqlite3
from bcrypt import hashpw, gensalt, checkpw

# Inizializza il database
def initialize_db():
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Aggiunge un nuovo utente con password hashata
def add_user(username, password):
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    hashed_password = hashpw(password.encode(), gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Nome utente già esistente.")
    conn.close()

# Verifica l'utente con password hashata
def verify_user(username, password):
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and checkpw(password.encode(), user[0]):
        return True
    return False
