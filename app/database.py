import sqlite3 
from hashlib import sha256

def initialize_database(): 
    conn = sqlite3.connect('mindhug.db') 
    cursor = conn.cursor() 
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE, 
            name TEXT, 
            email TEXT, 
            password TEXT) ''') 
    cursor.execute(''' CREATE TABLE IF NOT EXISTS surveys
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
    cursor.execute(''' CREATE TABLE IF NOT EXISTS categories 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            category TEXT) ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS suggestions 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            description TEXT,
            category_id INTEGER,
            level INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id))''')    
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_access_log 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id))''')

def get_user(user_id):
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchall()
    conn.close()
    return user

def add_user(username, name, email, password):
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    password_hash = sha256(password.encode()).hexdigest()
    try:
        cursor.execute('INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)', 
                  (username, name, email, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    password_hash = sha256(password.encode()).hexdigest()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password_hash))
    user = cursor.fetchone()
    if user:
        log_user_access(user[0])
    conn.close()
    return user

def add_response(user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history):
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    try:
        cursor.execute(''' INSERT INTO surveys 
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
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM surveys WHERE user_id = ?', (user_id,))
    responses = cursor.fetchall()
    conn.close()
    return responses

def get_all_responses():
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM surveys')
    responses = cursor.fetchall()
    conn.close()
    return responses

def get_last_response(user_id):
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM surveys WHERE user_id = ? order by id desc LIMIT 1', (user_id,))
    last_response = cursor.fetchall()
    conn.close()
    return last_response

def add_suggestions(records):
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()    
    # inserting data into the suggestions table

    try:
        cursor.executemany('''
            INSERT INTO suggestions (title, description, category_id, level)
            VALUES (?, ?, ?, ?)
            ''', records)
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()

def get_suggestions():
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suggestions')
    responses = cursor.fetchall()
    conn.close()
    return responses

def add_categories():
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    # data to be inserted
    records = [
        ("sleep-duration",),
        ("dietary-habits",),
        ("study-satisfaction",),
        ("study-hours",),
        ("academic-pressure",),
        ("cgpa",),
        ("financial-stress",),
        ("suicidal-thoughts",)  
    ]
    # inserting data into the categories table
    cursor.executemany('''INSERT INTO categories (category) VALUES (?)''', records)
    conn.commit()
    conn.close()
    print("Categories successfully inserted!")

def log_user_access(user_id):
    # insert the user login in the log table
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO user_access_log (user_id) VALUES (?)''', (user_id,))
        conn.commit()
    finally:
        conn.close()

def get_access_logs():
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_access_log')
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_user_last_log(user_id):
    conn = sqlite3.connect('mindhug.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp FROM user_access_log WHERE user_id = ? ORDER BY id DESC LIMIT 1', (user_id,))
    log = cursor.fetchone()
    conn.close()
    return log