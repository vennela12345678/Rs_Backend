CREATE DATABASE IF NOT EXISTS `animal_medicines`;
USE `animal_medicines`;


CREATE TABLE IF NOT EXISTS `register` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `full_name` varchar(100) NOT NULL,
    `email` varchar(150) NOT NULL,
    `password` varchar(255) NOT NULL,
    `farm_name` varchar(100) NOT NULL,
    `otp` varchar(10) DEFAULT NULL,
    `otp_expiry` datetime DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `role` varchar(20) DEFAULT 'farmer',
    `phone_number` varchar(20) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `admin_users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `email` varchar(100) NOT NULL,
    `password` varchar(255) NOT NULL,
    `otp` varchar(10) DEFAULT NULL,
    `otp_expiry` datetime DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `phone_number` varchar(20) DEFAULT NULL,
    `organization` varchar(100) DEFAULT NULL,
    `position` varchar(100) DEFAULT NULL,
    `location` varchar(150) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `withdrawlstatus` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `COL 1` varchar(100) NOT NULL, -- Species
    `COL 2` varchar(100) NOT NULL, -- Drug Name
    `COL 3` varchar(50) DEFAULT '0', -- Meat Withdrawal Days
    `COL 4` varchar(50) DEFAULT '0', -- Milk Withdrawal Days
    `COL 5` varchar(50) DEFAULT 'NA', -- Eggs Withdrawal Days
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `animals` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `species` varchar(50) NOT NULL,
    `tag_id` varchar(50) NOT NULL,
    `animal_name` varchar(100) DEFAULT '',
    `dob` date NOT NULL,
    `gender` varchar(20) NOT NULL,
    `weight_kg` varchar(50) NOT NULL,
    `breed` varchar(100) DEFAULT '',
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `register`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `treatments` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `animal_tag_id` varchar(50) NOT NULL,
    `animal_type` varchar(50) NOT NULL,
    `drug_name` varchar(100) NOT NULL,
    `dosage` varchar(100) NOT NULL,
    `treatment_date` date NOT NULL,
    `meat_safe_date` date DEFAULT NULL,
    `milk_safe_date` date DEFAULT NULL,
    `egg_safe_date` date DEFAULT NULL,
    `notes` text,
    `status` varchar(20) DEFAULT 'Active',
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `register`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
