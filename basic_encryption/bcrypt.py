from flask import Flask, request, render_template
from mysqlconnection import MySQLConnector
# imports Bcrypt module
from flask.ext.bcrypt import bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQLConnector('database_name')

# loads page with 2 forms: one for registration and one for login
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# --- generate_password_hash --- create new user
@app.route('/create_user', methods=['POST'])
def create_user():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    # run validations - if successful create password hash with bcrypt
    pw_hash = bcrypt.generate_password_hash(password)
    # now insert new user into users database
    insert_query = "INSERT INTO users (email, username, pw_hash, created_at) VALUES ('{}', '{}', '{}', NOW())".format(email, username, pw_hash)
    mysql.change(insert_query)
    # redirect to success page

# --- check_password_hash --- user login
# how it works
password = 'password'
pw_hash = bcrypt.generate_password_hash(password)
test_password_1 = 'thisiswrong'
bcrypt.check_password_hash(pw_hash, test_password_1)
test_password_2 = 'password'
bcrypt.check_password_hash(pw_hash, test_password_2)
#------
# user login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(email)
    user = mysql.fetch(user_query)
    if bcrypt.check_password_hash(user[0]['pw_hash'], password):
        # login user
    else:
        # set flash error message and redirect to login page    
