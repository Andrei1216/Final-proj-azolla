from flask import Flask, render_template, request, redirect, flash, jsonify, make_response, url_for, render_template_string

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

from flask_mail import Mail, Message 

import serial
import json
import time
import jwt
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SECRET_KEY")

app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT") 
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME") 
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD") 
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME") 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# DATABASE TABLE
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db .String(255), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


from functools import wraps
def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        access_token = request.cookies.get('token')

        if not access_token:
            return redirect(url_for('login'))
        
        try:
            decoded_token = jwt.decode(access_token, os.environ.get("SECRET_KEY"), algorithms="HS256")
            return view_func(*args, **kwargs)
        
        except:
            return redirect(url_for('login'))      

    return wrapped_view

# LOGIN PAGE
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = Admin.query.filter_by(email = email).first()

        if user is not None:
            if email == user.email:
                checked_password = bcrypt.check_password_hash(user.password, password)

                if checked_password:
                    encoded_jwt = jwt.encode({"username": user.username}, os.environ.get("SECRET_KEY"), algorithm="HS256")

                    response = make_response(redirect('dashboard'))
                    response.set_cookie('token', encoded_jwt)

                    return response
                
                else:
                    flash("Incorrect Username or Password")
                    return redirect("login")
        else:
            flash("User doesn't exist")
            
    return render_template('login.html')

# PASSWORD RESET
@app.route('/reset_password', methods=["POST", "GET"])
def reset_password():

    if request.method == "POST":
        user = Admin.query.filter_by(email = request.form["email"]).first()

        if user is None:
            flash("Email is not registered", "error")
            return redirect(url_for('reset_password'))

        encode_token = jwt.encode({"email": user.email}, os.environ.get("SECRET_KEY"), algorithm="HS256")
        reset_link = url_for('reset_password_token', token = encode_token, _external=True)
        dev_email = "romeoestoy0101@gmail.com", 
        email = user.email

        msg = Message(subject="Password Reset Request", recipients=[user.email])

        msg.html = f"""<h3>Dear Mam/Sir,</h3>
                    <p>We received a request to recover your account associated with the email address: { email }. If this was not initiated by you, please disregard this email.</p>
                    <p>To reset your account password, please click on the link below:</p>
                    <p><a href='{ reset_link }'>{ reset_link }</a></p>
                    <p>If you are unable to click the link, please copy and paste it into your browser's address bar.</p>
                    <p>If you did not request this password reset, please contact our support team immediately at { dev_email } for assistance.</p>
                    <br>
                    <p>Thank you for using our services.</p>"""
        
        mail.send(msg)
        flash('Password reset instructions sent to your email.', "success")

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=["POST", "GET"])
def reset_password_token(token):

    decode_token = jwt.decode(token, 'secret_key', algorithms="HS256")
    email = decode_token["email"]

    user = Admin.query.filter_by(email = email).first()

    if request.method == "POST":

        user_pass = request.form["password"]
        user.password = bcrypt.generate_password_hash(user_pass)
        db.session.commit()

        flash("Password updated", "success")
        return redirect(url_for('login'))

    return render_template('update_password.html')

# DASHBOARD PAGE
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# PROFILE PAGE
# @app.route('/profile')
# @login_required
# def profile():   
#     return render_template('profile.html')
    

# LOGOUT THE USER
# CLEAR THE COOKIES
@app.route('/logout')
@login_required
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', '', expires=0)
    return response



@app.route('/open_pump', methods=["POST"])
def open_pump():
    # Replace 'COMx' with the correct serial port
    ser = serial.Serial('COM5', 9600, timeout=1)

    # while True:
    data = {
        "pump_id": 2,
        "status": 1
    }

    json_data = json.dumps(data)  # Convert Python dictionary to JSON string
    ser.write(json_data.encode())  # Send the JSON data to the Arduino

    # print(json_data)
    time.sleep(1)  # Send data every 1 second

    return "Hello"

@app.route('/close_pump', methods=["POST"])
def close_pump():
    # Replace 'COMx' with the correct serial port
    ser = serial.Serial('COM5', 9600, timeout=1)

    # while True:
    data = {
        "pump_id": 2,
        "status": 0
    }

    json_data = json.dumps(data)  # Convert Python dictionary to JSON string
    ser.write(json_data.encode())  # Send the JSON data to the Arduino

    # print(json_data)
    time.sleep(1)  # Send data every 1 second

    return "Hello"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
