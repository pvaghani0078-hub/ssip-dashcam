from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
# Secret key is required to use 'sessions' securely
app.secret_key = 'super_secret_car_key_2026'

# --- CREDENTIALS (For Prototype) ---
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# 1. The Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if credentials match
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Username or Password. Try again.", "error")
            return redirect(url_for('login'))

    # If it's a GET request, just show the login page
    return render_template('login.html')

# 2. The Dashboard Route (Protected)
@app.route('/')
def dashboard():
    # If the user is NOT logged in, kick them back to the login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # If they are logged in, show the main dashboard (we will build this next)
    return render_template('index.html')

# 3. The Logout Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
import random
from flask import jsonify

# --- API ROUTES FOR DASHBOARD ---

@app.route('/api/status')
def get_status():
    # In the real project, this data comes from your Raspberry Pi Sensors and GPS module
    # For now, we simulate data so you can see the web app working
    data = {
        "speed": random.randint(60, 75), # Simulated Speed
        "heading": "NORTH EAST",         # Simulated Direction
        "drowsy": random.choice([True, False, False, False]), # Mostly false, sometimes true
        "phone_usage": random.choice([True, False, False, False]),
        "alcohol_level": 0.000,          # 0.000 is clean
        "lat": 23.0225 + random.uniform(-0.001, 0.001), # Simulating car movement in Ahmedabad
        "lon": 72.5714 + random.uniform(-0.001, 0.001)
    }
    # Simulate a drunk driver occasionally for testing
    if random.random() > 0.9: 
        data["alcohol_level"] = 0.085 

    return jsonify(data)

@app.route('/api/emergency', methods=['POST'])
def trigger_emergency():
    # This runs when the family clicks the "ALERT POLICE / HOSPITAL" button
    print("CRITICAL: FAMILY TRIGGERED EMERGENCY OVERRIDE!")
    print("Sending GPS location to Police and nearby Hospitals...")
    # Here you would add the Python code to trigger the buzzer or send the WhatsApp message
    
    return jsonify({"status": "success", "message": "Emergency Services and Car Alarm Activated!"})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)