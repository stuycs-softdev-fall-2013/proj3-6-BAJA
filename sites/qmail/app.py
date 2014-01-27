from json import dumps

from flask import Flask, redirect, render_template, request, session

from game.database import Database

app = Flask(__name__)
app.secret_key = "X7jfId6Jb8T3sxVJ6xMQeEfGkqm3Qwft"
db = Database("database.db")

PORT = 6680

# End-user routes

@app.route("/")
def index():
    if not session.get("user"):
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    address = request.form.get("address")
    password = request.form.get("password")
    if not address or not password:
        return render_template("login.html", error="All fields are required.")
    user = db.verify(address, password)
    if user:
        session["user"] = user
        return redirect("/")
    else:
        return render_template("login.html", error="Invalid login info.")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    address = request.form.get("address")
    first = request.form.get("first")
    last = request.form.get("last")
    password = request.form.get("password")
    if not address or not first or not last or not password:
        return render_template("register.html", error="All fields are required.")
    result, data = db.register(address, first, last, password)
    if result:
        session["user"] = data
        return redirect("/")
    return render_template("register.html", error=data)

# API routes

@app.route("/email/{eid}.json")
def email(eid):
    if not session.get("user"):
        return redirect("/login")
    email = db.get_email(eid, session["user"])
    return dumps(email.serialize())

@app.route("/send", methods=["POST"])
def send():
    if not session.get("user"):
        return redirect("/login")
    if request.method == "GET":
        return render_template("send.html", invalid=False)
    else:
        to = request.form['to']
        if not db.valid_address(to):
            return render_template("send.html", invalid=True)

        d.add_email(to, session['user'], request.form['subject'], request.form['message'], request.form['attaches'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
