import sqlite3

def initialize_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS users (
                  username TEXT PRIMARY KEY,
                  name TEXT,
                  email TEXT,
                  password TEXT
              )
              ''')
    conn.commit()
    conn.close()

def add_user(username, name, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)', 
                  (username, name, email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users