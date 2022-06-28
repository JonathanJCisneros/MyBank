from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Form:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.date_of_birth = data['date_of_birth']
        self.social_security = data['social_security']
        self.employment_status = data['employment_status']
        self.annual_income = data['annual_income']
        self.street = data['street']
        self.apt_suite_num = data['apt_suite_num']
        self.city = data['city']
        self.state = data['state']
        self.zipcode = data['zipcode']
        self.status = data['status']
        self.type = data['type']
        self.amount = data['amount']
        self.drivers_license = data['drivers_license']
        self.ssc = data['ssc']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.administrators_id = data['administrators_id']

    
    @classmethod
    def list_all(cls):
        query =  "SELECT * "
        query += "FROM forms;"

        result = connectToMySQL(DATABASE).query_db(query)

        form_list = []

        if len(result) > 0:
            for form in result:
                form_list.append(cls(form))

        return form_list


    @classmethod
    def add_form(cls, data):
        query =  "INSERT INTO forms(first_name, last_name, email, phone_number, date_of_birth, social_security, employment_status, annual_income, street, apt_suite_num, city, state, zipcode, status, type, amount, drivers_license, ssc, users_id, administrators_id) "
        query += "VALUES(%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(date_of_birth)s, %(social_security)s, %(employment_status)s, %(annual_income)s, %(street)s, %(apt_suite_num)s, %(city)s, %(state)s, %(zipcode)s, %(status)s, %(type)s, %(amount)s, %(drivers_license)s, %(ssc)s, %(users_id)s, %(administrators_id)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result


    @classmethod
    def list_one(cls, data):
        query =  "SELECT * "
        query += "FROM forms "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        
        if len(result) > 0:
            return cls(result[0])
        else:
            return None


    @classmethod
    def update_status(cls, data):
        query =  "UPDATE forms "
        query += "SET status = %(status)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_request(data):
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


