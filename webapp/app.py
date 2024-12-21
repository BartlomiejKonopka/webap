import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

USER_DB = "users.json"  # Path to your users.json file

# Helper functions to load and save users to the JSON file
def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, 'w') as file:
            json.dump([], file)  # Initialize with an empty list
    with open(USER_DB, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USER_DB, 'w') as file:
        json.dump(users, file, indent=4)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user_exists = False  # Flag to track if the user already exists
    if request.method == 'POST':
        email = request.form['email']  # First the email
        username = request.form['username']  # Then the username
        password = request.form['password']

        # Load users and check if email already exists
        users = load_users()
        if any(user['email'] == email for user in users):
            user_exists = True  # User already exists
        else:
            # Hash the password using pbkdf2:sha256
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            users.append({'email': email, 'username': username, 'password': hashed_password})
            save_users(users)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('home'))

    return render_template('signup.html', user_exists=user_exists)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Load users and find the user
    users = load_users()
    user = next((user for user in users if user['email'] == email), None)
    if user and check_password_hash(user['password'], password):
        flash("Login successful!", "success")
        return redirect(url_for('home'))
    else:
        flash("Invalid email or password.", "error")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
