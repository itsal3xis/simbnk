from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

# Setup Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_file = 'data/users.json'

# Create the data file if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump({}, f)

# Load user data
def load_users():
    with open(data_file, 'r') as f:
        return json.load(f)

# Save user data
def save_users(users):
    with open(data_file, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        return render_template('login_error.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username not in users:
            users[username] = {
                'password': password,
                'balance': 1000,
                'transactions': [1000, 200, 200]
            }
            save_users(users)
            return redirect(url_for('login'))
        return 'User already exists'
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user']
        users = load_users()
        balance = users[user]['balance']
        transactions = users[user]['transactions']
        return render_template('dashboard.html', balance=balance, transactions=transactions)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
