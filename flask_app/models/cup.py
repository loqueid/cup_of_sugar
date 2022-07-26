from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user
from flask_app.models import post
from flask import flash
from datetime import date

db = 'sugar_2'
table = 'cups'

class Cup:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.date = data['date']
        self.description = data['description']
        self.address = data['address']
        self.creator_id = data['creator_id']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = ""
        self.users_following = []
        self.posts = []

    @classmethod
    def create(cls, data):
        query = f"INSERT INTO {table} (title, date, description, address, creator_id, type) VALUES (%(title)s, %(date)s, %(description)s, %(address)s, %(creator_id)s, %(type)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls, data, id):
        query = f"UPDATE {table} SET title = %(title)s, date = %(date)s, description = %(description)s, address = %(address)s, updated_at = NOW() WHERE id = {id};"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = f"DELETE FROM {table} WHERE id = {id};"
        return connectToMySQL(db).query_db(query, {'id': id})

    @classmethod
    def get_all_cups(cls, id):
        query = f"SELECT * FROM {table} LEFT JOIN users_following ON cups.id = users_following.cup_id AND users_following.follower_id = {id};"
        results = connectToMySQL(db).query_db(query)
        data = []
        for row in results:
            cup_data = cls(row)
            cup_data.users_following.append(row['follower_id'])
            data.append(cup_data)
        return data

    @classmethod
    def get_cups_by_type(cls, data):
        query = "SELECT * FROM cups LEFT JOIN users_following ON cups.id = users_following.cup_id AND users_following.follower_id = %(id)s WHERE type = %(type)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        data = []
        for row in results:
            cup_data = cls(row)
            cup_data.users_following.append(row['follower_id'])
            data.append(cup_data)
        return data

    @classmethod
    def get_cups_by_userid(cls, id):
        query = f"SELECT * FROM {table} LEFT JOIN users ON users.id = creator_id WHERE creator_id = {id};"
        results = connectToMySQL(db).query_db(query)
        data = []
        for row in results:
            # cup_data = cls(row)
            # cup_data.users_following.append(row['follower_id'])
            data.append(cls(row))
        return data

    @classmethod
    def get_mycups(cls, id):
        query = f"SELECT cups.*, users_following.* FROM {table} LEFT JOIN users ON users.id = creator_id LEFT  JOIN users_following ON cups.id = cup_id WHERE follower_id = {id};"
        results = connectToMySQL(db).query_db(query)
        data = []
        for row in results:
            cup_data = cls(row)
            cup_data.users_following.append(row['follower_id'])
            data.append(cup_data)
        return data

    @classmethod
    def get_one(cls, id):
        query = f"SELECT cups.*, users.first_name as creator FROM {table} LEFT JOIN users ON users.id = creator_id WHERE cups.id = {id};"
        results = connectToMySQL(db).query_db(query, {'id': id})
        new_data = cls(results[0])
        new_data.creator = results[0]['creator']
        return new_data

    @classmethod
    def add_mycups(cls, data):
        query = "INSERT INTO users_following (follower_id, cup_id) VALUES (%(follower_id)s, %(cup_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def rem_mycups(cls, data):
        query = "DELETE FROM users_following WHERE follower_id = %(follower_id)s AND cup_id = %(cup_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_cup(cup):
        is_valid = True
        if len(cup['title']) < 11:
            flash("You must include brief title (more than 10 characters).", "cup")
            is_valid = False
        if len(cup['description']) < 42:
            flash("You description must be detailed.", "cup")
            is_valid = False
        return is_valid
# eof