from flask import Flask, render_template, redirect, flash, session, request, jsonify
app = Flask(__name__)
app.secret_key = 'AustralopithecusFriendsTilTheEnd'
from mysqlconnection import MySQLConnector
mysql = MySQLConnector('full_friends')

#routes to landing page whoch holds friends table and add friend form
@app.route('/')
def index():
    # get all items from friends table in full_friends database
    friends = mysql.fetch('SELECT * FROM friends')
    return render_template('index.html', friends=friends)

# handles form that adds to friends table
@app.route('/friends', methods=['POST'])
def create():
    # define query to run with change method
    add_friend = "INSERT INTO friends(first_name, last_name, occupation, created_at, updated_at) VALUES('{}', '{}', '{}', NOW(), NOW())".format(request.form['first_name'], request.form['last_name'], request.form['occupation'])

    # calls change method from imported python file
    mysql.change(add_friend)

    # returns to landing page with updated data
    return redirect('/')

# routes to friend page based on id selected
@app.route('/friends/<id>/edit')
def edit(id):
    fetch = "SELECT * FROM friends WHERE id = {}".format(id)
    friend = mysql.fetch(fetch)
    # return jsonify(friend)
    return render_template('friends.html', this_friend=friend[0])

# handles edit method on friends page, updates selected friend
@app.route('/friends/<id>', methods=['POST'])
def update(id):

    update_friend = "UPDATE friends SET first_name = '{}', last_name = '{}', occupation = '{}', updated_at = NOW() WHERE id = '{}'".format(request.form['first_name'], request.form['last_name'], request.form['occupation'], id)
    mysql.change(update_friend)
    return redirect('/')

# handles delete method and redirects to updated landing page
@app.route('/friends/<id>/delete')
def destroy(id):

    delete_friend = "DELETE FROM friends WHERE id = '{}'".format(id)
    mysql.change(delete_friend)
    return redirect('/')

app.run(debug=True)
