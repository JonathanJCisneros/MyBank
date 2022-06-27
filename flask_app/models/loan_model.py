from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Loan:
    def __init__(self, data):
        self.id = data['id']
        self.account_type = data['account_type']
        self.loan_number = data['loan_number']
        self.balance = data['balance']
        self.apr = data['apr']
        self.maturity_date = data['maturity_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']