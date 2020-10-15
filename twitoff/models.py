"""SQLAlchemy models and utility functions for Twitoff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class user(DB.Model):
    """Twitter Users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<user: {}>".format(self.name)


class tweet(DB.Model):
    """Tweet related to a user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable = False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),nullable = False)
    user = DB.relationship('user', backref = DB.backref('tweets', lazy = True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)

    # def insert_example_users():
    #     """ Example users"""
    #     bill = user(id = 1, name = 'BillGates')
    #     elon = user(id = 2, name = 'ElonMusk')
    #     DB.session.add(bill)
    #     DB.session.add(elon)
    #     DB.session.commit()