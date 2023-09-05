from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from flask_migrate import Migrate
from token_utils import generate_reset_token, verify_reset_token
from datetime import datetime, timedelta
import os, smtplib, socket
smtplib.SMTP.debuglevel = 1

app = Flask(__name__)

environment = os.environ.get('MY_APP_ENV', 'production')

if environment == 'test':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user_credentials.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_credentials.db'

app.config['MAIL_SERVER'], app.config['MAIL_PORT'], app.config['MAIL_USERNAME'] = 'smtp.yahoo.com', 587, 'wuowen681@yahoo.com'
app.config['MAIL_PASSWORD'], app.config['MAIL_USE_TLS'], app.config['MAIL_USE_SSL'] = 'Holo-light1234!', True, False

mail = Mail(app)

app.secret_key =  '.'

# Initialize the database
from db import db
db.init_app(app)

# Initialize the migrate instance
migrate = Migrate(app, db)

# Now import the User model
from db import User

@app.route('/') 
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route accessed.")
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.refresh(user)
        # If user exists and account is locked
        if user and user.locked_until and datetime.utcnow() < user.locked_until:
            return "Too many failed login attempts. Try again in {} minutes.".format((user.locked_until - datetime.utcnow()).seconds // 60)

        if user and user.password == password:
            print('Login successful')
            user.login_attempts = 0  # reset login attempts
            db.session.commit()
            session['username'] = username
            return redirect(url_for('landing'))
        elif user:
            user.login_attempts += 1
            print("Login attempts incremented:", user.login_attempts)
            if user.login_attempts >= 10: #on the 11th try that the user gets wrong, it will lock the user out for 5 minutes
                user.locked_until = datetime.utcnow() + timedelta(minutes=5)
            db.session.commit()
            print("Data committed to DB.")
            if user.login_attempts >= 10:
                return "Too many failed login attempts. Try again in 5 minutes."
        return 'Login failed'
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)  
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
    
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        token = generate_reset_token(email)
        send_reset_email(email, token)
        return "An email has been sent with instructions to reset your password."
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        return 'Invalid or expired token', 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return 'User not found', 404
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # You can add more validation here, e.g. check password length, strength, etc.
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('reset_password', token=token))
        
        user.set_password(password)
        db.session.flush()
        db.session.commit()  # Assuming you're using SQLAlchemy and have imported 'db'
        flash('Your password has been reset! Please login with your new password.', 'success')
        return redirect(url_for('login'))  # Assuming you have a route named 'login'
    
    return render_template('reset_password.html')

def send_reset_email(email, token):
    with app.app_context():
        msg = Message('Password Reset Request',
                      sender='noreply@yourdomain.com',
                      recipients=[email])
        msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
        mail.send(msg)

@app.route('/list_tables')
def list_tables():
    with app.app_context():
        table_names = db.engine.table_names()
        print("Database Tables:", table_names)
    return "Check the console for the list of tables."

@app.route('/list_users')
def list_users():
    users = User.query.all()
    for user in users:
        print(user.username, user.password)
    return "Check the console for the list of users."

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

#TO DO

#make sure all your unit tests are actually accurate by testing them manually - not sure if test10triesout.py is actually correct because I change the range function to 5 and 15, and it still passes
# after 5 minutes, it still says you're locked out - this works now!!!!!!!!!!! september 4th evening - I just tried it manually
# the mail feature still dosen't work

#-----

#THE TEST10TRIESOUT.PY TEST NEVER PASSED - WHEN YOU EXECUTE PYTHON3 -M UNITTEST TEST10TRIESOUT.PY, it fails!!!!!

#try to use python3 -m unittest filename.py instead of python3 filename.py
# make sure the flask app can handle many requests at once 
#after making email feature work, write unittest for each route - forgot_password, reset_password, send_reset_email, etc
#add some kind of testing automation tool that can automatically login to a browser and simulate human interactions like selenium
# YOU MUST USE SELENIUM TO TEST LOGGING IN OR REGISTERING OR LOGGING OUT BECAUSE UNIT TESTS DO NOT CONSIDER EXTERNAL DEPENDENCIES LIKE DATABASES!!!!!

#already did:
#1. login + logout + register feature + database integration
#2. wrote test for registration and login that worked with testlogin.py and testregistration.py
#3. added list_tables and list_users routes to list all tables and list all usernames and passwords from the database
#4. fixed the database persistance issue where running python3 testlogin.py would delete all usernames and passwords from database - solution was #bug fix solution for testlogin.py overriding database;
# export MY_APP_ENV=test; python3 testlogin.py; flask run - a won't be able to login
# unset MY_APP_ENV; flask run - a will still be able to login
# 5. managed to create a feature branch on git so that you can rollback changes in case new features break already existing features or unittests - very important
# 6. managed to get selenium to automate the tests or user registration and login
# 7. tried implementing the 10 tries locked out in 5 minute feature, and I created login_attempts and locked_until in db.py but had to apply a database migration for this to work and apply the changes from my code to the actual database itself
# 8. was able to make 10 tries lockout feature work
# 9. verified that registration unit test was working by breaking it by changing self.assertin(b'Login') to self.assertin(b'adfsadf') and seeing if the test fails
#10. verified that the registration unit test was working by changing the login credentials and seeing if that new credentials appeared under list_users route

#5. fixed issue where testregistration unittest would fail after executing testlogin.py unit test first by generating unique data everytime the test is run so that you don't get already registered user by using unique_username = "testuser_" + str(uuid.uuid4()) - more in test_valid_registration function in testregistration.py

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

#debugging experience: locking user out for 5 minutes after getting password wrong 10 times not working - print("Login attempts incremented:", user.login_attempts) after user.login_attempts += 1
#possible reasons? login count not incrementing?
#login route says "Login failed" more than 10 times without locking out the user
#THE ISSUE WAS THAT YOU HAVE TO USE A CORRECT USERNAME AND INCORRECT PASSWORD TO TRIGGER LOGIN ATTEMPTS INCREMENTED BECAUSE ELIF BLOCK IS ELIF USER MEANING USER OR USERNAME IS STILL CORRECT