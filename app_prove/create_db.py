import sqlite3

# Connessione al database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Creazione della tabella users
c.execute('''
          CREATE TABLE IF NOT EXISTS users
          (username TEXT PRIMARY KEY,
          password TEXT)
          ''')

# Salva i cambiamenti e chiudi la connessione
conn.commit()
conn.close()
