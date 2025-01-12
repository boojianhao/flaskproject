from flask import Flask, request, redirect, url_for, render_template, session, flash
from flask_mail import Mail, Message
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

# Generate OTP
def generate_otp():
    return random.randint(100000, 999999)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']
    otp = generate_otp()
    session['otp'] = otp
    session['email'] = email

    msg = Message('Your OTP Code', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}'
    mail.send(msg)

    flash('OTP has been sent to your email.', 'info')
    return redirect(url_for('verify_otp'))

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form['otp']
        if 'otp' in session and int(otp) == session['otp']:
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html')

if __name__ == '__main__':
    app.run(debug=True)