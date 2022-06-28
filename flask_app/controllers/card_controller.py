from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.card_model import Card
from flask_app.models.form_model import Form


@app.route("/credit")
def display_credit():
    return render_template("credit.html")


@app.route("/user_request", methods = ['POST'])
def card_request_form():
    if Card.validate_credit_request(request.form):
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "phone_number" : request.form['phone_number'],
            "date_of_birth" : request.form['date_of_birth'],
            "social_security" : request.form['social_security'],
            "employment_status" : request.form['employment_status'],
            "annual_income" : request.form['annual_income'],
            "street" : request.form['street'],
            "apt_suite_num" : request.form['apt_suite_num'],
            "city" : request.form['city'],
            "state" : request.form['state'],
            "zipcode" : request.form['zipcode'],
            "drivers_license" : request.form['drivers_license'],
            "ssc" : request.form['ssc'],
            "type" : request.form['type'],
            "amount" : 0,
            "status" : request.form['status'],
            "users_id" : request.form['users_id'],
            "administrators_id" : request.form['administrators_id']
        }
        Form.add_form(data)
        flash("Your request is being processed, we will get back to you shortly", "request_received")
        return redirect("/user/dashboard/")
    else:
        return redirect("/user/credit/request")
