from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

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