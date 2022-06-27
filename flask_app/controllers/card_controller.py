from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.card_model import Card
from flask_app.models.user_model import User


@app.route("/credit")
def display_credit():
    return render_template("credit.html")

@app.route("/user/credit/request")
def user_card_request():
    if User.validate_session():
        return render_template("user/creditSignup.html")
    else:
        flash("You must login to see this information", "error_not_logged_in")
        return redirect("/user/login")

@app.route("/card_request", methods = ['POST'])
def card_request_form():
    if Card.validate_credit_request(request.form):
        num = session['id']
        flash("Your request is being processed, we will get back to you shortly", "request_received")
        return redirect(f"/user/dashboard/{num}")
    else:
        return redirect("/user/credit/request")
