import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def connect(self):
        con = sqlite3.connect(self.db_path, timeout=5)
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def setup_tables(self):
        conn = sqlite3.connect(self.db_path, timeout=5)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                password TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(subject_id) REFERENCES subjects(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                external_id TEXT NOT NULL,
                title TEXT NOT NULL,
                keywords TEXT NOT NULL,
                entry_id INTEGER NOT NULL,
                FOREIGN KEY(entry_id) REFERENCES entries(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                at TEXT NOT NULL,
                source_type TEXT,
                source_id TEXT,
                learning_goal_id INTEGER NOT NULL,
                FOREIGN KEY(learning_goal_id) REFERENCES learning_goals(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS taxonomy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                kennen REAL,
                kunnen REAL,
                confidence REAL,
                snapshot_id INTEGER NOT NULL,
                FOREIGN KEY(snapshot_id) REFERENCES snapshots(id)
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_entries_student_id
            ON entries(student_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_entries_subject_id
            ON entries(subject_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_learning_goals_entry_id
            ON learning_goals(entry_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_snapshots_learning_goal_id
            ON snapshots(learning_goal_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_taxonomy_snapshot_id
            ON taxonomy(snapshot_id)
        """)

        conn.commit()
        conn.close()


def load_sample_data(db_path: str):
    conn = sqlite3.connect(db_path, timeout=5)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    sample_path = os.path.join(BASE_DIR, "data-sample.json")
    with open(sample_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data.get("entries", []):
        student = entry.get("student", {})
        subject = entry.get("subject", {})

        student_id = student.get("id")
        student_name = student.get("name")
        subject_id = subject.get("id")
        subject_name = subject.get("name")

        cursor.execute("""
            INSERT OR IGNORE INTO students (id, name)
            VALUES (?, ?)
        """, (student_id, student_name))

        cursor.execute("""
            INSERT OR IGNORE INTO subjects (id, name)
            VALUES (?, ?)
        """, (subject_id, subject_name))

        cursor.execute("""
            INSERT INTO entries (student_id, subject_id)
            VALUES (?, ?)
        """, (student_id, subject_id))
        entry_id = cursor.lastrowid

        for lg in entry.get("learningGoals", []):
            cursor.execute("""
                INSERT INTO learning_goals (external_id, title, keywords, entry_id)
                VALUES (?, ?, ?, ?)
            """, (lg.get("id"), lg.get("title"), lg.get("keywords"), entry_id))
            learning_goal_id = cursor.lastrowid

            for snapshot in lg.get("snapshots", []):
                source = snapshot.get("source", {})

                cursor.execute("""
                    INSERT INTO snapshots (at, source_type, source_id, learning_goal_id)
                    VALUES (?, ?, ?, ?)
                """, (
                    snapshot.get("at"),
                    source.get("type"),
                    source.get("id"),
                    learning_goal_id
                ))
                snapshot_id = cursor.lastrowid

                for tax in snapshot.get("taxonomy", []):
                    cursor.execute("""
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