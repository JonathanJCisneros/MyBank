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
        self.formatted_balance = "${:,}".format(self.balance)

    def account_number_display(self):
        output = "******"
        last_four = str(self.account_number)[-4:]
        output += last_four
        return output
        

    @classmethod
    def get_accounts(cls, data):
        query =  "SELECT * "
        query += "FROM accounts "
        query += "WHERE users_id = %(users_id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        account_list = []

        if len(result) > 0:
            for account in result:
                account_list.append(cls(account))
        
        return account_list



    @classmethod
    def get_one_account(cls, data):
        query =  "SELECT * "
        query += "FROM accounts "
        query += "WHERE users_id = %(users_id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        
        if len(result) > 0:
            return cls(result[0])
        else:
            return None


    @classmethod
    def new_account(cls, data):
        query =  "INSERT INTO accounts(account_type, account_number, interest_rate, balance, users_id) "
        query += "VALUES(%(account_type)s, %(account_number)s, %(interest_rate)s, %(balance)s, %(users_id)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def deposit_account(cls, data):
        query =  "UPDATE accounts "
        query += "SET balance = balance + %(amount)s "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def withdraw_account(cls, data):
        query =  "UPDATE accounts "
        query += "SET balance = balance - %(amount)s "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def delete_accounts(cls, data):
        query =  "DELETE FROM accounts "
        query += "WHERE users_id = %(users_id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result
