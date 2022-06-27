from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Card:
    def __init__(self, data):
        self.id = data['id']
        self.card_type = data['card_type']
        self.card_number = data['card_number']
        self.exp_date = data['exp_date']
        self.ccv = data['ccv']
        self.credit_limit = data['credit_limit']
        self.pin = data['pin']
        self.current_balance = data['current_balance']
        self.purchase_apr = data['purchase_apr']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @staticmethod
    def validate_credit_request(data):
        isValid = True
        if data['first_name'] == "":
            flash("You must provide your first name.", "error_register_first_name")
            isValid = False
        if len(data['first_name']) < 2:
            flash("Your first name must have at least 2 characters.", "error_register_first_name")
            isValid = False
        if data['last_name'] == "":
            flash("You must provide your last name.", "error_register_last_name")
            isValid = False
        if len(data['last_name']) < 2:
            flash("Your last name must have at least 2 characters.", "error_register_last_name")
            isValid = False
        if data['email'] == "":
            flash("You must provide your email.", "error_register_email")
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide a valid email.", "error_register_email")
            isValid = False
        if data['date_of_birth'] == "":
            flash("You must provide your date of birth.", "error_register_birth")
            isValid = False
        if len(data['social_security']) < 9:
            flash("Invalid Social Security", "error_register_social")
            isValid = False
        if data['employment_status'] == "Choose...":
            flash("You must provide your employment status.", "error_register_employment")
            isValid = False
        if data['annual_income'] == "":
            flash("You must provide your income.", "error_register_income" )
            isValid = False
        if data['street'] == "":
            flash("You must provide your Street.", "error_register_street" )
            isValid = False
        if data['city'] == "":
            flash("You must provide your City.", "error_register_city" )
            isValid = False
        if data['state'] == "Choose...":
            flash("You must provide your State.", "error_register_state" )
            isValid = False
        if len(data['zipcode']) < 5:
            flash("Invalid Zipcode", "error_register_zip")
            isValid = False
        return isValid