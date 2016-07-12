from flask import Flask, request, redirect, render_template, flash
app = Flask(__name__)
# salt encryption
import os, binascii
salt = binascii.b2a_hex(os.urandom(15))

# basic encryption
# import the md5 module to generate a hash
import md5
password = 'password';
# encrypt the password we provided as 32 character string
encrypted_password = md5.new(password).hexdigest();
print encrypted_password
# encrypted password returned: 5f4dcc3b5aa765d61d8327deb882cf99

# create new user in database
@app.route('/users/create', methods=['POST'])
def create_user():
    username = request.form['username']
    email = request.form['email']
    password = md5.new(request.form['password']).hexdigest();
    insert_query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES ('{}', '{}', '{}', NOW(), NOW())".format(request.form['username'], request.form['email'], request.form['password'])
    mysql.change(insert_query) # runs update method from imported module

# existing user logging in
password = md5.new(request.form['password']).hexdigest() # does this need ';'?
email = request.form['email']
user_query = "SELECT * FROM users where users.email = '{}' AND users.password = '{}'".format(email, password)
user = mysql.fetch(user_query) # runs fetch method from imported module

#------- salt encryption below ---------------------
# user registration
username = request.form['username']
email = request.form['email']
password = request.form['password']
salt = binascii.b2a_hex(os.urandom(15))
encrypted_pw = md5.new(password + salt).hexdigest()
insert_query = "INSERT INTO users (username, email, password, salt, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(username, email, password, salt)
mysql.change(insert_query)

# authenticate user login
email = reques.form['email']
password = request.form['password']
user_query = "SELECT * FROM users WHERE users.email = '{}' LIMIT 1".format(email)
user = mysql.fetch(user_query)
if user[0]:
    encrypted_password = md5.new(password + user[0]['salt']).hexdigest();
    if user['password'] == encrypted_password:
        # successful login
    else:
        # invalid password
else:
    # invalid email            
