import os

from IPython.lib.editorhooks import notepadplusplus
from flask import Blueprint, render_template, jsonify, session

from models.student import Student
from models.teacher import Teacher
from routes.authentication_route import require_student

student_bp = Blueprint("student", __name__, url_prefix="/student")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

student = Student(DB_PATH)
teacher = Teacher(DB_PATH)


def get_current_student_id():
    return session.get("student_id")


@student_bp.route("/home")
def home_student():
    """Student sees his own dashboard"""
    # check if the student is logged in, if not redirect to login
    auth_check = require_student()
    if auth_check:
        return auth_check

    student_id = get_current_student_id()
    if student_id is None:
        return "Geen student ingelogd", 401

    return render_template("student/home_student.html", student_id=student_id)


@student_bp.route("/api/home")
def student_home_api():
    auth_check = require_student()
    if auth_check:
        return auth_check

    student_id = get_current_student_id()
    if student_id is None:
        return jsonify({"error": "Geen student ingelogd"}), 401

    subjects = student.get_subjects_with_scores(student_id)  # retrieve all subjects and scores for students overview

    # Retrieve average scores from core subjects
    biology = student.get_student_avg_biology(student_id)
    physics = student.get_student_avg_physics(student_id)
    science = student.get_student_avg_science(student_id)
    math = student.get_student_avg_math(student_id)

    subject_score = [subject[2]
                     for subject in [biology, physics, science, math]
                     if subject and subject[2] is not None]
    avg = sum(subject_score) / len(subject_score) if subject_score else 0 # calculate overall average score


    valid_score = [s[2] for s in subjects if s[2] is not None]
    # avg = sum(valid_score) / len(valid_score) if valid_score else 0
    on_level = sum(1 for score in valid_score if score >= 0.6)

    return jsonify({
        "avg_score": round(avg * 10, 1), # multiply by 10 for a 1-10 grade and round to 1 decimal
        "on_level": on_level,
        "total": len(subjects)
    })


@student_bp.route("/profile_alternative")
def profile_student():
    auth_check = require_student()
    if auth_check:
        return auth_check

    student_id = get_current_student_id()
    if student_id is None:
        return "Geen student ingelogd", 401

    student_data = student.get_student_score_id(student_id)
    weak_subjects = student.get_weak_subjects(student_id)

    return render_template(
        "student/profile.html",
        student=student_data,
        weak_subjects=weak_subjects
    )


@student_bp.route("/learning_goals")
def learning_goals_student():
    auth_check = require_student()
    if auth_check:
        return auth_check

    student_id = get_current_student_id()
    if student_id is None:
        return "Geen student ingelogd", 401

    leerdoelen = student.get_leerbronnen(student_id)

    return render_template(
        "student/learning_goals.html",
        leerdoelen=leerdoelen
    )


@student_bp.route("/subjects")
def subjects():
    auth_check = require_student()
    if auth_check:
        return auth_check

    student_id = get_current_student_id()
    if student_id is None:
        return "Geen student ingelogd", 401

    return render_template("student/subjects.html", student_id=student_id)


@student_bp.route("/subjects/<int:subject_id>")
def subject_detail(subject_id):
    auth_check = require_student()
    if auth_check:
        return auth_check

    student_id = get_current_student_id()
    if student_id is None:
        return "Geen student ingelogd", 401

    radar_data = student.get_taxonomy_radar_data(student_id, subject_id)

    return render_template(
        "student/subject_detail.html",
        radar_data=radar_data,
        subject_id=subject_id
    )


@student_bp.route("/profile", methods=["GET", "POST"])
def alternative_profile_student():
    auth_check = require_student()
    if auth_check:
        return auth_check

    student_id = get_current_student_id()
    if student_id is None:
        return "Geen student ingelogd", 401

    student_data = student.get_student_score_id(student_id)
    weak_subjects = student.get_weak_subjects(student_id)
    gender = student.get_gender(student_id) # used to decide student's profile picture

    return render_template(
        "student/alternative_profile.html",
        student_id=student_id, gender=gender)

@student_bp.route("/api/profile_grades/<int:student_id>")
def profile_grades(student_id):
    """returns all (profile) grades of a specific student"""
    auth_check = require_student()
    if auth_check:
        return auth_check

    student_id = get_current_student_id()
    if student_id is None:
        return "Geen student ingelogd", 401

    student_biology = student.get_student_avg_biology(student_id)
    student_physics = student.get_student_avg_physics(student_id)
    student_science = student.get_student_avg_science(student_id)
    student_math = student.get_student_avg_math(student_id)

    return jsonify({
        "student_biology": student_biology,
        "student_physics": student_physics,
        "student_science": student_science,
        "student_math": student_math,
    })

@student_bp.route("/api/profile_subjects/<int:student_id>")
def profile_subjects(student_id):
    """returns all (profile) subjects of a student"""
    auth_check = require_student()
    if auth_check:
        return auth_check

    subjects_data = student.all_subjects()
    subjects_data = [subject[0] for subject in subjects_data]

    return jsonify({
        "subject_name": subjects_data
    })


@student_bp.route("/api/myteachers/<int:student_id>")
def student_myteachers(student_id):
    """returns all teachers of a student"""
    auth_check = require_student()
    if auth_check:
        return auth_check

    teachers_data = student.all_teachers()
    teachers_data = [teacher[0] for teacher in teachers_data]

    return jsonify({
        "teacher_name": teachers_data
    })


@student_bp.route("/api/name/<int:student_id>")
def student_name(student_id):
    """returns the name of a student"""
    auth_check = require_student()
    if auth_check:
        return auth_check

    # student_id = get_current_student_id()
    # if student_id is None:
    if get_current_student_id() is None:
        return jsonify({"error": "Geen student ingelogd"}), 401

    name = student.student_name(student_id)

    return jsonify({
        "student_name": name
    })

@student_bp.route("/progress", methods=["GET", "POST"])
def student_progress():
    student_id = session.get("student_id")
    return render_template("/student/student_progress_chart.html", student_id=student_id)

@student_bp.route("/api/student_progress_chart/<int:student_id>/<int:subject_id>")
def student_progress_chart_api(student_id, subject_id):
    auth_check = require_student()
    if auth_check:
        return auth_check

    if student_id is None:
        return jsonify({"error": "Geen student ingelogd"}), 401

    data = student.get_student_progress_chart(student_id, subject_id)
    return jsonify(data)
