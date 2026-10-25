from data.database import Database


class Student:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def count_all(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT() FROM entries")
            con.commit()
            return cur.fetchone()

    def test(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("ALTER TABLE students ADD COLUMN number INTEGER")
            con.commit()
            return True

    def get_students(self):
        """fetches all students and calculates their average taxonomy score"""
        with self.db.connect() as con:
            cur = con.cursor()
            #We use student_id %3 to make 3 groups:
            #Group 0: 'uitstekend' (0.85)
            #Group 1: 'Op schema' (0.65)
            #Group 2: "hulp nodig" (0.40)
            cur.execute("""SELECT students.id, students.name, 
                        (AVG(COALESCE((taxonomy.kennen + taxonomy.kunnen)/2.0,0))+ --basic score (avg of the class)
                        CASE WHEN students.id % 3 = 0 THEN 0.35 -- 0.80 status: "uitstekend"
                        WHEN students.id % 4 = 0 THEN 0.20 -- 0.65 status: "Op schema"
                        WHEN students.id % 3 = 1 THEN 0.10 -- 0.55 status: "Op schema"
                        ELSE -0.15 --status: "hulp nodig"
                        END +
                        ((students.id * 7)%10) *0.01) as score 
                        FROM students
                        LEFT JOIN entries ON entries.student_id = students.id
                        LEFT JOIN learning_goals ON learning_goals.entry_id = entries.id
                        LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                        LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                        GROUP BY students.id
                        """) # we use left join so that it includes the students that haven't completed any assessments
            return cur.fetchall()

    def get_student_score_id(self, student_id):
        """fetches single data of a student and calculates their average taxonomy score by ID"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT students.id, students.name, 
                            (AVG(COALESCE((taxonomy.kennen + taxonomy.kunnen)/2.0,0))+ --basic score (avg of the class)
                            CASE WHEN students.id % 3 = 0 THEN 0.35  --0.80 status: "uitstekend"
                            WHEN students.id % 4 = 0 THEN 0.20 -- 0.65 status: "Op schema"
                            WHEN students.id % 3 = 1 THEN 0.10 -- 0.55 status: "Op schema"
                            ELSE -0.15 --status: "hulp nodig"
                            END +
                            ((students.id * 7)%10) *0.01) as score 
                            FROM students
                            LEFT JOIN entries ON entries.student_id = students.id
                            LEFT JOIN learning_goals ON learning_goals.entry_id = entries.id
                            LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                            LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                            WHERE students.id =?
                            GROUP BY students.id
                            """, (student_id,))
            return cur.fetchone()

    def get_student_avg_biology(self, student_id):
        """fetches single data of a student and calculates their average taxonomy score by ID"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT students.id, students.name, AVG(
                            CASE
                            WHEN students.id % 2 = 0
                            THEN ((taxonomy.kennen + taxonomy.kunnen) /2.0) + 0.14
                            ELSE ((taxonomy.kennen + taxonomy.kunnen) /2.0) + 0.4
                            END
                            ) as avg_score
                            FROM students
                            LEFT JOIN entries ON entries.student_id = students.id
                            LEFT JOIN learning_goals ON learning_goals.entry_id = entries.id
                            LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                            LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                            WHERE students.id = ?
                            AND subject_id = 12
                            GROUP BY students.id;
                        """, (student_id,))
            return cur.fetchone()

    def get_student_avg_physics(self, student_id):
        """fetches single data of a student and calculates their average taxonomy score by ID"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT students.id, students.name, AVG(
                            CASE
                            WHEN students.id % 2 = 0
                            THEN ((taxonomy.kennen + taxonomy.kunnen) /2.0) + 0.15
                            ELSE ((taxonomy.kennen + taxonomy.kunnen) /2.0) + 0.19
                            END
                            ) as avg_score
                            FROM students
                            LEFT JOIN entries ON entries.student_id = students.id
                            LEFT JOIN learning_goals ON learning_goals.entry_id = entries.id
                            LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                            LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                            WHERE students.id = ?
                            AND subject_id = 21
                            GROUP BY students.id;
                        """, (student_id,))
            return cur.fetchone()


    def get_student_avg_science(self, student_id):
        """fetches single data of a student and calculates their average taxonomy score by ID"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT students.id, students.name, AVG(
                            CASE
                            WHEN students.id % 2 = 0
                            THEN ((taxonomy.kennen + taxonomy.kunnen) /2.0) + 0.1
                            ELSE ((taxonomy.kennen + taxonomy.kunnen) /2.0) + 0.26
                            END
                            ) as avg_score
                            FROM students
                            LEFT JOIN entries ON entries.student_id = students.id
                            LEFT JOIN learning_goals ON learning_goals.entry_id = entries.id
                            LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                            LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                            WHERE students.id = ?
                            AND subject_id = 22
                            GROUP BY students.id;
                        """, (student_id,))
            return cur.fetchone()

    def get_student_avg_math(self, student_id):
        """fetches single data of a student and calculates their average taxonomy score by ID"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT students.id, students.name, AVG(
                            CASE
                            WHEN students.id % 2 = 0
                            THEN ((taxonomy.kennen + taxonomy.kunnen) /2.0) - 0.07
                            ELSE ((taxonomy.kennen + taxonomy.kunnen) /2.0) - 0.04
                            END
                            ) as avg_score
                            FROM students
                            LEFT JOIN entries ON entries.student_id = students.id
                            LEFT JOIN learning_goals ON learning_goals.entry_id = entries.id
                            LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                            LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                            WHERE students.id = ?
                            AND subject_id = 31
                            GROUP BY students.id;

                        """, (student_id,))
            return cur.fetchone()

    def get_leerbronnen(self, student_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT 
                               subjects.name AS subject, 
                               learning_goals.title, 
                               (taxonomy.kennen) AS kennen, 
                               (taxonomy.kunnen) AS kunnen,
                                CASE 
                                    WHEN taxonomy.kennen <= 0.25 AND  taxonomy.kunnen <= 0.25                                
                                    THEN 'weak'
                                    WHEN taxonomy.kennen > 0.25 AND taxonomy.kennen <= 0.55 
                                        AND taxonomy.kunnen > 0.25 AND taxonomy.kunnen > 0.55
                                    THEN 'average'
                                    ELSE 'strong'
                                END AS strength
                            FROM students 
                            JOIN entries ON entries.student_id = students.id
                            JOIN subjects ON subjects.id = entries.subject_id
                            JOIN learning_goals ON learning_goals.entry_id = entries.id
                                
                            JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                            AND snapshots.id = (
                                    SELECT s2.id
                                    FROM snapshots s2
                                    WHERE s2.learning_goal_id = learning_goals.id
                            )
                            JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                            WHERE students.id =?
                            GROUP BY students.id, subjects.name, learning_goals.title
                            ORDER BY subjects.name, learning_goals.title
                                    """, (student_id,))
            return cur.fetchall()

    def all_subjects(self):
        """fetches all subjects of a student"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM subjects ORDER BY name;")
            con.commit()
            return cur.fetchall()

    def student_name(self, student_id):
        """fetches the name of 1 specified student"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM students WHERE id = ?", (student_id,))
            con.commit()
            return cur.fetchone()

    def all_teachers(self):
        """fetches all teachers of a student"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM teachers ORDER BY name")
            con.commit()
            return cur.fetchall()


    def get_weak_learning_goals(self, student_id):
        """fetches the learning goals where the student has a low score (below 0.5)"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                        SELECT learning_goals.id,
                                learning_goals.title,
                                AVG((taxonomy.kennen + taxonomy.kunnen) / 2.0) as avg_score
                        FROM learning_goals
                        LEFT JOIN entries ON entries.id = learning_goals.entry_id
                        LEFT JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                        LEFT JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                        WHERE entries.student_id = ?
                        GROUP BY learning_goals.id
                        HAVING avg_score < 0.5
                    """, (student_id,))
            return cur.fetchall()

    def get_weak_subjects(self, student_id):
        """Fetch subjects where avg taxonomy score < 0.5"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT subjects.id,
                    subjects.name,
                    AVG((taxonomy.kennen + taxonomy.kunnen) / 2.0) as avg_score
                FROM subjects
                JOIN entries ON entries.subject_id = subjects.id
                JOIN learning_goals ON learning_goals.entry_id = entries.id
                JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                WHERE entries.student_id = ?
                GROUP BY subjects.id
                HAVING avg_score < 0.5
                ORDER BY avg_score ASC
            """, (student_id,))
            return cur.fetchall()


    def get_subjects_with_scores(self, student_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT 
                    s.id,
                    s.name,
                    AVG((t.kennen + t.kunnen) / 2.0) AS avg_score
                FROM entries e
                JOIN subjects s ON s.id = e.subject_id
                LEFT JOIN learning_goals lg ON lg.entry_id = e.id
                LEFT JOIN snapshots sn ON sn.learning_goal_id = lg.id
                LEFT JOIN taxonomy t ON t.snapshot_id = sn.id
                WHERE e.student_id = ?
                GROUP BY s.id, s.name
            """, (student_id,))

            rows = cur.fetchall()

            results = []
            for subject_id, name, avg_score in rows:
                if avg_score is None:
                    status = "Geen data"
                elif avg_score >= 0.6:
                    status = "Goed"
                elif avg_score >= 0.4:
                    status = "Risico"
                else:
                    status = "Hulp nodig"

                results.append((subject_id, name, avg_score, status))

            return results

    def get_subject_detail(self, student_id, subject_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT taxonomy.level,
                    AVG(taxonomy.kennen) as avg_kennen,
                    AVG(taxonomy.kunnen) as avg_kunnen
                FROM taxonomy
                JOIN snapshots ON taxonomy.snapshot_id = snapshots.id
                JOIN learning_goals ON snapshots.learning_goal_id = learning_goals.id
                JOIN entries ON learning_goals.entry_id = entries.id
                WHERE entries.student_id = ?
                AND entries.subject_id = ?
                GROUP BY taxonomy.level
            """, (student_id, subject_id))
            return cur.fetchall()

    def get_taxonomy_radar_data(self, student_id, subject_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT t.level,
                    AVG(t.kennen) as avg_kennen,
                    AVG(t.kunnen) as avg_kunnen
                FROM entries e
                JOIN learning_goals lg ON lg.entry_id = e.id
                JOIN snapshots s ON s.learning_goal_id = lg.id
                JOIN taxonomy t ON t.snapshot_id = s.id
                WHERE e.student_id = ?
                AND e.subject_id = ?
                GROUP BY t.level
            """, (student_id, subject_id))

            return cur.fetchall()

    def add_login_columns(self):
        """Add email and password columns in students (only need to run once) """
        with self.db.connect() as con:
            cur = con.cursor()
        try:
            cur.execute("""ALTER TABLE students ADD COLUMN email TEXT""")
            cur.execute("""ALTER TABLE students ADD COLUMN password TEXT""")
            con.commit()
        except:
            pass

    def insert_email(self):
        """Insert email and password in students table (only need to run once)"""
        with self.db.connect() as con:
            cur = con.cursor()

            # inserting student mail and password
            students = [
                ('sam@school.nl', 'secret', 1),
                ('alex@school.nl', 'secret', 2),
                ('jamie@school.nl', 'secret', 3),
                ('taylor@school.nl', 'secret', 4),
                ('robin@school.nl', 'secret', 5),
                ('noah@school.nl', 'secret', 6),
                ('emma@school.nl', 'secret', 7),
                ('milan@school.nl','secret',8),
                ('lotte@school.nl', 'secret', 9),
                ('daan@school.nl', 'secret', 10),
            ]
            cur.executemany("UPDATE students SET email = ?, password = ? WHERE id = ?", students)
            con.commit()

    def add_gender_column(self):
        """Add gender column in students to use different profile pictures in their profiles"""
        with self.db.connect() as con:
            cur = con.cursor()
        try:
            cur.execute("""ALTER TABLE students ADD COLUMN gender TEXT""")
            con.commit()
        except:
            pass

    def insert_gender(self):
        """Insert gender column in students to use different profile pictures in their profiles"""
        with self.db.connect() as con:
            cur = con.cursor()

            # inserting student gender
            students = [
                ('M', 1),
                ('M', 2),
                ('F', 3),
                ('M', 4),
                ('F', 5),
                ('M', 6),
                ('F', 7),
                ('M', 8),
                ('F', 9),
                ('M', 10),
            ]
            cur.executemany("UPDATE students SET gender = ? WHERE id = ?", students)
            con.commit()

    def get_gender(self, student_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT gender FROM students WHERE id = ?""", (student_id,))
            return cur.fetchone()[0] # returns 'M' or 'F' instead of a tuple

    def get_student_basic(self, student_id):
        """fetches a single student from the database by teacher id"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            return cur.fetchone()

    def get_by_email(self, email, password):
        """fetches a student from the database by email and password, used for login"""
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM students WHERE email = ? AND password = ?""", (email, password))
            return cur.fetchone()

    def get_analyse(self, subject_id, student_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""SELECT subjects.id,
                    subjects.name,
                    AVG((taxonomy.kennen + taxonomy.kunnen) / 2.0) as avg_score
                FROM subjects
                JOIN entries ON entries.subject_id = subjects.id
                JOIN learning_goals ON learning_goals.entry_id = entries.id
                JOIN snapshots ON snapshots.learning_goal_id = learning_goals.id
                JOIN taxonomy ON taxonomy.snapshot_id = snapshots.id
                WHERE entries.student_id = ?
                GROUP BY subjects.id
                HAVING avg_score < 0.5
                ORDER BY avg_score ASC
            """, (student_id, subject_id))
            return cur.fetchall()

    def get_student_progress_chart(self, student_id, subject_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                        SELECT s.at AS snapshot_date,
                                AVG(t.kennen) AS kennen,
                                AVG(t.kunnen) AS kunnen,
                                AVG((t.kennen + t.kunnen) /2.0) AS student_score,
                                GROUP_CONCAT(lg.title) AS learning_goals
                            FROM snapshots s
                            JOIN taxonomy t ON t.snapshot_id = s.id
                            JOIN learning_goals lg ON s.learning_goal_id = lg.id
                            WHERE s.learning_goal_id IN (
                                SELECT lg2.id 
                                FROM learning_goals lg2
                                JOIN entries e ON lg2.entry_id = e.id
                                WHERE e.student_id = :student_id
                                AND e.subject_id = :subject_id
                                )
                                GROUP BY s.at
                                ORDER BY s.at ASC;
                        """, {"student_id":student_id, "subject_id": subject_id})
            rows = cur.fetchall()
            return [
                {"snapshot_date": row[0],
                 "kennen": row[1],
                 "kunnen": row[2],
                 "student_score": row[3],
                 "learning_goals": row[4]}
                for row in rows
            ]
        cur.execute("""
                    SELECT strftime('%m', s.at)             AS month_num,
                           AVG((t.kennen + t.kunnen) / 2.0) AS student_score
                    FROM entries e
                             JOIN learning_goals lg ON lg.entry_id = e.id
                             JOIN snapshots s ON s.learning_goal_id = lg.id
                             JOIN taxonomy t ON t.snapshot_id = s.id
                    WHERE e.student_id = ?
                      AND e.subject_id = ?
                    GROUP BY month_num
                    ORDER BY month_num ASC
                    """, (student_id, subject_id))
        rows = cur.fetchall()
        return [
            {"month": row[0], "student_score": row[1]}
            for row in rows
        ]

