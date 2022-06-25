from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

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

        return redirect(url_for("index"))
    elif request.method == "GET":
        return render_template("register.html", title="Register")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        email = request.form["email"] 
        password = request.form["password"]
        phno = request.form["phno"]

        return redirect(url_for("index"))
    elif request.method == "GET":
        return render_template("login.html", title="Login")


if __name__ == "__main__":
    app.run(debug=True)