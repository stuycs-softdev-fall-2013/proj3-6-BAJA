from json import dumps

from flask import Flask, make_response, redirect, render_template, request, session

from game.database import Database
from game.user import User
from game.utils import get_port

app = Flask(__name__)
app.secret_key = "X7jfId6Jb8T3sxVJ6xMQeEfGkqm3Qwft"
db = Database("database.db")

DOMAIN = "@qmail.com"

def do_api_reply(json):
    resp = make_response(dumps(json))
    resp.mimetype = "application/json"
    return resp

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

    address = request.form.get("email")
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

    address = request.form.get("email")
    first = request.form.get("first")
    last = request.form.get("last")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    if not address or not first or not last or not password:
        return render_template("register.html", error="All fields are required.")
    if password != confirm:
        return render_template("register.html", error="Passwords must match.")

    result, data = db.register(address + DOMAIN, first, last, password)
    if result:
        session["user"] = data
        return redirect("/")
    return render_template("register.html", error=data)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# API routes

@app.route("/inbox.json")
def inbox():
    if not session.get("user"):
        return do_api_reply({"error": "You are not logged in."})
    return do_api_reply(db.get_inbox(session["user"]))

@app.route("/sentbox.json")
def sentbox():
    if not session.get("user"):
        return do_api_reply({"error": "You are not logged in."})
    return do_api_reply(db.get_sentbox(session["user"]))

@app.route("/send.json", methods=["POST"])
def send():
    def build_user(address):
        if address.endswith(DOMAIN):
            return db.get_user_from_address(address).tuple()
        return (address, None)

    if not session.get("user"):
        return do_api_reply({"error": "You are not logged in."})

    sender = db.get_user(session["user"])
    subject = request.form.get("subject")
    body = request.form.get("body")
    try:
        to = [build_user(addr) for addr in request.form.get("to").split(",")]
        cc = [build_user(addr) for addr in request.form.get("cc").split(",")]
        bcc = [build_user(addr) for addr in request.form.get("bcc").split(",")]
    except IndexError:
        return do_api_reply({"error": "Invalid address(es) given."})
    attachments = None

    if not subject or not body or not to:
        return do_api_reply({"error": "Missing required field(s)."})

    email = db.send_email(sender.tuple(), subject, body, to, cc, bcc, attachments)
    return do_api_reply(email)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=get_port("qmail"), debug=True)
