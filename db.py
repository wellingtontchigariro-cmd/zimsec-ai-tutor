
import os
import sqlite3
import random

# Database file
DB_NAME = os.environ.get("DB_NAME", "zimsec.db")


def init_db():
    """Create the database tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    try:
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                phone TEXT PRIMARY KEY,
                score INTEGER DEFAULT 0
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        """)

        conn.commit()
    finally:
        conn.close()


def add_user(phone):
    """Register a user without resetting an existing score."""
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute(
            "INSERT OR IGNORE INTO users (phone, score) VALUES (?, 0)",
            (phone,)
        )
        conn.commit()
    finally:
        conn.close()


def update_score(phone, points):
    """Add points to a user's existing score."""
    add_user(phone)
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute(
            "UPDATE users SET score = score + ? WHERE phone = ?",
            (points, phone)
        )
        conn.commit()
    finally:
        conn.close()


def get_score(phone):
    conn = sqlite3.connect(DB_NAME)
    try:
        c = conn.cursor()
        c.execute("SELECT score FROM users WHERE phone = ?", (phone,))
        row = c.fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        return c.fetchall()
    finally:
        conn.close()


def get_random_question(subject):
    """Return a question as (id, subject, question, answer)."""
    conn = sqlite3.connect(DB_NAME)
    try:
        c = conn.cursor()
        c.execute(
            """SELECT id, subject, question, answer
               FROM questions
               WHERE LOWER(subject) = LOWER(?)""",
            (subject,)
        )
        questions = c.fetchall()
        return random.choice(questions) if questions else None
    finally:
        conn.close()


def add_question(subject, question, answer):
    """Add a question and its answer to the database."""
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute(
            """INSERT INTO questions (subject, question, answer)
               VALUES (?, ?, ?)""",
            (subject.strip().lower(), question, answer)
        )
        conn.commit()
    finally:
        conn.close()


# Initialise the database when this module is imported.
init_db()
