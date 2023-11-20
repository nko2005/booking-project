# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:24:24 2023

@author: Nawaf
"""

from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector

from wtforms import Form, StringField, PasswordField, validators
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


    

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password ="",
                               database='booking')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.InputRequired()])
    def hash_password(self):
        self.password.data = generate_password_hash(self.password.data)
    def check_password(self, password):
        return check_password_hash(self.password, password)

#Define a route to test function
@app.route('/login', methods=['GET', 'POST'])
def login ():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
         # Query the database to get the user
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username FROM airline_staff WHERE username = %s", (form.username.data,))
        
        user = cursor.fetchone()
        #if user and form.check_password(form.password.data):
        if user:
            return "Logged in successfully!"
        else:
            return "Invalid username or password."
   
    return render_template('customer-login.html', form=form)
    


app.secret_key = '123456'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True,use_reloader=False)