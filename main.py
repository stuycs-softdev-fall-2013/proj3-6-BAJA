from flask import Flask
from flask import redirect, render_template, request, session

PORT = 6004

app = Flask(__name__)
app.secret_key = "cy9wuDOTpKKl8waurlOhbuwbKyvsRAQJ"

@app.route("/")
def home():
    if session.get("username"):
        return redirect("/index.html")
    error = session.pop("error", None)
    focus_login = session.pop("focus_login", False)
    return render_template("login.html", error=error, focus_login=focus_login)

