import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = 'school_feedback.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def register_teacher(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO teachers (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        return True, 'Account created successfully.'
    except sqlite3.IntegrityError:
        return False, 'Username already exists. Please choose a different one.'
    finally:
        conn.close()


def login_teacher(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT teacher_id, password_hash FROM teachers WHERE username = ?',
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False, None

    teacher_id, stored_hash = row

    if check_password_hash(stored_hash, password):
        return True, teacher_id

    return False, None
