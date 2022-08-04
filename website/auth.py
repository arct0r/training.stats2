from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, current_user, login_required, login_manager

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    checkAdmin()
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        '''-------------------------- this searches the user in the db for the given unique parameter'''
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                '''------------------------ this checks if the given password is equal to the hashed password of the user found'''
                '''-------------------------------------------------- and then logins the user, storing it in the flask session'''
                login_user(user, remember=True)
                '''----------------------------------------------------------------------------------------------------------- '''

                flash('Logged in!', category='success')
                return redirect(url_for("views.stats"))
            else:
                flash('Wrong password', category = 'error')

        else:
            flash('User not found', category = 'error')

    return render_template('login.html')



@auth.route('/logout')  
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():  
    checkAdmin()
    if request.method=="POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        print(username, email, password1, password2)
        '''-------------------------------------- this check if a user with the given email already exists'''
        user = User.query.filter_by(username=username).first()
        user1 = User.query.filter_by(email=email).first()
        '''-----------------------------------------------------------'''
        if user:
            flash('Username already in use', category='error')
        elif user1:
            flash('email already in use', category = 'error')
        elif len(email) > 3 and password1 == password2 and len(username) > 3:
            '''-----------------------------------------------------------'''   
            '''-------------------------------- creates a user in the db if the sign-up goes we(ll'''
            new_user = User(email=email, username = username, password = generate_password_hash(password1, method='sha256'))
            '''------------------------------------------------------------- and adds it to the DB'''
            db.session.add(new_user)
            db.session.commit()
            '''-----------------------------------------------------------'''
            login_user(new_user, remember=True )
            flash("account created", category="success")
            return redirect(url_for('views.terminal'))
            '''--------------------- il redirect "views.home" funziona perchè views è un blueprint'''

            
        elif len(email) < 4:
            flash("email too short", category="error")
        elif password1 != password2:
            flash("passwords don't match", category="error")
        elif len(username) < 3:
            flash("username too short", category="error")
        #elif userNotFound:
            #flash("user not found", category="error")

    return render_template('signup.html')

def checkAdmin():
    admin = User.query.filter(
    User.username == 'arct0r'
            ).first()
    if not admin:
        arct0r = User(email='123@gmail.com', username = 'arct0r', password = generate_password_hash('123', method='sha256'))
        db.session.add(arct0r)
        db.session.commit()