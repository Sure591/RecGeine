from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Mock user data
users = {'admin': 'password'}

class User(UserMixin):
    def __init__(self, username):
        self.username = username

@login_manager.user_loader
def load_user(username):
    return User(username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        recommendations = recommend(user_id)
        return render_template('index.html', recommendations=recommendations)
    return render_template('index.html', recommendations=None)

def recommend(user_id):
    # Placeholder recommendation logic
    return ["Product 1", "Product 2", "Product 3"]

if __name__ == '__main__':
    app.run(debug=True)
