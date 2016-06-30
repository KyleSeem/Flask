"""
reate a flask project capable of handling the following routes:

localhost:5000/
    This route should serve a view file called index.html and display a greeting.
localhost:5000/ninjas
    This route should serve a view file called ninjas.html and display
    information about ninjas.
localhost:5000/dojos/new
    This route should serve a view file called dojos.html and have a form
    (don't worry where the form should be sent to - action=' ').

Now create a folder inside of our project labeled static. Remember, this static
folder will be used to serve all of our static content (stylesheets, images,
javascript files, etc.)! Now try placing a stylesheet in the static folder and
referencing it in our view files (templates).
"""

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
#routes to localhost:5000/

def index():
    return render_template('index.html', greeting='Hello there!')
#grabs the index.html template and defines 'greeting'

@app.route('/ninjas')
#routes to localhost:500/ninjas

def ninjas():
    return render_template('ninjas.html')

@app.route('/dojos/new')
#routes to localhost:5000/dojos/new

def dojos():
    return render_template('dojos.html')

app.run(debug=True)
