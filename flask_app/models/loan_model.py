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
        self.formatted_balance = "${:,}".format(self.balance)

    def loan_number_display(self):
        output = "******"
        last_four = str(self.loan_number)[-4:]
        output += last_four
        return output

    @classmethod
    def new_loan(cls,data):
        query =  "INSERT INTO loans(account_type, loan_number, balance, apr, maturity_date, users_id) "
        query += "VALUES(%(account_type)s, %(loan_number)s, %(balance)s, %(apr)s, %(maturity_date)s, %(users_id)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def get_loans(cls, data):
        query =  "SELECT * "
        query += "FROM loans "
        query += "WHERE users_id = %(users_id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        loan_list = []

        if len(result) > 0:
            for loan in result:
                loan_list.append(cls(loan))
        
        return loan_list


    @classmethod
    def update_balance_loan(cls, data):
        query =  "UPDATE loans "
        query += "SET balance = balance - %(amount)s "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def delete_loans(cls, data):
        query =  "DELETE FROM loans "
        query += "WHERE users_id = %(users_id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result