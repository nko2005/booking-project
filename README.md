
# Flask Booking Project

This project is a Flask-based web application that implements user authentication and login functionality to create a larger and more complicated flight booking system.

## Installation

1. Clone the repository.
2. In the repository directory, create a virtual environment by running the following command:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - For Windows:
     ```bash
     venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required dependencies by running the following command:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database by running apache server in xampp and open phpmyadmin:

4. import the database using the ```booking.sql``` file 

5. Start the application by running the python file: ```web-script.py```


## Usage

1. Open your web browser and navigate to `http://localhost:5000/login`.
2. Register a new user account or log in with an existing account.
3. You can test the login using username "staff1" and password "password1"
   for now it only checks for airline staff 

## Dependencies

- Flask
- Flask-Login
- SQLAlchemy
- WTForms
- etc.

