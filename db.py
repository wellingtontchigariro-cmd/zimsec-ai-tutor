import sqlite3

DB_NAME = "zimsec.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, name TEXT, score INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY, subject TEXT, question TEXT, answer TEXT)''')
    conn.commit()
    conn.close()

def add_user(phone, name="Student"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (phone, name) VALUES (?,?)", (phone, name))
    conn.commit()
    conn.close()

def get_user(phone):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE phone=?", (phone,))
    user = c.fetchone()
    conn.close()
    return user

def update_score(phone, points):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET score = score +? WHERE phone=?", (points, phone))
    conn.commit()
    conn.close()

def add_question(subject, question, answer):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO questions (subject, question, answer) VALUES (?,?,?)", (subject, question, answer))
    conn.commit()
    conn.close()

def get_random_question(subject):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE subject=? ORDER BY RANDOM() LIMIT 1", (subject,))
    q = c.fetchone()
    conn.close()
    return q
