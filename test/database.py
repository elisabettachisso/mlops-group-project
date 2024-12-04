import sqlite3

def initialize_database():
    conn = sqlite3.connect('db/users.db')
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
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)', 
                  (username, name, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

#inserisce una riga nel db

def verify_user(username, password):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user