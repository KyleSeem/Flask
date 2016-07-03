"""
Create a site that when a user loads it creates a random number between 1-100
and stores the number in session. Allow the user to guess at the number and
tell them when they are too high or too low. If they guess the correct number
tell them and offer to play again.

Import random # import the random module.
Use "pop" to remove something from the session.
"""

from flask import Flask, render_template, request, redirect, session, flash
import random
app = Flask(__name__)
app.secret_key = 'HarryPotterJellyfish'

#routes to landing page - index.html;
#checks to see if random # has already been defined, if not, generates new #
#using session[''] method ensures random number remains the same during session
@app.route('/')
def index():
    try:
        session['my_num']
    except:
        session['my_num'] = random.randrange(1,101)
        print session['my_num']
    return render_template('index.html')

#triggered with submission of user input, uses post to compare input and rand#
#flash messages with category allows for alert classification
#redirects to blank landing page so user can complete next action
@app.route('/compare', methods=['POST'])
def compare_input():
    guess = int(request.form['guess'])
    if guess > session['my_num']:
        flash(u'Nope, {} is too high... try again!'.format(guess),'alert alert-danger')
    elif guess < session['my_num']:
        flash(u'Sorry, {} is too low. Try again!'.format(guess),'alert alert-info')
    #can't figure out proper syntax, too much time spent, will come back later
    # elif guess == null:
    #     flash(u'Please enter a number.','alert alert-warning')
    elif guess == session['my_num']:
        flash(u'Yep, {} was the number! Click Reset to play again.'.format(guess),'alert alert-success')
    return redirect('/')

#triggered with reset button, clears stored random # and creates a new one
@app.route('/reset')
def reset_game():
    session.pop('my_num')
    return redirect('/')

app.run(debug=True)
