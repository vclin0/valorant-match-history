from flask import Flask, render_template, request, redirect, url_for
import json
from .valApi import ValorantAPI
import time

app = Flask(__name__)

match_movement_hash = {
  'INCREASE': 'Increase',
  'MINOR_INCREASE': 'Minor Increase',
  'MAJOR_INCREASE': 'Major Increase',
  'DECREASE': 'Decrease',
  'MAJOR_DECREASE': 'Major Decrease',
  'MINOR_DECREASE': 'Minor Decrease',
  'PROMOTED': 'Promoted',
  'DEMOTED': 'Demoted'
}

maps_hash = {
  '/Game/Maps/Duality/Duality': 'bind',
  '/Game/Maps/Bonsai/Bonsai': 'split',
  '/Game/Maps/Ascent/Ascent': 'ascent',
  '/Game/Maps/Port/Port': 'icebox',
  '/Game/Maps/Triad/Triad': 'haven'
}

@app.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route('/')
def home():
  return render_template('login.html')
  # return '<h1>Hello World<h1>'

#   return Response(json_res, mimetype="application/json")

@app.route('/match_history', methods=['GET'])
def redirect_to_login():
  return redirect(url_for('home'))

@app.route('/match_history', methods=['POST'])
def display_match_history():
  try:
    username = request.form['username']
    password = request.form['password']
    region = request.form['region']

    valorant = ValorantAPI(username, password, region)
    print('hello world')

    json_res = valorant.get_match_history()

    posts = []
    for match in json_res['Matches']:
      # print(match)
      if match['CompetitiveMovement'] == 'MOVEMENT_UNKNOWN':
        continue
      game_outcome = 'Victory' if 'INCREASE' in match['CompetitiveMovement'] or 'PROMOTED' in match['CompetitiveMovement'] else 'Defeat'
      lp_change = ''

      game_map = 'images/maps/' + maps_hash[match['MapID']] + '.png'

      tier = 'images/ranks/' + str(match['TierAfterUpdate']) + '.png'
      epoch_time = match['MatchStartTime'] // 1000
      date = time.strftime('%m-%d-%Y', time.localtime(epoch_time))

      before = match['TierProgressBeforeUpdate']
      after = match['TierProgressAfterUpdate']

      if match['CompetitiveMovement'] == 'PROMOTED':
        lp_change = '+' + str(after + 100 - before)
        match_data = {
          'lp_change': lp_change,
          'current_lp': after,
          'game_outcome': game_outcome,
          'movement': match_movement_hash[match['CompetitiveMovement']],
          'tier': tier,
          'date': date,
          'game_map': game_map,
        }
      elif match['CompetitiveMovement'] == 'DEMOTED':
        lp_change = '-' + str(before + 100 - after)
        match_data = {
          'lp_change': lp_change,
          'current_lp': after,
          'game_outcome': game_outcome,
          'movement': match_movement_hash[match['CompetitiveMovement']],
          'tier': tier,
          'date': date,
          'game_map': game_map,
        }
      else:
        if before < after:
          # won
          lp_change = '+' + str(after - before)
        else:
          # lost
          lp_change = str(after - before)

        match_data = {
          'lp_change': lp_change,
          'current_lp': after,
          'game_outcome': game_outcome,
          'movement': match_movement_hash[match['CompetitiveMovement']],
          'tier': tier,
          'date': date,
          'game_map': game_map,        
        }
      posts.append(match_data)
    print(posts)
    return render_template('match_history.html', posts=posts, name=valorant.game_name, title='VALORANTELO - Match History')
  except:
    print('An error occurred. F')
    return render_template('error.html')

@app.route('/example', methods=['GET'])
def view_example_data():
  example_data = [{'lp_change': '+8', 'current_lp': 44, 'game_outcome': 'Victory', 'movement': 'Increase', 'tier': 'images/ranks/23.png', 'date': '12-21-2020', 'game_map': 'images/maps/haven.png'}, {'lp_change': '+10', 'current_lp': 36, 'game_outcome': 'Victory', 'movement': 'Increase', 'tier': 'images/ranks/23.png', 'date': '12-21-2020', 'game_map': 'images/maps/haven.png'}, {'lp_change': '+16', 'current_lp': 26, 'game_outcome': 'Victory', 'movement': 'Major Increase', 'tier': 'images/ranks/23.png', 'date': '12-21-2020', 'game_map': 'images/maps/ascent.png'}, {'lp_change': '+9', 'current_lp': 10, 'game_outcome': 'Victory', 'movement': 'Increase', 'tier': 'images/ranks/23.png', 'date': 
'12-21-2020', 'game_map': 'images/maps/haven.png'}, {'lp_change': '+27', 'current_lp': 1, 'game_outcome': 'Victory', 'movement': 'Promoted', 'tier': 'images/ranks/23.png', 'date': '12-21-2020', 'game_map': 'images/maps/split.png'}, {'lp_change': '-15', 'current_lp': 74, 'game_outcome': 'Defeat', 'movement': 'Decrease', 'tier': 'images/ranks/22.png', 'date': '12-21-2020', 'game_map': 'images/maps/bind.png'}, {'lp_change': '+24', 'current_lp': 89, 'game_outcome': 'Victory', 'movement': 'Increase', 'tier': 'images/ranks/22.png', 'date': '12-21-2020', 'game_map': 'images/maps/split.png'}, {'lp_change': '-14', 'current_lp': 65, 'game_outcome': 'Defeat', 'movement': 'Decrease', 'tier': 'images/ranks/22.png', 'date': '12-21-2020', 'game_map': 'images/maps/ascent.png'}, {'lp_change': '+23', 'current_lp': 79, 'game_outcome': 'Victory', 'movement': 'Increase', 'tier': 'images/ranks/22.png', 'date': '12-21-2020', 'game_map': 'images/maps/split.png'}, {'lp_change': '+12', 'current_lp': 56, 'game_outcome': 'Victory', 'movement': 'Increase', 'tier': 'images/ranks/22.png', 'date': '12-21-2020', 'game_map': 'images/maps/icebox.png'}, {'lp_change': '+9', 'current_lp': 44, 'game_outcome': 'Victory', 'movement': 'Minor Increase', 'tier': 'images/ranks/22.png', 'date': '12-21-2020', 'game_map': 'images/maps/icebox.png'}]
  return render_template('match_history.html', posts=example_data, name='Example #RIOT', title='VALORANTELO - Example')

