from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user
from flask_app.models import cup
from flask import flash
from datetime import datetime
import math

db = 'sugar_2'
table = 'posts'

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.poster_id = data['poster_id']
        self.poster = data['poster']
        self.cup_id = data['cup_id']
        self.created_at = data['created_at']

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def create(cls, data):
        query = f"INSERT INTO {table} (content, poster_id, cup_id) VALUES (%(content)s, %(poster_id)s, %(cup_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = f"DELETE FROM {table} WHERE id = {id};"
        return connectToMySQL(db).query_db(query, {'id': id})

    @classmethod
    def get_cup_posts(cls, cup_id):
        query = f"SELECT users.first_name as poster, posts.* FROM {table} LEFT JOIN users ON users.id = posts.poster_id WHERE cup_id = {cup_id};"
        results = connectToMySQL(db).query_db(query)
        data = []
        for row in results:
            band_data = cls(row)
            data.append(band_data)
        return data

    @classmethod
    def get_one(cls, id):
        query = f"SELECT * FROM {table} WHERE id = {id};"
        results = connectToMySQL(db).query_db(query, {'id': id})
        return cls(results[0])

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) < 1:
            flash("Your post must include content.", "post")
            is_valid = False
        return is_valid
# eof