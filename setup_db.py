import sqlite3

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_progress (
    username TEXT,
    category TEXT,
    difficulty TEXT,
    score INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS badges (
    username TEXT,
    badge TEXT
)
''')

print("Tables ensured.")
conn.commit()
conn.close()
