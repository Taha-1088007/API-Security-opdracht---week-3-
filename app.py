import os

from flask import Flask, render_template, g

from data.database import Database
from models.student import Student
from models.teacher import Teacher
from models.user import User
from routes.student_route import student_bp
from routes.teacher_route import teacher_bp
from routes.authentication_route import auth_bp, load_user

app = Flask(__name__)
app.secret_key = "super_secret_key"

app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(auth_bp)

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

_db = Database(DB_PATH)
_db.setup_tables()

student = Student(DB_PATH)
teacher = Teacher(DB_PATH)
user = User(DB_PATH)

# Alleen laten staan als deze functies veilig meerdere keren kunnen draaien.
teacher.create_teachers()
teacher.insert_teachers_with_subjects()
teacher.add_login_columns()
teacher.insert_email()
teacher.add_gender_column()
teacher.insert_gender()
student.add_login_columns()
student.insert_email()
student.add_gender_column()
student.insert_gender()
user.add_roles()


@app.route("/")
def index():
    counts = {
        "student": student.count_all()[0],
        "teacher": teacher.count_all()[0],
    }
    return render_template("index.html")


@app.before_request
def before_request():
    # Runs before every single request to identify the logged-in user.
    load_user()


@app.context_processor
def insert_user():
    # Makes current_user and role variables automatically available in every HTML template
    return {
        "current_user": g.get("current_user"),
        "role": g.get("role")
    }


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

print("APP DB_PATH =", DB_PATH)