from flask import Flask, make_response, redirect, render_template, request, session

from game.database import Database
from game.utils import get_port

app = Flask(__name__)
app.secret_key = "Kk3lsHgOEuPqhMyWbRAByk1fOdN1XEMu"
db = Database("database.db")

@app.route("/")
def index():
    return render_template("BAJASchool.html")

@app.route("/student")
def student():
    return render_template("StudentLogin.html")

@app.route("/teacher")
def teacher():
    return render_template("TeacherLogin.html")

@app.route("/teachers")
def teachers():
    return render_template("ListOfTeachers.html", teachers=db.get_teachers())

@app.route("/teacher/<tid>")
def teacher_class(tid):
    return render_template("TeacherClass.html", students=db.get_students(tid))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=get_port("school"), debug=True)
