-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2023 at 02:37 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `booking`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `Airline_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`Airline_name`) VALUES
('Shanghai Global');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `Airline_name` varchar(20) NOT NULL,
  `Username` varchar(15) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `password` varchar(25) NOT NULL,
  `Dob` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`Airline_name`, `Username`, `first_name`, `last_name`, `password`, `Dob`) VALUES
('Shanghai Global', 'Weaver432', 'Gregory', 'Weaver', 'Requiem115', '1970/03/23');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `Airplane_ID` varchar(15) NOT NULL,
  `Airline_name` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`Airplane_ID`, `Airline_name`) VALUES
('223454', 'Shanghai Global'),
('344788', 'Shanghai Global'),
('454033', 'Shanghai Global');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `Airport_name` varchar(20) NOT NULL,
  `City` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`Airport_name`, `City`) VALUES
('JFK', 'New York'),
('PVG', 'Shanghai'),
('SDY', 'Sydney');

-- --------------------------------------------------------

--
-- Table structure for table `booking_agent`
--

CREATE TABLE `booking_agent` (
  `Booking_agent_ID` varchar(8) NOT NULL,
  `Airline_Name` varchar(20) DEFAULT NULL,
  `Email` varchar(25) NOT NULL,
  `Password` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_agent`
--

INSERT INTO `booking_agent` (`Booking_agent_ID`, `Airline_Name`, `Email`, `Password`) VALUES
('115', 'Shanghai Global', 'JasonHudson@gmail.com', '234442');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `Email` varchar(25) NOT NULL,
  `Building` varchar(25) DEFAULT NULL,
  `Building_no` varchar(7) DEFAULT NULL,
  `Street` varchar(25) DEFAULT NULL,
  `City` varchar(25) DEFAULT NULL,
  `Passport_expiration` varchar(12) NOT NULL,
  `phone_number` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`first_name`, `last_name`, `Email`, `Building`, `Building_no`, `Street`, `City`, `Passport_expiration`, `phone_number`) VALUES
('Alex', 'Mason', 'AlexMason@gmail.com', 'International Continental', '2', 'West Street', 'Washington', '2033', '+6113505421'),
('Vicktor', 'Reznov', 'JohnTrent@gmail.com', 'Madison Towers', '5', 'Madison Street', 'Washington', '2025', '+6450405986');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `Flight_number` varchar(8) NOT NULL,
  `Airline_name` varchar(20) NOT NULL,
  `Arrival_Airport` varchar(20) NOT NULL,
  `Departure_Airport` varchar(20) NOT NULL,
  `Departure_hr` decimal(2,0) DEFAULT NULL CHECK (`Departure_hr` >= 0 and `Departure_hr` < 24),
  `Departure_min` decimal(2,0) DEFAULT NULL CHECK (`Departure_min` >= 0 and `Departure_min` < 60),
  `Arrival_hr` decimal(2,0) DEFAULT NULL CHECK (`Arrival_hr` >= 0 and `Arrival_hr` < 24),
  `Arrival_min` decimal(2,0) DEFAULT NULL CHECK (`Arrival_min` >= 0 and `Arrival_min` < 60),
  `Airplane_ID` varchar(15) DEFAULT NULL,
  `Price` varchar(15) DEFAULT NULL,
  `Status` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`Flight_number`, `Airline_name`, `Arrival_Airport`, `Departure_Airport`, `Departure_hr`, `Departure_min`, `Arrival_hr`, `Arrival_min`, `Airplane_ID`, `Price`, `Status`) VALUES
('1333', 'Shanghai Global', 'SDY', 'PVG', 11, 30, 7, 30, '223454', '200', 'Upcoming'),
('2178', 'Shanghai Global', 'JFK', 'PVG', 15, 30, 12, 30, '454033', '500', 'In-progress'),
('3443', 'Shanghai Global', 'JFK', 'PVG', 19, 30, 2, 30, '454033', '500', 'Upcoming'),
('4343', 'Shanghai Global', 'PVG', 'JFK', 17, 30, 4, 30, '344788', '500', 'Delayed');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `Ticket_ID` varchar(8) NOT NULL,
  `Flight_Number` varchar(8) DEFAULT NULL,
  `Customer_Email` varchar(25) DEFAULT NULL,
  `Booking_Agent_Email` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`Ticket_ID`, `Flight_Number`, `Customer_Email`, `Booking_Agent_Email`) VALUES
('12334', '2178', 'JohnTrent@gmail.com', 'JasonHudson@gmail.com'),
('32033', '3443', 'JohnTrent@gmail.com', NULL),
('34355', '4343', 'AlexMason@gmail.com', 'JasonHudson@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`Airline_name`);

--
-- Indexes for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`Username`),
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`Airplane_ID`),
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`Airport_name`);

--
-- Indexes for table `booking_agent`
--
ALTER TABLE `booking_agent`
  ADD PRIMARY KEY (`Email`),
  ADD KEY `Airline_Name` (`Airline_Name`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`Email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`Flight_number`),
  ADD KEY `Airline_name` (`Airline_name`),
  ADD KEY `Arrival_Airport` (`Arrival_Airport`),
  ADD KEY `Departure_Airport` (`Departure_Airport`),
  ADD KEY `Airplane_ID` (`Airplane_ID`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`Ticket_ID`),
  ADD KEY `Customer_Email` (`Customer_Email`),
  ADD KEY `Booking_Agent_Email` (`Booking_Agent_Email`),
  ADD KEY `Flight_Number` (`Flight_Number`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `airline` (`Airline_name`);

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `airline` (`Airline_name`);

--
-- Constraints for table `booking_agent`
--
ALTER TABLE `booking_agent`
  ADD CONSTRAINT `booking_agent_ibfk_1` FOREIGN KEY (`Airline_Name`) REFERENCES `airline` (`Airline_name`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `airline` (`Airline_name`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`Arrival_Airport`) REFERENCES `airport` (`Airport_name`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`Departure_Airport`) REFERENCES `airport` (`Airport_name`),
  ADD CONSTRAINT `flight_ibfk_4` FOREIGN KEY (`Airplane_ID`) REFERENCES `airplane` (`Airplane_ID`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`Customer_Email`) REFERENCES `customer` (`Email`),
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`Booking_Agent_Email`) REFERENCES `booking_agent` (`Email`),
  ADD CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`Flight_Number`) REFERENCES `flight` (`Flight_number`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
