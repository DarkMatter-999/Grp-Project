from flask import Flask, render_template, redirect, url_for, request, session
import hashlib
from datetime import timedelta
import datetime
from flask_sqlalchemy import SQLAlchemy
from utils import dbfunc, weather
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.secret_key = "plzzzworrkkk"
app.permanent_session_lifetime = timedelta(minutes=5)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

UPLOAD_FOLDER = os.path.join('static','upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSTIONS = set(["jpg" , "jpeg" , "jfif" , "pjpeg" , "pjp", "png", "svg", "webp"])

types = ["Place", "Food", "Handicraft", "Fruit", "Landscape", "Event"]

db = dbfunc.get_db()

wea = weather.Weather()

@app.route("/")
def index():
    posts = db.session.query(dbfunc.Data).order_by(dbfunc.Data.time.desc()).all()[:6]
    latest_posts = db.session.query(dbfunc.Data).order_by(dbfunc.Data.like.desc())[:6]
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
            return render_template("login.html", title="Login", error="User not found")

        if user.passwd == hashlib.sha256(password.encode('utf-8')).hexdigest():
            session.permanent = True
            session["email"] = email
            return redirect(url_for("user"))
        else:
            return render_template("register.html", title="Login", error="Email or password incorrect")
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
        user = dbfunc.User.query.filter_by(email=user).first()

        posts = dbfunc.Data.query.filter_by(uid=user._id).all()
        return render_template("user.html", user=user, posts=posts)
    else:
        return redirect(url_for("login"))

@app.route("/post", methods = ['POST', 'GET'])
def post():
    if request.method == "POST":
        if "email" in session:
            title = request.form["title"]
            content = request.form["content"]
            time = datetime.datetime.now()

            time = "-".join((str(time.day), str(time.month), str(time.year))) + " " + ":".join((str(time.hour), str(time.minute))) 
            
            city = request.form["city"]
            city_weather = wea.getweather(city)
            if not city_weather:
                return render_template("upload.html", title="Post", types=types, error="City not found")  

            type_ = request.form["type"]

            address = request.form["address"]

            if 'img' not in request.files:
                return redirect(url_for("post"))
            img = request.files['img']
            filename = dbfunc.generate_random(32) + "." + str(img.filename).split(".")[-1]
            # path = secure_filename(filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(path)

            user = session["email"]
            user = dbfunc.User.query.filter_by(email=user).first()

            data = dbfunc.Data(filename, title, content, time, user._id, city, address, type_)
            db.session.add(data)
            db.session.commit()

        return redirect(url_for("index"))

    elif request.method == "GET":
        if "email" in session:
            return render_template("upload.html", title="Post", types=types)  
        return render_template("login.html", title="Login")

@app.route("/post/<int:did>")
def show_post(did):
    post = db.session.query(dbfunc.Data).filter_by(_did=did).first()
    if post != None:
        user = dbfunc.User.query.filter_by(_id=post.uid).first()
        return render_template("post.html", post=post, username=user.name)
    else:
        return redirect(url_for("index"))

@app.route("/like/<did>")
def like_post(did):
    post = db.session.query(dbfunc.Data).filter_by(_did=did).first()
    post.like += 1
    db.session.commit()

    return redirect(url_for('post')+"/"+str(did))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/weather")
def weather():
    city = request.args.get('city')
    w = wea.getweather(city)

    return w


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)