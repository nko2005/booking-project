create table Airline(
    Airline_name varchar(20) not null,
    primary key (Airline_name)
);

create table Airline_Staff(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Airline_name varchar(20) not null,
    Username     varchar(15) not null UNIQUE, 
    first_name   varchar(20) not null, 
    last_name    varchar(20) not null, 
    password     varchar(255) not null,
    Dob          DATE, 
    permission   enum('admin','staff') DEFAULT NULL,
    foreign key (Airline_Name) references Airline(Airline_Name)
);

create table Airplane(
    Airplane_ID  varchar(15) not null,
    Airline_name varchar(20),
    Seats       numeric(3) not null,
    primary key (Airplane_ID),
    foreign key (Airline_Name) references Airline(Airline_Name)
);


create table Airport(
    Airport_name varchar(20) not null,
    City         varchar(20) not null,
    primary key (Airport_name)
);



create table Flight(
    Flight_number      varchar(8) not null,
    Airline_name       varchar(20) not null,
    Arrival_Airport    varchar(20) not null,
    Arrival_City       varchar(20) not null,
    Arrival_date       DATE not null,
    Departure_Airport  varchar(20) not null,
    Departure_City     varchar(20) not null,
    Departure_date     DATE not null,
    Departure_hr       numeric(2) check (Departure_hr >= 0 and Departure_hr < 24),
    Departure_min      numeric(2) check (Departure_min >= 0 and Departure_min < 60),
    Arrival_hr         numeric(2) check (Arrival_hr >= 0 and Arrival_hr < 24),
    Arrival_min        numeric(2) check (Arrival_min >= 0 and Arrival_min < 60),
    Airplane_ID        varchar(15),
    Price              DECIMAL(10, 2),
    Status             ENUM('Upcoming', 'Cancelled', 'Delayed', 'in-progress'),
    Seats_Left        numeric(3), 
    Primary Key (Flight_number),
    foreign key (Airline_Name) references Airline(Airline_Name),
    foreign key (Arrival_Airport) references Airport(Airport_name),
    foreign key (Departure_Airport) references Airport(Airport_name),
    foreign key (Airplane_ID) references Airplane(Airplane_ID)
);

create table Booking_Agent(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Booking_agent_ID  varchar(8) not null, 
    Airline_Name      varchar(20),
    Email             varchar(25) not null UNIQUE,
    Password          varchar(255), 
    foreign key (Airline_Name) references Airline(Airline_Name)
);

create table Customer(
    id INT AUTO_INCREMENT PRIMARY KEY,		
    first_name           varchar(20) not null, 
    last_name            varchar(20) not null, 
    Email                varchar(25) not null UNIQUE,
    Password             varchar(255) not null,
    Building             varchar(25),
    Building_no          varchar(7),
    Street               varchar(25),
    City                 varchar(25),
    Passport_expiration  DATE not null,
    phone_number         varchar(25)
);


create table Ticket(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Ticket_ID            varchar(8) not null UNIQUE,
    Airline_name         varchar(20) not NULL,
    Flight_Number        varchar(8) not null,
    Customer_Email       varchar(25) not null,
    Booking_Agent_Email  varchar(25),
    Purchase_date        DATE not null,
    Seat_Number          numeric(3) not null,   
    foreign key(Customer_Email) references Customer(Email),
    foreign key(Booking_Agent_Email) references Booking_Agent(Email),
    foreign key(Flight_Number) references Flight(Flight_number),
    foreign key(Airline_name) references Flight(Airline_name)
);



	
	
	
	
	


		
	
	