"""
Create a mini-game that helps a ninja make some money! When you start the game,
your ninja should have 0 gold. The ninja can go to different places and earn
different amounts of gold. In the case of a casino, your ninja can earn or LOSE
up to 50 golds. Your job is to create a web app that allows this ninja to earn
gold and to display past activities of this ninja.

Make the following forms appear when the user goes to http://localhost:5000:
    * Farm - earns 10-20 golds
    * Cave - earns 5-10 golds
    * House - earns 2-5 golds
    * Casino - earns or loses 0-50 golds

For the farm, your form would look something like <form action="/process_money"
method="post"><input type="hidden" name="building" value="farm" /><input
type="submit" value="Find Gold!"/></form>. Basically, include a hidden value
in the form and have each form submit the form information to /process_money.

Have /process_money determine how much gold the user should have. You should
only have 2 routes -- '/' and '/process_money' (reset can be another route if
you implement this feature).
"""

from flask import Flask, render_template, request, redirect, session, flash
import random
app = Flask(__name__)
app.secret_key = 'OmgPleaseBeQuietCat'


class Bank(object):
    def __init__(self):
        self.value = 0
        self.plunder = []
    def push(self,earnings):
        self.plunder.append(earnings)

#defines instance to keep track of accumulated gold
wallet = Bank()

#routes to landing page, session total for wallet amount displayed
@app.route('/')
def index():
    session['wallet'] = wallet.value
    return render_template('index.html')

#triggered by submit, determines which form was selected, creates random #
#based on each form's gold return, updates
@app.route('/process_money', methods=['POST'])
def process():
    if request.form['action'] == 'farm':
        farm_gold = random.randrange(10,21)
        wallet.value += farm_gold
        flash('Earned {} gold pieces from the farm!'.format(int(farm_gold)),'text-success')

    elif request.form['action'] == 'cave':
        cave_gold = random.randrange(5,11)
        wallet.value += cave_gold
        flash('Earned {} gold pieces from the cave!'.format(int(cave_gold)),'text-success')

    elif request.form['action'] == 'house':
        house_gold = random.randrange(2,5)
        wallet.value += house_gold
        flash('Earned {} gold pieces from the house!'.format(int(house_gold)),'text-success')

    elif request.form['action'] == 'casino':
        casino_gold = random.randrange(-50,51)
        wallet.value += casino_gold
        if int(casino_gold) > 0:
            flash('Earned {} gold pieces from the casino!'.format(int(casino_gold)),'text-success')
        elif int(casino_gold) < 0:
            flash('Lost {} gold pieces from the casino!'.format(int(casino_gold)),'text-danger')
        elif int(casino_gold) == 0:
            flash('You broke even at the casino...could be worse!','text-muted')

    return redirect('/')
#made several attempts to dislay differently, but spent too much time with no
#proper results, must continue w/ class, will return at a later date to finish

#resets wallet to 0, triggered by reset button
@app.route('/reset')
def reset_wallet():
    wallet.value = 0
    return redirect('/')

app.run(debug=True)
