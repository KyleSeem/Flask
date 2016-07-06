"""
1) On the default page it should display a view that says "No ninjas here"
2) When user visits /ninja, it should display all four Ninja Turtles (Leonardo,
    Michelangelo, Raphael, and Donatello)
3) /ninja/[ninja_color], should display the corresponding Ninja Turtle (grab
    the color parameter out of the requested URL)

    a. If user visits /ninja/blue, it should only display Leonardo.
    b. /ninja/orange - Ninja Turtle Michelangelo.
    c. /ninja/red - Ninja Turtle Raphael
    d. /ninja/purple - Ninja Turtle Donatello
    e. If a user tries to hack into your web app by specifying a color or string
    combination other than the colors (Blue, Orange, Red, and Purple),
    example: /ninja/black or /ninja/123, then display Megan Fox who was April
    O'Neil in the most recent ninja turtles movie.
"""

from flask import Flask, render_template, request, redirect
app = Flask(__name__)
#each section on the html page corresponds to a 'ninja' declaration

# initial route directs to basic landing page
# ninja declaration: specific name defined 'none'
@app.route('/')
def index():
    return render_template('index.html', ninja='none')

# triggered by button, routes to dojo page (contains all ninjas) page
# ninja declaration: specific name defined 'all'
@app.route('/ninja')
def ninja():
    return render_template('index.html', ninja='all')

# ninja declaration: general type defined specifics within if statements on html
# <color> allows specific to be defined in if statements in html
@app.route('/ninja/<color>')
def ninja_color(color):
    return render_template('index.html', ninja=color)

app.run(debug=True)
