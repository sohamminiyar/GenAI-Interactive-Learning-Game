import sqlite3

DB_NAME = "user_data.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        score INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS badges (
        username TEXT,
        badge TEXT,
        FOREIGN KEY(username) REFERENCES users(username)
    )
    """)

    conn.commit()
    conn.close()

def update_user_score(username, score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, score) VALUES (?, ?) ON CONFLICT(username) DO UPDATE SET score=?", (username, score, score))
    conn.commit()
    conn.close()

def get_user_score(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def assign_badge(username, badge):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO badges (username, badge) VALUES (?, ?)", (username, badge))
    conn.commit()
    conn.close()

def get_badges(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT badge FROM badges WHERE username=?", (username,))
    badges = [row[0] for row in cursor.fetchall()]
    conn.close()
    return badges
