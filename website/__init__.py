from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask.ext.markdown import Markdown
from werkzeug.security import generate_password_hash, check_password_hash



'''---------------------------------  database object creation'''
db = SQLAlchemy()
DB_NAME = "database.db"
'''-----------------------------------------------------------'''
'''-----------------------------------------------------------'''

def create_app():
    '''---------------------------------------------  flask object initialization'''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'BuddhistCoding'
    '''--------------------------------------------------------------------------'''
    '''--------------------------------------- this part right here tells our flask object where the database is stored and initializes it'''
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    '''--------------------------------------------------------------------------'''
    '''--------------------------------------------------------------------------'''
    '''questa è tutta la magia del login manager, per loggare e salvare l'user nella sessione. Non ci capisco granchè'''
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    '''--------------------------------------------------------------------------'''

    
    '''--------------------------------------------------------------------------'''
    '''--------------------------------------- Blueprints import and registration'''
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/') 
    app.register_blueprint(auth, url_prefix='/') 
    '''--------------------------------------------------------------------------'''
    '''Ora lo script che controlla, ad ogni avvio del server, se il database esiste o va creato'''
    '''--------------------------------------------------------------------------'''
    from .models import User, Exercise, Cardio
    
    create_database(app)
    Markdown(app)


    return app


def create_database(app):
    '''-------------------------- Path.exists checka se il database esiste nel determinato path'''
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)
        print('DB Created')
