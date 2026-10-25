import json
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")
JSON_PATH = os.path.join(BASE_DIR, "data", "data-sample.json")

conn = sqlite3.connect(DB_PATH, timeout=5)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# Maak alles eerst leeg
cur.execute("DELETE FROM taxonomy")
cur.execute("DELETE FROM snapshots")
cur.execute("DELETE FROM learning_goals")
cur.execute("DELETE FROM entries")
cur.execute("DELETE FROM subjects")
cur.execute("DELETE FROM students")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data.get("entries", []):
    student = entry.get("student", {})
    subject = entry.get("subject", {})

    student_id = student.get("id")
    student_name = student.get("name")
    subject_id = subject.get("id")
    subject_name = subject.get("name")

    cur.execute("""
        INSERT OR IGNORE INTO students (id, name)
        VALUES (?, ?)
    """, (student_id, student_name))

    cur.execute("""
        INSERT OR IGNORE INTO subjects (id, name)
        VALUES (?, ?)
    """, (subject_id, subject_name))

    cur.execute("""
        INSERT INTO entries (student_id, subject_id)
        VALUES (?, ?)
    """, (student_id, subject_id))
    entry_id = cur.lastrowid

    for lg in entry.get("learningGoals", []):
        cur.execute("""
            INSERT INTO learning_goals (external_id, title, keywords, entry_id)
            VALUES (?, ?, ?, ?)
        """, (
            lg.get("id"),
            lg.get("title"),
            json.dumps(lg.get("keywords")),
            entry_id
        ))
        learning_goal_id = cur.lastrowid

        for snapshot in lg.get("snapshots", []):
            source = snapshot.get("source", {})

            cur.execute("""
                INSERT INTO snapshots (at, source_type, source_id, learning_goal_id)
                VALUES (?, ?, ?, ?)
            """, (
                snapshot.get("at"),
                source.get("type"),
                source.get("id"),
                learning_goal_id
            ))
            snapshot_id = cur.lastrowid

            for tax in snapshot.get("taxonomy", []):
                cur.execute("""
                    INSERT INTO taxonomy (level, kennen, kunnen, confidence, snapshot_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    tax.get("level"),
                    tax.get("kennen"),
                    tax.get("kunnen"),
                    tax.get("confidence"),
                    snapshot_id
                ))

conn.commit()
conn.close()

print("Import voltooid.")