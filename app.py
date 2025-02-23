from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import sqlite3
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
import re
from keras.models import load_model
from PIL import Image

app = Flask(__name__)
app.secret_key = "wge@#^&#!*#!ghrufekfjehege545124"

# Load your model
model = load_model('C:\Users\sesha\Downloads\DRP\DRP\model\detect525.h5')

def init_db(db_name='users.db'):
    """
    Initialize the database by creating a 'users' table if it doesn't exist.
    
    Args:
        db_name (str): The name of the database file. Defaults to 'users.db'.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create table with correct syntax for SQLite
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

init_db()

# Password validation function
def validate_password(password, confirm_password=None):
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search("[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search("[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search("[0-9]", password):
        errors.append("Password must contain at least one number.")
    if not re.search("[@#$%^&+=]", password):
        errors.append("Password must contain at least one special character (@, #, $, etc.).")
    if confirm_password and password != confirm_password:
        errors.append("Passwords do not match.")
    return errors

# Default Route (Login & Register)
@app.route('/', methods=['GET', 'POST'])
def auth():
    errors = []
    if request.method == 'POST':
        # Check if login or registration is being requested
        action = request.form.get('action')
        
        if action == 'login':
            # Handle login
            email = request.form['email']
            password = request.form['password']

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('dashboard'))
            else:
                errors.append('Login failed. Check your credentials.')

        elif action == 'register':
            # Handle registration
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Validate passwords
            password_errors = validate_password(password, confirm_password)
            if password_errors:
                errors.extend(password_errors)
            else:
                # If no errors, register the user
                hashed_password = generate_password_hash(password)
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
                conn.commit()
                conn.close()
                flash('Registration successful! Please log in.')

    return render_template('auth.html', errors=errors)

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('auth'))





@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Preprocess the image as needed
    img = Image.open(file)
    img = img.resize((224, 224))  # Example resizing, adjust as necessary
    img_array = np.array(img) / 255.0  # Normalize if necessary
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Make prediction
    prediction = model.predict(img_array)
    level = np.argmax(prediction)  # Assuming 5 classes

    # Map levels to descriptions
    levels = {
        0: ("No DR", "No signs of diabetic retinopathy."),
        1: ("Mild DR", "This indicates mild diabetic retinopathy."),
        2: ("Moderate DR", "This indicates moderate diabetic retinopathy."),
        3: ("Severe DR", "This indicates severe diabetic retinopathy."),
        4: ("Proliferative DR", "This indicates proliferative diabetic retinopathy.")
    }

    result = levels.get(level, ("Unknown", "Prediction not available."))
    return jsonify({'prediction': result[0], 'description': result[1]})


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('auth'))

if __name__ == '__main__':
    app.run(debug=True)
