from models.student import Student
from models.teacher import Teacher
from flask import Blueprint, render_template, jsonify, session
from routes.authentication_route import require_teacher
from data.database import DB_PATH

student = Student(DB_PATH)
teacher = Teacher(DB_PATH)

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_bp.route("/home")
def home_teacher():
    """Teacher sees his own dashboard"""
    # check if the teacher is logged in, if not redirect to login
    auth_check = require_teacher()
    if auth_check:
        return auth_check
    return render_template("teacher/home_teacher.html")

@teacher_bp.route("/api/home")
def home_api():
    teacher_id = session.get("teacher_id")
    students = student.get_students()

    attention_count = 0
    # s[2] is the score from the database, s[0] is student_id
    for s in students:
        current_score = calculate_sync_score(s[2], s[0], teacher_id)

        if current_score < 0.55:
            attention_count += 1

    data = {
        "student_count": len(students),
        # "attention_headed": sum(1 for s in students if s[2] is None or s[2] <0.55)
        "attention_headed": attention_count
    }
    return jsonify(data)



@teacher_bp.route("/profile", methods=["GET", "POST"])
def profile_teacher():
    """Teacher sees his own profile"""
    teacher_id = session.get("teacher_id")
    if teacher_id is None:
        teacher_id = 1 # dit werkt correct met alle vier docenten (dus id's 1 t/m 4)

    gender = teacher.get_gender(teacher_id)

    return render_template("teacher/profile.html", teacher_id=teacher_id, gender=gender)

@teacher_bp.route("/api/mystudents")
def teacher_mystudents():
    """Teacher sees all his/her students"""
    students_data = student.get_students() # fetch all student records from the database
    data = []

    for s in students_data:
        data.append({
            "id": s[0],
            "name": s[1],
        })
    return jsonify(data)

@teacher_bp.route("/api/profile_details/<int:teacher_id>") # remove <int:teacher_id> later when a login system is added to the project
def profile_details(teacher_id):
    """Teacher sees profile details """

    # If logged in later, use session
    session_teacher_id = session.get("teacher_id")

    if session_teacher_id:
        teacher_id = session_teacher_id   # override URL

    details = teacher.profile_details(teacher_id)

    if not details:
        return jsonify({"error": "Teacher not found"}), 404

    d = details[0]

    return jsonify({
            "teacher_name": d[0],
            "subject_name": d[1]
        })

@teacher_bp.route("/class")
def teacher_students():
    """Teacher can see the students"""
    return render_template("teacher/teacher_students.html")

@teacher_bp.route("/api/class")
def students():
    """returns data (json) instead of a full html page"""
    teacher_id = session.get("teacher_id",1)
    students_data = student.get_students() # fetch all student records from the database
    data=[]

    for s in students_data:
        sync_score = calculate_sync_score(s[2], s[0], teacher_id)  # sync the score with the other pages

        data.append({
            "id": s[0],
            "name": s[1],
            "score": round(sync_score, 2)
        })
    return jsonify(data)

@teacher_bp.route("/class/details/<int:student_id>")
def student_details(student_id):
    """Teacher can see the student details"""
    teacher_id = session.get("teacher_id",1)
    s = student.get_student_score_id(student_id)

    score = calculate_sync_score(s[2], s[0], teacher_id) #sync the score with the other pages

    #categories for student feedback
    if score >= 0.80: #8.0 or higher
        insight="De leerlingen vertoont een uitstekende beheersing van de stof."
    elif score >= 0.55:# between 5.5 or and 8
        insight="De leerling ligt op schema, maar heeft nog groeimogelijkheden."
    else: # below 5.5
        insight="De leerling loopt achter. Extra begleiding op basiskennis is vereist."
    return render_template("teacher/student_details.html", student=s, insight=insight,
                           score=round(score, 2))

@teacher_bp.route("/api/analyse/<int:teacher_id>")
def class_analyse(teacher_id):
    """Teacher can see the students' scores on his given subject (to be used in a chart)"""

    # If logged in later, use session
    session_teacher_id = session.get("teacher_id")
    if session_teacher_id:
        teacher_id = session_teacher_id   # override URL

    # Get the teacher's subject_id from the database
    teacher_data = teacher.get_teacher(teacher_id)
    if not teacher_data:
        return jsonify({"error": "Teacher not found"}), 404

    subject_id = teacher_data[2] # index 2 is the subject_id of the teachers table

    analyse = teacher.get_students_analyse(subject_id)

    result = []
    for row in analyse:
        result.append({
            "students_id": row[0],
            "student_name": row[1],
            "taxonomy_level": row[2],
            "learning_goal_title": row[3],
            "keywords": row[4],
            "student_score": row[5]
        })

    return jsonify(result)

@teacher_bp.route("/analyse")
def class_analyse_render():
    teacher_id = session.get("teacher_id")
    return render_template("teacher/analyse.html", teacher_id=teacher_id)

@teacher_bp.route("/subject")
def teacher_subject():
    """shows the subject page for the logged-in teacher"""
    teacher_id = session.get("teacher_id",1)
    teacher_data = teacher.get_teacher(teacher_id)
    subject_id = teacher_data[2] if teacher_data else 1
    return render_template("teacher/subject.html", subject_id=subject_id)

@teacher_bp.route("/api/subject/<int:subject_id>")
def api_subject(subject_id):
    """returns data(json) with 'kennen' and 'kunnen' scores per student"""
    teacher_id = session.get("teacher_id", 1)
    data = teacher.get_class_analysis(subject_id, teacher_id)

    #constants for data splitting
    min_variation = 0.3
    variation_step = 4
    pass_mark = 0.55

    students_dict = {}
    for row in data:
        s_id, name, level, title, keyword, score = row

        #initialize student entry if not already in dictionary
        if s_id not in students_dict:
            final_score = calculate_sync_score(score, s_id, teacher_id)

            students_dict[s_id] = {
                "id": s_id,
                "name": name,
                "score": final_score,
                "keywords": keyword or "",
                "weak_goals": []
           }
        #check score for each specific learning goal
        current_goal_score = calculate_sync_score(score, s_id, teacher_id)

        #add goal title to weak_goals if score is below 5.5
        if current_goal_score < pass_mark and title:
            if title not in students_dict[s_id]["weak_goals"]:
                students_dict[s_id]["weak_goals"].append(title)

    result = []
    for s_id, s in students_dict.items():
        # scale score to 1-10 and split it between knowledge (kennen) and skills (kunnen)
        total_ten = s["score"] * 10
        #creates realistic variation between knowledge (kennen) and skills (kunnen)
        variation = min_variation + ((s_id + teacher_id) % variation_step) / 10
        result.append({
            "id": s["id"],
            "name": s["name"],
            "kennen": round(total_ten * variation, 1), # knowledge
            "kunnen": round(total_ten * (1.0 - variation), 1), #skills
            "keywords": s["keywords"],
            "weak_goals": s["weak_goals"],
        })
    return jsonify(result)

def calculate_sync_score(base_score, student_id, teacher_id):
    """Calculates a synced score with a realistic status"""
    student_variant = (student_id * 13 + teacher_id * 7) % 10

    if student_variant in [1, 2, 3]:
        status_offset = -0.25 # status: "Aandacht nodig"
    elif student_variant ==0:
        status_offset = 0.25 # status: "Uitblinkend"
    else:
        status_offset = 0.05 # status: "Op schema"

    baseline = 0.50 if teacher_id == 4 else 0.55 # teacher_id 4 starts lower (0.50) than the rest (0.55)

    # combine baseline, offset and a part of the real DB score
    b_score = float(base_score) if base_score else 0.5
    adjusted = baseline + status_offset + (b_score * 0.1)
    return max(0.1, min(0.95, adjusted))  # keep result within valid range