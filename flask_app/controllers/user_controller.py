from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user_model import User

@app.route("/")
@app.route("/home")
def display_home():
    return render_template("home.html")

@app.route("/user/login")
def user_login():
    return render_template("user/userLogin.html")

@app.route("/user/register")
def user_register():
    return render_template("user/userRegister.html")

@app.route("/user_register", methods= ['POST'])
def register_user():
    if User.validate_register(request.form) == True:
        data = {
            "email" : request.form['email']
        }

        result = User.get_one(data)
        if result == None:
            data = {
                "title" : request.form['title'],
                "first_name" : request.form['first_name'],
                "last_name" : request.form['last_name'],
                "email" : request.form['email'],
                "password" : request.form['password'],
                "pin" : request.form['pin']
            }
            admin_id = Administrator.add_one(data)
            session['admin_id'] = admin_id
            session['first_name'] = request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['email'] = request.form['email']
            session['pin'] = request.form['pin']
            return redirect("/admin/dashboard")
        else:
            flash("Email already in use, please provide another", "error_register_email")
            return redirect("/admin")
    else:
        return redirect("/user/register")
