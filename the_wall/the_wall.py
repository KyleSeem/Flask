from flask import Flask, render_template, redirect, request, session, flash, jsonify
# import module from mysqlconnection.py - creates access to database
from mysqlconnection import MySQLConnector
# import encryption module
from flask_bcrypt import Bcrypt
import re
app = Flask(__name__)
app.secret_key = 'V5lSBqpXZydAA3ETI7rgfIqcBhHDXXsPpxj3eAahyVlgk'
bcrypt = Bcrypt(app)
mysql = MySQLConnector('the_wall') # database utilized
# define the format of email address for validation purposes
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# routes to landing page - has 2 forms: register and login
@app.route('/')
def index():
    return render_template('index.html')

# handles registration form - creates new user if input passes validation
@app.route('/create_user', methods=['POST'])
def create_user():
    # use session to hold user's input from registration form
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['new_email'] = request.form['new_email']
    password = request.form['password']
    confirm_pw = request.form['confirm_pw']

    # ------- begin validation process -------
    # check email to see if already in database
    try:
        find_email = "SELECT * FROM users WHERE email = '{}'".format(request.form['new_email'])
        dup_email = mysql.fetch(find_email)
        flash('Error: This email has already been registered.')
        return redirect('/')
    except:
        pass

    # create alerts list if any validation errors occur
    alerts = []
    
    # name areas cannot be left blank
    if len(session['first_name']) < 1:
        alerts.append('Error: First name cannot be left blank.')
    if len(session['last_name']) < 1:
        alerts.append('Error: Last name cannot be left blank.')

    # email cannot be blank and must match proper format
    if len(session['new_email']) < 1:
        alerts.append('Error: Email cannot be left blank.')
    elif not EMAIL_REGEX.match(session['new_email']):
        alerts.append('Error: Invalid email.')

    # password cannot be blank and must be at least 8 characters long
    if len(password) < 1:
        alerts.append('Error: Password cannot be left blank.')
    elif len(password) < 8:
        alerts.append('Error: Password must contain at least eight characters.')

    # password confirmation - must match password
    if confirm_pw != password:
        alerts.append('Error: Passwords do not match.')

    if alerts:
        for alert in alerts:
            flash(alert)
        return redirect('/')
    # if no alerts exist, registration successful, do this:
    else:
        # create encrypted password hash with bcrypt
        pw_hash = bcrypt.generate_password_hash(password)
        # add user info to database
        add_user = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(session['first_name'], session['last_name'], session['new_email'], pw_hash)
        # use change method from imported module to push changes
        mysql.change(add_user)
        # grab user info for use on wall page
        find_user = "SELECT * FROM users WHERE email = '{}'".format(session['new_email'])
        user = mysql.fetch(find_user)
        session['username'] = user[0]['first_name']
        session['user_id'] = user[0]['id']
        # direct to comments page with new user message
        return redirect('/wall')

# handles login form, routes to comments page in input passes validation
@app.route('/login', methods=['POST'])
def login():
    session['email'] = request.form['email']
    password = request.form['password']
    # find this user in the database using the email provided
    find_user = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(session['email'])
    # create variable to define fetch method from imnported module
    user = mysql.fetch(find_user)
    # use fetch method and bcrypt to ensure password provided matches database
    if bcrypt.check_password_hash(user[0]['pw_hash'], password):
        # password validation successful, grab user's name, login user
        session['username'] = user[0]['first_name']
        session['user_id'] = user[0]['id']
        return redirect('/wall')
    else:
        # password validation failed, redirect to landing page, flash error
        flash('Error: The password provided does not match our records.')
        return redirect('/')

# load wall page
@app.route('/wall')
def load_wall():
    # query to get messages from database
    get_messages = "SELECT messages.id, messages.user_id, CONCAT(users.first_name,' ',users.last_name) AS author, DATE_FORMAT(messages.created_at, '%M %D, %Y') AS message_date, messages.message FROM messages LEFT JOIN users ON messages.user_id = users.id ORDER BY messages.created_at DESC"
    # create variable and run query - variables will be used on wall.html
    messages = mysql.fetch(get_messages)

    # query to get comments from database
    get_comments = "SELECT comments.id, comments.user_id, comments.message_id, CONCAT(users.first_name,' ',users.last_name) AS comment_author, DATE_FORMAT(comments.created_at, '%M %D, %Y') AS comment_date, comments.comment FROM comments LEFT JOIN messages ON comments.message_id = messages.id LEFT JOIN users ON comments.user_id = users.id ORDER BY comments.created_at"

    comments = mysql.fetch(get_comments)
    return render_template('wall.html', messages=messages, comments=comments)

# handles add_message form on wall page
@app.route('/add_message', methods=['POST'])
def add_message():
    # define query to insert new message into database
    new_message = "INSERT INTO messages (message, user_id, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(request.form['new_message'], session['user_id'])

    mysql.change(new_message)

    return redirect('/wall')

# handles add_comment form
@app.route('/add_comment', methods=['POST'])
def add_comment():
    # define query to insert new comment into database
    new_comment = "INSERT INTO comments (comment, user_id, message_id, created_at, updated_at) VALUES ('{}', '{}', '{}', NOW(), NOW())".format(request.form['new_comment'], session['user_id'], request.form['related_message_id'])

    mysql.change(new_comment)

    return redirect('/wall')

# routes to landng page and clears session effectively logging user out
@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')

app.run(debug=True)
