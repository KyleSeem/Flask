from flask import Flask, render_template, request, redirect, session, flash
import re
#ergex ensures email follows proper format
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
#num and cap regex below ensure password contains at least one of each
#I'm sure there is an easier way to do this, but I couldn't find it in a reasonable
#amount of time, so this will do for now
NUM_REGEX = re.compile(r'[0-9]')
CAP_REGEX = re.compile(r'[A-Z]')

app = Flask(__name__)
app.secret_key = 'AeIoUandSometimesY'

# routes to landing page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
# session will hold user input so it remains even if errors out
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    session['verify'] = request.form['verify']

# alerts list created in order to append any and all applicable errors
# category determines what color the warning message will be
    alerts = []
    category = ''

# begin validation process
    if len(session['first_name']) < 1:
        alerts.append('Please enter your first name.')
    if len(session['last_name']) < 1:
        alerts.append('Please enter your last name.')

    if len(session['email']) < 1:
        alerts.append('Please enter your email address.')
    elif not EMAIL_REGEX.match(session['email']):
        alerts.append('Please enter a valid email address.')

# password input validation: meets length and character requirements
    if len(session['password']) < 1:
        alerts.append('Please create a new password.')
    elif len(session['password']) < 8:
        alerts.append('Password must contain at least 8 characters.')
    else:
        if not NUM_REGEX.search(session['password']):
            alerts.append('Password must contain at least 1 uppercase letter and 1 numeric value.')
        elif not CAP_REGEX.search(session['password']):
            alerts.append('Password must contain at least 1 uppercase letter and 1 numeric value.')

# verify password input validation
    if len(session['verify']) < 8:
        alerts.append('Please confirm your password.')
    elif session['verify'] != session['password']:
        alerts.append('Error: Passwords do not match.')

#if validation errors exist, do this:
    if alerts:
        category = 'alert alert-danger'
        for alert in alerts:
            flash(alert, category)
        return redirect('/')
    else:
        category = 'alert alert-success'
        flash('You have successfully registered!', category)
        return redirect('/')

#to be completed at a later date:
    #add birthdate and validation
    #decide how you want to clear session - new template?

app.run(debug=True)
