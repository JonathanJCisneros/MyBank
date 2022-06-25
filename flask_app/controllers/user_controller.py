from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user_model import User

@app.route("/")
@app.route("/home")
def display_home():
    return render_template("home.html")

@app.route("/user/login")
def user_login():
    return render_template("userLogin.html")

@app.route("/user/register")
def user_register():
    return render_template("userRegister.html")