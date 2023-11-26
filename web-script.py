# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:24:24 2023 by Nawaf

This script is a Flask web application that handles user login functionality.
"""
#import necessary libraries
from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm 
import mysql.connector 
from wtforms import DateField, Form, RadioField, StringField, PasswordField, SubmitField, validators 
from werkzeug.security import generate_password_hash 
from werkzeug.security import check_password_hash 
from wtforms.validators import DataRequired, Email, Length, InputRequired, Regexp, Optional
# Initialize the app from Flask
app = Flask(__name__)#forms for flask

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password ="",
                               database='booking')
# Define a form for login
class LoginForm(Form):
    username = StringField('Username', [validators.Optional(),validators.Length(min=4, max=25)])

    email = StringField('Email', [validators.Email(message='Invalid email'),validators.Optional()])
    
    password = PasswordField('Password', [validators.InputRequired()])
  
    #Hashes the password entered by the user. This is done before querying the database to check if the user exists.
    def check_password(self,hashedpassword):
        return check_password_hash(hashedpassword, self.password.data)  
#Define a route to login function
@app.route('/login', methods=['GET', 'POST'])#get: egt stuff; post: send stuff
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
        cursor.execute("(SELECT username,password FROM airline_staff WHERE username = %s) UNION (SELECT email,password FROM customer WHERE email = %s) UNION (SELECT booking_agent_id,password FROM booking_agent WHERE booking_agent_id = %s) ", (form.username.data, form.email.data, form.username.data))
        #pur sql statements here
        user = cursor.fetchone()#receive from database
        print(user)  # Print the user information
        # Check if the user exists and the password is correct
        conn.commit()
        cursor.close()
        if user and ('username' in user or 'email' in user) and form.check_password(user['password']):
            # If the user exists and the password is correct, store the username in a session
            if form.username.data is not None:
              session['username'] = form.username.data
            else:
                session['username'] = form.email.data
            
            return "Logged in successfully!"
        else:
            return "Invalid username or password."
    return render_template('main-login.html', form=form)


class RoleForm(FlaskForm):
    role = RadioField('Role', choices=[('customer','Customer'), ('airline_staff','Airline Staff'), ('booking_agent','Booking Agent')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RoleForm()
    if form.validate_on_submit():
        if form.role.data == 'customer':
            return redirect(url_for('register_customer'))
        elif form.role.data == 'airline_staff':
            return redirect(url_for('register_airline_staff'))
        elif form.role.data == 'booking_agent':
            return redirect(url_for('register_booking_agent'))
    return render_template('main-reg.html', form=form)


class AirlineStaffRegisterForm(Form):
    airline_name = StringField('Airline Name', [validators.Length(min=1, max=25),validators.InputRequired()])

    username = StringField('Username', [validators.Length(min=4, max=25),validators.InputRequired()])

    first_name = StringField('First Name', [validators.Length(min=1, max=25)])

    last_name = StringField('Last Name', [validators.Length(min=1, max=25)])

    dob = DateField('Date of Birth', [validators.InputRequired()])



    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=8),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters'
        )
    ])

    confirm_password = PasswordField('Confirm Password', [
        validators.InputRequired(),
        validators.Length(min=8),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters'
        )
    ]) 
    @staticmethod
    def hash_password(self,password):
        """
        Hashes the given password using the generate_password_hash function from werkzeug.security.

        :param password: The password to be hashed.
        :return: The hashed password.
        """
        return generate_password_hash(password)

@app.route('/register/airline_staff', methods=['GET', 'POST'])
def register_airline_staff():
    form = AirlineStaffRegisterForm(request.form)
    if request.method == 'POST' and form.validate() and form.password.data == form.confirm_password.data:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM airline_staff WHERE username = %s",
            (form.username.data)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            return "User already exists"

        else:

            cursor.execute(
                "INSERT INTO airline_staff(airline_name,username, first_name, last_name,password, DOB ) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    form.airline_name.data,
                    form.username.data,
                    form.first_name.data,
                    form.last_name.data,
                    form.hash_password(form.password.data),
                    form.dob.data,
                    
                )
            )
        conn.commit()
        cursor.close()
        # Add code to handle airline staff registration
        return "Airline staff registered successfully!"
    return render_template('airline-staff-reg.html', form=form)

# @app.route('/register/booking_agent', methods=['GET', 'POST'])
# def register_booking_agent():
#     form = BookingAgentRegisterForm()
#     if form.validate_on_submit():
#         # Add code to handle booking agent registration
#         return "Booking agent registered successfully!"
#     return render_template('booking-agent-reg.html', form=form)

class CustomerRegisterForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=25)])

    email = StringField('Email', [validators.Email(message='Invalid email'), validators.Optional()])

    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=8),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters'
        )
    ])

    confirm_password = PasswordField('Confirm Password', [
        validators.InputRequired(),
        validators.Length(min=8),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters'
        )
    ])
    city_name = StringField('City Name', [validators.Length(min=1, max=25), validators.Optional()])
    street_name = StringField('Street Name', [validators.Length(min=1, max=25), validators.Optional()])
    building_name = StringField('Building Name', [validators.Length(min=1, max=25), validators.Optional()])

    building_number = StringField('Building Number', [validators.Length(min=1, max=50), validators.Optional()])

    passport_expiry = DateField('Passport Expiry', [validators.InputRequired()])
    phone_number = StringField('Phone Number', [validators.Length(min=1, max=25), validators.Optional()])

    @staticmethod
    def hash_password(password):
        """
        Hashes the given password using the generate_password_hash function from werkzeug.security.

        :param password: The password to be hashed.
        :return: The hashed password.
        """
        return generate_password_hash(password)


@app.route('/register/register_customer', methods=['GET', 'POST'])
def register_customer():
    form = CustomerRegisterForm(request.form)
    
    if request.method == 'POST' and form.validate() and form.password.data == form.confirm_password.data:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customer(first_name, last_name, email, password, building, building_no, street, city, passport_expiration, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
            (
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.hash_password(form.password.data),
                form.building_name.data if form.building_name.data is not None else None,
                form.building_number.data if form.building_number.data is not None else None,
                form.street_name.data if form.street_name.data is not None else None,
                form.city_name.data if form.city_name.data is not None else None,
                form.passport_expiry.data,
                form.phone_number.data if form.phone_number.data is not None else None
            )
        )
        conn.commit()
        cursor.close()
        print("entered")
        return "Customer registered successfully!"


    return render_template('customer-registration.html', form=form)

class BookingAgentRegisterForm(Form):
    
    booking_agent_id = StringField('Booking Agent ID', [validators.Length(min=1, max=25),validators.InputRequired()])
    email = StringField('Email', [validators.Email(message='Invalid email'), validators.Optional()])

    airline_name = StringField('Airline Name', [validators.Length(min=1, max=25),validators.InputRequired()])

    email = StringField('Email', [validators.Email(message='Invalid email'),validators.Optional()])

     password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=8),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters'
        )
    ])

    confirm_password = PasswordField('Confirm Password', [
        validators.InputRequired(),
        validators.Length(min=8),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters'
        )
    ])







# Set the secret key for the app
app.secret_key = '123456'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.config['WTF_CSRF_ENABLED'] = True
    app.run('127.0.0.1', 5000, debug=True, use_reloader=False)
