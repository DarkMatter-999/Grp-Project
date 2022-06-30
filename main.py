from flask import Flask, render_template, redirect, url_for, request, session
import hashlib
from datetime import timedelta
import datetime
from flask_sqlalchemy import SQLAlchemy
from utils import dbfunc

app = Flask(__name__)
app.secret_key = "plzzzworrkkk"
app.permanent_session_lifetime = timedelta(minutes=5)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = dbfunc.get_db()

@app.route("/")
def index():
    posts = db.session.query(dbfunc.Data).order_by(dbfunc.Data.time.desc())
    latest_posts = db.session.query(dbfunc.Data).order_by(dbfunc.Data.like.desc())
    return render_template("index.html", title="Travel. Destination", posts=posts, latest_posts=latest_posts)

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        user = request.form["username"]
        email = request.form["email"] 
        password = request.form["password"]
        phno = request.form["phno"]
        
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

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

        user = dbfunc.User.query.filter_by(email=email).first()
        if user == None:
            return redirect(url_for("login"))

        if user.passwd == hashlib.sha256(password.encode('utf-8')).hexdigest():
            session.permanent = True
            session["email"] = email
            return redirect(url_for("user"))
        else:
            return redirect(url_for("login"))
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

@app.route("/post", methods = ['POST', 'GET'])
def post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        time = datetime.datetime.now()

        time = "-".join((str(time.day), str(time.month), str(time.year))) + " " + ":".join((str(time.hour), str(time.minute))) 
        
        city = "CHANGE ME"

        img = "CHANGE ME"

        user = session["email"]
        user = dbfunc.User.query.filter_by(email=user).first()

        data = dbfunc.Data(img, title, content, time, user._id, city)
        db.session.add(data)
        db.session.commit()

        return redirect(url_for("index"))

    elif request.method == "GET":
        if "email" in session:
            cities = db.session.query(dbfunc.City)

            return render_template("upload.html", title="Post", cities=cities)  
        return render_template("login.html", title="Login")

@app.route("/post/<int:did>")
def show_post(did):
    post = db.session.query(dbfunc.Data).filter_by(_did=did).first()
    if post != None:
        # TODO: render post page
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))



if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)