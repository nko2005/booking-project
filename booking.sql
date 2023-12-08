-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 03, 2023 at 09:16 PM
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
--z

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

INSERT INTO `airline_staff` (`id`, `Airline_name`, `Username`, `first_name`, `last_name`, `password`, `Dob`, `permission`) VALUES
(1, 'Shanghai Global', 'staff1', 'John', 'Doe', 'scrypt:32768:8:1$1dZCs1FKpfgdFlFu$4e34b3d2eda8b7118c7fbe7eb77573f690217dfcfa777916d4fc2cb528c054dbc80bcf44d583abdf9ac7c6be907edbdec0e82f062f9422453be097082632e8b9', '1980-01-01', 'admin'),
(2, 'Shanghai Global ', 'staff2', 'Khaled', 'gggg', 'scrypt:32768:8:1$1SCf1Vnz5EvOqKT0$c176b62cadeb891a8cf204f8cdf7a301e509474d9aeb3d365f07bad32b8b73f3c5a90c28d7ad307e73ae77b8bda40c2453192c565bde93293502731440cf727b', '2023-12-03', 'admin'),
(3, 'Shanghai Global ', 'staff5', 'Ahmed', 'Noob', 'scrypt:32768:8:1$OV42TtrFmjvMBxeS$3d8d2afeb9a1712a04a83e779efee2f9fa031718628d11f4f1c0f56417780c612cf1d3c32d27cc6088c41274afb9c8f1309c3889ddf88fdb37ae9144c1c2f3d1', '2023-11-07', 'staff');

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
('123321', 'Shanghai Global'),
('454033', 'Shanghai Global'),
('454034', 'Shanghai Global'),
('454035', 'Shanghai Global'),
('454036', 'Shanghai Global');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `Airport_name` varchar(20) NOT NULL,
  `City` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`Airport_name`, `City`) VALUES
('ABC', 'Bejing'),
('JFK', 'New York'),
('KFI', 'Dammam'),
('LAX', 'Los Angeles'),
('ORD', 'Chicago'),
('PVG', 'Shanghai'),
('SEA', 'Seattle');

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
(1, 'agent1', 'Shanghai Global', 'agent1@gmail.com', 'scrypt:32768:8:1$TJF9NVJVTJGDwTP2$ecff7988e93d7d6d891515e7ca3b3035dd95257cd016b16906bc167ab467ad976c7ae1e2ea24dd2b6937f36055ad90427fa7766517fbbe57b726cf60a698b212'),
(2, '878789', 'Shanghai Global ', 'vicktor@gmail.com', 'scrypt:32768:8:1$kpj1ZMOUz6rTDhNC$d4cddf28339195ee848a164a590cf040313c18c232e59a31b9880c8ef20ebc301cb4440cf8abc638b568900b3e43ed4b4bd8133fff9fd359215cbe5be97a405e');

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
(1, 'John', 'Trent', 'JohnTrent@gmail.com', 'hashed_password3', 'Building 1', '1', 'Street 1', 'City 1', '2023-01-01', '1234567890'),
(5, 'Khaled', 'Alotaishan', 'otaishan@yahoo.com', 'scrypt:32768:8:1$7T6dmQC1MVAcO2Mr$0115c3aa63d6a64097e1a7999fcf34245a9d25f78c33e3f668c4ab2177da2a1ed2bcf665b6c0392ce17e4f576a638eb7b951c35989876cf23542731894eb224f', NULL, '33', '8183, Ab', 'Dammam', '2023-12-01', '15618272538'),
(6, 'Khaled', 'Alotaishan', 'trent@gmail.com', 'scrypt:32768:8:1$EUJk2mLUoLoCGgGa$9ec22d93588ddf5e8a67848b4d6956ea9f6a0cd1f889c72bd68437f9cc6b950f16c0418907b023a3a135b8461a66562ea928b4e3e2f227323fd0465860dcabca', NULL, '', '8183, Ab', 'Dammam', '2023-12-01', '');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `Flight_number` varchar(8) NOT NULL,
  `Airline_name` varchar(20) NOT NULL,
  `Arrival_Airport` varchar(20) NOT NULL,
  `Arrival_City` varchar(20) NOT NULL,
  `Arrival_date` date NOT NULL,
  `Departure_Airport` varchar(20) NOT NULL,
  `Departure_City` varchar(20) NOT NULL,
  `Departure_date` date NOT NULL,
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

INSERT INTO `flight` (`Flight_number`, `Airline_name`, `Arrival_Airport`, `Arrival_City`, `Arrival_date`, `Departure_Airport`, `Departure_City`, `Departure_date`, `Departure_hr`, `Departure_min`, `Arrival_hr`, `Arrival_min`, `Airplane_ID`, `Price`, `Status`) VALUES
('3443', 'Shanghai Global', 'JFK', 'New York', '2023-12-02', 'PVG', 'Shanghai', '2023-12-01', 19, 30, 2, 30, '454033', 500.00, 'Upcoming'),
('3444', 'Shanghai Global', 'LAX', 'Los Angeles', '2023-12-02', 'PVG', 'Shanghai', '2023-12-01', 20, 30, 3, 30, '454034', 600.00, 'Upcoming'),
('3445', 'Shanghai Global', 'ORD', 'Chicago', '2023-12-03', 'PVG', 'Shanghai', '2023-12-02', 21, 30, 4, 30, '454035', 700.00, 'Upcoming'),
('3446', 'Shanghai Global', 'SEA', 'Seattle', '2023-12-04', 'PVG', 'Shanghai', '2023-12-03', 22, 30, 5, 30, '454036', 800.00, 'Delayed'),
('34663', 'Shanghai Global', 'ABC', 'Bejing', '2023-12-07', 'PVG', 'Shanghai', '2023-12-06', 2, 21, 2, 21, '454033', 800.00, NULL),
('36663', 'Shanghai Global', 'LAX', 'Los Angeles', '2023-12-04', 'PVG', 'Shanghai', '2023-12-03', 2, 21, 2, 21, '123321', 80.00, NULL),
('36663555', 'Shanghai Global', 'JFK', 'New York', '2023-12-07', 'PVG', 'Shanghai', '2023-12-05', 2, 32, 2, 32, '454035', 44000.00, 'Delayed');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `id` int(11) NOT NULL,
  `Ticket_ID` varchar(8) NOT NULL,
  `Airline_name` varchar(20) NOT NULL,
  `Flight_Number` varchar(8) NOT NULL,
  `Customer_Email` varchar(25) NOT NULL,
  `Booking_Agent_Email` varchar(25) DEFAULT NULL,
  `Purchase_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`id`, `Ticket_ID`, `Airline_name`, `Flight_Number`, `Customer_Email`, `Booking_Agent_Email`, `Purchase_date`) VALUES
(1, '04259eed', 'Shanghai Global', '36663', 'trent@gmail.com', NULL, '2023-12-03'),
(2, '0c3662a5', 'Shanghai Global', '3446', 'trent@gmail.com', NULL, '2023-12-03'),
(3, '62b95272', 'Shanghai Global', '3444', 'trent@gmail.com', 'vicktor@gmail.com', '2023-12-04');

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
  ADD PRIMARY KEY (`Airport_name`);

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
  ADD KEY `Departure_Airport` (`Departure_Airport`),
  ADD KEY `Airplane_ID` (`Airplane_ID`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Ticket_ID` (`Ticket_ID`),
  ADD KEY `Customer_Email` (`Customer_Email`),
  ADD KEY `Booking_Agent_Email` (`Booking_Agent_Email`),
  ADD KEY `Flight_Number` (`Flight_Number`),
  ADD KEY `Airline_name` (`Airline_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `airline_staff`
--
ALTER TABLE `airline_staff`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `booking_agent`
--
ALTER TABLE `booking_agent`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `ticket`
--
ALTER TABLE `ticket`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
  ADD CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`Flight_Number`) REFERENCES `flight` (`Flight_number`),
  ADD CONSTRAINT `ticket_ibfk_4` FOREIGN KEY (`Airline_name`) REFERENCES `flight` (`Airline_name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
