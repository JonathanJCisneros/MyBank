from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.date_of_birth = data['date_of_birth']
        self.social_security = data['social_security']
        self.phone_number = data['phone_number']
        self.employment_status = data['employment_status']
        self.annual_income = data['annual_income']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.format_create = self.created_at.strftime(" %B %d, %Y")
        self.format_income = "${:,}".format(self.annual_income)
        self.format_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', self.phone_number)

    @classmethod
    def get_one(cls, data):
        query =  "SELECT * "
        query += "FROM users "
        query += "WHERE username = %(username)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def get_all(cls):
        query =  "SELECT * "
        query += "FROM users "
        query += "ORDER BY created_at DESC;"

        result = connectToMySQL(DATABASE).query_db(query)

        user_list = []

        for user in result:
            user_list.append(cls(user))

        return user_list

    @classmethod
    def create_user(cls, data):
        query =  "INSERT into users(first_name, last_name, email, phone_number, date_of_birth, social_security, employment_status, annual_income, username, password) "
        query += "VALUES(%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(date_of_birth)s, %(social_security)s, %(employment_status)s, %(annual_income)s, %(username)s, %(password)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users "
        query += "SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, phone_number = %(phone_number)s, date_of_birth = %(date_of_birth)s, social_security = %(social_security)s, employment_status = %(employment_status)s, annual_income = %(annual_income)s, username = %(username)s, password = %(password)s "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    
    @classmethod
    def delete_one(cls, data):
        query =  "DELETE FROM users "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result


    @staticmethod
    def validate_register(data):
        isValid = True
        if data['first_name'] == "":
            flash("You must provide your first name.", "error_register_first_name" )
            isValid = False
        if len(data['first_name']) < 2:
            flash("Your first name must have at least 2 characters.", "error_register_first_name" )
            isValid = False
        if data['last_name'] == "":
            flash("You must provide your last name.", "error_register_last_name" )
            isValid = False
        if len(data['last_name']) < 2:
            flash("Your last name must have at least 2 characters.", "error_register_last_name" )
            isValid = False
        if data['email'] == "":
            flash("You must provide your email.", "error_register_email" )
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide a valid email.", "error_register_email")
            isValid = False
        if data['date_of_birth'] == "":
            flash("You must provide your date of birth.", "error_register_birth" )
            isValid = False
        if len(data['social_security']) < 9:
            flash("Invalid Social Security", "error_register_social")
            isValid = False
        if data['employment_status'] == "Choose...":
            flash("You must provide your employment status.", "error_register_employment" )
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
        if data['username'] == "":
            flash("You must provide a username.", "error_register_username")
            isValid = False
        if len(data['username']) < 5:
            flash("Username must be at least 5 characters long.", "error_register_username")
            isValid = False
        if data['password'] == "":
            flash("You must provide a password.", "error_register_password")
            isValid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long.", "error_register_password")
            isValid = False
        if data['password_confirmation'] != data['password']:
            flash("Your password confirmationan doesn't match.", "error_register_password_confirmation")
        return isValid

    @staticmethod
    def validate_session():
        if "id" not in session:
            return False
        else:
            return True