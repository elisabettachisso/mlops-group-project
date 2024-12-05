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
              gender TEXT, 
              age INTEGER, 
              accademic_pressure INTEGER, 
              cgpa FLOAT, 
              study_satisfaction INTEGER, 
              sleep_duration TEXT, 
              dietary_habits TEXT, 
              degree TEXT, 
              suicidal_thoughts TEXT,   
              study_hours INTEGER, 
              financial_stress INTEGER, 
              family_history TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
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


def add_response(user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history):
    conn = sqlite3.connect('db/mindhug.db')
    c = conn.cursor()
    try:
        c.execute(''' INSERT INTO surveys 
                  (user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', 
                  (user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def get_responses(user_id):
    conn = sqlite3.connect('db/mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM surveys WHERE user_id = ?', (user_id,))
    responses = c.fetchall()
    conn.close()
    return responses
