from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.administrator_model import Administrator
from flask_app.models.form_model import Form
from flask_app.models.card_model import Card
from flask_app.models.account_model import Account
from flask_app.models.loan_model import Loan



@app.route("/admin")
def display_admin_register():
    return render_template("admin/adminRegister.html")


@app.route("/admin_register", methods = ['POST'])
def register_admin():
    if Administrator.validate_register(request.form) == True:
        data = {
            "email" : request.form['email']
        }

        result = Administrator.get_one(data)
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
        return redirect("/admin")


@app.route("/admin_login", methods = ['POST'])
def login():
    data = {
        "email" : request.form['email']
    }

    result = Administrator.get_one(data)

    if result == None:
        flash("Wrong Cridentials", "error_login")
        return redirect("/admin")
    else:
        session['admin_id'] = result.id
        session['title'] = result.title
        session['first_name'] = result.first_name
        session['last_name'] = result.last_name
        session['email'] = result.email
        session['pin'] = result.pin
        return redirect("/admin/dashboard")


@app.route("/admin/dashboard")
def display_dashboard():
    if Administrator.validate_session():
        forms = Form.list_all()
        return render_template("admin/adminDashboard.html", forms = forms)
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/admin")



@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin")


@app.route("/admin/view/<int:id>")
def view_form(id):
    if Administrator.validate_session():
        data = {
            "id" : id
        }
        form = Form.list_one(data)
        session['type'] = form.type
        session['users_id'] = form.users_id
        session['user_first'] = form.first_name
        session['user_last'] = form.last_name
        session['form_id'] = form.id
        return render_template("admin/adminView.html", form = form)
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/admin")


@app.route("/accept/account")
def create_account():
    if Administrator.validate_session():
        account_type = session['type']
        return render_template("admin/newAccount.html", account_type = account_type)
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/admin")

@app.route("/new_account", methods = ['POST'])
def create_product():
    if session['type'] == "Credit Card":
        data = {
            "card_type" : request.form['card_type'],
            "card_number" : request.form['card_number'],
            "exp_date" : request.form['exp_date'],
            "ccv" : request.form['ccv'],
            "credit_limit" : request.form['credit_limit'],
            "current_balance" : request.form['current_balance'],
            "purchase_apr" : request.form['purchase_apr'],
            "pin" : request.form['pin'],
            "users_id" : request.form['users_id']
        }
        Card.new_card(data)
        data3 = {
            "id" : session['form_id'],
            "status" : "Approved"
        }
        Form.update_status(data3)
        return redirect("/admin/dashboard")
    elif session['type'] == "Checking" or "Savings":
        data1 = {
            "account_type" : request.form['account_type'],
            "account_number" : request.form['account_number'],
            "interest_rate" : request.form['interest_rate'],
            "balance" : request.form['balance'],
            "users_id" : request.form['users_id']
        }
        Account.new_account(data1)
        data4 = {
            "id" : session['form_id'],
            "status" : "Approved"
        }
        Form.update_status(data4)
        return redirect("/admin/dashboard")
    elif session['type'] == "Auto" or "Personal" or "Mortgage":
        data2 = {
            "account_type" : request.form['account_type'],
            "loan_number" : request.form['loan_number'],
            "apr" : request.form['apr'],
            "balance" : request.form['balance'],
            "maturity_date" : request.form['maturity_date'],
            "users_id" : request.form['users_id']
        }
        Loan.new_loan(data2)
        data5 = {
            "id" : session['form_id'],
            "status" : "Approved"
        }
        Form.update_status(data5)
        return redirect("/admin/dashboard")
    else:
        return redirect("/accept/account")