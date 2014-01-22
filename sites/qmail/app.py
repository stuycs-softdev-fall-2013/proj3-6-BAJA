from flask import Flask, session

from game.database import Database

app = Flask(__name__)
app.secret_key = "X7jfId6Jb8T3sxVJ6xMQeEfGkqm3Qwft"
db = Database("database.db")

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
        return render_template("login.html")
    else:

@app.route("/create", methods=["GET", "POST"]) 
def createAccount():
    if request.method == "GET":
        return render_template("create_account.html")
    else:
        first, last, password, address = request.form['first'], request.form['last'], request.form['passwd'], request.form['addr']

    if d.contains(address):
        return url_for("createAccount")
    session['user'] = address
    d.register(first, last, password, address)
    
    return url_for("index")

