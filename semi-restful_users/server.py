from flask import Flask, render_template, redirect, request, session, flash, jsonify
# import module from mysqlconnection.py - creates access to database
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
app.secret_key = 'Lp9cPeMMww5bX3bChij5QbPFavUqBdpA498RFcUv'
mysql = MySQLConnector('semi_restful_routes')
# define email format to pass validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# landing page - shows list of all users
@app.route('/users')
def index():
    # display all users
    users = mysql.fetch("SELECT id, CONCAT(first_name,' ',last_name) AS full_name, email, DATE_FORMAT(created_at, '%M %D, %Y') AS create_date FROM users")
    return render_template('index.html', users=users)

# routes to new users form
@app.route('/users/new')
def new_user():

    return render_template('new_users.html')

# handles processing of new user form
@app.route('/users/create', methods=['POST'])
def create_user():
    # create alerts list to use if any validation errors exist
    alerts = []
    # validation criteria: no fields left blank, email must meet format reqs
    if len(request.form['first_name']) < 1:
        alerts.append('Error: First name cannot be left blank.')
    if len(request.form['last_name']) < 1:
        alerts.append('Error: Last name cannot be left blank.')

    if len(request.form['email']) < 1:
        alerts.append('Error: Email cannot be left blank.')
    elif not EMAIL_REGEX.match(request.form['email']):
        alerts.append('Error: invalid email.')

    # if alerts exists, do this:
    if alerts:
        for alert in alerts:
            flash(alert)
        return redirect('/users/new')
    # if no alerts exist, do this
    else:
        create = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES ('{}', '{}', '{}', NOW(), NOW())".format(request.form['first_name'], request.form['last_name'], request.form['email'])
        # run the query
        mysql.change(create)

        return redirect('/users')

# routes to individual user's information/page using id passed in
@app.route('/users/<id>')
def show_user(id):
    fetch = "SELECT id, CONCAT(first_name,' ',last_name) AS full_name, email, DATE_FORMAT(created_at, '%M %D, %Y') AS create_date FROM users WHERE id = '{}'".format(id)
    user = mysql.fetch(fetch)
    return render_template('this_user.html', this_user=user[0])

# routes to edit user form
@app.route('/users/<id>/edit')
def edit_user(id):
    fetch = "SELECT * FROM users WHERE id = '{}'".format(id)
    user = mysql.fetch(fetch)
    return render_template('edit_users.html', this_user=user[0])

# handles processing of edit user form
@app.route('/users/<id>/update', methods=['POST'])
def update_user(id):
    # create alerts list to use if validation errors exist
    alerts = []
    # validation criteria: no fields left blank, email must meet format reqs
    if len(request.form['first_name']) < 1:
        alerts.append('Error: First name cannot be left blank.')
    if len(request.form['last_name']) < 1:
        alerts.append('Error: Last name cannot be left blank.')

    if len(request.form['email']) < 1:
        alerts.append('Error: Email cannot be left blank.')
    elif not EMAIL_REGEX.match(request.form['email']):
        alerts.append('Error: invalid email.')

    # if alerts exist, do this:
    if alerts:
        for alert in alert:
            flash(alert)
        return redirect('/users/<id>/edit')
    # if no alerts exist, do this:
    else:
        update = "UPDATE users SET first_name = '{}', last_name = '{}', email = '{}', updated_at = NOW() WHERE id = '{}'".format(request.form['first_name'], request.form['last_name'], request.form['email'], id)
        user = mysql.change(update)

        return redirect('/users')

# delete user
@app.route('/users/<id>/destroy')
def delete_user(id):
    delete = "DELETE FROM users WHERE id = '{}'".format(id)
    mysql.change(delete)
    # flash message?
    return redirect('/users')

app.run(debug=True)
