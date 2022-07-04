from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Question:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.format_create = self.created_at.strftime(" %B %d, %Y - %I:%M%p")

    @classmethod
    def add_question(cls, data):
        query =  "INSERT INTO questions(first_name, last_name, email, comments) "
        query += "VALUES(%(first_name)s, %(last_name)s, %(email)s, %(comments)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @classmethod
    def list_all(cls):
        query =  "SELECT * "
        query += "FROM questions "
        query += "WHERE status = 'Pending';"

        result = connectToMySQL(DATABASE).query_db(query)

        quest_list = []

        if len(result) > 0:
            for question in result:
                quest_list.append(cls(question))

        return quest_list

    @classmethod
    def update_status(cls, data):
        query =  "UPDATE questions "
        query += "SET status = 'Responded' "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @staticmethod
    def validate_message(data):
        isValid = True
        if data['first_name'] == "":
            flash("You must provide your first name.", "error_message_first" )
            isValid = False
        if len(data['first_name']) < 2:
            flash("Your first name must have at least 2 characters.", "error_message_first" )
            isValid = False
        if data['last_name'] == "":
            flash("You must provide your last name.", "error_message_last" )
            isValid = False
        if len(data['last_name']) < 2:
            flash("Your last name must have at least 2 characters.", "error_message_last" )
            isValid = False
        if data['email'] == "":
            flash("You must provide your email.", "error_message_email" )
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide a valid email.", "error_message_email")
            isValid = False
        if len(data['comments']) < 4:
            flash("Your comment must be at least 4 characters long", "error_message_comments" )
            isValid = False
        return isValid