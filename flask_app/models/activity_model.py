from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import app

class Activity:
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.from_account = data['from_account']
        self.to = data['to']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @classmethod
    def show_all_activity(cls, data):
        query =  "SELECT * "
        query += "FROM activities "
        query += "WHERE users_id = %(users_id)s;"

        results = connectToMySQL(DATABASE).query_db(query, data)

        activity_list = []

        if len(result) > 0:
            for activity in result:
                activity_list.append(cls(activity))
        
        return activity_list
    
    @classmethod
    def add_avtivity(cls, data):
        query =  "INSERT INTO activities(type, from_account, to, amount, users_id) "
        query += "VALUES(%(type)s, %(from_account)s, %(to)s, %(amount)s, %(users_id)s);"

        results = connectToMySQL(DATABASE).query_db(query, data)

        return result


