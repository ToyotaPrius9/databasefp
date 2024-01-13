-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 12, 2024 at 11:36 PM
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
-- Database: `databasetek`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `customer_name` varchar(255) NOT NULL,
  `customer_email` varchar(100) NOT NULL,
  `customer_phone_number` varchar(20) NOT NULL,
  `customer_address` varchar(300) NOT NULL,
  `points` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `customer_name`, `customer_email`, `customer_phone_number`, `customer_address`, `points`) VALUES
(2, 'Johng Xina', 'fj@fx.com', '9919919', 'Beijing, China', 3),
(3, 'Yes Yes', 'yes.yes@binus.ac.id', '+62 000000000', 'AgainSomewhere, JKT', 0),
(6, 'Sam', 'Samuel@example.com', '919110391', 'Example Example St', 7);

-- --------------------------------------------------------

--
-- Table structure for table `customer_orders`
--

CREATE TABLE `customer_orders` (
  `customer_order_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `item_id` int(11) DEFAULT NULL,
  `item_price` int(100) NOT NULL,
  `item_quantity_ordered` int(11) NOT NULL,
  `sale_time` datetime NOT NULL DEFAULT current_timestamp(),
  `sale_total` int(100) NOT NULL,
  `points_used` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_orders`
--

INSERT INTO `customer_orders` (`customer_order_id`, `customer_id`, `item_id`, `item_price`, `item_quantity_ordered`, `sale_time`, `sale_total`, `points_used`) VALUES
(42, 2, 3, 2200000, 2, '2023-12-30 23:37:21', 3960000, 10),
(43, 2, 7, 2800000, 2, '2023-12-30 23:42:20', 5600000, 0),
(44, 6, 7, 2800000, 2, '2024-01-12 19:52:07', 5600000, 0),
(45, 6, 7, 2800000, 2, '2024-01-12 19:53:25', 5208000, 7),
(46, 2, 7, 2800000, 1, '2024-01-12 20:40:00', 2520000, 10),
(47, 2, 7, 2800000, 1, '2024-01-12 20:41:29', 2716000, 3);

--
-- Triggers `customer_orders`
--
DELIMITER $$
CREATE TRIGGER `after_update_customer_orders` AFTER UPDATE ON `customer_orders` FOR EACH ROW BEGIN
    UPDATE sales
    SET sale_total = NEW.sale_total
    WHERE customer_order_id = NEW.customer_order_id;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `before_insert_customer_orders` BEFORE INSERT ON `customer_orders` FOR EACH ROW BEGIN
    SET NEW.item_price = (SELECT item_price FROM items WHERE item_id = NEW.item_id);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `employee_id` int(11) NOT NULL,
  `employee_name` varchar(100) NOT NULL,
  `employee_role` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`employee_id`, `employee_name`, `employee_role`) VALUES
(1, 'Chester Stone', 'Manager'),
(2, 'Shang Abi', 'Sales'),
(3, 'Kim Jeong', 'Accountant'),
(4, 'Mai Dong', 'Sales'),
(7, 'Da Wok', 'Sales');

-- --------------------------------------------------------

--
-- Table structure for table `employees_attendance`
--

CREATE TABLE `employees_attendance` (
  `employee_id` int(100) NOT NULL,
  `Present_Sessions` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees_attendance`
--

INSERT INTO `employees_attendance` (`employee_id`, `Present_Sessions`) VALUES
(1, 201),
(3, 180),
(4, 90),
(2, 502);

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_id` int(11) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `item_weight` int(11) NOT NULL,
  `item_price` int(100) NOT NULL,
  `item_quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_id`, `item_name`, `item_weight`, `item_price`, `item_quantity`) VALUES
(1, 'Focal Bathys ', 350, 10000000, 30),
(2, 'Focal Utopia ', 490, 10000000, 10),
(3, 'Beats Studio 3 Wireless', 215, 2200000, 28),
(4, 'Sennheiser Momentum 3 WNC', 305, 3000000, 30),
(5, 'Sennheiser Momentum 4', 293, 4000000, 30),
(6, 'Sony WH1000XM4', 254, 3800000, 33),
(7, 'Audio Technica ATH M50xbt', 310, 2800000, 26),
(8, 'Moondrop Venus Planar', 615, 10000000, 30);

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `supplier_id` int(11) NOT NULL,
  `purchase_time` datetime DEFAULT current_timestamp(),
  `supply_order_id` int(11) NOT NULL,
  `purchase_total` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`supplier_id`, `purchase_time`, `supply_order_id`, `purchase_total`) VALUES
(1, '2024-01-12 19:47:40', 8, 4000000),
(1, '2024-01-12 19:48:22', 9, 4000000);

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `customer_id` int(11) NOT NULL,
  `sale_time` datetime NOT NULL DEFAULT current_timestamp(),
  `customer_order_id` int(11) NOT NULL,
  `sale_total` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`customer_id`, `sale_time`, `customer_order_id`, `sale_total`) VALUES
(2, '2023-12-30 23:37:21', 42, 3960000),
(2, '2023-12-30 23:42:20', 43, 5600000),
(6, '2024-01-12 19:52:07', 44, 5600000),
(6, '2024-01-12 19:53:25', 45, 5208000),
(2, '2024-01-12 20:40:00', 46, 2520000),
(2, '2024-01-12 20:41:29', 47, 2716000);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `supplier_id` int(11) NOT NULL,
  `supplier_name` varchar(100) NOT NULL,
  `supplier_email` varchar(320) NOT NULL,
  `supplier_address` varchar(320) NOT NULL,
  `supplier_phone_number` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`supplier_id`, `supplier_name`, `supplier_email`, `supplier_address`, `supplier_phone_number`) VALUES
(1, 'A', 'Focal@example.com', 'Saint-Étienne, France, 23rd Example Street', '+01 111111'),
(2, 'B', 'BeatsByApple@Example.com', 'California, Santa Monica, 3rd Example Ave', '+02 222222'),
(3, 'C', 'Sennheiser@Example.com', 'Wedemark, Germany, 2nd Example Street', '+03 333333'),
(4, 'D', 'AudioTechnica@Example.com', 'Shinjuku, Tokyo, Japan, 9th Example Street', '+04 444444'),
(5, 'E', 'Sony@Example.com', 'Nihonbashi, Chūō, Tokyo, Japan', '+05 555555'),
(6, 'F', 'Moondrop@example.com', 'Wenjiang District, Chengdu, China', '+06 666666'),
(7, 'G', 'Bose@Example.com', 'California, Santa Monica, 12th Example Street', '+07 777777');

-- --------------------------------------------------------

--
-- Table structure for table `supply_orderss`
--

CREATE TABLE `supply_orderss` (
  `supply_order_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `purchase_time` datetime NOT NULL DEFAULT current_timestamp(),
  `supply_quantity_ordered` int(11) NOT NULL,
  `purchase_total` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supply_orderss`
--

INSERT INTO `supply_orderss` (`supply_order_id`, `supplier_id`, `item_id`, `purchase_time`, `supply_quantity_ordered`, `purchase_total`) VALUES
(8, 1, 7, '2024-01-12 19:47:40', 2, 4000000),
(9, 1, 7, '2024-01-12 19:48:22', 2, 4000000);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `customer_email` (`customer_email`),
  ADD UNIQUE KEY `customer_phone_number` (`customer_phone_number`),
  ADD KEY `customer_name` (`customer_name`),
  ADD KEY `customer_address` (`customer_address`),
  ADD KEY `points` (`points`);

--
-- Indexes for table `customer_orders`
--
ALTER TABLE `customer_orders`
  ADD PRIMARY KEY (`customer_order_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `item_id` (`item_id`),
  ADD KEY `item_price` (`item_price`),
  ADD KEY `item_quantity_ordered` (`item_quantity_ordered`),
  ADD KEY `sale_time` (`sale_time`),
  ADD KEY `points_used` (`points_used`),
  ADD KEY `sale_total` (`sale_total`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`employee_id`),
  ADD KEY `Employee Name` (`employee_name`),
  ADD KEY `Employee Role` (`employee_role`);

--
-- Indexes for table `employees_attendance`
--
ALTER TABLE `employees_attendance`
  ADD KEY `employee_id` (`employee_id`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `idx_item_name` (`item_name`),
  ADD KEY `item_name` (`item_name`),
  ADD KEY `item_weight` (`item_weight`),
  ADD KEY `item_quantity` (`item_quantity`),
  ADD KEY `item_price` (`item_price`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
  ADD KEY `supplier_id` (`supplier_id`),
  ADD KEY `supply_order_id` (`supply_order_id`),
  ADD KEY `purchase_time` (`purchase_time`),
  ADD KEY `purchase_total` (`purchase_total`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `customer_order_id` (`customer_order_id`),
  ADD KEY `sale_time` (`sale_time`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`supplier_id`),
  ADD KEY `supplier_id` (`supplier_id`),
  ADD KEY `supplier_address_2` (`supplier_address`),
  ADD KEY `supplier_email` (`supplier_email`),
  ADD KEY `supplier_address` (`supplier_email`),
  ADD KEY `supplier_phone_number` (`supplier_phone_number`),
  ADD KEY `Supplier Name` (`supplier_name`);

--
-- Indexes for table `supply_orderss`
--
ALTER TABLE `supply_orderss`
  ADD PRIMARY KEY (`supply_order_id`),
  ADD KEY `item_id` (`item_id`),
  ADD KEY `supplier_id` (`supplier_id`),
  ADD KEY `purchase_time` (`purchase_time`),
  ADD KEY `purchase_total` (`purchase_total`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `customer_orders`
--
ALTER TABLE `customer_orders`
  MODIFY `customer_order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supplier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `supply_orderss`
--
ALTER TABLE `supply_orderss`
  MODIFY `supply_order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `customer_orders`
--
ALTER TABLE `customer_orders`
  ADD CONSTRAINT `customer_orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  ADD CONSTRAINT `customer_orders_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`);

--
-- Constraints for table `employees_attendance`
--
ALTER TABLE `employees_attendance`
  ADD CONSTRAINT `employees_attendance_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`);

--
-- Constraints for table `purchases`
--
ALTER TABLE `purchases`
  ADD CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`),
  ADD CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`supply_order_id`) REFERENCES `supply_orderss` (`supply_order_id`),
  ADD CONSTRAINT `purchases_ibfk_3` FOREIGN KEY (`purchase_time`) REFERENCES `supply_orderss` (`purchase_time`);

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  ADD CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`customer_order_id`) REFERENCES `customer_orders` (`customer_order_id`),
  ADD CONSTRAINT `sales_ibfk_3` FOREIGN KEY (`sale_time`) REFERENCES `customer_orders` (`sale_time`);

--
-- Constraints for table `supply_orderss`
--
ALTER TABLE `supply_orderss`
  ADD CONSTRAINT `supply_orderss_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`),
  ADD CONSTRAINT `supply_orderss_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
