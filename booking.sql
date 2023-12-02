-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 22, 2023 at 11:42 AM
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
  `id` int(11) NOT NULL,
  `Airline_name` varchar(20) NOT NULL,
  `Username` varchar(15) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `Dob` date DEFAULT NULL,
  `permission` enum('admin','staff') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`id`, `Airline_name`, `Username`, `first_name`, `last_name`, `password`, `Dob`,`permission`) VALUES
(1, 'Shanghai Global', 'staff1', 'John', 'Doe', 'scrypt:32768:8:1$1dZCs1FKpfgdFlFu$4e34b3d2eda8b7118c7fbe7eb77573f690217dfcfa777916d4fc2cb528c054dbc80bcf44d583abdf9ac7c6be907edbdec0e82f062f9422453be097082632e8b9', '1980-01-01','admin');

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
('454033', 'Shanghai Global');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `Airport_name` varchar(20) NOT NULL,
  `City` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`Airport_name`, `City`) VALUES
('JFK', 'New York'),
('PVG', 'Shanghai');

-- --------------------------------------------------------

--
-- Table structure for table `booking_agent`
--

CREATE TABLE `booking_agent` (
  `id` int(11) NOT NULL,
  `Booking_agent_ID` varchar(8) NOT NULL,
  `Airline_Name` varchar(20) DEFAULT NULL,
  `Email` varchar(25) NOT NULL,
  `Password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_agent`
--

INSERT INTO `booking_agent` (`id`, `Booking_agent_ID`, `Airline_Name`, `Email`, `Password`) VALUES
(1, 'agent1', 'Shanghai Global', 'agent1@gmail.com', 'scrypt:32768:8:1$TJF9NVJVTJGDwTP2$ecff7988e93d7d6d891515e7ca3b3035dd95257cd016b16906bc167ab467ad976c7ae1e2ea24dd2b6937f36055ad90427fa7766517fbbe57b726cf60a698b212');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `Email` varchar(25) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Building` varchar(25) DEFAULT NULL,
  `Building_no` varchar(7) DEFAULT NULL,
  `Street` varchar(25) DEFAULT NULL,
  `City` varchar(25) DEFAULT NULL,
  `Passport_expiration` date NOT NULL,
  `phone_number` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `first_name`, `last_name`, `Email`, `Password`, `Building`, `Building_no`, `Street`, `City`, `Passport_expiration`, `phone_number`) VALUES
(1, 'John', 'Trent', 'JohnTrent@gmail.com', 'hashed_password3', 'Building 1', '1', 'Street 1', 'City 1', '2023-01-01', '1234567890');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `Flight_number` varchar(8) NOT NULL,
  `Airline_name` varchar(20) NOT NULL,
  `Arrival_Airport` varchar(20) NOT NULL,
  `Arrival_City` varchar(15) NOT NULL,
  `Arrival_date` date DEFAULT NULL,
  `Departure_Airport` varchar(20) NOT NULL,
  `Departure_City` varchar(15) NOT NULL,
  `Departure_date` date DEFAULT NULL,
  `Departure_hr` decimal(2,0) DEFAULT NULL CHECK (`Departure_hr` >= 0 and `Departure_hr` < 24),
  `Departure_min` decimal(2,0) DEFAULT NULL CHECK (`Departure_min` >= 0 and `Departure_min` < 60),
  `Arrival_hr` decimal(2,0) DEFAULT NULL CHECK (`Arrival_hr` >= 0 and `Arrival_hr` < 24),
  `Arrival_min` decimal(2,0) DEFAULT NULL CHECK (`Arrival_min` >= 0 and `Arrival_min` < 60),
  `Airplane_ID` varchar(15) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Status` enum('Upcoming','Cancelled','Delayed','in-progress') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`Flight_number`, `Airline_name`, `Arrival_Airport`, `Arrival_date`, `Departure_Airport`, `Departure_date`, `Departure_hr`, `Departure_min`, `Arrival_hr`, `Arrival_min`, `Airplane_ID`, `Price`, `Status`) 
VALUES
('3443', 'Shanghai Global', 'JFK', '2022-12-01', 'PVG', '2022-11-30', 19, 30, 2, 30, '454033', 500.00, 'Upcoming');
-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `id` int(11) NOT NULL,
  `Ticket_ID` varchar(8) NOT NULL,
  `Airline_name` varchar(20) DEFAULT NULL,
  `Flight_Number` varchar(8) NOT NULL,
  `Customer_Email` varchar(25) NOT NULL,
  `Booking_Agent_Email` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`id`, `Ticket_ID`, `Flight_Number`, `Customer_Email`, `Booking_Agent_Email`) VALUES
(1, '32033', '3443', 'JohnTrent@gmail.com', NULL);

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
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Username` (`Username`),
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
  ADD PRIMARY KEY (`Airport_name`),
  

--
-- Indexes for table `booking_agent`
--
ALTER TABLE `booking_agent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `Airline_Name` (`Airline_Name`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`Flight_number`),
  ADD KEY `Airline_name` (`Airline_name`),
  ADD KEY `Arrival_Airport` (`Arrival_Airport`),
  ADD KEY `Arrival_City` (`Arrival_City`), 
  ADD KEY `Departure_Airport` (`Departure_Airport`),
  ADD KEY `Departure_City` (`Departure_City`),
  ADD KEY `Airplane_ID` (`Airplane_ID`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Ticket_ID` (`Ticket_ID`),
  ADD KEY `Customer_Email` (`Customer_Email`),
  ADD KEY `Booking_Agent_Email` (`Booking_Agent_Email`),
  ADD KEY `Flight_Number` (`Flight_Number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `airline_staff`
--
ALTER TABLE `airline_staff`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `booking_agent`
--
ALTER TABLE `booking_agent`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ticket`
--
ALTER TABLE `ticket`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
