"""SQLAlchemy models and utility functions for Twitoff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class user(DB.Model):
    """Twitter Users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<user: {}>".format(self.name)


class tweet(DB.Model):
    """Tweet related to a user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    test = DB.Column(DB.Unicode(300)) 
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),nullable = False)
    user = DB.relationship('user', backref = DB.backref('tweets', lazy = True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)