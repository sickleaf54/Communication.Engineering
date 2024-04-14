from flask import Flask, render_template, jsonify
from database import get_all_players
from networking import Networking
from networming_moves import Networking


app = Flask(_name_)

networking_instance = Networking()
networking_moves_instance = Networming()
networking_instance.save_player_info_to_spreadsheet()
networking_moves_instance.save_player_moves_to_spreadsheet()


players = get_all_players()
for player in players:
    print(player)

# Define routes
@app.route('/tic')
def index():
    return render_template('tic.html')

@app.route('/scoreboard')
def scoreboard():
    # Pass the players array to the template
    return render_template('scoreboard.html', players=players)

if _name_ == '_main_':
    app.run(debug=True)
