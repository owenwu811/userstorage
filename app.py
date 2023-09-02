from flask import Flask, render_template, request, redirect, url_for, session 
from flask_sqlalchemy import SQLAlchemy
from db import db, User  # assuming your app's filename is 'app.py'

app, app.config['SQLALCHEMY_DATABASE_URI'], app.secret_key = Flask(__name__), 'sqlite:///user_credentials.db', '.'
db.init_app(app)

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

@app.route('/logout')
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

@app.route('/landing')
def landing():
    if 'username' in session:
        username = session['username']
        return render_template('landing.html', username=username)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()

#already did:
#1. login + logout + register feature + database integration

#plan
#0. must add ways for automated testing with a jenkins ci pipeline
#0. have a seperate testing enviornment from development with a seperate test database
#1. add a feature to let users reset their password with forgot password link to email
#1.5. let users click a button that says logout after already logging into the landing page
#2. secure user passwords in the database
#3. implement a feature so that it automatically locks users out if they get the password wrong 10 times in a row meaning they have to reset it via email
#3. integrate a jenkins build trigger so that, everytime you make a new change to the application locally, jenkins automatically builds a fresh new docker image 
#4. make this website available for others on an aws ec2 instance so that they can go to a public domain and get to this login page you see