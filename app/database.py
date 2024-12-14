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
    cursor.execute('''CREATE TABLE IF NOT EXISTS suggestions (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              title TEXT, 
              description TEXT,
              category_id INTEGER,
              level INTEGER,
              FOREIGN KEY (category_id) REFERENCES categories(id))''')    
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_access_log (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users(id))''')

def add_suggestions():
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()    
    # Dati da inserire
    records = [
        ("Balance Studies and Personal Life", "Maintain your balance between studies and personal life. Keep organizing your time effectively.", 5, 0),
        ("Time Management Techniques", "Use techniques like time-blocking to ensure you have time for relaxing activities.", 5, 0),
        ("Discuss Workloads", "Reduce academic pressure by discussing workloads and deadlines with your professors or tutors.", 5, 1),
        ("Stress Management Tips", "Try stress management techniques such as meditation or breathing exercises.", 5, 1),
        ("Consult Academic Counselors", "Consider consulting an academic counselor for personalized support.", 5, 2),
        ("Reduce Course Loads", "Explore options to reduce course loads or assignments, if possible.", 5, 2),
        ("Join Support Groups", "Join support groups or seek psychological help to manage academic stress effectively.", 5, 2),
        ("Stay Motivated", "Stay motivated and continue to track your progress.", 6, 0),
        ("Set SMART Goals", "Set SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goals to further improve.", 6, 0),
        ("Improve One Subject at a Time", "Focus on improving in small areas, like working on one subject at a time.", 6, 1),
        ("Use Study Apps", "Use tools like study apps or join study groups to enhance learning.", 6, 1),
        ("Focus on Learning Process", "Shift your focus from grades to the learning process itself.", 6, 2),
        ("Feedback from Tutors", "Consult your tutor or professor for feedback and recovery strategies.", 6, 2),
        ("Take an Academic Break", "Consider taking an academic break if necessary.", 6, 2),
        ("Identify Study Satisfaction", "Identify what gives you satisfaction in your studies and incorporate it further into your routine.", 3, 0),
        ("Balance Studies and Hobbies", "Keep balancing your time between studying and personal hobbies.", 3, 0),
        ("Engaging Study Methods", "Explore more engaging study methods, such as gamification or visual tools like mind maps.", 3, 1),
        ("Exchange Ideas with Peers", "Connect with peers to exchange ideas and make studying more dynamic.", 3, 1),
        ("Reflect on Academic Goals", "Reflect on your academic motivations and goals. Discuss them with a mentor or counselor.", 3, 2),
        ("Optimize Study Environment", "Modify your study environment to make it more comfortable and less stressful.", 3, 2),
        ("Regular Sleep Routine", "Maintain a regular sleep routine, going to bed and waking up at consistent times.", 1, 0),
        ("Avoid Caffeine Before Bedtime", "Avoid caffeine or electronic devices before bedtime.", 1, 0),
        ("Relaxation Techniques", "Try relaxation techniques like meditation or reading a book before sleeping.", 1, 1),
        ("Create a Sleep-Friendly Environment", "Create a better sleep environment: ensure it’s dark, quiet, and at a comfortable temperature.", 1, 1),
        ("Consult a Doctor for Sleep Issues", "Consult a doctor if you’re experiencing insomnia or sleep disturbances.", 1, 2),
        ("Adopt a Restorative Evening Routine", "Adopt an evening routine that encourages deep, restorative sleep.", 1, 2),
        ("Follow a Balanced Diet", "Continue following a balanced diet, including fresh and nutritious foods.", 2, 0),
        ("Monitor Hydration", "Monitor your hydration and ensure you drink enough water.", 2, 0),
        ("Reduce Sugars and Processed Foods", "Reduce the intake of sugars and processed foods. Add more fruits, vegetables, and proteins to your diet.", 2, 1),
        ("Plan Meals in Advance", "Plan meals in advance to avoid skipping meals.", 2, 1),
        ("Consult a Nutritionist", "Consult a nutritionist to create a diet plan that enhances both mental and physical well-being.", 2, 2),
        ("Avoid Comfort Food", "Avoid relying on comfort food and seek healthier alternatives to manage stress.", 2, 2),
        ("Share Your Feelings", "Talk to someone you trust about your feelings, even if they seem mild.", 8, 0),
        ("Track Emotions", "Keep track of your emotions with a journal or a mental health app.", 8, 0),
        ("Seek Professional Help", "Seek professional help from a counselor or psychologist. Don’t ignore these warning signs.", 8, 1),
        ("Join Support Groups", "Join support groups to connect with others experiencing similar challenges.", 8, 1),
        ("Reach Out in Crisis", "Reach out to a mental health professional or emergency services immediately.", 8, 2),
        ("Talk to Trusted Friends", "Speak with trusted friends or family members and avoid dealing with these thoughts alone.", 8, 2),
        ("Maintain Balance Between Work and Life", "Maintain a healthy balance between work/study and personal time.", 4, 0),
        ("Take Regular Breaks", "Take regular breaks to enhance productivity and avoid burnout.", 4, 0),
        ("Reduce Intense Study Hours", "Consider reducing intense study or work hours if possible.", 4, 1),
        ("Use Productivity Techniques", "Use productivity techniques like the Pomodoro method to manage time effectively.", 4, 1),
        ("Reduce Workload", "Consider significantly reducing your workload.", 4, 2),
        ("Consult a Counselor for Time Management", "Consult a counselor for strategies to manage your time and stress more effectively.", 4, 2),
        ("Monitor Your Expenses", "Continue monitoring your expenses and maintaining a good budget.", 7, 0),
        ("Look for Ways to Save", "Look for ways to save or explore opportunities for additional income.", 7, 0),
        ("Consult a Financial Advisor", "Talk to a financial advisor to identify short- and long-term solutions.", 7, 1),
        ("Focus on Essential Expenses", "Focus on essential expenses and avoid unnecessary spending.", 7, 1),
        ("Seek Financial Aid", "Seek financial aid programs or scholarships, if applicable.", 7, 2),
        ("Share Financial Concerns", "Share your financial concerns with trusted family members or friends for support.", 7, 2),
    ]
    # Inserimento dei dati nella tabella suggestions
    c.executemany('''
    INSERT INTO suggestions (title, description, category_id, level)
    VALUES (?, ?, ?, ?)
    ''', records)
    conn.commit()
    conn.close()
    print("Suggerimenti inseriti con successo!")

def add_categories():
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    
    # Dati da inserire
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
    
    # Inserimento dei dati nella tabella categories
    c.executemany('''
    INSERT INTO categories (category)
    VALUES (?)
    ''', records)
    
    conn.commit()
    conn.close()
    print("Categorie inserite con successo!")


def get_user(user_id):
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchall()
    conn.close()
    return user


def add_user(username, name, email, password):
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    password_hash = sha256(password.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)', 
                  (username, name, email, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

#inserisce una riga nel db

def verify_user(username, password):
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    password_hash = sha256(password.encode()).hexdigest()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password_hash))
    user = c.fetchone()
    if user:
        log_user_access(user[0])
    conn.close()
    return user


def add_response(user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history):
    conn = sqlite3.connect('mindhug.db')
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
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM surveys WHERE user_id = ?', (user_id,))
    responses = c.fetchall()
    conn.close()
    return responses

def get_all_responses():
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM surveys')
    responses = c.fetchall()
    conn.close()
    return responses

def get_last_response(user_id):
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM surveys WHERE user_id = ? order by id desc LIMIT 1', (user_id,))
    last_response = c.fetchall()
    conn.close()
    return last_response


def get_suggestions():
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM suggestions')
    responses = c.fetchall()
    conn.close()
    return responses

def log_user_access(user_id):
    """
    Registra l'accesso di un utente nella tabella di log.
    """
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