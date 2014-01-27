from flask import Flask, redirect, render_template, request, session

from game.database import Database

app = Flask(__name__)
app.secret_key = "X7jfId6Jb8T3sxVJ6xMQeEfGkqm3Qwft"
db = Database("database.db")

PORT = 6680

@app.route("/")
def index():
    if not session.get("user"):
        return redirect("/login")
    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    address = request.form.get("address")
    password = request.form.get("password")
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
    error = db.register(address, first, last, password)
    if error:
        return render_template("register.html", error=error)
    session["user"] = db.verify(address, password)  # Temporary hack so I don't need another function
    return redirect("/")

@app.route("/message/{mid}")
def message(mid):
    if not session.get("user"):
        return redirect("/login")
    email = db.getMessage(mid)
    return render_template("message.html", recipient=email['To'], sender=email['From'],
                            sub=email['Subject'], msg=email['Message'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
