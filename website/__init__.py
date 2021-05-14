from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#SQLAlchemy instance
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # creating instance for flask
    app = Flask(__name__)

    # creating secret key for session and cookie
    app.config['SECRET_KEY'] = 'Fate1234$#@'

    # database configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # blueprint
    from .views import views

    app.register_blueprint(views, url_prefix = '/')

    # models
    from .models import User
    # this function will create a database
    create_database(app)
    
    # loginmanager
    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# creating database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created database')