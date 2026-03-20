import flask
from flask import render_template, request, url_for, jsonify
from werkzeug.utils import redirect

from models.matches import get_matches, give_court, finnish_game
from models.courts import get_courts
from models.users import check_login

app = flask.Flask(__name__)
admin = flask.Blueprint('admin', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/matches')
def matches():

    matches_list, status_info = get_matches()
    court_list = get_courts()

    courts_serializable = [dict(court) if not isinstance(court, dict) else court for court in court_list]

    return jsonify({
        "status": "success",
        "count": len(matches_list),
        "matches": matches_list,
        "courts": courts_serializable,
    }), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_record = check_login(username, password)
        if user_record:
            return redirect(url_for('admin.admin_index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/api/score', methods=['POST'])
def enter_score():
    data = request.json

    game_id = data.get('game_id')
    score_t1 = data.get('score_t1')
    score_t2 = data.get('score_t2')

    if not game_id:
        return jsonify({"status": "error", "message": "Game ID is required"}), 400

    result = finnish_game(game_id, score_t1, score_t2)
    return jsonify(result)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@admin.route('/')
def admin_index():
    return render_template('admin/admin_index.html')

@admin.route('/matches')
def admin_matches():
    return render_template('admin/admin_matches.html')

@admin.route('/players')
def admin_players():
    return render_template('admin/admin_players.html')

@admin.route('/api/assign_court', methods=['POST'])
def assign_court():
    data = request.json
    result = give_court(data['game_id'], data['court_id'])

    return jsonify(result)

app.register_blueprint(admin, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)