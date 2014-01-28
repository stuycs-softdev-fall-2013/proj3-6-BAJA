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
    return render_template("ListOfTeachers.html", teachers=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=get_port("school"), debug=True)
