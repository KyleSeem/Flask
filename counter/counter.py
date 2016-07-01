"""
* Create a simple web application that holds a counter that increments every
    time the page is visited. Complete this using session.
* For ninjas: add a +2 button underneath the counter that increments the counter
    by 2 and reloads the page.
* For hackers: add a reset button that will reset the counter to 1
 """

from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'BlackAndYellowBurgerMustard'

#define class to make counter object
class Counter(object):
    def __init__(self):
        self.tally = 0

#defines class that will reflect appropriate grammar in counter
class Grammar(object):
    def __init__(self):
        self.value = ''

#new instances of Counter and Grammar created
count = Counter()
visit = Grammar()

#routes to and renders landing page initializes/updates counter & verbiage
@app.route('/')
def index():
    count.tally += 1
    session['tally'] = count.tally

    #value of tally determines appropriate grammar
    if count.tally == 1:
        visit.value = 'Visit!'
    else:
        visit.value = 'Visits!'
    session['vis'] = visit.value

    return render_template('index.html')

#linked to button on index.html, only +1 to tally b/c redirect is also +1
@app.route('/ninjas')
def ninjas():
    count.tally += 1
    return redirect('/')

#linked to button on index.html - resets counter to 1
@app.route('/hackers')
def hackers():
    count.tally = 0
    return redirect('/')

app.run(debug=True)
