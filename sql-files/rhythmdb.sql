-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 27, 2024 at 04:24 PM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rhythmdb`
--

-- --------------------------------------------------------
-- Create Database
CREATE DATABASE IF NOT EXISTS rhythmdb;
--

USE rhythmdb;
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
CREATE TABLE IF NOT EXISTS `admins` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `admin_username` varchar(255) NOT NULL,
  `admin_password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`admin_id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `admin_username`, `admin_password`, `created_at`) VALUES
(17, 'admin', 'scrypt:32768:8:1$tigwUNjxpobIU2a9$00d9e2db5d6784952bac030bb4b2ec5f013b0dfc878dada7658835216fcb56d0286e35a0ec5d68bcd6f5f26889e641f849e523705bf71d301be73488340575a3', '2024-03-27 13:32:55');

-- --------------------------------------------------------

--
-- Table structure for table `badges`
--

DROP TABLE IF EXISTS `badges`;
CREATE TABLE IF NOT EXISTS `badges` (
  `badge_id` int NOT NULL AUTO_INCREMENT,
  `badge_name` varchar(256) NOT NULL,
  `badge_url` varchar(256) NOT NULL,
  `badge_desc` varchar(256) NOT NULL,
  PRIMARY KEY (`badge_id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `badges`
--

INSERT INTO `badges` (`badge_id`, `badge_name`, `badge_url`, `badge_desc`) VALUES
(1, 'new', '../static/storage/badges/new.png', 'New Member'),
(3, 'verified', '../static/storage/badges/verified.png', 'Verified Member'),
(4, 'guitar', '../static/storage/badges/guitar.png', 'Guitarist'),
(5, 'piano', '../static/storage/badges/piano.png', 'Pianist'),
(6, 'flute', '../static/storage/badges/flute.png', 'Flautist '),
(7, 'listen', '../static/storage/badges/listen.png', 'Music Enjoyer'),
(8, 'drum', '../static/storage/badges/drum.png', 'Drummer');

-- --------------------------------------------------------

--
-- Table structure for table `banned_users`
--

DROP TABLE IF EXISTS `banned_users`;
CREATE TABLE IF NOT EXISTS `banned_users` (
  `ban_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `banTimestamp` timestamp NOT NULL,
  `banReason` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`ban_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
CREATE TABLE IF NOT EXISTS `comments` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  `comment_text` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `comment_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`),
  KEY `user_id` (`user_id`),
  KEY `post_id` (`post_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `deleted_posts`
--

DROP TABLE IF EXISTS `deleted_posts`;
CREATE TABLE IF NOT EXISTS `deleted_posts` (
  `dlt_post_id` int NOT NULL AUTO_INCREMENT,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `caption` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `tags` varchar(50) DEFAULT NULL,
  `media_url` varchar(255) DEFAULT NULL,
  `media_type` enum('photo','video') DEFAULT NULL,
  `timestamp` timestamp NOT NULL,
  `deleted_by` varchar(255) NOT NULL,
  PRIMARY KEY (`dlt_post_id`),
  KEY `user_id` (`user_id`),
  KEY `post_id` (`post_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `discussion_forums`
--

DROP TABLE IF EXISTS `discussion_forums`;
CREATE TABLE IF NOT EXISTS `discussion_forums` (
  `df_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `creation_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`df_id`),
  KEY `creater` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `discussion_forums`
--

INSERT INTO `discussion_forums` (`df_id`, `user_id`, `title`, `creation_timestamp`) VALUES
(3, 1, 'Hello Guys! This is a demo Forum!', '2024-03-27 16:20:40');

-- --------------------------------------------------------

--
-- Table structure for table `discussion_forums_comments`
--

DROP TABLE IF EXISTS `discussion_forums_comments`;
CREATE TABLE IF NOT EXISTS `discussion_forums_comments` (
  `df_cmnt_id` int NOT NULL AUTO_INCREMENT,
  `df_id` int NOT NULL,
  `user_id` int NOT NULL,
  `comment` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `comment_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`df_cmnt_id`),
  KEY `df_id` (`df_id`),
  KEY `userid` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `discussion_forums_comments`
--

INSERT INTO `discussion_forums_comments` (`df_cmnt_id`, `df_id`, `user_id`, `comment`, `comment_timestamp`) VALUES
(4, 3, 1, 'Github - x0tic0p', '2024-03-27 16:21:19');

-- --------------------------------------------------------

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
CREATE TABLE IF NOT EXISTS `followers` (
  `follow_id` int NOT NULL AUTO_INCREMENT,
  `source_user_id` int NOT NULL,
  `target_user_id` int NOT NULL,
  `follow_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`follow_id`),
  KEY `source_user_id` (`source_user_id`),
  KEY `target_user_id` (`target_user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lessons`
--

DROP TABLE IF EXISTS `lessons`;
CREATE TABLE IF NOT EXISTS `lessons` (
  `lesson_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `caption` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `media_url` varchar(255) DEFAULT NULL,
  `media_type` enum('photo','video') DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `approval_status` enum('approved','pending','declined') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`lesson_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
CREATE TABLE IF NOT EXISTS `likes` (
  `like_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `post_id` int DEFAULT NULL,
  `like_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`like_id`),
  KEY `user_id` (`user_id`),
  KEY `post_id` (`post_id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
CREATE TABLE IF NOT EXISTS `messages` (
  `msg_id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `content` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`msg_id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
CREATE TABLE IF NOT EXISTS `posts` (
  `post_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `caption` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `tags` varchar(50) DEFAULT NULL,
  `media_url` varchar(255) DEFAULT NULL,
  `media_type` enum('photo','video') DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`post_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_id`, `user_id`, `caption`, `tags`, `media_url`, `media_type`, `timestamp`) VALUES
(11, 1, 'Classic!', NULL, '../static/storage/posts/photos\\gJrEtha99H0eewihlPDYi7lDT932M078YRaUK8VVKny6nH9d8ffQ4UK6UWIHs0tHNanIqsTzkwNQQu7L.jpg', 'photo', '2024-03-27 16:19:32');

-- --------------------------------------------------------

--
-- Table structure for table `sheet_music`
--

DROP TABLE IF EXISTS `sheet_music`;
CREATE TABLE IF NOT EXISTS `sheet_music` (
  `sheet_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `caption` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `media_url` varchar(255) DEFAULT NULL,
  `media_type` enum('photo','video') DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `approval_status` enum('approved','pending','declined') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`sheet_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `sheet_music`
--

INSERT INTO `sheet_music` (`sheet_id`, `user_id`, `caption`, `media_url`, `media_type`, `timestamp`, `approval_status`) VALUES
(2, 1, '...', '../static/storage/posts/photos\\Dc-QErnOJ5XRyoou9EtWs-fR24ZmTPbLfHhLIMZWHckuRC4i1SApgn6x-8VQAEBgY9jXXCs3w0VSZmWM.png', 'photo', '2024-03-27 16:19:44', 'approved');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_pass` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `display_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_dob` date DEFAULT NULL,
  `user_bio` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_pfp` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '../static/storage/pfps/default_pfp.png',
  `user_badges` json DEFAULT NULL,
  `user_interests` json DEFAULT NULL,
  `user_creation_timestamp` timestamp NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `user_pass`, `display_name`, `user_email`, `user_dob`, `user_bio`, `user_pfp`, `user_badges`, `user_interests`, `user_creation_timestamp`) VALUES
(1, 'user', 'scrypt:32768:8:1$5HCbdQ8K4oC509mm$e3c5c9e0dc01081e303457d3a5abe2da9fce7c355fc29f2ba1894029da4b14393dfa7b45d0013db4f98eb732817e788c5d38b9c7e20dc338ed01d8fcb0044ff5', 'Test User', 'example@gmail.com', '2004-01-22', 'Github - x0tic0p', '../static/storage/pfps\\default_pfp.png', '[{\"new\": \"equipped\", \"drum\": \"notequipped\", \"flute\": \"notequipped\", \"piano\": \"notequipped\", \"guitar\": \"notequipped\", \"listen\": \"notequipped\"}]', NULL, '2024-03-04 13:27:26');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
