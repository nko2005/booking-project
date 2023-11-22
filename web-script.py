# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:24:24 2023

This script is a Flask web application that handles user login functionality.
"""
#import necessary libraries
from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector
from wtforms import Form, StringField, PasswordField, validators
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password ="",
                               database='booking')
# Define a form for login
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.InputRequired()])
    def hash_password(self):
        self.password.data = generate_password_hash(self.password.data)
    def check_password(self,hashedpassword):
        return check_password_hash(hashedpassword, self.password.data)  
#Define a route to login function
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the login functionality.

    This function receives a POST request with login form data and validates it.
    If the form data is valid, it queries the database to check if the user exists.
    If the user exists, it returns a success message. Otherwise, it returns an error message.
    If the request method is GET, it renders the customer-login.html template with the login form.

    :return: A success message if the user is logged in successfully, or an error message if the username or password is invalid.
    """
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username,password FROM airline_staff WHERE username = %s", (form.username.data,))
        user = cursor.fetchone()
        print(user)
         # Check if the user exists and the password is correct
        if user and form.check_password(user['password']):
            return "Logged in successfully!"
        else:
            return "Invalid username or password."
    return render_template('customer-login.html', form=form)
    

# Set the secret key for the app
app.secret_key = '123456'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True, use_reloader=False)
