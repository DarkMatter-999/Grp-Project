from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from utils import dbfunc

app = Flask(__name__)
app.secret_key = "plzzzworrkkk"
app.permanent_session_lifetime = timedelta(minutes=5)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = dbfunc.get_db()

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
        
        user = dbfunc.User(user, email, phno, password)
        db.session.add(user)
        db.session.commit()

        session.permanent = True
        session["email"] = email
        return redirect(url_for("user"))

    elif request.method == "GET":
        return render_template("register.html", title="Register")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form["email"] 
        password = request.form["password"]
        
        session.permanent = True
        session["email"] = email
        return redirect(url_for("user"))
    elif request.method == "GET":
        if "email" in session:
            return redirect("user")
        return render_template("login.html", title="Login")

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("login")

@app.route("/user")
def user():
    if "email" in session:
        user = session["email"]
        return render_template("user.html", user=user)
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)