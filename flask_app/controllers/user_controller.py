from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.address_model import Address


@app.route("/")
@app.route("/home")
def display_home():
    return render_template("home.html")


@app.route("/user/register")
def user_register():
    return render_template("user/userRegister.html")


@app.route("/user_register", methods= ['POST'])
def register_user():
    if User.validate_register(request.form) == True:
        data = {
            "username" : request.form['username']
        }

        result = User.get_one(data)
        if result == None:
            data = {
                "first_name" : request.form['first_name'],
                "last_name" : request.form['last_name'],
                "email" : request.form['email'],
                "phone_number" : request.form['phone_number'],
                "date_of_birth" : request.form['date_of_birth'],
                "social_security" : request.form['social_security'],
                "employment_status" : request.form['employment_status'],
                "annual_income" : request.form['annual_income'],
                "username" : request.form['username'],
                "password" : request.form['password']
            }
            User.create_user(data)
            user = User.get_one(data)
            session['id'] : user.id
            session['first_name'] : user.first_name
            session['last_name'] : user.last_name
            session['username'] : user.username
            data1 = {
                "street" : request.form['street'],
                "apt_suite_num" : request.form['apt_suite_num'],
                "city" : request.form['city'],
                "state" : request.form['state'],
                "zipcode" : request.form['zipcode'],
                "users_id" : session['id']
            }
            Address.add_one(data1)
            return redirect("/user/dashboard/")
        else:
            flash("Email already in use, please provide another", "error_register_email")
            return redirect("/user/register")
    else:
        return redirect("/user/register")


@app.route("/user/login")
def user_login():
    return render_template("user/userLogin.html")


@app.route("/user_login", methods= ['POST'])
def login_user():
    data = {
        "username" : request.form['username']
    }

    result = User.get_one(data)

    if result == None:
        flash("Wrong Cridentials", "error_login")
        return redirect("/user/login")
    else:
        session['id'] = result.id
        session['first_name'] = result.first_name
        session['last_name'] = result.last_name
        session['username'] = result.username
        return redirect("/user/dashboard")


@app.route("/user/dashboard")
def user_dashboard():
    if User.validate_session():
        return render_template("user/userDashboard.html")
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/user/login")


@app.route("/user/logout")
def user_logout():
    session.clear()
    return redirect("/home")
