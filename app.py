import flask
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from models.users import check_login

app = flask.Flask(__name__)
admin = flask.Blueprint('admin', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_record = check_login(username, password)
        print(f"DEBUG: user_record: {user_record}")
        if user_record:
            return redirect(url_for('admin.admin_index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@admin.route('/')
def admin_index():
    return render_template('admin/admin_index.html')

app.register_blueprint(admin, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)