""" Main app/routing file for Twitoff"""
from flask import Flask, render_template, request
from dotenv import load_dotenv
from .models import DB, user
from .twitter import add_or_update_user, update_all_users
from os import getenv
from .predict import predict_user

load_dotenv()

def create_app():
    """Create and configure an instance of the flask application"""
    app = Flask(__name__)
    app.config['SQLAlchemy_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)


    @app.route('/')
    def root():
        return render_template("base.html", title="home", users = user.query.all())

    @app.route('/compare', methods = ['POST'])
    def compare(message = ''):
        # grabs inputted values from the dropdown
        user0, user1 = sorted(
            [request.values['user1'],
             request.values['user2']]
        )

        if user0 == user1:
            # tells application user they cant compare same twitter users
            message = "Cannot compare users to themselves!"

        else:
            #running prediction and return the prediction to user as a message
            prediction = predict_user(user0. user1. request.values['tweet_text'])
            message = "{} is more likely to be said by {} than {}".format(
                request.values['tweet_text'], user1 if prediction else user0,
                user0 if prediction else user1)

        return render_template('prediction.html', title = 'Prediction', message = message)

    
    @app.route('/user', methods = ['POST'])
    @app.route('/user/<name>', methods = ['GET'])
    def user(name = None, message = ''):
        name = name or request.values['user_name']

        try:
            # if button is clicked then do this 
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} sucessfully added!'.format(name)
            # tweets are always collected if the user exist
            tweets = user.query.filter(user.name == none).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format (name, e)
            # if we get an error then no tweets are displayed 
            tweets = []

        return render_template('user.html', title = name, tweets = tweets, message = message)

    @app.route('/update')
    def update():
        # updates our users from the function in twitter.py
        update_all_users()
        return render_template('base.html', title = 'Tweets have been updated!', users = user.query.all())

    @app.route('/reset')
    def reset():
        # resets database
        DB.drop_all()
        # creates database again
        DB.create_all()
        return render_template('base.html', title = 'Reset Database!')


    return app
