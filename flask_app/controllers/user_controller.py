from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.address_model import Address
from flask_app.models.card_model import Card
from flask_app.models.account_model import Account
from flask_app.models.loan_model import Loan
from flask_app.models.form_model import Form


@app.route("/")
@app.route("/home")
def display_home():
    return render_template("home.html")


@app.route("/credit")
def display_credit():
    return render_template("credit.html")


@app.route("/checking")
def display_checking():
    return render_template("checking.html")


@app.route("/savings")
def display_savings():
    return render_template("savings.html")


@app.route("/auto")
def display_auto():
    return render_template("auto.html")


@app.route("/personal")
def display_personal():
    return render_template("personal.html")


@app.route("/mortgage")
def display_mortgage():
    return render_template("mortgage.html")


@app.route("/about")
def display_about():
    return render_template("about.html")


@app.route("/contact")
def display_contact():
    return render_template("contact.html")


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
            session['id'] = user.id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['username'] = user.username
            data1 = {
                "street" : request.form['street'],
                "apt_suite_num" : request.form['apt_suite_num'],
                "city" : request.form['city'],
                "state" : request.form['state'],
                "zipcode" : request.form['zipcode'],
                "users_id" : user.id
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
        return redirect("/user/dashboard/")


@app.route("/user/request", methods = ['POST'])
def user_card_request():
    if User.validate_session():
        request_type = request.form['type']
        return render_template("user/userSignup.html", request_type = request_type)
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/user/login")


@app.route("/user/dashboard/")
def user_dashboard():
    if User.validate_session():
        data = {
            "users_id" : session['id']
        }
        card_list = Card.get_cards(data)
        account_list = Account.get_accounts(data)
        loan_list = Loan.get_loans(data)
        form_list = Form.user_list_one(data)
        return render_template("user/userDashboard.html", card_list = card_list, account_list = account_list, loan_list = loan_list, form_list = form_list)
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/user/login")


@app.route("/user/logout")
def user_logout():
    session.clear()
    return redirect("/home")
