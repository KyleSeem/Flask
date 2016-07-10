from flask import Flask, session, render_template, request, redirect, flash, jsonify
app = Flask(__name__)
app.secret_key = 'ThatsThatNewNewRichHueyDueyAndLouie'
import re
from mysqlconnection import MySQLConnector
mysql = MySQLConnector('email_validation')
# regular expression object to run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# routes to landing page with registration form
@app.route('/')
def index():
    return render_template('index.html')

# routes to process method (validation)
@app.route('/process', methods=['POST'])
def process():
    # if email input is left blank, do this:
    if len(request.form['email']) < 1:
        flash('Email cannot be left blank.')
    # if email does not match email format, do this:
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email address.')
    else:
        # add email to database
        add_email = "INSERT INTO emails(email, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(request.form['email'])
        mysql.change(add_email)
        # collect that email and store in session
        session['email'] = request.form['email']
        # uses session to store 'type' - determines flash message
        session['type'] = 'submitted'
        # send to success page
        return redirect('/success')

    # if email criteria not met:
    return redirect('/')

# routes to update method (delete emails)
@app.route('/update', methods=['POST'])
def update_emails():
    delete_email = "DELETE FROM emails WHERE id = '{}'".format(request.form['id'])
    mysql.change(delete_email)
    # uses session to store 'type' - determines flash message
    session['type'] = 'deleted'
    emails = mysql.fetch('SELECT * FROM emails')

    return redirect('/success')

# routes to success page
@app.route('/success')
def success():
    # if email was entered:
    if session['type'] == 'submitted':
        flash("You have successfully registered with email address:{}.".format(session['email']))
        # if email was deleted:
    elif session['type'] == 'deleted':
        flash("The selected email has been deleted.")

    # get all data from database
    emails = mysql.fetch('SELECT * FROM emails')

    return render_template('success.html', emails=emails)

app.run(debug=True)
