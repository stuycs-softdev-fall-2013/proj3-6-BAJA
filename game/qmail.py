from flask import Flask

from .database import Database

app = Flask(__name__)
app.secret_key = "X7jfId6Jb8T3sxVJ6xMQeEfGkqm3Qwft"
db = Database("database.db")

@route("/")
def index():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
