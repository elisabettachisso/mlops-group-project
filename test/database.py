import sqlite3 

def initialize_database(): 
    conn = sqlite3.connect('db/mindhug.db') 
    c = conn.cursor() 
    c.execute(''' CREATE TABLE IF NOT EXISTS users 
              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT UNIQUE, 
              name TEXT, 
              email TEXT, 
              password TEXT) ''') 
    c.execute(''' CREATE TABLE IF NOT EXISTS surveys
              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              user_id INTEGER, 
              age INTEGER, 
              study_hours INTEGER, 
              stress_level TEXT, 
              exercise TEXT, 
              FOREIGN KEY (user_id) 
              REFERENCES users(id)) ''')
    conn.commit()

def add_user(username, name, email, password):
    conn = sqlite3.connect('db/mindhug.db')
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
    conn = sqlite3.connect('db/mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

def add_user(username, name, email, password):
    conn = sqlite3.connect('db/mindhug.db')
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
    conn = sqlite3.connect('db/mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user


def add_response(user_id, age, study_hours, stress_level, exercise):
    conn = sqlite3.connect('db/mindhug.db')
    c = conn.cursor()
    try:
        c.execute(''' INSERT INTO surveys 
                  (user_id, age, study_hours, stress_level, exercise) VALUES (?, ?, ?, ?, ?) ''', 
                  (user_id, age, study_hours, stress_level, exercise))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def get_responses():
    conn = sqlite3.connect('db/mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM surveys')
    responses = c.fetchall()
    conn.close()
    return responses
