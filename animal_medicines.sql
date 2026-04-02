-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 02, 2026 at 06:59 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `animal_medicines`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_users`
--

CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `otp` varchar(10) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `phone_number` varchar(20) DEFAULT NULL,
  `organization` varchar(100) DEFAULT NULL,
  `position` varchar(100) DEFAULT NULL,
  `location` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_users`
--

INSERT INTO `admin_users` (`id`, `username`, `email`, `password`, `otp`, `otp_expiry`, `created_at`, `phone_number`, `organization`, `position`, `location`) VALUES
(1, 'Niranjan Admin11', 'gniranjan1523@gmail.com', 'Gvenni@11', NULL, NULL, '2026-03-30 05:53:45', '7799099493', 'ResidueSafe Global', 'Lead System Architect', 'Chennai, Tamil Nadu');

-- --------------------------------------------------------

--
-- Table structure for table `animals`
--

CREATE TABLE `animals` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `species` varchar(50) NOT NULL,
  `tag_id` varchar(50) NOT NULL,
  `animal_name` varchar(100) DEFAULT '',
  `dob` date NOT NULL,
  `gender` varchar(20) NOT NULL,
  `weight_kg` varchar(50) NOT NULL,
  `breed` varchar(100) DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `animals`
--

INSERT INTO `animals` (`id`, `user_id`, `species`, `tag_id`, `animal_name`, `dob`, `gender`, `weight_kg`, `breed`, `created_at`) VALUES
(4, 4, 'Cow', 'cow-001', '', '2021-03-30', '---', '30', '', '2026-03-30 18:05:29'),
(5, 4, 'Buffalo', 'Buffalo-001', '', '2022-03-30', '---', '50', '', '2026-03-30 18:05:54'),
(6, 4, 'Pig', 'pig-001', '', '2024-03-30', '---', '10', '', '2026-03-30 18:06:10'),
(7, 4, 'Sheep', 'sheep-002', '', '2021-03-30', '---', '20', '', '2026-03-30 18:06:30'),
(8, 4, 'Goat', 'Goat-001', '', '2011-03-30', '---', '20', '', '2026-03-30 18:06:55'),
(9, 4, 'Hen', 'Hen-001', '', '2024-03-30', '---', '50', '', '2026-03-30 18:07:29');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `farm_name` varchar(100) NOT NULL,
  `otp` varchar(10) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `role` varchar(20) DEFAULT 'farmer',
  `phone_number` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `full_name`, `email`, `password`, `farm_name`, `otp`, `otp_expiry`, `created_at`, `role`, `phone_number`) VALUES
(4, 'Vennela', 'gvennela1105@gmail.com', 'scrypt:32768:8:1$3AWwmaFlc6zJLvsE$7410420c808cad617e0df94b00fd9f7582696af6705a72297c208b650034acd0db06b2a3c4584a98d60b71db7316f17a2c7d5c8a4c9810bca363008fb077c301', 'VennuFarms ', NULL, NULL, '2026-03-30 18:03:10', 'farmer', '');

-- --------------------------------------------------------

--
-- Table structure for table `treatments`
--

CREATE TABLE `treatments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `animal_tag_id` varchar(50) NOT NULL,
  `animal_type` varchar(50) NOT NULL,
  `drug_name` varchar(100) NOT NULL,
  `dosage` varchar(100) NOT NULL,
  `treatment_date` date NOT NULL,
  `meat_safe_date` date DEFAULT NULL,
  `milk_safe_date` date DEFAULT NULL,
  `egg_safe_date` date DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `treatments`
--

INSERT INTO `treatments` (`id`, `user_id`, `animal_tag_id`, `animal_type`, `drug_name`, `dosage`, `treatment_date`, `meat_safe_date`, `milk_safe_date`, `egg_safe_date`, `notes`, `status`, `created_at`) VALUES
(3, 4, 'Hen-001', 'Hen', 'Dolo', '10ml', '2026-03-30', '2026-04-27', '2026-04-06', '2026-04-06', '[Statutory Minimum Applied]', 'Active', '2026-03-30 18:08:09'),
(4, 4, 'Hen-001', 'Hen', 'Tylosin', '10ml', '2026-03-30', '2026-03-31', '2026-03-30', '2026-03-30', '', 'Active', '2026-03-30 18:10:40'),
(12, 4, 'sheep-002', 'Sheep', 'Amoxicillin', '1.5ml', '2026-03-31', '2026-04-09', '2026-04-04', '2026-03-31', '', 'Active', '2026-03-31 09:03:08'),
(13, 4, 'cow-001', 'Cow', 'Penicillin G', '10ml', '2026-03-31', '2026-04-10', '2026-04-03', '2026-03-31', '', 'Active', '2026-03-31 10:03:15'),
(14, 4, 'cow-001', 'Cow', 'Ceftiofur', '100ml', '2026-04-01', '2026-04-01', '2026-04-01', '2026-04-01', '', 'Active', '2026-04-01 07:35:32'),
(15, 4, 'COW--222', 'Cow', 'Albendazole', '500ML', '2026-04-01', '2026-04-28', '2026-04-04', '2026-04-01', 'DFSDRGTDRG', 'Active', '2026-04-01 07:56:03');

-- --------------------------------------------------------

--
-- Table structure for table `withdrawlstatus`
--

CREATE TABLE `withdrawlstatus` (
  `COL 1` varchar(7) DEFAULT NULL,
  `COL 2` varchar(18) DEFAULT NULL,
  `COL 3` int(2) DEFAULT NULL,
  `COL 4` varchar(2) DEFAULT NULL,
  `COL 5` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `withdrawlstatus`
--

INSERT INTO `withdrawlstatus` (`COL 1`, `COL 2`, `COL 3`, `COL 4`, `COL 5`) VALUES
('cow', 'Penicillin G', 10, '3', '0'),
('Cow', 'Oxytetracycline', 28, '4', 'NA'),
('Cow', 'Ivermectin', 48, '0', 'NA'),
('Cow', 'Amoxicillin', 9, '3', 'NA'),
('Cow', 'Ceftiofur', 0, '0', 'NA'),
('Cow', 'Enrofloxacin', 28, '0', 'NA'),
('Cow', 'Sulfaquinoxaline', 10, '4', 'NA'),
('Cow', 'Fenbendazole', 8, '0', 'NA'),
('Cow', 'Albendazole', 27, '3', 'NA'),
('Cow', 'Meloxicam', 15, '5', 'NA'),
('Cow', 'Dexamethasone', 7, '3', 'NA'),
('Cow', 'Tylosin', 21, '4', 'NA'),
('Cow', 'Florfenicol', 28, '0', 'NA'),
('Cow', 'Gentamicin', 30, '5', 'NA'),
('Cow', 'Tilmicosin', 28, '0', 'NA'),
('Cow', 'Moxidectin', 14, '0', 'NA'),
('Cow', 'Doramectin', 35, '0', 'NA'),
('Cow', 'Clorsulon', 8, '0', 'NA'),
('Cow', 'Ketoprofen', 4, '2', 'NA'),
('Cow', 'Flunixin', 4, '2', 'NA'),
('cow', 'Penicillin G', 10, '3', '0'),
('Goat', 'Oxytetracycline', 28, '4', 'NA'),
('Goat', 'Ivermectin', 11, '0', 'NA'),
('Goat', 'Amoxicillin', 9, '4', 'NA'),
('Goat', 'Fenbendazole', 6, '0', 'NA'),
('Goat', 'Albendazole', 7, '3', 'NA'),
('Goat', 'Meloxicam', 15, '5', 'NA'),
('Goat', 'Enrofloxacin', 28, '0', 'NA'),
('Goat', 'Tylosin', 21, '4', 'NA'),
('Goat', 'Moxidectin', 14, '0', 'NA'),
('Goat', 'Ceftiofur', 0, '0', 'NA'),
('Goat', 'Florfenicol', 28, '0', 'NA'),
('Goat', 'Sulfaquinoxaline', 10, '4', 'NA'),
('Goat', 'Dexamethasone', 7, '3', 'NA'),
('Goat', 'Levamisole', 3, '0', 'NA'),
('Goat', 'Monensin', 0, '0', 'NA'),
('Goat', 'Sulfadimethoxine', 7, '3', 'NA'),
('Goat', 'Trimethoprim/Sulfa', 10, '4', 'NA'),
('Goat', 'Eprinomectin', 0, '0', 'NA'),
('Goat', 'Thiamine', 0, '0', 'NA'),
('cow', 'Penicillin G', 10, '3', '0'),
('Hen', 'Oxytetracycline', 5, 'NA', '0'),
('Hen', 'Amprolium', 0, 'NA', '0'),
('Hen', 'Tylosin', 1, 'NA', '0'),
('Hen', 'Bacitracin', 0, 'NA', '0'),
('Hen', 'Sulfaquinoxaline', 10, 'NA', '10'),
('Hen', 'Piperazine', 14, 'NA', '0'),
('Hen', 'Erythromycin', 1, 'NA', '0'),
('Hen', 'Chlortetracycline', 1, 'NA', '0'),
('Hen', 'Lasalocid', 3, 'NA', 'NA'),
('Hen', 'Monensin', 0, 'NA', 'NA'),
('Hen', 'Nystatin', 0, 'NA', '0'),
('Hen', 'Levamisole', 7, 'NA', '9'),
('Hen', 'Ivermectin', 14, 'NA', '7'),
('Hen', 'Fenbendazole', 0, 'NA', '0'),
('Hen', 'Albendazole', 14, 'NA', '7'),
('Hen', 'Flubendazole', 7, 'NA', '0'),
('Hen', 'Sulfadimethoxine', 5, 'NA', '5'),
('Hen', 'Enrofloxacin', 14, 'NA', '14'),
('Hen', 'Lincomycin', 0, 'NA', '0'),
('cow', 'Penicillin G', 10, '3', '0'),
('Buffalo', 'Oxytetracycline', 28, '5', 'NA'),
('Buffalo', 'Ivermectin', 48, '0', 'NA'),
('Buffalo', 'Amoxicillin', 10, '3', 'NA'),
('Buffalo', 'Ceftiofur', 0, '0', 'NA'),
('Buffalo', 'Enrofloxacin', 28, '0', 'NA'),
('Buffalo', 'Fenbendazole', 8, '0', 'NA'),
('Buffalo', 'Albendazole', 27, '4', 'NA'),
('Buffalo', 'Tylosin', 21, '5', 'NA'),
('Buffalo', 'Florfenicol', 30, '0', 'NA'),
('Buffalo', 'Meloxicam', 15, '6', 'NA'),
('Buffalo', 'Dexamethasone', 7, '4', 'NA'),
('Buffalo', 'Gentamicin', 35, '6', 'NA'),
('Buffalo', 'Doramectin', 42, '0', 'NA'),
('Buffalo', 'Moxidectin', 14, '0', 'NA'),
('Buffalo', 'Ketoprofen', 4, '3', 'NA'),
('Buffalo', 'Flunixin', 4, '3', 'NA'),
('Buffalo', 'Tilmicosin', 28, '0', 'NA'),
('Buffalo', 'Eprinomectin', 0, '0', 'NA'),
('Buffalo', 'Levamisole', 3, '0', 'NA'),
('cow', 'Penicillin G', 10, '3', '0'),
('Sheep', 'Oxytetracycline', 28, '4', 'NA'),
('Sheep', 'Ivermectin', 11, '0', 'NA'),
('Sheep', 'Amoxicillin', 9, '4', 'NA'),
('Sheep', 'Fenbendazole', 6, '0', 'NA'),
('Sheep', 'Albendazole', 7, '3', 'NA'),
('Sheep', 'Meloxicam', 15, '5', 'NA'),
('Sheep', 'Moxidectin', 14, '0', 'NA'),
('Sheep', 'Ceftiofur', 0, '0', 'NA'),
('Sheep', 'Florfenicol', 28, '0', 'NA'),
('Sheep', 'Levamisole', 3, '0', 'NA'),
('Sheep', 'Monensin', 0, '0', 'NA'),
('Sheep', 'Sulfadimethoxine', 7, '3', 'NA'),
('Sheep', 'Trimethoprim/Sulfa', 10, '4', 'NA'),
('Sheep', 'Eprinomectin', 0, '0', 'NA'),
('Sheep', 'Tylosin', 21, '4', 'NA'),
('Sheep', 'Dexamethasone', 7, '3', 'NA'),
('Sheep', 'Doramectin', 35, '0', 'NA'),
('Sheep', 'Clorsulon', 8, '0', 'NA'),
('Sheep', 'Ketoprofen', 4, '2', 'NA'),
('cow, he', 'Dolo', 2, '2', '10'),
('1', '1', 1, '1', '1'),
('1', '1', 1, '1', '1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_users`
--
ALTER TABLE `admin_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `animals`
--
ALTER TABLE `animals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `treatments`
--
ALTER TABLE `treatments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_users`
--
ALTER TABLE `admin_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `animals`
--
ALTER TABLE `animals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `register`
--
ALTER TABLE `register`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `treatments`
--
ALTER TABLE `treatments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `animals`
--
ALTER TABLE `animals`
  ADD CONSTRAINT `animals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `register` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `treatments`
--
ALTER TABLE `treatments`
  ADD CONSTRAINT `treatments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `register` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
