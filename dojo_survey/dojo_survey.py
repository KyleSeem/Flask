from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = 'ListeningToSomethingAwesome'

#landing page routes to html.index and will handle form
@app.route('/')
def index():
    return render_template('index.html')

#this route will handle and display form submission
#use session to hold info
@app.route('/result', methods=['POST'])
def display_results():
    session['name'] = request.form['name']
    session['location'] = request.form['location']
    session['language'] = request.form['language']
    session['comments'] = request.form['comments']

    #allows multiple errors to be displayed at once
    alerts = []

    #if statements ensure all data has been appropriately completed
    #flash messages exist if any input fails validation
    #name and comments cannot be blank, coments must be 120 char or less
    if len(session['name']) < 1:
        alerts.append('Please enter your name.')
    if len(session['comments']) < 1:
        alerts.append('Please enter comments.')
    if len(session['comments']) > 120:
        alerts.append('Please limit comments to 120 characters or less')

    if alerts:
        for alert in alerts:
            flash(alert)
        return redirect('/')
    else:
        return render_template('result.html')

#refreshes session so personal info is cleared
@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

app.run(debug=True)
