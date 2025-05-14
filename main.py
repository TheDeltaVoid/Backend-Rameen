import flask
import sqlite3

from util_funcs import *

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return flask.render_template("login.html")

@app.route("/api/register", methods=["POST"])
def register():
    with sqlite3.connect("user_data.db") as user_db_conn:
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        pw_hash = hash(password)

        user_db_conn.execute(f"""INSERT INTO user_data (id, username, password, password_hash) VALUES (NULL, "{username}", "{password}", "{pw_hash}")""")

        print(user_db_conn.execute("SELECT * FROM user_data").fetchall())
    
    return flask.redirect("/")

@app.route("/api/login", methods=["POST"])
def login():
    user_db_conn = sqlite3.connect("user_data.db")

    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    pw_hash = hash_sha256(password)

    print(password, pw_hash)

    users = user_db_conn.execute("SELECT * FROM user_data").fetchall()
    for user in users:
        print(user)
        if user[1] == username and user[3] == pw_hash:
            resp = cookie_resp(user)

            resp.set_data(flask.render_template("simon.html"))
            return resp

    return flask.redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
