from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re


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
        self.formatted_balance = "${:,.2f}".format(self.current_balance)
        self.formatted_credit = "${:,}".format(self.credit_limit)
        self.format_exp = self.exp_date.strftime(" %m/%y")

    def card_number_display(self):
        output = "************"
        last_four = str(self.card_number)[-4:]
        output += last_four
        return output

    @classmethod
    def get_cards(cls, data):
        query =  "SELECT * "
        query += "FROM cards "
        query += "WHERE users_id = %(users_id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        card_list = []

        if len(result) > 0:
            for card in result:
                card_list.append(cls(card))
        
        return card_list


    @classmethod
    def new_card(cls, data):
        query =  "INSERT INTO cards(card_type, card_number, exp_date, ccv, credit_limit, pin, current_balance, purchase_apr, users_id) "
        query += "VALUES(%(card_type)s, %(card_number)s, %(exp_date)s, %(ccv)s, %(credit_limit)s, %(pin)s, %(current_balance)s, %(purchase_apr)s, %(users_id)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def update_balance_card(cls, data):
        query =  "UPDATE cards "
        query += "SET current_balance = current_balance - %(current_balance)s "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def get_all_cards(cls):
        query =  "SELECT * "
        query += "FROM cards "
        query += "ORDER BY created_at DESC;"

        result = connectToMySQL(DATABASE).query_db(query)

        card_list = []

        for card in result:
            card_list.append(cls(card))

        return card_list



    @classmethod
    def delete_cards(cls, data):
        query =  "DELETE FROM cards "
        query += "WHERE users_id = %(users_id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result