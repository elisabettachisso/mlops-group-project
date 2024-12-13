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
    cursor.execute('''CREATE TABLE IF NOT EXISTS suggestions (
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               title TEXT, 
               description TEXT,
               category_id INTEGER,
               FOREIGN KEY (category_id) REFERENCES categories(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_access_log (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users(id))''')


    # # Nuovi record da aggiungere
    # records = [
    #     # (description, title, category_id, level)
    #     ("Maintain your balance between studies and personal life. Keep organizing your time effectively.", 
    #     "Balance Studies and Personal Life", 5, 0),
    #     ("Use techniques like time-blocking to ensure you have time for relaxing activities.", 
    #     "Time Management with Time-Blocking", 5, 0),
    #     ("Reduce academic pressure by discussing workloads and deadlines with your professors or tutors.", 
    #     "Discuss Workloads with Professors", 5, 1),
    #     ("Try stress management techniques such as meditation or breathing exercises.", 
    #     "Practice Stress Management Techniques", 5, 1),
    #     ("Consider consulting an academic counselor for personalized support.", 
    #     "Seek Academic Counseling", 5, 2),
    #     ("Explore options to reduce course loads or assignments, if possible.", 
    #     "Reduce Course Loads", 5, 2),
    #     ("Join support groups or seek psychological help to manage academic stress effectively.", 
    #     "Join Support Groups or Seek Help", 5, 2),
    #     ("Stay motivated and continue to track your progress.", 
    #     "Stay Motivated and Track Progress", 6, 0),
    #     ("Set SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goals to further improve.", 
    #     "Set SMART Goals", 6, 0),
    #     ("Focus on improving in small areas, like working on one subject at a time.", 
    #     "Focus on Small Improvements", 6, 1),
    #     ("Use tools like study apps or join study groups to enhance learning.", 
    #     "Use Study Apps or Join Groups", 6, 1),
    #     ("Shift your focus from grades to the learning process itself.", 
    #     "Focus on Learning Over Grades", 6, 2),
    #     ("Consult your tutor or professor for feedback and recovery strategies.", 
    #     "Seek Feedback from Tutors", 6, 2),
    #     ("Consider taking an academic break if necessary.", 
    #     "Consider Academic Breaks", 6, 2),
    #     ("Identify what gives you satisfaction in your studies and incorporate it further into your routine.", 
    #     "Find Satisfaction in Studies", 3, 0),
    #     ("Keep balancing your time between studying and personal hobbies.", 
    #     "Balance Studies and Hobbies", 3, 0),
    #     ("Explore more engaging study methods, such as gamification or visual tools like mind maps.", 
    #     "Use Engaging Study Methods", 3, 1),
    #     ("Connect with peers to exchange ideas and make studying more dynamic.", 
    #     "Connect with Peers", 3, 1),
    #     ("Reflect on your academic motivations and goals. Discuss them with a mentor or counselor.", 
    #     "Reflect on Academic Goals", 3, 2),
    #     ("Modify your study environment to make it more comfortable and less stressful.", 
    #     "Improve Study Environment", 3, 2),
    #     ("Maintain a regular sleep routine, going to bed and waking up at consistent times.", 
    #     "Maintain a Sleep Routine", 1, 0),
    #     ("Avoid caffeine or electronic devices before bedtime.", 
    #     "Avoid Caffeine Before Bed", 1, 0),
    #     ("Try relaxation techniques like meditation or reading a book before sleeping.", 
    #     "Try Relaxation Before Bed", 1, 1),
    #     ("Create a better sleep environment: ensure it’s dark, quiet, and at a comfortable temperature.", 
    #     "Create an Optimal Sleep Environment", 1, 1),
    #     ("Consult a doctor if you’re experiencing insomnia or sleep disturbances.", 
    #     "Consult a Doctor for Sleep Issues", 1, 2),
    #     ("Adopt an evening routine that encourages deep, restorative sleep.", 
    #     "Adopt an Evening Routine", 1, 2),
    #     ("Continue following a balanced diet, including fresh and nutritious foods.", 
    #     "Follow a Balanced Diet", 2, 0),
    #     ("Monitor your hydration and ensure you drink enough water.", 
    #     "Monitor Hydration", 2, 0),
    #     ("Reduce the intake of sugars and processed foods. Add more fruits, vegetables, and proteins to your diet.", 
    #     "Reduce Sugars and Eat Healthy", 2, 1),
    #     ("Plan meals in advance to avoid skipping meals.", 
    #     "Plan Meals Ahead", 2, 1),
    #     ("Consult a nutritionist to create a diet plan that enhances both mental and physical well-being.", 
    #     "Consult a Nutritionist", 2, 2),
    #     ("Avoid relying on comfort food and seek healthier alternatives to manage stress.", 
    #     "Avoid Comfort Food", 2, 2),
    #     ("Talk to someone you trust about your feelings, even if they seem mild.", 
    #     "Talk About Feelings", 8, 0),
    #     ("Keep track of your emotions with a journal or a mental health app.", 
    #     "Track Emotions", 8, 0),
    #     ("Seek professional help from a counselor or psychologist. Don’t ignore these warning signs.", 
    #     "Seek Professional Help", 8, 1),
    #     ("Join support groups to connect with others experiencing similar challenges.", 
    #     "Join Support Groups", 8, 1),
    #     ("Reach out to a mental health professional or emergency services immediately.", 
    #     "Reach Out for Immediate Help", 8, 2),
    #     ("Speak with trusted friends or family members and avoid dealing with these thoughts alone.", 
    #     "Speak with Trusted People", 8, 2),
    #     ("Maintain a healthy balance between work/study and personal time.", 
    #     "Balance Work and Personal Time", 4, 0),
    #     ("Take regular breaks to enhance productivity and avoid burnout.", 
    #     "Take Regular Breaks", 4, 0),
    #     ("Consider reducing intense study or work hours if possible.", 
    #     "Reduce Intense Work Hours", 4, 1),
    #     ("Use productivity techniques like the Pomodoro method to manage time effectively.", 
    #     "Use the Pomodoro Method", 4, 1),
    #     ("Consider significantly reducing your workload.", 
    #     "Consider Reducing Workload", 4, 2),
    #     ("Consult a counselor for strategies to manage your time and stress more effectively.", 
    #     "Consult a Counselor for Strategies", 4, 2),
    #     ("Continue monitoring your expenses and maintaining a good budget.", 
    #     "Monitor Expenses and Budget", 7, 0),
    #     ("Look for ways to save or explore opportunities for additional income.", 
    #     "Explore Income Opportunities", 7, 0),
    #     ("Talk to a financial advisor to identify short- and long-term solutions.", 
    #     "Consult a Financial Advisor", 7, 1),
    #     ("Focus on essential expenses and avoid unnecessary spending.", 
    #     "Focus on Essential Expenses", 7, 1),
    #     ("Seek financial aid programs or scholarships, if applicable.", 
    #     "Seek Financial Aid", 7, 2),
    #     ("Share your financial concerns with trusted family members or friends for support.", 
    #     "Share Financial Concerns", 7, 2),
    # ]

    # # Inserimento dei record nel database
    # for description, title, category_id, level in records:
    #     cursor.execute('''
    #     INSERT INTO suggestions (title, description, category_id, level)
    #     VALUES (?, ?, ?, ?)
    #     ''', (title, description, category_id, level))    
    conn.commit()


def get_users():
    conn = sqlite3.connect('mindhug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

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
