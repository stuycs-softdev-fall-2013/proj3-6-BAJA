from json import dumps

from flask import Flask, make_response, redirect, render_template, request, session

from game.database import Database
from game.user import User

app = Flask(__name__)
app.secret_key = "X7jfId6Jb8T3sxVJ6xMQeEfGkqm3Qwft"
db = Database("database.db")

DOMAIN = "@qmail.com"
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

    result, data = db.register(address + DOMAIN, first, last, password)
    if result:
        session["user"] = data
        return redirect("/")
    return render_template("register.html", error=data)

# API routes
@app.route("/get")
def get():
    if not session.get("user"):
        return redirect("/login")

    emails = db.get_emails(session["user"])
    resp = make_response(dumps(emails.serialize()))
    resp.mimetype = "application/json"
    return resp


@app.route("/get/{eid}.json")
def email(eid):
    if not session.get("user"):
        return redirect("/login")

    email = db.get_email(eid, session["user"])
    resp = make_response(dumps(email.serialize()))
    resp.mimetype = "application/json"
    return resp

@app.route("/send.json", methods=["POST"])
def send():
    def build_user(address):
        if address.endswith(DOMAIN):                                                # Actually verify the address.
            return db.get_user(address)                                             # This is the wrong library call and it is prone to errors. Fix.
        return User(-1, address, None, None)

    if not session.get("user"):
        return redirect("/login")

    sender = db.get_user(session["user"])
    subject = request.form.get("subject")
    body = request.form.get("body")
    to = [build_user(addr) for addr in request.form.get("to").split(",")]
    cc = [build_user(addr) for addr in request.form.get("cc").split(",")]
    bcc = [build_user(addr) for addr in request.form.get("bcc").split(",")]
    attachments = None

    if not sender or not subject or not body or not to:
        return dumps({"error": "Missing required field(s)."})

    email = db.send_email(sender, subject, body, to, cc, bcc, attachments)
    resp = make_response(dumps(email.serialize()))
    resp.mimetype = "application/json"
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
