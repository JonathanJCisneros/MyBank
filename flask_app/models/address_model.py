from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.controllers import user_controller

class Address:
    def __init__(self,data):
        self.id = data['id']
        self.street = data['street']
        self.apt_suite_num = data['apt_suite_num']
        self.city = data['city']
        self.state = data['state']
        self.zipcode = data['zipcode']
        self.users_id = data['users_id']

    @classmethod
    def add_one(cls, data):
        query =  "INSERT INTO addresses(street, apt_suite_num, city, state, zipcode, users_id) "
        query += "VALUES(%(street)s, %(apt_suite_num)s, %(city)s, %(state)s, %(zipcode)s, %(users_id)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    
    @classmethod
    def get_address(cls, data):
        query =  "SELECT * "
        query += "FROM addresses "
        query += "WHERE users_id = %(users_id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        address_list = []

        if len(result) > 0:
            for address in result:
                address_list.append(cls(address))        
        return address_list
