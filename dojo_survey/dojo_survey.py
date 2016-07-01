from flask import Flask, render_template, request, redirect
app = Flask(__name__)

#landing page routes to html.index and will handle form
@app.route('/')
def index():
    return render_template('index.html')

#this route will handle and display form submission
@app.route('/result', methods=['POST'])
def display_results():
    return render_template('result.html')
    name = request.form['name']
    location = request.form['location']
    language = request.form['language']
    comments = request.form['comments']

app.run(debug=True)
