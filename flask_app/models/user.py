from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import cup
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'sugar_2'
table = 'users'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.pwd = data['pwd']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone = data['phone']
        self.address = data['address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.following = []

    @classmethod
    def create(cls, data):
        query = f"INSERT INTO {table} (email, pwd, first_name, last_name, phone, address) VALUES (%(email)s, %(pwd)s, %(first_name)s, %(last_name)s, %(phone)s, %(address)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update_profile(cls, data, id):
        query = f"UPDATE {table} SET first_name = %(first_name)s, last_name = %(last_name)s, phone = %(phone)s, address = %(address)s WHERE id = {id};"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, id):
        query = f"SELECT * FROM users WHERE users.id = {id}"
        results = connectToMySQL(db).query_db(query)
        return cls(results[0])

    @classmethod
    def get_one_email(cls, data):
        query = f"SELECT * FROM {table} WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash("First Name must be entered.", "register")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last Name must be entered.", "register")
            is_valid = False
        if len(user['phone']) < 10:
            flash("Please include a 10-digit phone number (no non-numerical charaacters).", "register")
            is_valid = False
        # if len(user['address']) < 1:
        #     flash("Please include a 'Google-map-able' address.", "register")
        #     is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", "register")
            is_valid = False
        if len(user['pwd']) < 8:
            flash("Your password must be at least 8 characters.", "register")
            is_valid = False
        if user['pwd'] != user['pwd-2']:
            flash("Your passwords do not match.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", "login")
            is_valid = False
        return is_valid
# eof