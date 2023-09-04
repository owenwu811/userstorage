from flask import Flask, render_template, request, redirect, url_for, session 
from flask_sqlalchemy import SQLAlchemy
from db import db, User  # assuming your app's filename is 'app.py'
import os

app = Flask(__name__)

environment = os.environ.get('MY_APP_ENV', 'production')

if environment == 'test':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user_credentials.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_credentials.db'

app.secret_key =  '.'
db.init_app(app)

@app.route('/') #this is called a decorator in Python
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            print('Login successful')
            session['username'] = username
            return redirect(url_for('landing'))  # Redirect to the landing page
        return 'Login failed'
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username, password, confirm_password = request.form['username'], request.form['password'], request.form['confirm_password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists."
        if password != confirm_password:
            return "Passwords do not match."
        # Store user data in the dictionary (insecure for demonstration purposes)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/landing', methods=['GET','POST'])
def landing():
    if 'username' in session:
        username = session['username']
        return render_template('landing.html', username=username)
    else:
        return redirect(url_for('login'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

#already did:
#1. login + logout + register feature + database integration
#2. wrote test for registration and login that worked with testlogin.py and testregistration.py

#2. bug: database sometimes fails to save usernames after shutting down app - it only happens after I run the testlogin.py unittest because there is a db.drop_all() - use seperate database for testing?
#0. add feature where users can't enter the wrong password more than 10 times
#1. add a feature to let users reset their password with forgot password link to email
#2.5 add two factor authentication feature 
#2.6 hash user passwords
#3. integrate jenkins so that you don't have to manually run each testfile everytime you make a feature change in your local dev

#plan
#0. must add ways for automated testing with a jenkins ci pipeline
#0. have a seperate testing enviornment from development with a seperate test database
#1. add a feature to let users reset their password with forgot password link to email
#2. secure user passwords in the database
#3. implement a feature so that it automatically locks users out if they get the password wrong 10 times in a row meaning they have to reset it via email
#3. integrate a jenkins build trigger so that, everytime you make a new change to the application locally, jenkins automatically builds a fresh new docker image 
#4. make this website available for others on an aws ec2 instance so that they can go to a public domain and get to this login page you see


#bug fix solution for testlogin.py overriding database;
# export MY_APP_ENV=test; python3 testlogin.py; flask run - a won't be able to login
# unset MY_APP_ENV; flask run - a will still be able to login



#chmod +x /Users/owenwu/trial/.git/hooks/pre-push