from flask import Flask, render_template, redirect, request, flash, session, jsonify
from mysqlconnection import MySQLConnector
# import encryption module
from flask_bcrypt import Bcrypt
import re
app = Flask(__name__)
app.secret_key = '7dQ8bbNhpWwl3Vh8zX1zGLhZIveJ4enHSFEyFGqH'
bcrypt = Bcrypt(app)
mysql = MySQLConnector('log_reg')
# define the format of email address for validation purposes
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# define charcter requirements for name fields - validation if letters only
NAME_REGEX = re.compile(r'[\d\W]')

# routes to landing page - has 2 forms: register and login
@app.route('/')
def index():
    return render_template('index.html')

# handles registration form - creates new user if passes validation
@app.route('/create_user', methods=['POST'])
def create_user():
    # use session to hold user's input from registration form
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    session['confirm_pw'] = request.form['confirm_pw']

    # create alerts list if any validation errors occur
    alerts = []
    # ---- begin validation process ----
    # first name - not blank, length of 2 or more, letters only
    if len(session['first_name']) < 1:
        alerts.append('Error: First name cannot be left blank.')
    elif len(session['first_name']) < 2:
        alerts.append('Error: First Name must be at least two letters.')
    elif NAME_REGEX.search(session['first_name']):
        alerts.append('Error: First name must contain letters only.')

    # last name - not blank, length of 2 or more, letters only
    if len(session['last_name']) < 1:
        alerts.append('Error: Last name cannot be left blank.')
    elif len(session['last_name']) < 2:
        alerts.append('Error: Last Name must be at least two letters.')
    elif NAME_REGEX.search(session['last_name']):
        alerts.append('Error: Last name must contain letters only.')

    # email - not blank, valid email format, not already in database
    if len(session['email']) < 1:
        alerts.append('Error: Email cannot be left blank.')
    elif not EMAIL_REGEX.match(session['email']):
        alerts.append('Error: Invalid email.')
    # else:
    # should have a query to make sure email is not already registered. not required for assignment, so will come back at later date to add

    # password - not left blank, at least 8 characters
    if len(session['password']) < 1:
        alerts.append('Error: Password cannot be left blank.')
    elif len(session['password']) < 8:
        alerts.append('Error: Password must contain at least eight characters.')

    # password confirmation - must match password
    if session['confirm_pw'] != session['password']:
        alerts.append('Error: Passwords do not match.')

    # if validation errors exist, do this:
    if alerts:
        for alert in alerts:
            flash(alert)
        return redirect('/')
    # if no alerts exist, registration successful, do this:
    else:
        # create encrypted password hash with bcrypt
        pw_hash = bcrypt.generate_password_hash(session['password'])
        # add user info to users database
        add_user = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(session['first_name'], session['last_name'], session['email'], pw_hash)
        # use change method from imported module to push changes through
        mysql.change(add_user)
        # direct to new user portion of profile template
        return render_template('profile.html', profile_type='register')

# handles login form, routes to profile if input passes validation
@app.route('/login', methods=['POST'])
def login():
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    # find this user in the database using the email provided
    find_user = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(session['email'])
    # use fetch method from imported module to complete search
    user = mysql.fetch(find_user)
    # ensure password provided matches what is on record
    if bcrypt.check_password_hash(user[0]['pw_hash'], session['password']):
        # password validation successful, login user
        return render_template('profile.html', profile_type='login')
    else:
        # password validation failed, redirect to landing page with error
        flash('Error: The password entered does not match our records.')
        return redirect('/')


app.run(debug=True)
