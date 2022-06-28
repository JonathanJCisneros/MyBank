from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.administrator_model import Administrator
from flask_app.models.form_model import Form



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
        return render_template("admin/adminView.html", form = form)
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/admin")


@app.route("/accept/credit")
def create_account():
    return render_template("admin/newAccount.html")