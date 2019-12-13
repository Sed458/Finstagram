-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8890
-- Generation Time: Dec 12, 2019 at 11:23 PM
-- Server version: 5.7.26
-- PHP Version: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `Finstagram`
--

-- --------------------------------------------------------

--
-- Table structure for table `BelongTo`
--

CREATE TABLE `BelongTo` (
  `member_username` varchar(20) NOT NULL,
  `owner_username` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `BelongTo`
--

INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES
('A', 'A', 'NYU'),
('B', 'A', 'NYU'),
('A', 'C', 'best friends');

-- --------------------------------------------------------

--
-- Table structure for table `Follow`
--

CREATE TABLE `Follow` (
  `username_followed` varchar(20) NOT NULL,
  `username_follower` varchar(20) NOT NULL,
  `followstatus` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Follow`
--

INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES
('A', 'B', 1),
('A', 'C', 1),
('B', 'A', 1),
('B', 'D', 1),
('B', 'E', 1),
('C', 'A', 1),
('C', 'D', 1),
('D', 'A', 0),
('E', 'A', 1);

-- --------------------------------------------------------

--
-- Table structure for table `Friendgroup`
--

CREATE TABLE `Friendgroup` (
  `groupOwner` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  `description` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Friendgroup`
--

INSERT INTO `Friendgroup` (`groupOwner`, `groupName`, `description`) VALUES
('A', 'NYU', NULL),
('C', 'best friends', 'Cathy\'s best friends'),
('D', 'best friends', 'Dave\'s best friends');

-- --------------------------------------------------------

--
-- Table structure for table `Likes`
--

CREATE TABLE `Likes` (
  `username` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  `liketime` datetime DEFAULT NULL,
  `rating` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Likes`
--

INSERT INTO `Likes` (`username`, `photoID`, `liketime`, `rating`) VALUES
('D', 1, '2019-12-11 00:00:00', 5),
('D', 2, '2019-12-11 00:00:00', 5),
('E', 1, '2019-12-11 00:00:00', 3);

-- --------------------------------------------------------

--
-- Table structure for table `Person`
--

CREATE TABLE `Person` (
  `username` varchar(20) NOT NULL,
  `password` char(64) DEFAULT NULL,
  `firstName` varchar(20) DEFAULT NULL,
  `lastName` varchar(20) DEFAULT NULL,
  `bio` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Person`
--

INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`) VALUES
('A', '559aead08264d5795d3909718cdd05abd49572e84fe55590eef31a88a08fdffd', 'Ann', 'Andrews', 'Ann is awesome'),
('B', 'B', 'Bill', 'Barker', 'Bill is a big shot'),
('C', 'C', 'Cathy', 'Chen', 'Cathy is charismatic'),
('D', 'D', 'Dave', 'Davis', 'Dave is diligent'),
('E', 'E', 'Emily', 'Elhaj', 'Emily is energetic');

-- --------------------------------------------------------

--
-- Table structure for table `Photo`
--

CREATE TABLE `Photo` (
  `photoID` int(11) NOT NULL,
  `postingdate` datetime DEFAULT NULL,
  `filepath` varchar(100) DEFAULT NULL,
  `allFollowers` tinyint(1) DEFAULT NULL,
  `caption` varchar(100) DEFAULT NULL,
  `photoPoster` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Photo`
--

INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES
(1, '2019-12-10 00:00:00', 'photo1B.jpg', 1, 'photo 1', 'B'),
(2, '2019-12-11 00:00:00', 'photo2C.jpg', 1, 'photo 2', 'C'),
(3, '2019-12-12 00:00:00', 'photo3D.jpg', 1, 'photo 3', 'D'),
(4, '2019-12-13 00:00:00', 'photo4D.jpg', 1, NULL, 'D'),
(5, '2019-12-14 00:00:00', 'photo5E.jpg', 0, 'photo 5', 'E'),
(6, '2019-12-12 14:18:12', 'Five.png', 1, 'High Five', 'A'),
(7, '2019-12-12 14:18:40', 'HandFull.jpg', 0, 'Full', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `SharedWith`
--

CREATE TABLE `SharedWith` (
  `groupOwner` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `SharedWith`
--

INSERT INTO `SharedWith` (`groupOwner`, `groupName`, `photoID`) VALUES
('C', 'best friends', 2),
('D', 'best friends', 3);

-- --------------------------------------------------------

--
-- Table structure for table `Tagged`
--

CREATE TABLE `Tagged` (
  `username` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  `tagstatus` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Tagged`
--

INSERT INTO `Tagged` (`username`, `photoID`, `tagstatus`) VALUES
('D', 1, 1),
('D', 2, 1),
('E', 1, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `BelongTo`
--
ALTER TABLE `BelongTo`
  ADD PRIMARY KEY (`member_username`,`owner_username`,`groupName`),
  ADD KEY `owner_username` (`owner_username`,`groupName`);

--
-- Indexes for table `Follow`
--
ALTER TABLE `Follow`
  ADD PRIMARY KEY (`username_followed`,`username_follower`),
  ADD KEY `username_follower` (`username_follower`);

--
-- Indexes for table `Friendgroup`
--
ALTER TABLE `Friendgroup`
  ADD PRIMARY KEY (`groupOwner`,`groupName`);

--
-- Indexes for table `Likes`
--
ALTER TABLE `Likes`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- Indexes for table `Person`
--
ALTER TABLE `Person`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `Photo`
--
ALTER TABLE `Photo`
  ADD PRIMARY KEY (`photoID`),
  ADD KEY `photoPoster` (`photoPoster`);

--
-- Indexes for table `SharedWith`
--
ALTER TABLE `SharedWith`
  ADD PRIMARY KEY (`groupOwner`,`groupName`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- Indexes for table `Tagged`
--
ALTER TABLE `Tagged`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Photo`
--
ALTER TABLE `Photo`
  MODIFY `photoID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `BelongTo`
--
ALTER TABLE `BelongTo`
  ADD CONSTRAINT `belongto_ibfk_1` FOREIGN KEY (`member_username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `belongto_ibfk_2` FOREIGN KEY (`owner_username`,`groupName`) REFERENCES `Friendgroup` (`groupOwner`, `groupName`);

--
-- Constraints for table `Follow`
--
ALTER TABLE `Follow`
  ADD CONSTRAINT `follow_ibfk_1` FOREIGN KEY (`username_followed`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `follow_ibfk_2` FOREIGN KEY (`username_follower`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Friendgroup`
--
ALTER TABLE `Friendgroup`
  ADD CONSTRAINT `friendgroup_ibfk_1` FOREIGN KEY (`groupOwner`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Likes`
--
ALTER TABLE `Likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

--
-- Constraints for table `Photo`
--
ALTER TABLE `Photo`
  ADD CONSTRAINT `photo_ibfk_1` FOREIGN KEY (`photoPoster`) REFERENCES `Person` (`username`);

--
-- Constraints for table `SharedWith`
--
ALTER TABLE `SharedWith`
  ADD CONSTRAINT `sharedwith_ibfk_1` FOREIGN KEY (`groupOwner`,`groupName`) REFERENCES `Friendgroup` (`groupOwner`, `groupName`),
  ADD CONSTRAINT `sharedwith_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

--
-- Constraints for table `Tagged`
--
ALTER TABLE `Tagged`
  ADD CONSTRAINT `tagged_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `tagged_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);
