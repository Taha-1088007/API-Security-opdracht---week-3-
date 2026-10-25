from flask import Blueprint, render_template, request, session, redirect, g

from models.student import Student
from models.teacher import Teacher
from data.database import DB_PATH

auth_bp = Blueprint("auth", __name__)

teacher_model = Teacher(DB_PATH)
student_model = Student(DB_PATH)


def require_teacher():
    """if user is not teacher, redirect them to login page"""
    if not session.get("teacher_id"):
        return redirect("/login?role=teacher")
    return None


def require_student():
    """if user is not student, redirect them to login page"""
    if not session.get("student_id"):
        return redirect("/login?role=student")
    return None


def load_user():
    """identify logged in user and make their data available globally in templates"""
    g.current_user = None
    g.role = None

    teacher_id = session.get("teacher_id")
    student_id = session.get("student_id")

    if teacher_id:
        # fetch full teacher profile if logged in
        g.current_user = teacher_model.get_teacher(teacher_id)
        g.role = "teacher"
    elif student_id:
        # fetch full student profile if logged in
        g.current_user = student_model.get_student_basic(student_id)
        g.role = "student"


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    role = request.args.get("role") or request.form.get("role")
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        session.clear()  # clear old session data before logging in

        if role == "teacher":
            teacher = teacher_model.get_by_email(email, password)
            if teacher:
                # save teacher information in the session to stay logged in
                session["role"] = "teacher"
                session["teacher_id"] = teacher[0]  # index 0 is the id column
                return redirect("/teacher/home")
            error = "Verkeerd emailadres of wachtwoord"

        elif role == "student":
            student = student_model.get_by_email(email, password)
            if student:
                # save student information in the session to stay logged in
                session["role"] = "student"
                session["student_id"] = student[0] #index 0 is the id column
                return redirect("/student/home")
            error = "Verkeerd emailadres of wachtwoord"

        else:
            error = "Kies eerst een rol"

    return render_template("login.html", error=error, role=role)


@auth_bp.route("/logout")
def logout():
    """clear session and go back to landing page"""
    session.clear()
    return redirect("/")