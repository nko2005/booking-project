# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:24:24 2023 by Nawaf

This script is a Flask web application that handles user login functionality.
"""
#import necessary libraries test
from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm 
import mysql.connector 
from wtforms import DateField, DateTimeField, Form, RadioField, StringField, PasswordField, SubmitField, validators, SelectField, IntegerField
from werkzeug.security import generate_password_hash 
from werkzeug.security import check_password_hash 
from wtforms.validators import DataRequired, Email, Length, InputRequired, Regexp, Optional
from datetime import datetime, timedelta
import ast
import uuid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# Initialize the app from Flask
app = Flask(__name__)#forms for flask
#
#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password ="",
                               database='booking', port = 3307)
@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html')
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
        user = None
        if form.username.data:
            cursor.execute("SELECT username,password,'airline_staff' as user_type FROM airline_staff WHERE username = %s", (form.username.data,))
            user = cursor.fetchone()
            session['username'] = form.username.data

        if not user and form.email.data:
            cursor.execute("SELECT Email,password,'customer' as user_type FROM customer WHERE Email = %s", (form.email.data,))
            user = cursor.fetchone()
            session['username'] = form.email.data

        if not user and form.agentID.data:
            print(form.agentID.data)
            cursor.execute("SELECT Email,booking_agent_id,password, 'booking_agent' as user_type FROM booking_agent WHERE booking_agent_id = %s", (form.agentID.data,))
            user = cursor.fetchone()
            session['username'] = form.agentID.data
            

        print("found agent",user)  # Print the user information
        # Check if the user exists and the password is correct
        conn.commit()
        cursor.close()
        if user and form.check_password(user['password']):
            # If the user exists and the password is correct, store the username in a session
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
                print("booking agent stuff",session['username'])
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""SELECT airline_name, Email FROM booking_agent WHERE Booking_agent_ID = %s """,
                (session['username'],))
                userinfo = cursor.fetchone()
                print(userinfo)
                session["airline"]= userinfo['airline_name']
                session["permission"] = "user"
                session["email"] = userinfo['Email']
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



@app.route('/login/airline_staff_dashboard', methods=['GET', 'POST'])
def airline_staff_dashboard():
    # Add your code here to handle the airline staff dashboard functionality
    username = session.get('username')

    return render_template('airline-staff/airline-staff-dashboard.html', username=username)
    # Import necessary libraries

    # ...


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

@app.route('/login/customer_dashboard')
def customer_dashboard():
    # Add your code here to handle the airline staff dashboard functionality
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403
    
    
    return render_template('customer/customer-dashboard.html',username=username)

@app.route('/login/booking_agent_dashboard', methods=['GET', 'POST'])
def booking_agent_dashboard():
    # Add your code here to handle the airline staff dashboard functionality
    email = session.get('email')

    return render_template('booking-agent/booking-agent-dashboard.html', email=email)

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
@app.route('/login/airline_staff_dashboard/view_flights', methods=['GET','POST'])
def view_flights():
        # Check if the user has the necessary permission
        if not session.get('permission') == 'admin':
            return "Unauthorized", 403
        form = ViewFlightsForm()
       
        # Get the airline staff's username
       
        print(datetime.now().date())
       
        if request.method == 'POST':
                if form.start_date.data is None or form.end_date.data is None:  
                     start_date = datetime.now().date()
                     end_date = start_date + timedelta(days=30) 
                     form.start_date.data = start_date
                     form.end_date.data = end_date

                
                if form.start_date.data is not None and  form.end_date.data is not None and form.start_date.data > form.end_date.data:
                    return "Invalid date range"
                
                if form.validate_on_submit(): 
                        start_date = form.start_date.data
                        end_date = form.end_date.data

                        
                        cursor = conn.cursor(dictionary=True)
                        cursor.execute("(SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s  AND Departure_Airport = %s AND Arrival_Airport = %s)", (session.get('airline'), start_date,end_date,form.depart_from.data,form.arrive_at.data))
                        
                        flights = cursor.fetchall()
                        conn.commit()
                        cursor.close()
                    
                        return render_template('airline-staff/view-flights.html', flights=flights,form = form)
                else:
                
                    start_date = datetime.now().date()
                    end_date = start_date + timedelta(days=30)
                    status = 'upcoming'
                        
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND Status = %s", (session.get('airline'), start_date, end_date,status))
                    flights = cursor.fetchall()
                    conn.commit()
                    cursor.close()
                    return render_template('airline-staff/view-flights.html', flights=flights,form = form)
        
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30)
        status = 'upcoming'
                    
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND Status = %s", (session.get('airline'), start_date, end_date,status))
        flights = cursor.fetchall()
        conn.commit()
        cursor.close()
        return render_template('airline-staff/view-flights.html', flights=flights,form = form)
        
@app.route('/login/airline_staff_dashboard/view_staff', methods=['GET','POST'])
def view_staff():
    # Check if the user has the necessary permission
    if not session.get('permission') == 'admin':
        return "Unauthorized", 403
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM airline_staff WHERE airline_name = %s", (session.get('airline'),))
    staffs = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('airline-staff/view-staff.html', staffs=staffs)     








class ChangeStaffStatusForm(FlaskForm):
    status = RadioField('Status', choices=[('staff','Staff'), ('admin','Admin')], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/change_staff_status/<username>', methods=['GET', 'POST'])
def change_staff_status(username):
        # Check if the user has the necessary permission
        if not session.get('permission') == 'admin':
            return "Unauthorized", 403
        print("da user is ",username)
        form = ChangeStaffStatusForm()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM airline_staff WHERE Username = %s", (username,))
        staff = cursor.fetchone()
        print(staff)
        # Handle the form submission to change the flight status
        if request.method == 'POST' and form.validate_on_submit():
            # Process the form data and update the flight status
            # ...
            new_status = form.status.data
            cursor.execute("UPDATE airline_staff SET permission = %s WHERE username = %s", (new_status, username))
            conn.commit()
            cursor.close()

            return redirect(url_for('view_staff'))
        conn.commit()
        cursor.close()
        return render_template('airline-staff/change-staff-status.html', staff=staff,form = form)
     
     







     
class ChangeFlightStatusForm(FlaskForm):
    status = RadioField('Status', choices=[('upcoming','Upcoming'), ('delayed','Delayed'), ('cancelled','Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Submit')
    # Define a route to change the status of flights
@app.route('/change_flight_status/<flight_num>', methods=['GET', 'POST'])
def change_flight_status(flight_num):
        # Check if the user has the necessary permission
        if not session.get('permission') == 'admin':
            return "Unauthorized", 403
        print(flight_num)
        form = ChangeFlightStatusForm()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM flight WHERE flight_number = %s", (flight_num,))
        flight = cursor.fetchone()
        print(flight)
        # Handle the form submission to change the flight status
        if request.method == 'POST' and form.validate_on_submit():
            # Process the form data and update the flight status
            # ...
            new_status = form.status.data
            cursor.execute("UPDATE flight SET status = %s WHERE flight_number = %s", (new_status, flight_num))
            conn.commit()
            cursor.close()

            return redirect(url_for('view_flights'))
        conn.commit()
        cursor.close()
        return render_template('airline-staff/change-flight-status.html', flight=flight,form = form)

class SearchPassengerForm(FlaskForm):
    flight_num = StringField('Flight Number', [validators.Length(min=1, max=25),validators.InputRequired()])
    submit = SubmitField('Submit')

@app.route('/login/airline_staff_dashboard/passenger_list/', methods=['GET','POST'])
def passenger_list():
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
        return render_template('airline-staff/passenger-list.html',search_form=search_form, passengers=passengers)
    else:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT * FROM ticket WHERE airline_name = %s""",
        (airline_name,))
        passengers = cursor.fetchall()
        conn.commit()
        cursor.close()
        return render_template('airline-staff/passenger-list.html',search_form=search_form, passengers=passengers)





class AgentRadioForm(FlaskForm):
    action = RadioField('Select Action:', choices=[('view','View Agents'), ('register','Register Agent')], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/login/airline_staff_dashboard/agent_actions', methods=['GET', 'POST'])
def agent_actions():
     

    if not session.get('permission') == 'admin':
                return "Unauthorized", 403
    form = AgentRadioForm()
    if form.validate_on_submit() and request.method == 'POST':
            print("we are here everyoen")
            if form.action.data == 'view':
                return redirect(url_for('view_agents'))
            elif form.action.data == 'register':

                return redirect(url_for('register_booking_agent'))

    return render_template('airline-staff/agent-actions.html', form=form)

class BookingAgentRegisterForm(Form):
    
    booking_agent_id = StringField('Booking Agent ID', [validators.Length(min=1, max=25),validators.InputRequired()])

    email = StringField('Email', [validators.Email(message='Invalid email'), validators.Optional()])


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
@app.route('/login/airline_staff_dashboard/agent_actions/register_booking_agent', methods=['GET','POST'])
def register_booking_agent():

    if not session.get('permission') == 'admin':
            return "Unauthorized", 403
    
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
                    session.get('airline'),
                    form.email.data,
                    form.hash_password(form.password.data),
                    
                )
            )
        conn.commit()
        cursor.close()
        
        print("entered")
        return "Booking Agent registered successfully!"


    return render_template('booking-agent/booking-agent-reg.html', form=form)


@app.route('/login/airline_staff_dashboard/agent_actions/view_agents', methods=['GET', 'POST'])
def view_agents():
    if not session.get('permission') == 'admin':
            return "Unauthorized", 403
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT booking_agent.Booking_agent_ID,booking_agent.Airline_Name,booking_agent.Email, SUM(Flight.Price*0.15) as commission
                   FROM booking_agent,Ticket,Flight
                   WHERE booking_agent.Airline_Name = %s AND booking_agent.Email = Ticket.Booking_Agent_Email AND Ticket.Flight_Number = Flight.Flight_number
                   Group by booking_agent.Email
                   Order by commission DESC""", (session.get('airline'),))
    agents = cursor.fetchall()
    print("the agents", agents)
    conn.commit()
    cursor.close()
    return render_template('airline-staff/view-agents.html', agents=agents)




















class AirRadioForm(FlaskForm):
    asset = RadioField('Select Asset:', choices=[('airport','Airport'), ('flight','Flight'), ('airplane','Airplane')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/login/airline_staff_dashboard/register_air/', methods=['GET', 'POST'])
def register_air():
    if not session.get('permission') == 'admin':
            return "Unauthorized", 403
    air_form = AirRadioForm()
    if air_form.validate_on_submit() and request.method == 'POST':
        if air_form.asset.data == 'airport':
            return redirect(url_for('add_airport'))
        elif air_form.asset.data == 'flight':
            return redirect(url_for('add_flight'))
        elif air_form.asset.data == 'airplane':
            return redirect(url_for('add_airplane'))
    return render_template('airline-staff/register-air.html', air_form=air_form)

class AddFlightForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(AddFlightForm, self).__init__(*args, **kwargs)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT airport_name, city FROM airport")
        city_list = cursor.fetchall()
        
    
        
        city_choices = [((city['airport_name'],city['city']), city['airport_name'] + ', ' + city['city']) for city in city_list]
        city_choices.insert(0, ('', 'Select a city'))  # Add an empty choice at the beginning
        self.depart_from.choices = city_choices
        self.arrive_at.choices = city_choices

       
        cursor.execute("SELECT  Airplane_ID FROM Airplane where airline_name = %s",(session.get('airline'),))

        plane_list = cursor.fetchall()
      
        plane_choices = [(plane['Airplane_ID'], plane['Airplane_ID']) for plane in plane_list]
        self.airplane_id.choices = plane_choices
        print("resulting:",self.airplane_id.choices)
        self.airplane_id.choices.insert(0, ('', 'Select a plane'))  # Add an empty choice at the beginning
        cursor.close()
        conn.commit()

    Flight_number = StringField('Flight Number', [validators.Length(min=1, max=25),validators.InputRequired()])

    depart_from = SelectField('Depart From', validators=[validators.InputRequired()])
    departure_date_time = DateTimeField('Start Date', default=datetime.now(),validators=[validators.Optional()],format = '%Y-%m-%dT%H:%M')
    arrive_at = SelectField('Arrive At', validators=[validators.InputRequired()])
    
    arrival_date_time = DateTimeField('End Date', default=(datetime.now() + timedelta(days=30)),validators=[validators.Optional()],format = '%Y-%m-%dT%H:%M')

    airplane_id = SelectField('Airplane ID', validators=[validators.InputRequired()])

    price = StringField('Price', [validators.Length(min=1, max=25),validators.InputRequired()])
    
    Submit = SubmitField('Submit')

@app.route('/login/airline_staff_dashboard/register_air/add_flight/', methods=['GET','POST'])
def add_flight():
    

    if not session.get('permission') == 'admin':
            return "Unauthorized", 403
    form = AddFlightForm(request.form)
    print("Departure date and time:", form.departure_date_time.data)
    print("Arrival date and time:", form.arrival_date_time.data)

    if request.method == 'POST':
        arrival_date_time = form.arrival_date_time.data = datetime.strptime(request.form['arrival_date_time'], '%Y-%m-%dT%H:%M')
        departure_date_time = form.departure_date_time.data = datetime.strptime(request.form['departure_date_time'], '%Y-%m-%dT%H:%M')  

        if arrival_date_time.date() < datetime.now().date() or departure_date_time.date() < datetime.now().date():
            return "Date cannot be before today"

        if form.validate(): 
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM flight WHERE flight_number = %s AND airline_name = %s",
                (form.Flight_number.data,session.get('airline'))
            )
            existing_flight = cursor.fetchone()
            if existing_flight:
                return "Flight already exists"
            else:
              
                print("the tuple",form.arrive_at.data)
               
                arrival_data = ast.literal_eval(form.arrive_at.data)
                arrival_airport = arrival_data[0]
                arrival_city = arrival_data[1]
                #arrival_airport = arrival_airport.strip()


                departure_data = ast.literal_eval(form.depart_from.data)
                departure_airport = departure_data[0]
                departure_city = departure_data[1]
                #departure_airport = departure_airport.strip()
                print("Departure airport:", departure_airport)
                print("Arrival airport:", arrival_airport)

                dep_hour, dep_minute = map(int, form.departure_date_time.data.strftime('%H:%M').split(':'))
                arr_hour, arr_minute = map(int, form.arrival_date_time.data.strftime('%H:%M').split(':'))
                cursor.execute("SELECT Seats FROM airplane WHERE Airplane_ID = %s", (form.airplane_id.data,))
                seats = cursor.fetchone()

                cursor.execute(
                    """INSERT INTO flight(
                    flight_number,
                    airline_name,
                    Arrival_Airport,
                    Arrival_City,
                    Arrival_Date,
                    Departure_Airport,
                    Departure_city,
                    Departure_date,
                    Departure_hr,
                    Departure_min,
                    Arrival_hr,
                    Arrival_min,
                    Airplane_ID,
                    price,
                    status,
                    Seats_Left
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,"Upcoming",%s)
                    """,
                    (
                        form.Flight_number.data,
                        session.get('airline'),
                        arrival_airport,
                        arrival_city,
                        arrival_date_time.date(),
                        departure_airport,
                        departure_city,
                        departure_date_time.date(),
                        dep_hour,
                        dep_minute,
                        arr_hour,
                        arr_minute,
                        form.airplane_id.data,
                        form.price.data,
                        seats['Seats']

                    )
                )
                conn.commit()
                cursor.close()
                return redirect(url_for('airline_staff_dashboard'))
        print(form.errors)

    return render_template('airline-staff/add-flight.html', form=form)








class AddAirPlaneForm(FlaskForm):

    airplane_id = StringField('Airplane ID', [validators.Length(min=1, max=25),validators.InputRequired()])
    Seat_capacity = IntegerField('Seat Capacity', [validators.NumberRange(min=1, max=25), validators.InputRequired()])
    submit = SubmitField('Submit')

@app.route('/login/airline_staff_dashboard/register_air/add_airplane', methods=['GET', 'POST'])
def add_airplane():
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
                "INSERT INTO airplane(airplane_id,airline_name,Seats) VALUES (%s, %s,%s)",
                (
                    form.airplane_id.data,
                    session.get('airline'),
                    form.Seat_capacity.data
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
    
@app.route('/login/airline_staff_dashboard/register_air/add_airport/', methods=['GET', 'POST'])
def add_airport():
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
    role = RadioField('Role', choices=[('customer','Customer'), ('airline_staff','Airline Staff')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RoleForm()
    if form.validate_on_submit():
        if form.role.data == 'customer':
            return redirect(url_for('register_customer'))
        elif form.role.data == 'airline_staff':
            return redirect(url_for('register_airline_staff'))
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
                "INSERT INTO airline_staff(Airline_name, username, first_name, last_name, password, DOB, permission) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    form.airline_name.data,
                    form.username.data,
                    form.first_name.data,
                    form.last_name.data,
                    form.hash_password(form.password.data),
                    form.dob.data,
                    'staff',
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





# New route for searching flights





@app.route('/login/search_flights', methods=['GET', 'POST'])
def search_flights():
    # Check if the user has the necessary permission
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403

    form = CustomerViewFlights()


    print(datetime.now().date())
       
    if request.method == 'POST':
            if form.start_date.data is None or form.end_date.data is None:  
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=30) 
                form.start_date.data = start_date
                form.end_date.data = end_date

                    
            if form.start_date.data is not None and  form.end_date.data is not None and form.start_date.data > form.end_date.data:
                return "Invalid date range"
                    
            if form.validate_on_submit(): 
                start_date = form.start_date.data
                end_date = form.end_date.data

                            
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                SELECT * FROM flight
                WHERE departure_date BETWEEN %s AND %s
                AND Departure_Airport = %s
                AND Arrival_Airport = %s
            """,(start_date,end_date,form.depart_from.data,form.arrive_at.data))   
                flights = cursor.fetchall()
                conn.commit()
                cursor.close()
                        
                return render_template('customer/search-flights.html', flights=flights, form=form, username=username)
            
            else:
                    
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=30)
                status = 'upcoming'
                            
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                SELECT * FROM flight
                WHERE departure_date BETWEEN %s AND %s
                AND Departure_Airport = %s
                AND Arrival_Airport = %s
            """,(start_date,end_date,form.depart_from.data,form.arrive_at.data))
                flights = cursor.fetchall()
                conn.commit()
                cursor.close()
                return render_template('customer/search-flights.html', flights=flights, form=form, username=username)
        
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30)
    status = 'upcoming'
                    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                SELECT * FROM flight
                WHERE departure_date BETWEEN %s AND %s
                AND Departure_Airport = %s
                AND Arrival_Airport = %s
            """,(start_date,end_date,form.depart_from.data,form.arrive_at.data))
    flights = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('customer/search-flights.html', flights=flights, form=form, username=username)


class PurchaseTicket(FlaskForm):
    #status = RadioField('Status', choices=[('upcoming','Upcoming'), ('delayed','Delayed'), ('cancelled','Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/login/purchase_flight_ticket/<flight_num>', methods=['GET', 'POST'])
def purchase_flight_ticket(flight_num):
    # Check if the user has the necessary permission
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403
    print(flight_num)
    form = PurchaseTicket()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM flight WHERE flight_number = %s", (flight_num,))

    flight = cursor.fetchone()
    print(flight)
    cursor.execute("SELECT Seats FROM Airplane WHERE Airplane_ID = %s ", (flight["Airplane_ID"],))
    seats = cursor.fetchone()
        # Handle the form submission to change the flight status
    
    if request.method == 'POST':
        ticket_id=str(uuid.uuid1())
        if flight["Seats_Left"]==0:
            return "No seats left"
        

        cursor.execute("INSERT INTO ticket(Ticket_ID, Airline_name, Flight_Number, Customer_Email, Booking_Agent_Email, Purchase_date,Seat_Number) VALUES (%s,%s,%s,%s,%s,%s,%s)",(ticket_id, flight["Airline_name"], flight["Flight_number"],username, None, datetime.now().date(), seats["Seats"]-flight["Seats_Left"]+1))
        cursor.execute("UPDATE flight SET Seats_Left = Seats_Left - 1 WHERE flight_number = %s", (flight_num,))
        conn.commit()
        cursor.close()

        print('Ticket Purchased Successfully!')
        return redirect(url_for('customer_dashboard'))
    
    return render_template('customer/purchase-flight-ticket.html', username=username, form=form, flight=flight)
    
    
# New route for tracking spending
@app.route('/login/track_spending')
def track_spending():
    # Implement logic to track spending, retrieve and display spending data
    # You may need to query your database for spending information
    username = session.get('username')
    print(username)
    if session.get('permission') != 'user':
        return "Unauthorized", 403
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT 
        DATE_FORMAT(Ticket.Purchase_date, '%Y-%m') AS month, 
        SUM(Flight.Price) AS total_spent
    FROM 
        Ticket,Flight
    WHERE 
        Ticket.Customer_Email = %s and Flight.Flight_number = Ticket.Flight_Number
    GROUP BY 
        month
    ORDER BY 
        month
    """, (username,))

    monthly_spendings = cursor.fetchall()
    cursor.execute("""
    SELECT 
        SUM(Flight.Price) AS total_spent
    FROM 
        Ticket
    JOIN 
        Flight ON Flight.Flight_number = Ticket.Flight_Number
    WHERE 
        Ticket.Customer_Email = %s
    """, (username,))
    total_spendings = cursor.fetchone()
    

    print(total_spendings)

    months = [row['month'] for row in monthly_spendings]
    totals = [row['total_spent'] for row in monthly_spendings]
    plt.clf()
    plt.bar(months, totals)
    plt.xlabel('Month')
    plt.ylabel('Total Spent')
    plt.title('Monthly Spendings')
    plt.savefig('static/images/customer/spendings.png')

    return render_template('customer/track-spending.html', image_file='images/customer/spendings.png', total_spendings= total_spendings)



@app.route('/login/track_revenue')
def track_revenue():
    print(session.get('permission'))
    if session.get('permission') != 'staff' and session.get('permission') != 'admin':
        return "Unauthorized", 403
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT
        DATE_FORMAT(Ticket.Purchase_date, '%Y-%m') AS month,
        SUM(Flight.Price) AS total_revenue
    FROM
        Ticket,Flight
    WHERE
        Flight.Airline_name = %s and Flight.Flight_number = Ticket.Flight_Number and Ticket.Booking_Agent_Email is NULL
    GROUP BY
        month
    ORDER BY
        month
    """, (session.get('airline'),))
    direct_revenue = cursor.fetchall()
    cursor.execute("""
    SELECT
        DATE_FORMAT(Ticket.Purchase_date, '%Y-%m') AS month,
        SUM(Flight.Price-Flight.Price*0.15) AS total_revenue
    FROM
        Ticket,Flight
    WHERE
        Flight.Airline_name = %s and Flight.Flight_number = Ticket.Flight_Number and Ticket.Booking_Agent_Email is not NULL
    GROUP BY
        month
    ORDER BY
        month
    """, (session.get('airline'),))
    indirect_revenue = cursor.fetchall()
    cursor.execute("""
    SELECT
        SUM(Flight.Price) AS total_revenue
    FROM
        Ticket,Flight
    WHERE
        Flight.Airline_name = %s and Flight.Flight_number = Ticket.Flight_Number and Ticket.Booking_Agent_Email is NULL
    """, (session.get('airline'),))
    total_direct_revenue = cursor.fetchone()
    cursor.execute("""
    SELECT
        SUM(Flight.Price) AS total_revenue
    FROM
        Ticket,Flight
    WHERE
        Flight.Airline_name = %s and Flight.Flight_number = Ticket.Flight_Number and Ticket.Booking_Agent_Email is not NULL
    """, (session.get('airline'),))
    plt.clf()
    total_indirect_revenue = cursor.fetchone()
    months = [row['month'] for row in direct_revenue]
    direct_totals = [row['total_revenue'] for row in direct_revenue]
    indirect_totals = [row['total_revenue'] for row in indirect_revenue]
    plt.bar(months, direct_totals, label='Direct Revenue')
    plt.bar(months, indirect_totals, label='Indirect Revenue')
    plt.xlabel('Month')
    plt.ylabel('Total Revenue')
    plt.title('Monthly Revenue')
    plt.legend()
    plt.savefig('static/images/staff/revenue.png')
    return render_template('airline-staff/track-revenue.html', image_file='images/staff/revenue.png', total_direct_revenue=total_direct_revenue, total_indirect_revenue=total_indirect_revenue)





     
         
# New route for tracking spending
@app.route('/login/track_commission')
def track_commission():
    # Implement logic to track spending, retrieve and display spending data
    # You may need to query your database for spending information
   
    if session.get('permission') != 'user':
        return "Unauthorized", 403
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT 
        DATE_FORMAT(Ticket.Purchase_date, '%Y-%m') AS month, 
        SUM(Flight.Price*0.15) AS total_commission
    FROM 
        Ticket,Flight
    WHERE 
        Ticket.Booking_Agent_Email = %s and Flight.Flight_number = Ticket.Flight_Number
    GROUP BY 
        month
    ORDER BY 
        month
    """, (session.get('email'),))

    monthly_commissions = cursor.fetchall()
    cursor.execute("""
    SELECT 
        SUM(Flight.Price*0.15) AS total_commission
    FROM 
        Ticket
    JOIN 
        Flight ON Flight.Flight_number = Ticket.Flight_Number
    WHERE 
        Ticket.Booking_Agent_Email = %s
    """, (session.get('email'),))
    total_commissions = cursor.fetchone()
    

    print(total_commissions)

    months = [row['month'] for row in monthly_commissions]
    totals = [row['total_commission'] for row in monthly_commissions]
    plt.clf()
    plt.bar(months, totals)
    plt.xlabel('Month')
    plt.ylabel('Total Spent')
    plt.title('Monthly Spendings')
    plt.savefig('static/images/agent/commissions.png')

    return render_template('booking-agent/agent-my-commission.html', image_file='images/agent/commissions.png', total_commissions= total_commissions)
    
















@app.route('/login/customer_view_flights')
def customer_view_flights():
        username = session.get('username')

        # Check if the user has the necessary permission
        if not session.get('permission') == 'user':
            return "Unauthorized", 403
        form = CustomerViewFlights()
               
        cursor = conn.cursor(dictionary=True)
        cursor.execute("(SELECT * FROM flight NATURAL JOIN ticket WHERE Customer_Email=%s)",(username,))
                
        ticket_flights = cursor.fetchall()
        print(ticket_flights)
        conn.commit()
        cursor.close()
                
        return render_template('customer/customer-view-flights.html', ticket_flights=ticket_flights,form = form,username = username)
        







class AgentViewFlights(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(AgentViewFlights, self).__init__(*args, **kwargs)
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


@app.route('/login/booking_agent_view_flights')
def booking_agent_view_flights():
        email = session.get('email')

        # Check if the user has the necessary permission
        if not session.get('permission') == 'user':
            return "Unauthorized", 403
        form = AgentViewFlights()
               
        cursor = conn.cursor(dictionary=True)
        cursor.execute("(SELECT * FROM flight NATURAL JOIN ticket WHERE Booking_Agent_Email=%s)",(email,))
                
        ticket_flights = cursor.fetchall()
        print(ticket_flights)
        conn.commit()
        cursor.close()
                
        return render_template('booking-agent/booking-agent-view-flights.html', ticket_flights=ticket_flights,form = form,email = email)


@app.route('/login/booking_agent_search_flights', methods=['GET', 'POST'])
def booking_agent_search_flights():
    # Check if the user has the necessary permission
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403

    form = AgentViewFlights()
    print(session.get('airline'))

    print(datetime.now().date())
       
    if request.method == 'POST':
            if form.start_date.data is None or form.end_date.data is None:  
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=30) 
                form.start_date.data = start_date
                form.end_date.data = end_date

                    
            if form.start_date.data is not None and  form.end_date.data is not None and form.start_date.data > form.end_date.data:
                return "Invalid date range"
                    
            if form.validate_on_submit(): 
                start_date = form.start_date.data
                end_date = form.end_date.data

                            
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                SELECT * FROM flight
                WHERE departure_date BETWEEN %s AND %s
                AND Departure_Airport = %s
                AND Arrival_Airport = %s AND Airline_name = %s
            """,(start_date,end_date,form.depart_from.data,form.arrive_at.data,session.get('airline')))   
                flights = cursor.fetchall()
                conn.commit()
                cursor.close()
                        
                return render_template('booking-agent/booking-agent-search-flights.html', flights=flights, form=form, username=username)
            
            else:
                    
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=30)
                status = 'upcoming'
                            
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                SELECT * FROM flight
                WHERE departure_date BETWEEN %s AND %s
                AND Departure_Airport = %s
                AND Arrival_Airport = %s AND Airline_name = %s
            """,(start_date,end_date,form.depart_from.data,form.arrive_at.data,session.get('airline')))   
                flights = cursor.fetchall()
                conn.commit()
                cursor.close()
                return render_template('booking-agent/booking-agent-search-flights.html', flights=flights, form=form, username=username)
        
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30)
    status = 'upcoming'
                    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                SELECT * FROM flight
                WHERE departure_date BETWEEN %s AND %s
                AND Departure_Airport = %s
                AND Arrival_Airport = %s
            """,(start_date,end_date,form.depart_from.data,form.arrive_at.data))
    flights = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('booking-agent/booking-agent-search-flights.html', flights=flights, form=form, username=username)

class AgentPurchaseTicket(FlaskForm):
    Customer_Email = StringField('Customer_Email', [validators.InputRequired()])
    submit = SubmitField('Submit')




@app.route('/login/booking_agent_purchase_flights/<flight_num>', methods=['GET', 'POST'])
def booking_agent_purchase_flights(flight_num):
    # Check if the user has the necessary permission
    username = session.get('username')
    if session.get('permission') != 'user':
        return "Unauthorized", 403
    form = AgentPurchaseTicket()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM flight WHERE flight_number = %s", (flight_num,))

    flight = cursor.fetchone()
    print(flight)
    cursor.execute("SELECT Seats FROM Airplane WHERE Airplane_ID = %s ", (flight["Airplane_ID"],))
    seats = cursor.fetchone()
        # Handle the form submission to change the flight status
    
    if request.method == 'POST' and form.validate():
        ticket_id=str(uuid.uuid1())
        cursor.execute("SELECT * FROM customer WHERE email = %s", (form.Customer_Email.data,))
        existing_customer = cursor.fetchone()
        print(existing_customer)
        if not existing_customer['Email']:
             return "Invalid Customer Email"
        
        if flight["Seats_Left"]==0:
            return "No seats left"

        cursor.execute("INSERT INTO ticket(Ticket_ID, Airline_name, Flight_Number, Customer_Email, Booking_Agent_Email, Purchase_date,Seat_Number) VALUES (%s,%s,%s,%s, %s, %s)",(ticket_id, flight["Airline_name"], flight["Flight_number"],existing_customer['Email'],session.get('email'), datetime.now().date(), seats["Seats"]-flight["Seats_Left"]+1))
        conn.commit()
        cursor.close()
        print('Ticket Purchased Successfully!')
        return redirect(url_for('customer_dashboard'))
    
    return render_template('booking-agent/booking-agent-purchase-flights.html', username=username, form=form, flight=flight)
    



# Set the secret key for the app
app.secret_key = '123456'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.config['WTF_CSRF_ENABLED'] = True
    app.run('127.0.0.1', 5000, debug=True, use_reloader=False)
