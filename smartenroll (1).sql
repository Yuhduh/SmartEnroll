-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2025 at 01:03 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartenroll`
--

-- --------------------------------------------------------

--
-- Table structure for table `academic_years`
--

CREATE TABLE `academic_years` (
  `id` int(11) NOT NULL,
  `year_name` varchar(50) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `semester` enum('1st Semester','2nd Semester','Full Year') DEFAULT 'Full Year',
  `is_active` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `academic_years`
--

INSERT INTO `academic_years` (`id`, `year_name`, `start_date`, `end_date`, `semester`, `is_active`, `created_at`) VALUES
(1, '2024-2025', '2024-08-01', '2025-05-31', 'Full Year', 1, '2025-12-18 22:37:29'),
(2, '2023-2024', '2023-08-01', '2024-05-31', 'Full Year', 0, '2025-12-18 22:37:32'),
(3, '2025-2026', '2025-08-01', '2026-05-31', 'Full Year', 0, '2025-12-18 22:37:32');

-- --------------------------------------------------------

--
-- Table structure for table `activity_log`
--

CREATE TABLE `activity_log` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `action` varchar(100) NOT NULL,
  `table_name` varchar(50) NOT NULL,
  `record_id` int(11) DEFAULT NULL,
  `old_value` text DEFAULT NULL,
  `new_value` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payment_transactions`
--

CREATE TABLE `payment_transactions` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_date` date NOT NULL,
  `payment_method` enum('Cash','Check','Bank Transfer','Online Payment','Installment') DEFAULT 'Cash',
  `reference_number` varchar(100) DEFAULT NULL,
  `receipt_number` varchar(100) DEFAULT NULL,
  `academic_year_id` int(11) DEFAULT NULL,
  `payment_type` enum('Tuition','Miscellaneous','Other') DEFAULT 'Tuition',
  `notes` text DEFAULT NULL,
  `recorded_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment_transactions`
--

INSERT INTO `payment_transactions` (`id`, `student_id`, `amount`, `payment_date`, `payment_method`, `reference_number`, `receipt_number`, `academic_year_id`, `payment_type`, `notes`, `recorded_by`, `created_at`) VALUES
(1, 4, 5000.00, '2025-12-19', 'Cash', NULL, 'REC-20251219-0001', NULL, 'Miscellaneous', 'hgehe', 1, '2025-12-18 23:45:07');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `room_number` varchar(20) NOT NULL,
  `building` varchar(50) NOT NULL,
  `capacity` int(11) DEFAULT 40,
  `status` enum('Active','Inactive') DEFAULT 'Active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `room_number`, `building`, `capacity`, `status`, `created_at`) VALUES
(1, '101', 'Main Building', 40, 'Active', '2025-12-18 18:11:46'),
(2, '102', 'Main Building', 40, 'Active', '2025-12-18 18:11:46'),
(3, '201', 'Main Building', 35, 'Active', '2025-12-18 18:11:46'),
(4, '202', 'Main Building', 35, 'Active', '2025-12-18 18:11:46'),
(5, '301', 'Annex Building', 30, 'Active', '2025-12-18 18:11:46'),
(6, '302', 'Annex Building', 30, 'Active', '2025-12-18 18:11:46'),
(7, '123', 'Main', 30, 'Active', '2025-12-18 21:31:12');

-- --------------------------------------------------------

--
-- Table structure for table `sections`
--

CREATE TABLE `sections` (
  `id` int(11) NOT NULL,
  `section_name` varchar(50) NOT NULL,
  `grade_level` enum('11','12') DEFAULT '11',
  `track` varchar(50) NOT NULL,
  `strand` varchar(100) NOT NULL,
  `capacity` int(11) DEFAULT 40,
  `teacher_id` int(11) DEFAULT NULL,
  `adviser_id` int(11) DEFAULT NULL,
  `room_number` varchar(20) DEFAULT NULL,
  `status` enum('Active','Inactive') DEFAULT 'Active',
  `academic_year_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sections`
--

INSERT INTO `sections` (`id`, `section_name`, `grade_level`, `track`, `strand`, `capacity`, `teacher_id`, `adviser_id`, `room_number`, `status`, `academic_year_id`, `created_at`) VALUES
(1, '11-Newton', '11', 'Academic', 'STEM', 40, 1, 1, '101', 'Active', NULL, '2025-12-18 18:11:46'),
(2, '11-Pythagoras', '11', 'Academic', 'STEM', 40, 2, 2, '102', 'Active', NULL, '2025-12-18 18:11:46'),
(3, '11-Rizal', '11', 'Academic', 'HUMSS', 35, 3, 3, '201', 'Active', NULL, '2025-12-18 18:11:46'),
(4, '11-Tycoon', '11', 'Academic', 'ABM', 35, 5, 5, '202', 'Active', NULL, '2025-12-18 18:11:46'),
(5, '11-Turing', '11', 'TVL', 'ICT', 30, 4, 4, '301', 'Active', NULL, '2025-12-18 18:11:46'),
(13, 'gwapo', '11', 'Academic', 'STEM', 25, 6, 6, '123', 'Active', NULL, '2025-12-18 21:55:36'),
(14, 'gwapo1', '11', 'Academic', 'STEM', 25, 6, 6, '302', 'Active', NULL, '2025-12-18 21:56:04');

-- --------------------------------------------------------

--
-- Table structure for table `section_assignments`
--

CREATE TABLE `section_assignments` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `section_id` int(11) NOT NULL,
  `assigned_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `removed_date` timestamp NULL DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `lrn` varchar(12) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `gender` enum('Male','Female') NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `address` text DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `guardian_name` varchar(100) DEFAULT NULL,
  `guardian_contact` varchar(20) DEFAULT NULL,
  `last_school` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `track` varchar(50) NOT NULL,
  `strand` varchar(100) NOT NULL,
  `grade_level` enum('11','12') DEFAULT '11',
  `academic_year_id` int(11) DEFAULT NULL,
  `section_id` int(11) DEFAULT NULL,
  `payment_status` enum('Pending','Paid','Partial') DEFAULT 'Pending',
  `status` enum('Pending','Enrolled','Dropped') DEFAULT 'Pending',
  `status_reason` text DEFAULT NULL,
  `status_changed_date` timestamp NULL DEFAULT NULL,
  `status_changed_by` int(11) DEFAULT NULL,
  `enrollment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `payment_mode` varchar(50) DEFAULT 'Full Payment',
  `total_fees` decimal(10,2) DEFAULT 0.00,
  `amount_paid` decimal(10,2) DEFAULT 0.00,
  `balance` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `lrn`, `full_name`, `first_name`, `last_name`, `middle_name`, `gender`, `date_of_birth`, `address`, `contact_number`, `guardian_name`, `guardian_contact`, `last_school`, `email`, `track`, `strand`, `grade_level`, `academic_year_id`, `section_id`, `payment_status`, `status`, `status_reason`, `status_changed_date`, `status_changed_by`, `enrollment_date`, `payment_mode`, `total_fees`, `amount_paid`, `balance`) VALUES
(1, '129648120080', 'carl masayon', 'carl', 'masayon', NULL, 'Male', NULL, 'N/A', '09289884464', NULL, NULL, NULL, 'asdas@gmail.com', 'Academic', 'HUMSS', '11', 1, 3, 'Pending', 'Enrolled', NULL, NULL, NULL, '2025-12-18 18:12:31', 'Full Payment', 0.00, 0.00, 0.00),
(2, '129648120010', 'love marie reyes', 'love marie', 'reyes', NULL, 'Male', NULL, 'N/A', '0912312312123123', NULL, NULL, NULL, 'love@gmail.com', 'Academic', 'ABM', '11', 1, 4, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-12-18 19:50:32', 'Full Payment', 0.00, 0.00, 0.00),
(3, '129131231123', 'loveasd asdasdas', 'loveasd', 'asdasdas', NULL, 'Male', NULL, 'N/A', '123121231232', NULL, NULL, NULL, 'asdl@gmail.com', 'Academic', 'HUMSS', '11', 1, 3, 'Pending', 'Enrolled', NULL, NULL, NULL, '2025-12-18 19:52:06', 'Full Payment', 0.00, 0.00, 0.00),
(4, '123123123121', 'aasdasd asdasdas asdasdsad', 'aasdasd', 'asdasdsad', NULL, 'Male', '2007-01-10', 'asdasdasdasd', '13212312312', NULL, NULL, NULL, 'asdd@gmail.com', 'Academic', 'STEM', '11', 1, 1, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-12-18 21:18:13', 'Full Payment', 0.00, 5000.00, -10000.00),
(5, '123123123101', 'Maria Santos Cruz', 'Maria', 'Cruz', 'Santos', 'Female', '2007-03-15', 'Brgy. Poblacion, Davao City', '09171234567', 'Rosa Cruz', '09181234567', 'Davao National High School', 'maria.cruz@email.com', 'Academic', 'STEM', '11', NULL, NULL, 'Partial', 'Enrolled', NULL, NULL, NULL, '2025-12-14 00:01:23', 'Full Payment', 15000.00, 7500.00, 7500.00),
(6, '123123123102', 'John Paul Reyes', 'John Paul', 'Reyes', 'Santos', 'Male', '2007-05-20', 'Brgy. Matina, Davao City', '09172345678', 'Pedro Reyes', '09182345678', 'Ateneo de Davao', 'john.reyes@email.com', 'Academic', 'ABM', '11', NULL, NULL, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-12-15 00:01:23', 'Full Payment', 15000.00, 15000.00, 0.00),
(7, '123123123103', 'Angela Mae Gonzales', 'Angela', 'Gonzales', 'Mae', 'Female', '2006-08-12', 'Brgy. Buhangin, Davao City', '09173456789', 'Carmen Gonzales', '09183456789', 'Holy Cross of Davao College', 'angela.gonzales@email.com', 'Academic', 'HUMSS', '12', NULL, NULL, 'Pending', 'Enrolled', NULL, NULL, NULL, '2025-12-16 00:01:23', 'Full Payment', 15000.00, 0.00, 15000.00),
(8, '123123123104', 'Michael James Tan', 'Michael', 'Tan', 'James', 'Male', '2007-01-25', 'Brgy. Agdao, Davao City', '09174567890', 'Linda Tan', '09184567890', 'Philippine Science High School', 'michael.tan@email.com', 'Academic', 'GAS', '11', NULL, NULL, 'Partial', 'Enrolled', NULL, NULL, NULL, '2025-12-17 00:01:23', 'Full Payment', 15000.00, 5000.00, 10000.00),
(9, '123123123105', 'Sarah Jane Ramos', 'Sarah', 'Ramos', 'Jane', 'Female', '2006-11-30', 'Brgy. Toril, Davao City', '09175678901', 'Roberto Ramos', '09185678901', 'University of Immaculate Conception', 'sarah.ramos@email.com', 'Academic', 'STEM', '12', NULL, NULL, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-12-18 00:01:23', 'Full Payment', 15000.00, 15000.00, 0.00),
(10, '123123123106', 'Carlo Antonio Diaz', 'Carlo', 'Diaz', 'Antonio', 'Male', '2007-07-18', 'Brgy. Catalunan Grande, Davao City', '09176789012', 'Maria Diaz', '09186789012', 'Davao City National High School', 'carlo.diaz@email.com', 'TVL', 'TVL', '11', NULL, NULL, 'Pending', 'Enrolled', NULL, NULL, NULL, '2025-12-19 00:01:23', 'Full Payment', 15000.00, 0.00, 15000.00),
(11, '123123123107', 'Patricia Anne Flores', 'Patricia', 'Flores', 'Anne', 'Female', '2006-04-22', 'Brgy. Panacan, Davao City', '09177890123', 'Juan Flores', '09187890123', 'Stella Maris Academy', 'patricia.flores@email.com', 'Academic', 'ABM', '12', NULL, NULL, 'Partial', 'Enrolled', NULL, NULL, NULL, '2025-12-13 00:01:23', 'Full Payment', 15000.00, 10000.00, 5000.00),
(12, '123123123108', 'Daniel Luis Garcia', 'Daniel', 'Garcia', 'Luis', 'Male', '2007-09-05', 'Brgy. Sasa, Davao City', '09178901234', 'Ana Garcia', '09188901234', 'Cor Jesu College', 'daniel.garcia@email.com', 'Academic', 'STEM', '11', NULL, NULL, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-12-12 00:01:23', 'Full Payment', 15000.00, 15000.00, 0.00),
(13, '123123123109', 'Kristine Joy Mendoza', 'Kristine', 'Mendoza', 'Joy', 'Female', '2007-02-14', 'Brgy. Lanang, Davao City', '09179012345', 'Elena Mendoza', '09189012345', 'Assumption College', 'kristine.mendoza@email.com', 'Academic', 'HUMSS', '11', NULL, NULL, 'Pending', 'Enrolled', NULL, NULL, NULL, '2025-12-11 00:01:23', 'Full Payment', 15000.00, 0.00, 15000.00),
(14, '123123123110', 'Ryan Miguel Santos', 'Ryan', 'Santos', 'Miguel', 'Male', '2006-06-28', 'Brgy. Maa, Davao City', '09170123456', 'Jose Santos', '09180123456', 'Brokenshire College', 'ryan.santos@email.com', 'Academic', 'GAS', '12', NULL, NULL, 'Partial', 'Enrolled', NULL, NULL, NULL, '2025-12-10 00:01:23', 'Full Payment', 15000.00, 7500.00, 7500.00),
(15, '123123123111', 'Jasmine Mae Torres', 'Jasmine', 'Torres', 'Mae', 'Female', '2007-10-10', 'Brgy. Talomo, Davao City', '09171234568', 'Rosa Torres', '09181234568', 'Regional Science High School', 'jasmine.torres@email.com', 'Academic', 'STEM', '11', NULL, NULL, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-12-09 00:01:23', 'Full Payment', 15000.00, 15000.00, 0.00),
(16, '123123123112', 'Kenneth Paul Villanueva', 'Kenneth', 'Villanueva', 'Paul', 'Male', '2007-12-03', 'Brgy. Bunawan, Davao City', '09172345679', 'Pedro Villanueva', '09182345679', 'Davao Christian High School', 'kenneth.villanueva@email.com', 'Academic', 'ABM', '11', NULL, NULL, 'Pending', 'Enrolled', NULL, NULL, NULL, '2025-12-08 00:01:23', 'Full Payment', 15000.00, 0.00, 15000.00),
(17, '123123123113', 'Michelle Anne Bautista', 'Michelle', 'Bautista', 'Anne', 'Female', '2006-03-17', 'Brgy. Calinan, Davao City', '09173456780', 'Carmen Bautista', '09183456780', 'Holy Child School of Davao', 'michelle.bautista@email.com', 'TVL', 'TVL', '12', NULL, NULL, 'Partial', 'Enrolled', NULL, NULL, NULL, '2025-12-07 00:01:23', 'Full Payment', 15000.00, 8000.00, 7000.00),
(18, '123123123114', 'Joshua David Cruz', 'Joshua', 'Cruz', 'David', 'Male', '2006-07-29', 'Brgy. Tigatto, Davao City', '09174567891', 'Linda Cruz', '09184567891', 'Philippine Women\'s College', 'joshua.cruz@email.com', 'Academic', 'HUMSS', '12', NULL, NULL, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-12-06 00:01:23', 'Full Payment', 15000.00, 15000.00, 0.00),
(19, '123123123115', 'Nicole Andrea Ramos', 'Nicole', 'Ramos', 'Andrea', 'Female', '2006-01-08', 'Brgy. Bajada, Davao City', '09175678902', 'Roberto Ramos', '09185678902', 'San Pedro College', 'nicole.ramos@email.com', 'Academic', 'STEM', '12', NULL, NULL, 'Pending', 'Enrolled', NULL, NULL, NULL, '2025-12-05 00:01:23', 'Full Payment', 15000.00, 0.00, 15000.00),
(20, '123123123116', 'Justin Carl Lopez', 'Justin', 'Lopez', 'Carl', 'Male', '2007-05-19', 'Brgy. Eden, Davao City', '09176789013', 'Maria Lopez', '09186789013', 'Notre Dame of Davao', 'justin.lopez@email.com', 'Academic', 'GAS', '11', NULL, NULL, 'Partial', 'Enrolled', NULL, NULL, NULL, '2025-12-04 00:01:23', 'Full Payment', 15000.00, 6000.00, 9000.00),
(21, '123123123117', 'Samantha Rose Perez', 'Samantha', 'Perez', 'Rose', 'Female', '2006-09-23', 'Brgy. Crossing, Davao City', '09177890124', 'Juan Perez', '09187890124', 'Xavier University', 'samantha.perez@email.com', 'Academic', 'ABM', '12', NULL, NULL, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-12-03 00:01:23', 'Full Payment', 15000.00, 15000.00, 0.00),
(22, '123123123118', 'Gabriel Luis Santos', 'Gabriel', 'Santos', 'Luis', 'Male', '2007-11-11', 'Brgy. Matina Crossing, Davao City', '09178901235', 'Ana Santos', '09188901235', 'Mindanao Medical Foundation College', 'gabriel.santos@email.com', 'Academic', 'STEM', '11', NULL, NULL, 'Pending', 'Enrolled', NULL, NULL, NULL, '2025-12-02 00:01:23', 'Full Payment', 15000.00, 0.00, 15000.00),
(23, '123123123119', 'Sophia Marie Dela Cruz', 'Sophia', 'Dela Cruz', 'Marie', 'Female', '2007-04-02', 'Brgy. Los Amigos, Davao City', '09179012346', 'Elena Dela Cruz', '09189012346', 'St. Mary\'s College', 'sophia.delacruz@email.com', 'Academic', 'HUMSS', '11', NULL, NULL, 'Partial', 'Enrolled', NULL, NULL, NULL, '2025-12-01 00:01:23', 'Full Payment', 15000.00, 9000.00, 6000.00),
(24, '123123123120', 'Nathan James Rivera', 'Nathan', 'Rivera', 'James', 'Male', '2007-08-16', 'Brgy. Magtuod, Davao City', '09170123457', 'Jose Rivera', '09180123457', 'Southern Christian College', 'nathan.rivera@email.com', 'TVL', 'TVL', '11', NULL, NULL, 'Paid', 'Enrolled', NULL, NULL, NULL, '2025-11-30 00:01:23', 'Full Payment', 15000.00, 15000.00, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `student_documents`
--

CREATE TABLE `student_documents` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `form_138` tinyint(1) DEFAULT 0,
  `psa_birth_cert` tinyint(1) DEFAULT 0,
  `good_moral` tinyint(1) DEFAULT 0,
  `medical_cert` tinyint(1) DEFAULT 0,
  `report_card` tinyint(1) DEFAULT 0,
  `verified_by` int(11) DEFAULT NULL,
  `verification_date` timestamp NULL DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `student_payments`
--

CREATE TABLE `student_payments` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `payment_type` varchar(50) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_date` date DEFAULT NULL,
  `status` enum('Pending','Paid','Partial') DEFAULT 'Pending',
  `payment_method` varchar(50) DEFAULT NULL,
  `reference_number` varchar(100) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `student_status_history`
--

CREATE TABLE `student_status_history` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `old_status` varchar(20) DEFAULT NULL,
  `new_status` varchar(20) NOT NULL,
  `reason` text DEFAULT NULL,
  `changed_by` int(11) DEFAULT NULL,
  `changed_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `status` enum('Active','Inactive') DEFAULT 'Active',
  `hire_date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`id`, `full_name`, `email`, `contact_number`, `department`, `specialization`, `status`, `hire_date`, `created_at`) VALUES
(1, 'Mrs. Ana Cruz', 'ana.cruz@school.edu', '09171234567', 'Science', 'STEM', 'Active', '2023-06-01', '2025-12-18 18:11:46'),
(2, 'Mr. Ben Santos', 'ben.santos@school.edu', '09181234567', 'Mathematics', 'STEM', 'Active', '2023-06-01', '2025-12-18 18:11:46'),
(3, 'Ms. Carla Gomez', 'carla.gomez@school.edu', '09191234567', 'English', 'HUMSS', 'Active', '2023-06-01', '2025-12-18 18:11:46'),
(4, 'Mr. Dante Reyes', 'dante.reyes@school.edu', '09201234567', 'ICT', 'TVL', 'Active', '2023-06-01', '2025-12-18 18:11:46'),
(5, 'Mrs. Elena Lim', 'elena.lim@school.edu', '09211234567', 'Business', 'ABM', 'Active', '2023-06-01', '2025-12-18 18:11:46'),
(6, 'Mrs. Eliza Veloria', 'eliza@gmai.com', '12312312', '', 'STEM', 'Active', '2025-12-19', '2025-12-18 19:12:13');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  `role` enum('staff','admin') DEFAULT 'staff',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `role`, `created_at`) VALUES
(1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', '2025-12-18 18:11:46'),
(2, 'carl', '0b23f06a6e9172772ffb31e48725eb33763fc25046b8a90cf055b5bfa22f6705', 'staff', '2025-12-18 20:47:31');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_years`
--
ALTER TABLE `academic_years`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `year_name` (`year_name`),
  ADD KEY `idx_active` (`is_active`);

--
-- Indexes for table `activity_log`
--
ALTER TABLE `activity_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user` (`user_id`),
  ADD KEY `idx_date` (`created_at`),
  ADD KEY `idx_action` (`action`);

--
-- Indexes for table `payment_transactions`
--
ALTER TABLE `payment_transactions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `receipt_number` (`receipt_number`),
  ADD KEY `academic_year_id` (`academic_year_id`),
  ADD KEY `recorded_by` (`recorded_by`),
  ADD KEY `idx_student` (`student_id`),
  ADD KEY `idx_date` (`payment_date`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_room` (`room_number`,`building`);

--
-- Indexes for table `sections`
--
ALTER TABLE `sections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teacher_id` (`teacher_id`),
  ADD KEY `adviser_id` (`adviser_id`),
  ADD KEY `academic_year_id` (`academic_year_id`);

--
-- Indexes for table `section_assignments`
--
ALTER TABLE `section_assignments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `assigned_by` (`assigned_by`),
  ADD KEY `idx_current` (`student_id`,`is_current`),
  ADD KEY `idx_section` (`section_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `lrn` (`lrn`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_full_name` (`full_name`),
  ADD KEY `idx_lrn` (`lrn`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_strand` (`strand`),
  ADD KEY `idx_section` (`section_id`),
  ADD KEY `fk_academic_year` (`academic_year_id`);

--
-- Indexes for table `student_documents`
--
ALTER TABLE `student_documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `verified_by` (`verified_by`);

--
-- Indexes for table `student_payments`
--
ALTER TABLE `student_payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `student_status_history`
--
ALTER TABLE `student_status_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `changed_by` (`changed_by`),
  ADD KEY `idx_student` (`student_id`),
  ADD KEY `idx_date` (`changed_date`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academic_years`
--
ALTER TABLE `academic_years`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `activity_log`
--
ALTER TABLE `activity_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payment_transactions`
--
ALTER TABLE `payment_transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `sections`
--
ALTER TABLE `sections`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `section_assignments`
--
ALTER TABLE `section_assignments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `student_documents`
--
ALTER TABLE `student_documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student_payments`
--
ALTER TABLE `student_payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student_status_history`
--
ALTER TABLE `student_status_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity_log`
--
ALTER TABLE `activity_log`
  ADD CONSTRAINT `activity_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `payment_transactions`
--
ALTER TABLE `payment_transactions`
  ADD CONSTRAINT `payment_transactions_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payment_transactions_ibfk_2` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_years` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `payment_transactions_ibfk_3` FOREIGN KEY (`recorded_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `sections`
--
ALTER TABLE `sections`
  ADD CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `sections_ibfk_2` FOREIGN KEY (`adviser_id`) REFERENCES `teachers` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `sections_ibfk_3` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_years` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `sections_ibfk_4` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_years` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `section_assignments`
--
ALTER TABLE `section_assignments`
  ADD CONSTRAINT `section_assignments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `section_assignments_ibfk_2` FOREIGN KEY (`section_id`) REFERENCES `sections` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `section_assignments_ibfk_3` FOREIGN KEY (`assigned_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `fk_academic_year` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_years` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `sections` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `students_ibfk_2` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_years` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `students_ibfk_3` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_years` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `student_documents`
--
ALTER TABLE `student_documents`
  ADD CONSTRAINT `student_documents_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `student_documents_ibfk_2` FOREIGN KEY (`verified_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `student_payments`
--
ALTER TABLE `student_payments`
  ADD CONSTRAINT `student_payments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `student_status_history`
--
ALTER TABLE `student_status_history`
  ADD CONSTRAINT `student_status_history_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `student_status_history_ibfk_2` FOREIGN KEY (`changed_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
