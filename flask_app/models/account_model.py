from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Account:
    def __init__(self, data):
        self.id = data['id']
        self.account_type = data['account_type']
        self.account_number = data['account_number']
        self.interest_rate = data['interest_rate']
        self.balance = data['balance']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']