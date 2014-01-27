from flask import Flask, render_template, session

from game.database import Database

app = Flask(__name__)
app.secret_key = "X7jfId6Jb8T3sxVJ6xMQeEfGkqm3Qwft"
db = Database("database.db")

PORT = 6680

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
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
        return render_template("login.html", error="")
    else:
        user = request.form['user']
        password = request.form['password']
        if(db.valid(user, password)):
            session['user'] = user
        else:
            return render_template("login.html", error="Invalid Password")

@app.route("/create", methods=["GET", "POST"])
def createAccount():
    if request.method == "GET":
        return render_template("create_account.html", error="")
    else:
        first, last, password, address = request.form['first'], request.form['last'], request.form['passwd'], request.form['addr']

    error = db.register(first, last, password, address)
    if not error:
        session['user'] = address
        return url_for("index")
    else:
        return render_template("create_account.html", error=error)

@app.route("/message/{mid}")
def message(mid):
    email = db.getMessage(mid)
    return render_template("message.html", recipient=email['To'], sender=email['From'],
                            sub=email['Subject'], msg=email['Message'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
