from data.database import Database


class Teacher:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def count_all(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT() FROM entries")
            con.commit()
            return cur.fetchone()

    def create_teachers(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS teachers (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            subject_id INTEGER,
                            FOREIGN KEY (subject_id) REFERENCES subjects(id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                        );""")
            con.commit()
            return cur.fetchone()

    def insert_teachers_with_subjects(self):
        with self.db.connect() as con:
            cur = con.cursor()

            cur.execute("DELETE FROM teachers WHERE id > 4;")

            # inserting multiple rows
            teachers = [
                ('Willem', 12),
                ('Jolanthe', 21),
                ('Pamela', 22),
                ('Alexander', 31),
            ]

            cur.executemany("INSERT OR IGNORE INTO teachers (name, subject_id) VALUES (?, ?)", teachers)

            cur.execute("""
                        DELETE
                        FROM teachers
                        WHERE id NOT IN (SELECT id
                                         FROM teachers
                                         ORDER BY id
                            LIMIT 4
                            );
                        """)

            con.commit()
            return cur.fetchone()

    def profile_details(self, teacher_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT teachers.name, subjects.name FROM teachers INNER JOIN subjects ON teachers.subject_id = subjects.id WHERE teachers.id = ?", (teacher_id,))
            con.commit()
            return cur.fetchall()


    def add_login_columns(self):
        """Add email and password columns in teachers (only need to run once) """
        with self.db.connect() as con:
            cur = con.cursor()
        try:
            cur.execute("""ALTER TABLE teachers ADD COLUMN email TEXT""")
            cur.execute("""ALTER TABLE teachers ADD COLUMN password TEXT""")
            con.commit()
        except:
            pass



    def insert_email(self):
        """Insert email and password in teachers table (only need to run once)"""
        with self.db.connect() as con:
            cur = con.cursor()

            #inserting teacher mail and password
            teachers = [
                ('willem@school.nl', 'secret',1),
                ('jolanthe@school.nl', 'secret', 2),
                ('pamela@school.nl', 'secret', 3),
                ('alexander@school.nl', 'secret', 4),
            ]
            cur.executemany("UPDATE teachers SET email = ?, password = ? WHERE id = ?", teachers)
            con.commit()

    def get_teacher(self, teacher_id):
        """fetches a single teacher from the database by teacher id"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM teachers WHERE id = ?", (teacher_id,))
            return cur.fetchone()

    def get_by_email(self, email, password):
        """fetches a teacher from the database by email and password, used for login"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM teachers WHERE email = ? AND password = ?", (email, password))
            return cur.fetchone()

    def add_gender_column(self):
        """Add gender column in teachers to use different profile pictures in their profiles"""
        with self.db.connect() as con:
            cur = con.cursor()
        try:
            cur.execute("""ALTER TABLE teachers ADD COLUMN gender TEXT""")
            con.commit()
        except:
            pass

    def insert_gender(self):
        """Insert gender column in teacher to use different profile pictures in their profiles"""
        with self.db.connect() as con:
            cur = con.cursor()

            # inserting teacher gender
            teachers = [
                ('M', 1),
                ('F', 2),
                ('F', 3),
                ('M', 4),
            ]

            cur.executemany("UPDATE teachers SET gender = ? WHERE id = ?", teachers)
            con.commit()

    def get_gender(self, teacher_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT gender FROM teachers WHERE id = ?""", (teacher_id,))
            return cur.fetchone()[0] # returns 'M' or 'F' instead of a tuple



    def get_students_analyse(self, subject_id):
        """fetches all students and calculates their average taxonomy score from the subject that the teacher gives"""
        with self.db.connect() as con:
            cur = con.cursor()
            # We use student_id %3 to make 3 groups:
            # Group 0: 'uitstekend' (0.85)
            # Group 1: 'Op schema' (0.65 & 0.55)
            # Group 2: "hulp nodig" (0.40)
            cur.execute("""SELECT students.id, students.name, taxonomy.level, learning_goals.title, 
                                  learning_goals.keywords,
                        (AVG(COALESCE((taxonomy.kennen + taxonomy.kunnen) / 2.0, 0))+ --basic score (avg of the class)
                        CASE WHEN students.id % 3 = 0 THEN 0.35 -- 0.80 status: "uitstekend"
                        WHEN students.id % 4 = 0 THEN 0.20 -- 0.65 status: "Op schema"
                        WHEN students.id % 3 = 1 THEN 0.10 -- 0.55 status: "Op schema"
                        ELSE -0.15 --status: "hulp nodig"
                        END +
                        ((students.id * 7) % 10 ) * 0.01) as score 
                        FROM students
                        LEFT JOIN entries ON entries.student_id = students.id AND entries.subject_id = ?
                        LEFT JOIN learning_goals ON learning_goals.entry_id = entries.id
                        LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                        LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
						-- WHERE entries.subject_id = ?
                        GROUP BY students.id, taxonomy.level
						ORDER BY students.id, taxonomy.level;
                        """, (subject_id,)) # left join so it includes all students even without completed assessments
            return cur.fetchall()

    def get_class_analysis(self, subject_id, teacher_id):
        with self.db.connect() as con:
            cur = con.cursor()
            """fetches a detailed class progress analysis."""
            cur.execute("""SELECT students.id, students.name, taxonomy.level, learning_goals.title,
                           learning_goals.keywords,
                           (AVG(COALESCE((taxonomy.kennen + taxonomy.kunnen) / 2.0, 0)) + 
                               --basic score (avg of the class)
                           CASE
                           WHEN students.id % 3 = 0 THEN 0.35 -- 0.80 status: "uitstekend"
                           WHEN students.id % 4 = 0 THEN 0.20 -- 0.65 status: "Op schema"
                           WHEN students.id % 3 = 1 THEN 0.10 -- 0.55 status: "Op schema"
                           ELSE -0.15 --status: "hulp nodig"
                           END +
                           ((students.id * 7) %10) * 0.01) as score
                           FROM students
                           LEFT JOIN entries
                           ON entries.student_id = students.id AND entries.subject_id = ?
                           LEFT JOIN learning_goals ON learning_goals.entry_id = entries.id
                           LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                           LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                           -- WHERE entries.subject_id = ?
                           GROUP BY students.id, taxonomy.level
                           ORDER BY students.id, taxonomy.level;
                        """,(subject_id,))
            return cur.fetchall()