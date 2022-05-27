-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 27, 2022 at 09:28 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `finding_missing_people`
--

-- --------------------------------------------------------

--
-- Table structure for table `found`
--

CREATE TABLE `found` (
  `complaintID` varchar(10) NOT NULL,
  `name` text NOT NULL,
  `gender` text NOT NULL,
  `guardian_name` text NOT NULL,
  `guardian_contact` varchar(10) NOT NULL,
  `address` varchar(40) NOT NULL,
  `helper_name` text NOT NULL,
  `helper_contact` int(10) NOT NULL,
  `found_location` varchar(40) NOT NULL,
  `missing_date` date NOT NULL,
  `found_date` date NOT NULL,
  `actual_image` varchar(30) NOT NULL,
  `suspect_image` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `found`
--

INSERT INTO `found` (`complaintID`, `name`, `gender`, `guardian_name`, `guardian_contact`, `address`, `helper_name`, `helper_contact`, `found_location`, `missing_date`, `found_date`, `actual_image`, `suspect_image`) VALUES
('cb001012', 'Elon', 'M', 'Musk Family', '2361872009', 'xyz', 'xxxxx', 2147483647, 'xyzz', '2022-05-26', '2022-05-28', 'Elon_Musk.JPG', 'musk_gates.JPG'),
('cb111021', 'Muskan Gupta', 'F', 'Anu', '8010334221', 'Delhi', 'mehak', 2147483647, 'delhi', '2022-05-23', '2022-05-28', 'Muskan.jpeg', 'Muskan1.jpeg'),
('cb111123', 'Anushka', 'F', 'Sen', '9999123612', 'mumbai', 'kartik', 2147483647, 'Delhi', '2022-05-28', '2022-05-28', 'anushka_sen.JPG', 'anushkaTest.JPG');

-- --------------------------------------------------------

--
-- Table structure for table `missing`
--

CREATE TABLE `missing` (
  `complaintID` varchar(10) NOT NULL,
  `name` text NOT NULL,
  `gender` text NOT NULL,
  `age` int(2) NOT NULL,
  `guardian_name` text NOT NULL,
  `guardian_contact` varchar(10) NOT NULL,
  `city` text NOT NULL,
  `pincode` int(6) NOT NULL,
  `image_name` varchar(20) NOT NULL,
  `missing_date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `missing`
--

INSERT INTO `missing` (`complaintID`, `name`, `gender`, `age`, `guardian_name`, `guardian_contact`, `city`, `pincode`, `image_name`, `missing_date`) VALUES
('cb000112', 'Tiger', 'M', 30, 'Jackie', '8899999988', 'Delhi', 100006, 'tiger.JPG', '2022-05-28'),
('cb002100', 'Alia', 'F', 32, 'mahesh', '7773228999', 'mumbai', 111021, 'Alia.JPG', '2022-05-28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `found`
--
ALTER TABLE `found`
  ADD PRIMARY KEY (`complaintID`);

--
-- Indexes for table `missing`
--
ALTER TABLE `missing`
  ADD PRIMARY KEY (`complaintID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
