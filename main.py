from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from utils import db

app = Flask(__name__)

conn = sqlite3.connect('database.db', check_same_thread=False)

@app.route("/")
def index():
    return render_template("index.html", title="Boost Tourism")

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        user = request.form["username"]
        email = request.form["email"] 
        password = request.form["password"]
        phno = request.form["phno"]

        db.insuser(conn, user, phno, password, email)

        return redirect(url_for("index"))
    elif request.method == "GET":
        return render_template("register.html", title="Register")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form["email"] 
        password = request.form["password"]

        return redirect(url_for("index"))
    elif request.method == "GET":
        return render_template("login.html", title="Login")


if __name__ == "__main__":
    app.run(debug=True)
    conn.close()