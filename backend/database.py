import sqlite3

conn = sqlite3.connect("candidates.db", check_same_thread=False)
cursor = conn.cursor()


def create_table():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        skills TEXT,
        experience INTEGER,
        score REAL
    )
    """)

    conn.commit()


def insert_candidate(email, skills, experience):

    cursor.execute("""
    INSERT INTO candidates (email, skills, experience, score)
    VALUES (?, ?, ?, 0)
    ON CONFLICT(email)
    DO UPDATE SET
        skills=excluded.skills,
        experience=excluded.experience
    """, (email, skills, experience))

    conn.commit()


def get_all_candidates():

    cursor.execute("SELECT * FROM candidates")

    candidates = cursor.fetchall()

    return candidates


def update_score(email, score):

    cursor.execute(
        "UPDATE candidates SET score=? WHERE email=?",
        (score, email)
    )

    conn.commit()