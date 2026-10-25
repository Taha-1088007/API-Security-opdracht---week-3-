from data.database import Database


class User:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def add_roles(self):
        with self.db.connect() as con:
            cur = con.cursor()

            # creating users table
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        id   INTEGER, 
                        role TEXT NOT NULL,
                        PRIMARY KEY (id)
                        );""")

            # inserting role values
            roles = [
                ('teacher',),
                ('student',)
            ]

            cur.executemany("INSERT OR IGNORE INTO users (role) VALUES (?)", roles)

            # limit table records to 2
            cur.execute("""
                        DELETE
                        FROM users
                        WHERE id NOT IN (SELECT id
                                         FROM users
                                         ORDER BY id
                            LIMIT 2
                            );
                        """)

            con.commit()
            return cur.fetchone()
