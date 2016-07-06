from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    return render_template('user.html', username=username)


app.run(debug=True)
