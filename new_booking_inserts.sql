insert into Airline (Airline_name) values ('Shanghai Global');

insert into Airplane (Airplane_ID, Airline_name) values ('454033', 'Shanghai Global');

INSERT INTO airplane (Airplane_ID, Airline_name) VALUES ('454034', 'Shanghai Global');
INSERT INTO airplane (Airplane_ID, Airline_name) VALUES ('454035', 'Shanghai Global');
INSERT INTO airplane (Airplane_ID, Airline_name) VALUES ('454036', 'Shanghai Global');

insert into Airline_Staff (Airline_name, Username, first_name, last_name, password, Dob,permission) values ('Shanghai Global', 'staff1', 'John', 'Doe', 'scrypt:32768:8:1$1dZCs1FKpfgdFlFu$4e34b3d2eda8b7118c7fbe7eb77573f690217dfcfa777916d4fc2cb528c054dbc80bcf44d583abdf9ac7c6be907edbdec0e82f062f9422453be097082632e8b9', '1980-01-01','admin');



insert into Airport (Airport_name, City) values ('JFK', 'New York');
insert into Airport (Airport_name, City) values ('PVG', 'Shanghai');

INSERT INTO Airport (Airport_name, City) VALUES ('LAX', 'Los Angeles');
INSERT INTO Airport (Airport_name, City) VALUES ('ORD', 'Chicago');
INSERT INTO Airport (Airport_name, City) VALUES ('SEA', 'Seattle');

insert into Flight (Flight_number, Airline_name, Arrival_Airport,Arrival_City,Arrival_date, Departure_Airport, Departure_City,Departure_date,Departure_hr, Departure_min, Arrival_hr, Arrival_min, Airplane_ID, Price, Status) values ('3443', 'Shanghai Global', 'JFK',"New York",'2023-12-02', 'PVG', "Shanghai","2023-12-01", 19, 30, 2, 30, '454033', 500, 'Upcoming');


INSERT INTO Flight (Flight_number, Airline_name, Arrival_Airport, Arrival_City, Arrival_date, Departure_Airport, Departure_City, Departure_date, Departure_hr, Departure_min, Arrival_hr, Arrival_min, Airplane_ID, Price, Status) 
VALUES ('3444', 'Shanghai Global', 'LAX', 'Los Angeles', '2023-12-02', 'PVG', 'Shanghai', '2023-12-01', 20, 30, 3, 30, '454034', 600, 'Upcoming');

INSERT INTO Flight (Flight_number, Airline_name, Arrival_Airport, Arrival_City, Arrival_date, Departure_Airport, Departure_City, Departure_date, Departure_hr, Departure_min, Arrival_hr, Arrival_min, Airplane_ID, Price,Status) 
VALUES ('3445', 'Shanghai Global', 'ORD', 'Chicago', '2023-12-03', 'PVG', 'Shanghai', '2023-12-02', 21, 30, 4, 30, '454035', 700, 'Upcoming');

INSERT INTO Flight (Flight_number, Airline_name, Arrival_Airport, Arrival_City, Arrival_date, Departure_Airport, Departure_City, Departure_date, Departure_hr, Departure_min, Arrival_hr, Arrival_min, Airplane_ID, Price, Status) 
VALUES ('3446', 'Shanghai Global', 'SEA', 'Seattle', '2023-12-04', 'PVG', 'Shanghai', '2023-12-03', 22, 30, 5, 30, '454036', 800, 'Upcoming');


insert into Booking_Agent (Booking_agent_ID, Airline_Name, Email, Password) values ('agent1', 'Shanghai Global', 'agent1@gmail.com', 'scrypt:32768:8:1$TJF9NVJVTJGDwTP2$ecff7988e93d7d6d891515e7ca3b3035dd95257cd016b16906bc167ab467ad976c7ae1e2ea24dd2b6937f36055ad90427fa7766517fbbe57b726cf60a698b212');

insert into Customer (first_name, last_name, Email, Password, Building, Building_no, Street, City, Passport_expiration, phone_number) values ('John', 'Trent', 'JohnTrent@gmail.com', 'hashed_password3', 'Building 1', '1', 'Street 1', 'City 1', '2023-01-01', '1234567890');

insert into Ticket (Ticket_ID, Airline_name, Flight_Number, Customer_Email, Booking_Agent_Email) values ('32033','Shanghai Global', '3443', 'JohnTrent@gmail.com', null);