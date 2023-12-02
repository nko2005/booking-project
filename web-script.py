# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:24:24 2023 by Nawaf

This script is a Flask web application that handles user login functionality.
"""
#import necessary libraries test
from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm 
import mysql.connector 
from wtforms import DateField, DateTimeField, Form, RadioField, StringField, PasswordField, SubmitField, validators, SelectField
from werkzeug.security import generate_password_hash 
from werkzeug.security import check_password_hash 
from wtforms.validators import DataRequired, Email, Length, InputRequired, Regexp, Optional
from datetime import datetime, timedelta
# Initialize the app from Flask
app = Flask(__name__)#forms for flask

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password ="",
                               database='booking', port = 3306)
# Define a form for login
class LoginForm(Form):
    username = StringField('Username', [validators.Optional(),validators.Length(min=4, max=25)])
    agentID= StringField('Agent ID', [validators.Optional(),validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Optional()])
    
    password = PasswordField('Password', [validators.InputRequired()])
  
    #Hashes the password entered by the user. This is done before querying the database to check if the user exists.
    def check_password(self,hashedpassword):
        print("what i entered",self.password.data)
        print("what is in db hashed:",hashedpassword)
        

        print(check_password_hash(hashedpassword, self.password.data)) 
        return check_password_hash(hashedpassword, self.password.data)  
#Define a route to login function
@app.route('/', methods=['GET', 'POST'])
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
        print(form.email.data)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT username,password,'airline_staff' as user_type FROM airline_staff WHERE username = %s""",(form.username.data,))
        user = cursor.fetchone()#receive from database
        if user is None:
            cursor.execute("""SELECT email,password,'customer' as user_type FROM customer WHERE email = %s""",(form.email.data,))
            user = cursor.fetchone()
        if user is None:
         #receive from database
            cursor.execute("""SELECT booking_agent_id,password, 'booking_agent' as user_type FROM booking_agent WHERE booking_agent_id = %s """,(form.agentID.data,))
            user = cursor.fetchone()

        print(user)  # Print the user information
        # Check if the user exists and the password is correct
        conn.commit()
        cursor.close()
        if user and ('username' in user or 'email' in user or "booking_agent_id" in user ) and form.check_password(user['password']):
            # If the user exists and the password is correct, store the username in a session
            if form.username.data is not None:
              session['username'] = form.username.data
            elif form.email.data is not None:
                session['username'] = form.email.data
            elif form.agentID.data is not None:
                session['username'] = form.agentID.data
            session['user_type'] = user['user_type']
            
            if user['user_type'] == 'airline_staff':
                # Serve the airline staff dashboard
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""SELECT airline_name, permission FROM airline_staff WHERE username = %s""", (session['username'],))
                userinfo = cursor.fetchone()
                session["airline"]= userinfo['airline_name']
                session["permission"] = userinfo['permission']
                conn.commit()
                cursor.close()
                return redirect(url_for('airline_staff_dashboard'))
            
            elif user['user_type'] == 'customer':
                # Serve the customer dashboard
            
                
                session["permission"] = "user"
                
                return redirect(url_for('customer_dashboard'))

            elif user['user_type'] == 'booking_agent':
            # Serve the booking agent dashboard
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""(SELECT airline_name, permission FROM booking_agent WHERE username = %s) """,
                (session['username']))
                userinfo = cursor.fetchone()
                session["airline"]= userinfo['airline_name']
                session["permission"] = "user"
                conn.commit()
                cursor.close()
                return redirect(url_for('booking_agent_dashboard'))
            
        else:
            return "Invalid username or password."
    return render_template('main-login.html', form=form)

@app.route('/logout')
def logout():
    # Add your code here to logout the user
    session.clear()
    return redirect(url_for('login'))



@app.route('/login/airline_staff_dashboard')
def airline_staff_dashboard():
    # Add your code here to handle the airline staff dashboard functionality
    username = session.get('username')

    return render_template('airline-staff/airline-staff-dashboard.html', username=username)
    # Import necessary libraries

    # ...
@app.route('/login/customer_dashboard')
def customer_dashboard():
    # Add your code here to handle the airline staff dashboard functionality
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403

    return render_template('customer/customer-dashboard.html', username=username)

@app.route('/login/booking_agent_dashboard')
def booking_agent_dashboard():
    # Add your code here to handle the airline staff dashboard functionality
    username = session.get('username')

    return render_template('booking-agent/booking-agent-dashboard.html', username=username)

class ViewFlightsForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ViewFlightsForm, self).__init__(*args, **kwargs)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT airport_name, city FROM airport")
        city_list = cursor.fetchall()
        cursor.close()
        conn.commit()
    
        
        city_choices = [(city['airport_name'], city['airport_name'] + ', ' + city['city']) for city in city_list]
        city_choices.insert(0, ('', 'Select a city'))  # Add an empty choice at the beginning
        self.depart_from.choices = city_choices
        self.arrive_at.choices = city_choices

    depart_from = SelectField('Depart From', validators=[validators.InputRequired()])
    arrive_at = SelectField('Arrive At', validators=[validators.InputRequired()])
    start_date = DateField('Start Date', default=datetime.now().date(), format='%Y-%m-%d',validators=[validators.Optional()])
    end_date = DateField('End Date', default=(datetime.now().date() + timedelta(days=30)), format='%Y-%m-%d',validators=[validators.Optional()])
    Submit = SubmitField('Submit')


# Define a route to view flights
@app.route('/login/airline_staff_dashboard/view_flights/user/<username>', methods=['GET','POST'])
def view_flights(username):
        # Check if the user has the necessary permission
        if not session.get('permission') == 'admin':
            return "Unauthorized", 403
        form = ViewFlightsForm()
       
        # Get the airline staff's username
       
        print(datetime.now().date())
       
        if form.validate_on_submit() and request.method == 'POST':
           
                if form.start_date.data > form.end_date.data:
                    return "Invalid date range"
                else:

                    

                    start_date = form.start_date.data
                    end_date = form.end_date.data
                    
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("(SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND arrival_date = %s AND Departure_Airport = %s AND Arrival_Airport = %s)", (session.get('airline'), start_date,end_date,end_date,form.depart_from.data,form.arrive_at.data))
                    
                    flights = cursor.fetchall()
                    conn.commit()
                    cursor.close()
                
                    return render_template('airline-staff/view-flights.html', flights=flights,form = form,username = username)
        else:
                
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=30)
                status = 'upcoming'
                    
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND Status = %s", (session.get('airline'), start_date, end_date,status))
                flights = cursor.fetchall()
                conn.commit()
                cursor.close()
                return render_template('view-flights.html', flights=flights,form = form,username = username)
            

class CreateFlightForm(Form):
    flight_num = StringField('Flight Number', [validators.Length(min=1, max=25),validators.InputRequired()])
    airline_name = StringField('Airline Name', [validators.Length(min=1, max=25),validators.InputRequired()])

    departure_airport = StringField('Departure Airport', [validators.Length(min=1, max=25),validators.InputRequired()])

    departure_time = DateField('Departure Time', [validators.InputRequired()])

    arrival_airport = StringField('Arrival Airport', [validators.Length(min=1, max=25),validators.InputRequired()])

    arrival_time = DateField('Arrival Time', [validators.InputRequired()])

    price = StringField('Price', [validators.Length(min=1, max=25),validators.InputRequired()])

    status = StringField('Status', [validators.Length(min=1, max=25),validators.InputRequired()])

    airplane_id = StringField('Airplane ID', [validators.Length(min=1, max=25),validators.InputRequired()])

    submit = SubmitField('Submit')


    # Define a route to create new flights
@app.route('/create_flight', methods=['GET', 'POST'])
def create_flight():
        # Check if the user has the necessary permission
        if not session.get('permission') == 'admin':
            return "Unauthorized", 403

        # Handle the form submission to create a new flight
        if request.method == 'POST':
            # Process the form data and create a new flight
            # ...

            return redirect(url_for('view_flights'))

        return render_template('create_flight.html')

class changeflightstatus(Form):
    flight_num = StringField('Flight Number', [validators.Length(min=1, max=25),validators.InputRequired()])
    airline_name = StringField('Airline Name', [validators.Length(min=1, max=25),validators.InputRequired()])
    status = RadioField('Status', [validators.Length(min=1, max=25),validators.InputRequired()])
    # Define a route to change the status of flights
@app.route('/change_flight_status', methods=['GET', 'POST'])
def change_flight_status():
        # Check if the user has the necessary permission
        if not session.get('permission') == 'admin':
            return "Unauthorized", 403

        # Handle the form submission to change the flight status
        if request.method == 'POST':
            # Process the form data and update the flight status
            # ...

            return redirect(url_for('view_flights'))

        return render_template('change_flight_status.html')

class SearchPassengerForm(FlaskForm):
    flight_num = StringField('Flight Number', [validators.Length(min=1, max=25),validators.InputRequired()])
    submit = SubmitField('Submit')

@app.route('/login/airline_staff_dashboard/passenger_list/user/<username>', methods=['GET','POST'])
def passenger_list(username):
    print(session.get('permission'))
    if not session.get('permission') == 'admin' and not session.get('permission') == 'staff':
            return "Unauthorized", 403
    search_form = SearchPassengerForm()
    airline_name = session.get('airline')

    if request.method == 'POST' and search_form.validate_on_submit():
        print("entered")
        print(search_form.flight_num.data)
        print(session.get('airline'))
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT * FROM ticket WHERE airline_name = %s AND flight_number = %s""",
        (airline_name, search_form.flight_num.data))
        passengers = cursor.fetchall()
        print(passengers)
        conn.commit()
        cursor.close()
        return render_template('airline-staff/passenger-list.html',search_form=search_form,username=username, passengers=passengers)
    else:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT * FROM ticket WHERE airline_name = %s""",
        (airline_name,))
        passengers = cursor.fetchall()
        conn.commit()
        cursor.close()
        return render_template('airline-staff/passenger-list.html',search_form=search_form,username=username, passengers=passengers)


class AirRadioForm(FlaskForm):
    asset = RadioField('Select Asset:', choices=[('airport','Airport'), ('flight','Flight'), ('airplane','Airplane')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/login/airline_staff_dashboard/register_air/user/<username>', methods=['GET', 'POST'])
def register_air(username):
    if not session.get('permission') == 'admin':
            return "Unauthorized", 403
    if username is None:
        return "Unauthorized", 403
    air_form = AirRadioForm()
    if air_form.validate_on_submit() and request.method == 'POST':
        print("we are here everyoen")
        if air_form.asset.data == 'airport':
            return redirect(url_for('add_airport',username= username))
        elif air_form.asset.data == 'flight':
            return redirect(url_for('create_flight',username= username))
        elif air_form.asset.data == 'airplane':
            return redirect(url_for('add_airplane',username= username))
    return render_template('airline-staff/register-air.html', air_form=air_form,username=username)

class AddFlight(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ViewFlightsForm, self).__init__(*args, **kwargs)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT airport_name, city FROM airport")
        city_list = cursor.fetchall()
        cursor.close()
        conn.commit()
    
        
        city_choices = [(city['airport_name'], city['airport_name'] + ', ' + city['city']) for city in city_list]
        city_choices.insert(0, ('', 'Select a city'))  # Add an empty choice at the beginning
        self.depart_from.choices = city_choices
        self.arrive_at.choices = city_choices

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT  Airplane_ID a FROM Airplane where airline_name = %s",(session.get('airline'),))

        plane_list = cursor.fetchall()
        self.airplane_id.choices = [(plane['Airplane_id'], plane['Airplane_id']) for plane in plane_list]
        self.airplane_id.choices.insert(0, ('', 'Select a plane'))  # Add an empty choice at the beginning
        cursor.close()
        conn.commit()

    Flight_number = StringField('Flight Number', [validators.Length(min=1, max=25),validators.InputRequired()])

    depart_from = SelectField('Depart From', validators=[validators.InputRequired()])
    departure_date_time = DateTimeField('Start Date', default=datetime.now().date(), format='%Y-%m-%d',validators=[validators.Optional()])
    arrive_at = SelectField('Arrive At', validators=[validators.InputRequired()])
    
    arrival_date_time = DateTimeField('End Date', default=(datetime.now().date() + timedelta(days=30)), format='%Y-%m-%d',validators=[validators.Optional()])

    airplane_id = SelectField('Airplane ID', validators=[validators.InputRequired()])

    price = StringField('Price', [validators.Length(min=1, max=25),validators.InputRequired()])
    
    Submit = SubmitField('Submit')

@app.route('/login/airline_staff_dashboard/register_air/create_flight/user/<username>', methods=['GET','POST'])
def add_flight(username):

    if not session.get('permission') == 'admin':
            return "Unauthorized", 403
    form = AddFlight()
    if request.method == 'POST' and form.validate():
        print("i go sneakin sneakin sneakin")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM flight WHERE flight_number = %s AND airline_name = %s",
            (form.Flight_number.data,session.get('airline'))
        )
        existing_user = cursor.fetchone()
        if existing_user:
            return "Flight already exists"
        else:
            cursor.execute(
                """INSERT INTO flight(flight_number,airline_name,Arrival_airport,
                Arrival_City,
                Arrival_Date,Departure_Airport,Departure_city,
                Departure_date,
                Departure_hr,
                Departure_min,
                Arrival_hr,
                Arrival_min,
                Airplane_ID,
                price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    form.Flight_number.data,
                    session.get('airline'),
                    form.depart_from.data,
                    form.departure_date_time.data,
                    form.arrive_at.data,
                    form.arrival_date_time.data,
                    form.airplane_id.data,
                    form.price.data
                )
            )
            conn.commit()
            cursor.close()
            return "Flight added successfully!"
    print(form.errors)








class AddAirPlaneForm(FlaskForm):

    airplane_id = StringField('Airplane ID', [validators.Length(min=1, max=25),validators.InputRequired()])
    submit = SubmitField('Submit')

@app.route('/login/airline_staff_dashboard/register_air/add_airplane/user/<username>', methods=['GET', 'POST'])
def add_airplane(username):
    if not session.get('permission') == 'admin':
            return "Unauthorized", 403
    form = AddAirPlaneForm(request.form)
    if request.method == 'POST' and form.validate():
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM airplane WHERE airplane_id = %s",
            (form.airplane_id.data,)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            return "Airplane already exists"
        else:
            cursor.execute(
                "INSERT INTO airplane(airplane_id,airline_name) VALUES (%s, %s)",
                (
                    form.airplane_id.data,
                    session.get('airline')
                )
            )
            conn.commit()
            cursor.close()
            return "Airplane added successfully!"
    print(form.errors)
    return render_template('airline-staff/add-airplane.html', form=form)





class AddAirPortForm(FlaskForm):
    airport_name = StringField('Airport Name', [validators.Length(min=1, max=25),validators.InputRequired()])
    city = StringField('City', [validators.Length(min=1, max=25),validators.InputRequired()])
    submit = SubmitField('Submit')
    
@app.route('/login/airline_staff_dashboard/register_air/add_airport/user/<username>', methods=['GET', 'POST'])
def add_airport(username):
    form = AddAirPortForm(request.form)
    if not session.get('permission') == 'admin':
            return "Unauthorized", 403
    if request.method == 'POST' and form.validate():
        print("i go sneakin sneakin sneakin")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Airport_name FROM airport WHERE airport_name = %s",
            (form.airport_name.data,)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            return "Airport already exists"
        else:
            cursor.execute(
                "INSERT INTO airport(Airport_name, City) VALUES (%s, %s)",
                (
                    form.airport_name.data,
                    form.city.data
                )
            )
            conn.commit()
            cursor.close()
            return "Airport added successfully!"
    print(form.errors)
    return render_template('airline-staff/add-airport.html', form=form)






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
    def hash_password(password):
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
            "SELECT * FROM airline_staff WHERE Username = %s",
            (form.username.data,)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            return "User already exists"
        else:
            cursor.execute(
                "INSERT INTO airline_staff(Airline_name, username, first_name, last_name, password, DOB) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    form.airline_name.data,
                    form.username.data,
                    form.first_name.data,
                    form.last_name.data,
                    form.hash_password(form.password.data),
                    form.dob.data
                )
            )
            conn.commit()
            cursor.close()
            return "Airline staff registered successfully!"
    return render_template('airline-staff/airline-staff-reg.html', form=form)

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

    passport_expiry = DateField('Passport Expiry', [validators.InputRequired()],format='%Y-%m-%d')
    phone_number = StringField('Phone Number', [validators.Length(min=1, max=25), validators.Optional()])

    @staticmethod
    def hash_password(password):
        """
        Hashes the given password using the generate_password_hash function from werkzeug.security.

        :param password: The password to be hashed.
        :return: The hashed password.
        """
        return generate_password_hash(password,method='scrypt')


@app.route('/register/register_customer', methods=['GET', 'POST'])
def register_customer():
    form = CustomerRegisterForm(request.form)
    
    if request.method == 'POST' and form.validate() and form.password.data == form.confirm_password.data:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer WHERE email = %s", (form.email.data,))
        existing_user = cursor.fetchone()
        if existing_user:
            return "User already exists"
        else:
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


    return render_template('customer/customer-registration.html', form=form)

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


    @staticmethod
    def hash_password(password):
        """
        Hashes the given password using the generate_password_hash function from werkzeug.security.

        :param password: The password to be hashed.
        :return: The hashed password.
        """
        return generate_password_hash(password)
@app.route('/register/register_booking_agent', methods=['GET', 'POST'])
def register_booking_agent():
    form = BookingAgentRegisterForm(request.form)
    if request.method == 'POST' and form.validate() and form.password.data == form.confirm_password.data:
        cursor = conn.cursor()
        cursor.execute("select * from booking_agent where booking_agent_id = %s", (form.booking_agent_id.data,))
        existing_user = cursor.fetchone()
        if existing_user:
            return "User already exists"
        else:
            cursor.execute(
                "INSERT INTO booking_agent(booking_agent_id, airline_name, email, password) VALUES (%s, %s, %s, %s)",
                (
                    form.booking_agent_id.data,
                    form.airline_name.data,
                    form.email.data,
                    form.hash_password(form.password.data),
                    
                )
            )
        conn.commit()
        cursor.close()
        
        print("entered")
        return "Booking Agent registered successfully!"


    return render_template('booking-agent-reg.html', form=form)


@app.route('/login/purchase_tickets')
def purchase_tickets():
    # Implement logic to allow the customer to purchase tickets
    # You may need to integrate with a payment gateway and update the database accordingly
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403
    
    return render_template('customer/purchase-tickets.html', username=username)

# New route for searching flights
@app.route('/login/search_flights')
def search_flights():
    # Implement logic to search for upcoming flights based on user input
    # You may need to query your database for available flights
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403
    
    return render_template('customer/search-flights.html', username=username)

# New route for tracking spending
@app.route('/login/track_spending')
def track_spending():
    # Implement logic to track spending, retrieve and display spending data
    # You may need to query your database for spending information
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403
    
    return render_template('customer/track-spending.html', username=username)

class CustomerViewFlights(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(CustomerViewFlights, self).__init__(*args, **kwargs)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT airport_name, city FROM airport")
        city_list = cursor.fetchall()
        cursor.close()
        conn.commit()
    
        
        city_choices = [(city['airport_name'], city['airport_name'] + ', ' + city['city']) for city in city_list]
        city_choices.insert(0, ('', 'Select a city'))  # Add an empty choice at the beginning
        self.depart_from.choices = city_choices
        self.arrive_at.choices = city_choices

    depart_from = SelectField('Depart From', validators=[validators.InputRequired()])
    arrive_at = SelectField('Arrive At', validators=[validators.InputRequired()])
    start_date = DateField('Start Date', default=datetime.now().date(), format='%Y-%m-%d',validators=[validators.Optional()])
    end_date = DateField('End Date', default=(datetime.now().date() + timedelta(days=30)), format='%Y-%m-%d',validators=[validators.Optional()])
    Submit = SubmitField('Submit')

@app.route('/login/customer_dashboard/customer_view_flights/user/<username>', methods=['GET','POST'])
def customer_view_flights(username):
        username = session.get('username')

        # Check if the user has the necessary permission
        if not session.get('permission') == 'user':
            return "Unauthorized", 403
        form = CustomerViewFlights()
       
        # Get the airline staff's username
       
        print(datetime.now().date())
       
        if form.validate_on_submit() and request.method == 'POST':
           
                if form.start_date.data > form.end_date.data:
                    return "Invalid date range"
                else:
                    start_date = form.start_date.data
                    end_date = form.end_date.data
                    
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("(SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND arrival_date = %s AND Departure_Airport = %s AND Arrival_Airport = %s)", (session.get('airline'), start_date,end_date,end_date,form.depart_from.data,form.arrive_at.data))
                    
                    flights = cursor.fetchall()
                    conn.commit()
                    cursor.close()
                
                    return render_template('customer/customer-view-flights.html', flights=flights,form = form,username = username)
        else:
                
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=30)
                status = 'upcoming'
                    
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND Status = %s", (session.get('airline'), start_date, end_date,status))
                flights = cursor.fetchall()
                conn.commit()
                cursor.close()
                return render_template('customer/customer-view-flights.html', flights=flights,form = form,username = username)
            






# Set the secret key for the app
app.secret_key = '123456'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.config['WTF_CSRF_ENABLED'] = True
    app.run('127.0.0.1', 5000, debug=True, use_reloader=False)
