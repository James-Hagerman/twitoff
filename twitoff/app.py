""" Main app/routing file for Twitoff"""
from flask import Flask 
from .models import DB, user

def create_app():
    """Create and configure an instance of the flask application"""
    app = Flask(__name__)
    app.config('SQLAlchemy_DATABASE_URI') = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)


    @app.route('/')
    def root():
        user = User.query.all()
        return render_template("base.html", title="home", users = user.query.all())

    return app
