from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.address_model import Address
from flask_app.models.card_model import Card
from flask_app.models.account_model import Account
from flask_app.models.loan_model import Loan
from flask_app.models.form_model import Form
from flask_app.models.activity_model import Activity
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


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
                "password" : bcrypt.generate_password_hash(request.form['password'])
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
        if not bcrypt.check_password_hash(result.password, request.form['password']):
            flash("Wrong Cridentials", "error_login")
            return redirect("/user/login")
        else:
            session['id'] = result.id
            session['first_name'] = result.first_name
            session['last_name'] = result.last_name
            session['username'] = result.username
            return redirect("/user/dashboard/")


@app.route("/user/dashboard/")
def user_dashboard():
    if User.validate_session():
        data = {
            "users_id" : session['id']
        }
        data1 = {
            "username" : session['username']
        }
        user_info = User.get_one(data1)
        address_info = Address.get_address(data)
        card_list = Card.get_cards(data)
        account_list = Account.get_accounts(data)
        activity_list = Activity.show_all_activity(data)
        loan_list = Loan.get_loans(data)
        form_list = Form.user_list_one(data)
        return render_template("user/userDashboard.html", user_info = user_info, address_info = address_info, card_list = card_list, account_list = account_list, activity_list = activity_list, loan_list = loan_list, form_list = form_list)
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/user/login")


@app.route("/user/logout")
def user_logout():
    session.clear()
    return redirect("/home")


@app.route("/user/request", methods = ['POST'])
def user_card_request():
    if User.validate_session():
        request_type = request.form['type']
        return render_template("user/userSignup.html", request_type = request_type)
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/user/login")


@app.route("/transfer", methods = ['POST'])
def user_transfer():
    from_data = request.form['from_account']
    from_data = from_data.split("-")
    if from_data[2] < request.form['amount']:
        flash("Not enough funds for transfer!", "error_transfer")
        return redirect("/user/dashboard")
    else:
        data = {
            "id" : from_data[0],
            "amount" : request.form['amount']
        }
        Account.withdraw_account(data)
        to_data = request.form['to_account']
        to_data = to_data.split("-")
        data1 = {
            "id" : to_data[0],
            "amount" : request.form['amount']
        }
        Account.deposit_account(data1)
        data2 = {
            "type" : request.form['type'],
            "from_account" : from_data[1],
            "to_account" : to_data[1],
            "amount" : request.form['amount'],
            "users_id" : session['id']
        }
        Activity.add_activity(data2)
        return redirect("/user/dashboard")


@app.route("/pay", methods = ['POST'])
def user_pay():
    fro_data = request.form['from_account']
    fro_data = fro_data.split("-")
    if fro_data[2] < request.form['amount']:
        flash("Not enough funds for payment!", "error_pay")
        return redirect("/user/dashboard")
    else:
        t_data = request.form['to_account']
        t_data = t_data.split("-")
        data = {
            "id" : fro_data[0],
            "amount" : request.form['amount']
        }
        Account.withdraw_account(data)
        if t_data[1] == "Credit Card":
            data1 = {
            "id" : t_data[0],
            "current_balance" : request.form['amount']
            }
            Card.update_balance_card(data1)
        if t_data[1] == "Auto" or t_data[1] == "Personal" or t_data[1] == "Mortgage":
            data2 = {
            "id" : t_data[0],
            "amount" : request.form['amount']
            }
            Loan.update_balance_loan(data2)
        data3 = {
            "type" : request.form['type'],
            "from_account" : fro_data[1],
            "to_account" : t_data[1],
            "amount" : request.form['amount'],
            "users_id" : session['id']
        }
        Activity.add_activity(data3)
        return redirect("/user/dashboard")

@app.route("/user_update", methods= ['POST'])
def update_user_info():
    data = {
        "id" : session['id'],
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "phone_number" : request.form['phone_number'],
        "date_of_birth" : request.form['date_of_birth'],
        "social_security" : request.form['social_security'],
        "employment_status" : request.form['employment_status'],
        "annual_income" : request.form['annual_income'],
        "username" : request.form['username'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    User.update_user(data)
    data1 = {
        "street" : request.form['street'],
        "apt_suite_num" : request.form['apt_suite_num'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "zipcode" : request.form['zipcode'],
        "users_id" : session['id']
    }
    Address.update_address(data1)
    return redirect("/user/dashboard/")


@app.route("/delete_all", methods= ['POST'])
def delete_user():
    data = {
        "users_id" : session['id']
    }
    data1 = {
        "id" : session['id']
    }
    Address.delete_address(data)
    Card.delete_cards(data)
    Account.delete_accounts(data)
    Form.delete_forms(data)
    Loan.delete_loans(data)
    Activity.delete_activity(data)
    User.delete_one(data1)
    session.clear()
    return redirect("/home")