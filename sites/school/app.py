from flask import Flask, make_response, redirect, render_template, request, session

from game.database import Database
from game.utils import get_port

app = Flask(__name__)
app.secret_key = "Kk3lsHgOEuPqhMyWbRAByk1fOdN1XEMu"
db = Database("database.db")

@app.route("/")
def index():
    return render_template("BAJASchool.html")

@app.route("/students")
def student():
    if request.method == "POST":
        student_name = request.form.get("student")
        password = request.form.get("password")
        try:
            student = db.get_student(student_name)
        except IndexError:
            return render_template("StudentLogin.html", error="Incorrect login.")
        if student[2] == password:
            session["student"] = student[0]
            return redirect("/student/grades")
    return render_template("StudentLogin.html")

@app.route("/students/grades")
def grades():
    if "student" not in session:
        return redirect("/students")
    return render_template("StudentGrades", student=db.get_student(session["student"]))

@app.route("/teachers", methods=["GET", "POST"])
def teacher():
    if request.method == "POST":
        if request.form.get("password") == "J8lSYJ":
            session["teacher"] = True
            return redirect("/teachers/list")
        return render_template("TeacherLogin.html", error="Incorrect login.")
    return render_template("TeacherLogin.html")

@app.route("/logout")
def logout():
    session.pop("student", None)
    session.pop("teacher", None)
    return redirect("/")

@app.route("/teachers/list")
def teachers():
    if "teacher" not in session:
        return redirect("/teachers")
    return render_template("ListOfTeachers.html", teachers=db.get_teachers())

@app.route("/teachers/<tid>", methods=["GET", "POST"])
def teacher_class(tid):
    if "teacher" not in session:
        return redirect("/teachers")
    if request.method == "POST":
        try:
            student_id = int(request.form["student"])
            grade = int(request.form["grade"])
        except (KeyError, ValueError):
            pass
        else:
            db.grade_student(student_id, tid, grade)
    return render_template("TeacherClass.html", teacher=db.get_teacher(tid), students=db.get_students(tid))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=get_port("school"), debug=True)
