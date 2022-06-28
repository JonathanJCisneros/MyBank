from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash


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


