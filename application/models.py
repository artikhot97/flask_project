"""Data models."""
# from . import db
# from flask import Flask 
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@123@127.0.0.1/sanicDB'
# db = SQLAlchemy(app)

# class User(db.Model):
#     """Data model for user accounts."""

#     __tablename__ = 'movie_users'
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(64),index=False,unique=True,nullable=False)
#     email = db.Column(db.String(80),index=True,unique=True,nullable=False)
#     created = db.Column(db.DateTime,index=False,unique=False,nullable=False)
#     admin = db.Column(db.Boolean,index=False,unique=False,nullable=False)
#     # password = db.Column(db.String(64),index=False,unique=True,nullable=False)

#     def __repr__(self):
#         return '<User {}>'.format(self.username)

# class Movie(db.Model):
#     """Data model for movie accounts."""

#     __tablename__ = 'movie'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64),index=False, unique=False)
#     genre = db.Column(db.String(500), unique=False)
#     director = db.Column(db.String(60), unique=False)
#     popularity = db.Column(db.Float,unique=False)
#     imdb_score = db.Column(db.Float,unique=False)

#     def __repr__(self):
#         return '<User {}>'.format(self.name)