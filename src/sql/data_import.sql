/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.20.31_23306
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44)
 Source Host           : 192.168.20.31:23306
 Source Schema         : fashion

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44)
 File Encoding         : 65001

 Date: 05/07/2024 20:56:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for customers
-- ----------------------------
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Customer ID',
  `customer_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Customer Name',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of customers
-- ----------------------------
INSERT INTO `customers` (customer_name) VALUES ('PolyU');
INSERT INTO `customers` (customer_name) VALUES ('John');
INSERT INTO `customers` (customer_name) VALUES ('Emily');
INSERT INTO `customers` (customer_name) VALUES ('James');
INSERT INTO `customers` (customer_name) VALUES ('Sophia');
INSERT INTO `customers` (customer_name) VALUES ('Michael');
INSERT INTO `customers` (customer_name) VALUES ('Olivia');
INSERT INTO `customers` (customer_name) VALUES ('William');

-- ----------------------------
-- Table structure for cutting_material_allocation
-- ----------------------------
DROP TABLE IF EXISTS `cutting_material_allocation`;
CREATE TABLE `cutting_material_allocation`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Cutting Task Material Allocation ID',
  `warehouse_material_id` int UNSIGNED NULL COMMENT 'Warehouse Material ID',
  `cutting_task_id` int UNSIGNED NOT NULL COMMENT 'Cutting Task ID',
  `allocated_num` int(11) NOT NULL DEFAULT 0 COMMENT 'Allocated Material Quantity',
  `is_allocated` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Is Material Allocated',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cutting_task_id`(`cutting_task_id`) USING BTREE,
  INDEX `warehouse_material_id`(`warehouse_material_id`) USING BTREE,
  CONSTRAINT `cutting_material_allocation_ibfk_1` FOREIGN KEY (`cutting_task_id`) REFERENCES `cutting_tasks` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cutting_material_allocation_ibfk_2` FOREIGN KEY (`warehouse_material_id`) REFERENCES `warehouse_material` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of cutting_material_allocation
-- ----------------------------
INSERT INTO `cutting_material_allocation` VALUES (1, 1, 1, 100, 1);
INSERT INTO `cutting_material_allocation` VALUES (10, 11, 10, 100, 1);
INSERT INTO `cutting_material_allocation` VALUES (11, 3, 11, 140, 1);
INSERT INTO `cutting_material_allocation` VALUES (12, 5, 11, 140, 1);
INSERT INTO `cutting_material_allocation` VALUES (13, 3, 12, 150, 1);
INSERT INTO `cutting_material_allocation` VALUES (14, 5, 12, 150, 1);
INSERT INTO `cutting_material_allocation` VALUES (15, 3, 13, 130, 1);
INSERT INTO `cutting_material_allocation` VALUES (16, 5, 13, 130, 1);
INSERT INTO `cutting_material_allocation` VALUES (17, 3, 14, 120, 1);
INSERT INTO `cutting_material_allocation` VALUES (18, 5, 14, 120, 1);
INSERT INTO `cutting_material_allocation` VALUES (19, 3, 15, 185, 1);
INSERT INTO `cutting_material_allocation` VALUES (2, 1, 2, 240, 1);
INSERT INTO `cutting_material_allocation` VALUES (20, 7, 15, 185, 1);
INSERT INTO `cutting_material_allocation` VALUES (21, 13, 16, 200, 1);
INSERT INTO `cutting_material_allocation` VALUES (22, 3, 16, 200, 1);
INSERT INTO `cutting_material_allocation` VALUES (23, 7, 16, 200, 1);
INSERT INTO `cutting_material_allocation` VALUES (24, 3, 17, 175, 1);
INSERT INTO `cutting_material_allocation` VALUES (25, 7, 17, 175, 1);
INSERT INTO `cutting_material_allocation` VALUES (26, 3, 18, 200, 1);
INSERT INTO `cutting_material_allocation` VALUES (27, 7, 18, 200, 1);
INSERT INTO `cutting_material_allocation` VALUES (28, 1, 19, 95, 1);
INSERT INTO `cutting_material_allocation` VALUES (29, 9, 19, 95, 1);
INSERT INTO `cutting_material_allocation` VALUES (3, 1, 3, 150, 1);
INSERT INTO `cutting_material_allocation` VALUES (30, 3, 20, 90, 1);
INSERT INTO `cutting_material_allocation` VALUES (31, 7, 20, 90, 1);
INSERT INTO `cutting_material_allocation` VALUES (32, 1, 21, 85, 1);
INSERT INTO `cutting_material_allocation` VALUES (33, 9, 21, 85, 1);
INSERT INTO `cutting_material_allocation` VALUES (34, 3, 22, 115, 1);
INSERT INTO `cutting_material_allocation` VALUES (35, 11, 23, 110, 1);
INSERT INTO `cutting_material_allocation` VALUES (36, 11, 24, 105, 1);
INSERT INTO `cutting_material_allocation` VALUES (37, 13, 25, 75, 1);
INSERT INTO `cutting_material_allocation` VALUES (38, 3, 25, 75, 1);
INSERT INTO `cutting_material_allocation` VALUES (39, 7, 25, 75, 1);
INSERT INTO `cutting_material_allocation` VALUES (4, 1, 4, 220, 1);
INSERT INTO `cutting_material_allocation` VALUES (40, 3, 26, 70, 1);
INSERT INTO `cutting_material_allocation` VALUES (41, 3, 27, 60, 1);
INSERT INTO `cutting_material_allocation` VALUES (42, 7, 27, 60, 1);
INSERT INTO `cutting_material_allocation` VALUES (43, 13, 27, 60, 1);
INSERT INTO `cutting_material_allocation` VALUES (44, 1, 28, 210, 1);
INSERT INTO `cutting_material_allocation` VALUES (45, 9, 28, 210, 1);
INSERT INTO `cutting_material_allocation` VALUES (46, 3, 29, 180, 1);
INSERT INTO `cutting_material_allocation` VALUES (47, 11, 30, 195, 1);
INSERT INTO `cutting_material_allocation` VALUES (48, 1, 31, 260, 0);
INSERT INTO `cutting_material_allocation` VALUES (49, 9, 31, 260, 0);
INSERT INTO `cutting_material_allocation` VALUES (5, 1, 5, 260, 1);
INSERT INTO `cutting_material_allocation` VALUES (50, 3, 32, 150, 0);
INSERT INTO `cutting_material_allocation` VALUES (51, 7, 32, 150, 0);
INSERT INTO `cutting_material_allocation` VALUES (52, 11, 33, 120, 0);
INSERT INTO `cutting_material_allocation` VALUES (53, 1, 34, 330, 0);
INSERT INTO `cutting_material_allocation` VALUES (54, 9, 34, 330, 0);
INSERT INTO `cutting_material_allocation` VALUES (6, 11, 6, 95, 1);
INSERT INTO `cutting_material_allocation` VALUES (7, 11, 7, 110, 1);
INSERT INTO `cutting_material_allocation` VALUES (8, 11, 8, 50, 1);
INSERT INTO `cutting_material_allocation` VALUES (9, 11, 9, 80, 1);

-- ----------------------------
-- Table structure for cutting_tasks
-- ----------------------------
DROP TABLE IF EXISTS `cutting_tasks`;
CREATE TABLE `cutting_tasks`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Cutting Task ID',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Cutting Task Start Time',
  `end_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Cutting Task End Time',
  `working_group_id` int UNSIGNED NOT NULL COMMENT 'Working Group ID',
  `order_product_id` int UNSIGNED NOT NULL COMMENT 'Order Product ID',
  `produced_wip_id` int UNSIGNED NOT NULL COMMENT 'Produced WIP material ID',
  `planned_number` int(11) NOT NULL DEFAULT 0 COMMENT 'Planned Cutting Quantity',
  `completed_number` int(11) NOT NULL DEFAULT 0 COMMENT 'Completed Cutting Quantity',
  `status` int(11) NOT NULL DEFAULT 0 COMMENT 'Status of the task 0: not start, 1: on-going, 2: completed',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `working_group_id`(`working_group_id`) USING BTREE,
  INDEX `order_product_id`(`order_product_id`) USING BTREE,
  CONSTRAINT `cutting_tasks_ibfk_1` FOREIGN KEY (`working_group_id`) REFERENCES `working_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cutting_tasks_ibfk_2` FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of cutting_tasks
-- ----------------------------
INSERT INTO `cutting_tasks` VALUES (1 ,'2024-01-10 00:00:00', '2024-01-18 00:00:00', 2, 1,  2, 100, 100, 2);
INSERT INTO `cutting_tasks` VALUES (10, '2024-03-02 00:00:00', '2024-03-29 00:00:00', 3, 10,4, 100, 100, 1);
INSERT INTO `cutting_tasks` VALUES (11, '2024-03-02 00:00:00', '2024-03-21 00:00:00', 4, 11,8, 140, 140, 1);
INSERT INTO `cutting_tasks` VALUES (12, '2024-03-02 00:00:00', '2024-03-27 00:00:00', 5, 12,10, 150, 150, 1);
INSERT INTO `cutting_tasks` VALUES (13, '2024-03-02 00:00:00', '2024-03-27 00:00:00', 2, 13,12, 130, 130, 1);
INSERT INTO `cutting_tasks` VALUES (14, '2024-03-02 00:00:00', '2024-03-18 00:00:00', 5, 14,6, 120, 120, 1);
INSERT INTO `cutting_tasks` VALUES (15, '2024-03-11 00:00:00', '2024-03-26 00:00:00', 2, 15,6, 185, 185, 1);
INSERT INTO `cutting_tasks` VALUES (16, '2024-03-11 00:00:00', '2024-04-10 00:00:00', 4, 16,8, 200, 200, 1);
INSERT INTO `cutting_tasks` VALUES (17, '2024-03-11 00:00:00', '2024-03-25 00:00:00', 2, 17,4, 175, 175, 1);
INSERT INTO `cutting_tasks` VALUES (18, '2024-03-11 00:00:00', '2024-04-07 00:00:00', 1, 18,10, 200, 200, 1);
INSERT INTO `cutting_tasks` VALUES (19, '2024-03-18 00:00:00', '2024-04-12 00:00:00', 4, 19,6, 95, 95, 1);
INSERT INTO `cutting_tasks` VALUES (2, '2024-01-10 00:00:00', '2024-02-02 00:00:00', 3, 2,  10, 240, 240, 1);
INSERT INTO `cutting_tasks` VALUES (20, '2024-03-18 00:00:00', '2024-04-15 00:00:00', 4, 20,12, 90, 90, 1);
INSERT INTO `cutting_tasks` VALUES (21, '2024-03-18 00:00:00', '2024-04-04 00:00:00', 4, 21,10, 85, 85, 1);
INSERT INTO `cutting_tasks` VALUES (22, '2024-03-25 00:00:00', '2024-04-09 00:00:00', 2, 22,10, 115, 115, 1);
INSERT INTO `cutting_tasks` VALUES (23, '2024-03-25 00:00:00', '2024-04-19 00:00:00', 3, 23,4, 110, 110, 1);
INSERT INTO `cutting_tasks` VALUES (24, '2024-03-25 00:00:00', '2024-04-23 00:00:00', 3, 24,8, 105, 105, 1);
INSERT INTO `cutting_tasks` VALUES (25, '2024-04-14 00:00:00', '2024-05-14 00:00:00', 2, 25,6, 75, 75, 1);
INSERT INTO `cutting_tasks` VALUES (26, '2024-04-14 00:00:00', '2024-05-04 00:00:00', 4, 26,4, 70, 70, 0);
INSERT INTO `cutting_tasks` VALUES (27, '2024-04-14 00:00:00', '2024-05-04 00:00:00', 4, 27,8, 60, 60, 0);
INSERT INTO `cutting_tasks` VALUES (28, '2024-04-19 00:00:00', '2024-05-12 00:00:00', 2, 28,4, 210, 210, 1);
INSERT INTO `cutting_tasks` VALUES (29, '2024-04-19 00:00:00', '2024-05-11 00:00:00', 2, 29,6, 180, 180, 2);
INSERT INTO `cutting_tasks` VALUES (3, '2024-01-10 00:00:00', '2024-01-19 00:00:00', 3, 3,  2, 150, 150, 2);
INSERT INTO `cutting_tasks` VALUES (30, '2024-04-19 00:00:00', '2024-04-26 00:00:00', 1, 30,10, 195, 195, 1);
INSERT INTO `cutting_tasks` VALUES (31, '2024-05-10 00:00:00', '2024-05-26 00:00:00', 3, 31,8, 260, 260, 1);
INSERT INTO `cutting_tasks` VALUES (32, '2024-06-01 00:00:00', '2024-06-17 00:00:00', 2, 32,8, 150, 120, 1);
INSERT INTO `cutting_tasks` VALUES (33, '2024-06-25 00:00:00', '2024-07-17 00:00:00', 3, 33,10, 120, 0, 0);
INSERT INTO `cutting_tasks` VALUES (34, '2024-06-30 00:00:00', '2024-07-10 00:00:00', 4, 34,2, 330, 0, 0);
INSERT INTO `cutting_tasks` VALUES (4, '2024-01-10 00:00:00', '2024-01-17 00:00:00', 2, 4,  4, 220, 220, 1);
INSERT INTO `cutting_tasks` VALUES (5, '2024-01-10 00:00:00', '2024-02-02 00:00:00', 2, 5,  8, 260, 260, 1);
INSERT INTO `cutting_tasks` VALUES (6, '2024-02-28 00:00:00', '2024-03-20 00:00:00', 3, 6,  6, 95, 95, 1);
INSERT INTO `cutting_tasks` VALUES (7, '2024-02-28 00:00:00', '2024-03-06 00:00:00', 2, 7,  12, 110, 110, 1);
INSERT INTO `cutting_tasks` VALUES (8, '2024-02-28 00:00:00', '2024-03-08 00:00:00', 4, 8,  6, 50, 50, 1);
INSERT INTO `cutting_tasks` VALUES (9, '2024-03-01 00:00:00', '2024-03-06 00:00:00', 3, 9,  12, 80, 80, 1);

-- ----------------------------
-- Table structure for materials
-- ----------------------------
DROP TABLE IF EXISTS `materials`;
CREATE TABLE `materials`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Material ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Material Name',
  `unit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Material Unit',
  `type` enum('wip','origin') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Material Type',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of materials
-- ----------------------------
INSERT INTO `materials` VALUES (1, 'Cotton Fabric', 'meters', 'origin');
INSERT INTO `materials` VALUES (10, 'Synthetic Fiber Pieces', 'pieces', 'wip');
INSERT INTO `materials` VALUES (11, 'Denim Fabric', 'meters', 'origin');
INSERT INTO `materials` VALUES (12, 'Denim Fabric Pieces', 'pieces', 'wip');
INSERT INTO `materials` VALUES (13, 'Down', 'kilograms', 'origin');
INSERT INTO `materials` VALUES (14, 'Down Pieces', 'pieces', 'origin');
INSERT INTO `materials` VALUES (2, 'Fabric Pieces', 'pieces', 'wip');
INSERT INTO `materials` VALUES (3, 'Wool', 'kilograms', 'origin');
INSERT INTO `materials` VALUES (4, 'Wool Pieces', 'pieces', 'wip');
INSERT INTO `materials` VALUES (5, 'Silk', 'grams', 'origin');
INSERT INTO `materials` VALUES (6, 'Silk Pieces', 'pieces', 'wip');
INSERT INTO `materials` VALUES (7, 'Leather', 'meters', 'origin');
INSERT INTO `materials` VALUES (8, 'Leather Pieces', 'pieces', 'wip');
INSERT INTO `materials` VALUES (9, 'Synthetic Fiber', 'kilograms', 'origin');

-- ----------------------------
-- Table structure for order_product
-- ----------------------------
DROP TABLE IF EXISTS `order_product`;
CREATE TABLE `order_product`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Order Product ID',
  `order_id` int UNSIGNED NOT NULL COMMENT 'Order ID',
  `product_id` int UNSIGNED NOT NULL COMMENT 'Product ID',
  `number` int(11) NOT NULL DEFAULT 0 COMMENT 'Order Product Quantity',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `order_id`(`order_id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  CONSTRAINT `order_product_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `order_product_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of order_product
-- ----------------------------
INSERT INTO `order_product` VALUES (1, 1, 1, 100);
INSERT INTO `order_product` VALUES (10, 2, 20, 100);
INSERT INTO `order_product` VALUES (11, 3, 21, 140);
INSERT INTO `order_product` VALUES (12, 3, 29, 150);
INSERT INTO `order_product` VALUES (13, 3, 13, 130);
INSERT INTO `order_product` VALUES (14, 3, 5, 120);
INSERT INTO `order_product` VALUES (15, 4, 22, 185);
INSERT INTO `order_product` VALUES (16, 4, 26, 200);
INSERT INTO `order_product` VALUES (17, 4, 14, 175);
INSERT INTO `order_product` VALUES (18, 4, 6, 200);
INSERT INTO `order_product` VALUES (19, 5, 23, 95);
INSERT INTO `order_product` VALUES (2, 1, 19, 240);
INSERT INTO `order_product` VALUES (20, 5, 30, 90);
INSERT INTO `order_product` VALUES (21, 5, 15, 85);
INSERT INTO `order_product` VALUES (22, 6, 25, 115);
INSERT INTO `order_product` VALUES (23, 6, 8, 110);
INSERT INTO `order_product` VALUES (24, 6, 16, 105);
INSERT INTO `order_product` VALUES (25, 7, 18, 75);
INSERT INTO `order_product` VALUES (26, 7, 17, 70);
INSERT INTO `order_product` VALUES (27, 7, 10, 60);
INSERT INTO `order_product` VALUES (28, 8, 7, 210);
INSERT INTO `order_product` VALUES (29, 8, 9, 180);
INSERT INTO `order_product` VALUES (3, 1, 3, 150);
INSERT INTO `order_product` VALUES (30, 8, 24, 195);
INSERT INTO `order_product` VALUES (31, 9, 15, 260);
INSERT INTO `order_product` VALUES (32, 10, 30, 150);
INSERT INTO `order_product` VALUES (33, 11, 20, 120);
INSERT INTO `order_product` VALUES (34, 12, 7, 330);
INSERT INTO `order_product` VALUES (4, 1, 11, 220);
INSERT INTO `order_product` VALUES (5, 1, 27, 260);
INSERT INTO `order_product` VALUES (6, 2, 12, 95);
INSERT INTO `order_product` VALUES (7, 2, 28, 110);
INSERT INTO `order_product` VALUES (8, 2, 2, 50);
INSERT INTO `order_product` VALUES (9, 2, 4, 80);

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Order ID',
  `user_id` int UNSIGNED NOT NULL COMMENT '客户ID',
  `order_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Order Name',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Order 创建Time ',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `customers` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (1, 1, 'PolyU_Tshirt', '2024-01-10 00:00:00');
INSERT INTO `orders` VALUES (10, 2, 'John_Jacket', '2024-06-01 00:00:00');
INSERT INTO `orders` VALUES (11, 3, 'Emily_Pants', '2024-06-02 00:00:00');
INSERT INTO `orders` VALUES (12, 4, 'James_Skirt', '2024-06-09 00:00:00');
INSERT INTO `orders` VALUES (2, 2, 'John_Pants', '2024-02-28 00:00:00');
INSERT INTO `orders` VALUES (3, 3, 'Emily_Dress', '2024-03-02 00:00:00');
INSERT INTO `orders` VALUES (4, 4, 'James_WinterOrder', '2024-03-11 00:00:00');
INSERT INTO `orders` VALUES (5, 5, 'Sophia_SkirtAndJacket', '2024-03-18 00:00:00');
INSERT INTO `orders` VALUES (6, 6, 'Michael_SweaterAndShorts', '2024-03-25 00:00:00');
INSERT INTO `orders` VALUES (7, 7, 'Olivia_WinterOrder', '2024-04-14 00:00:00');
INSERT INTO `orders` VALUES (8, 8, 'William_Skirt_Sweater_Shorts', '2024-04-19 00:00:00');
INSERT INTO `orders` VALUES (9, 1, 'PolyU_Skirt', '2024-05-10 00:00:00');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'product ID',
  `products_type_id` int UNSIGNED NOT NULL COMMENT 'product typeID',
  `attributes` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'product 属性',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `products_type_id`(`products_type_id`) USING BTREE,
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`products_type_id`) REFERENCES `products_types` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES (1, 1, 'Red, M size');
INSERT INTO `products` VALUES (10, 8, 'White, L size');
INSERT INTO `products` VALUES (11, 1, 'White, XL size');
INSERT INTO `products` VALUES (12, 2, 'Blue, 30 size');
INSERT INTO `products` VALUES (13, 3, 'Black, S size');
INSERT INTO `products` VALUES (14, 4, 'Yellow, L size');
INSERT INTO `products` VALUES (15, 5, 'Pink, M size');
INSERT INTO `products` VALUES (16, 6, 'Grey, XL size');
INSERT INTO `products` VALUES (17, 7, 'Blue, XL size');
INSERT INTO `products` VALUES (18, 8, 'Purple, S size');
INSERT INTO `products` VALUES (19, 1, 'Green, M size');
INSERT INTO `products` VALUES (2, 2, 'Blue, 35 size');
INSERT INTO `products` VALUES (20, 2, 'Grey, 29 size');
INSERT INTO `products` VALUES (21, 3, 'Gold, L size');
INSERT INTO `products` VALUES (22, 4, 'Brown, S size');
INSERT INTO `products` VALUES (23, 5, 'Green, XL size');
INSERT INTO `products` VALUES (24, 6, 'Red, L size');
INSERT INTO `products` VALUES (25, 7, 'Blue, S size');
INSERT INTO `products` VALUES (26, 8, 'Red, M size');
INSERT INTO `products` VALUES (27, 1, 'Yellow, S size');
INSERT INTO `products` VALUES (28, 2, 'Brown, 34 size');
INSERT INTO `products` VALUES (29, 3, 'Red, M size');
INSERT INTO `products` VALUES (3, 1, 'Blue, L size');
INSERT INTO `products` VALUES (30, 4, 'Black, XL size');
INSERT INTO `products` VALUES (4, 2, 'Black, 34 size');
INSERT INTO `products` VALUES (5, 3, 'Pink, S size');
INSERT INTO `products` VALUES (6, 4, 'Brown, L size');
INSERT INTO `products` VALUES (7, 5, 'Purple, M size');
INSERT INTO `products` VALUES (8, 6, 'Silver, S size');
INSERT INTO `products` VALUES (9, 7, 'Grey, L size');

-- ----------------------------
-- Table structure for products_types
-- ----------------------------
DROP TABLE IF EXISTS `products_types`;
CREATE TABLE `products_types`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'product typeID',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'product type描述',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of products_types
-- ----------------------------
INSERT INTO `products_types` VALUES (1, 'T-shirt');
INSERT INTO `products_types` VALUES (2, 'Pants');
INSERT INTO `products_types` VALUES (3, 'Dress');
INSERT INTO `products_types` VALUES (4, 'Jacket');
INSERT INTO `products_types` VALUES (5, 'Skirt');
INSERT INTO `products_types` VALUES (6, 'Shorts');
INSERT INTO `products_types` VALUES (7, 'Sweater');
INSERT INTO `products_types` VALUES (8, 'Coat');

-- ----------------------------
-- Table structure for sewing_material_allocation
-- ----------------------------
DROP TABLE IF EXISTS `sewing_material_allocation`;
CREATE TABLE `sewing_material_allocation`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Sewing Task Material 分配ID',
  `warehouse_material_id` int UNSIGNED NULL COMMENT 'warehouse Material ID',
  `sewing_task_id` int UNSIGNED NOT NULL COMMENT 'Sewing Task ID',
  `allocated_num` int(11) NOT NULL DEFAULT 0 COMMENT 'Material 分配number',
  `is_allocated` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Material 是否已分配',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sewing_task_id`(`sewing_task_id`) USING BTREE,
  INDEX `warehouse_material_id`(`warehouse_material_id`) USING BTREE,
  CONSTRAINT `sewing_material_allocation_ibfk_1` FOREIGN KEY (`sewing_task_id`) REFERENCES `sewing_tasks` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sewing_material_allocation_ibfk_2` FOREIGN KEY (`warehouse_material_id`) REFERENCES `warehouse_material` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sewing_material_allocation
-- ----------------------------
INSERT INTO `sewing_material_allocation` VALUES (1, 2, 1, 100, 1);
INSERT INTO `sewing_material_allocation` VALUES (10, 12, 10, 100, 1);
INSERT INTO `sewing_material_allocation` VALUES (11, 4, 11, 140, 1);
INSERT INTO `sewing_material_allocation` VALUES (12, 5, 11, 140, 1);
INSERT INTO `sewing_material_allocation` VALUES (13, 3, 12, 150, 1);
INSERT INTO `sewing_material_allocation` VALUES (14, 5, 12, 150, 1);
INSERT INTO `sewing_material_allocation` VALUES (15, 3, 13, 130, 1);
INSERT INTO `sewing_material_allocation` VALUES (16, 5, 13, 130, 1);
INSERT INTO `sewing_material_allocation` VALUES (17, 3, 14, 120, 1);
INSERT INTO `sewing_material_allocation` VALUES (18, 5, 14, 120, 1);
INSERT INTO `sewing_material_allocation` VALUES (19, 3, 15, 185, 1);
INSERT INTO `sewing_material_allocation` VALUES (2, 1, 2, 240, 1);
INSERT INTO `sewing_material_allocation` VALUES (20, 7, 15, 185, 1);
INSERT INTO `sewing_material_allocation` VALUES (21, 13, 16, 200, 1);
INSERT INTO `sewing_material_allocation` VALUES (22, 3, 16, 200, 1);
INSERT INTO `sewing_material_allocation` VALUES (23, 7, 16, 200, 1);
INSERT INTO `sewing_material_allocation` VALUES (24, 3, 17, 175, 1);
INSERT INTO `sewing_material_allocation` VALUES (25, 7, 17, 175, 1);
INSERT INTO `sewing_material_allocation` VALUES (26, 3, 18, 200, 1);
INSERT INTO `sewing_material_allocation` VALUES (27, 7, 18, 200, 1);
INSERT INTO `sewing_material_allocation` VALUES (28, 1, 19, 95, 1);
INSERT INTO `sewing_material_allocation` VALUES (29, 9, 19, 95, 1);
INSERT INTO `sewing_material_allocation` VALUES (3, 1, 3, 150, 1);
INSERT INTO `sewing_material_allocation` VALUES (30, 3, 20, 90, 1);
INSERT INTO `sewing_material_allocation` VALUES (31, 7, 20, 90, 1);
INSERT INTO `sewing_material_allocation` VALUES (32, 1, 21, 85, 1);
INSERT INTO `sewing_material_allocation` VALUES (33, 9, 21, 85, 1);
INSERT INTO `sewing_material_allocation` VALUES (34, 3, 22, 115, 1);
INSERT INTO `sewing_material_allocation` VALUES (35, 11, 23, 110, 1);
INSERT INTO `sewing_material_allocation` VALUES (36, 11, 24, 105, 1);
INSERT INTO `sewing_material_allocation` VALUES (37, 13, 25, 75, 1);
INSERT INTO `sewing_material_allocation` VALUES (38, 3, 25, 75, 1);
INSERT INTO `sewing_material_allocation` VALUES (39, 7, 25, 75, 1);
INSERT INTO `sewing_material_allocation` VALUES (4, 1, 4, 220, 1);
INSERT INTO `sewing_material_allocation` VALUES (40, 3, 26, 70, 1);
INSERT INTO `sewing_material_allocation` VALUES (41, 3, 27, 60, 1);
INSERT INTO `sewing_material_allocation` VALUES (42, 7, 27, 60, 1);
INSERT INTO `sewing_material_allocation` VALUES (43, 13, 27, 60, 1);
INSERT INTO `sewing_material_allocation` VALUES (44, 1, 28, 210, 1);
INSERT INTO `sewing_material_allocation` VALUES (45, 9, 28, 210, 1);
INSERT INTO `sewing_material_allocation` VALUES (46, 3, 29, 180, 1);
INSERT INTO `sewing_material_allocation` VALUES (47, 11, 30, 195, 1);
INSERT INTO `sewing_material_allocation` VALUES (48, 1, 31, 260, 0);
INSERT INTO `sewing_material_allocation` VALUES (49, 9, 31, 260, 0);
INSERT INTO `sewing_material_allocation` VALUES (5, 1, 5, 260, 1);
INSERT INTO `sewing_material_allocation` VALUES (50, 3, 32, 150, 0);
INSERT INTO `sewing_material_allocation` VALUES (51, 7, 32, 150, 0);
INSERT INTO `sewing_material_allocation` VALUES (52, 11, 33, 120, 0);
INSERT INTO `sewing_material_allocation` VALUES (53, 1, 34, 330, 0);
INSERT INTO `sewing_material_allocation` VALUES (54, 9, 34, 330, 0);
INSERT INTO `sewing_material_allocation` VALUES (6, 11, 6, 95, 1);
INSERT INTO `sewing_material_allocation` VALUES (7, 11, 7, 110, 1);
INSERT INTO `sewing_material_allocation` VALUES (8, 11, 8, 50, 1);
INSERT INTO `sewing_material_allocation` VALUES (9, 11, 9, 80, 1);

-- ----------------------------
-- Table structure for sewing_tasks
-- ----------------------------
DROP TABLE IF EXISTS `sewing_tasks`;
CREATE TABLE `sewing_tasks`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Sewing Task ID',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Sewing Task Start Time ',
  `end_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Sewing Task End Time ',
  `working_group_id` int UNSIGNED NOT NULL COMMENT 'Working Group ID',
  `order_product_id` int UNSIGNED NOT NULL COMMENT 'Order product ID',
  `planned_number` int(11) NOT NULL DEFAULT 0 COMMENT 'planned Sewing number',
  `completed_number` int(11) NOT NULL DEFAULT 0 COMMENT 'completed Sewing number',
  `status` int(11) NOT NULL DEFAULT 0 COMMENT 'Status of the task 0: not start, 1: on-going, 2: completed',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `working_group_id`(`working_group_id`) USING BTREE,
  INDEX `order_product_id`(`order_product_id`) USING BTREE,
  CONSTRAINT `sewing_tasks_ibfk_1` FOREIGN KEY (`working_group_id`) REFERENCES `working_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sewing_tasks_ibfk_2` FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sewing_tasks
-- ----------------------------
INSERT INTO `sewing_tasks` VALUES (1, '2024-01-18 00:00:00', '2024-02-07 00:00:00', 2, 1, 100, 100, 2);
INSERT INTO `sewing_tasks` VALUES (10, '2024-03-29 00:00:00', '2024-04-09 00:00:00', 2, 10, 100, 100, 0);
INSERT INTO `sewing_tasks` VALUES (11, '2024-03-21 00:00:00', '2024-04-14 00:00:00', 9, 11, 140, 100, 0);
INSERT INTO `sewing_tasks` VALUES (12, '2024-03-27 00:00:00', '2024-04-12 00:00:00', 2, 12, 150, 120, 1);
INSERT INTO `sewing_tasks` VALUES (13, '2024-03-27 00:00:00', '2024-04-06 00:00:00', 2, 13, 130, 120, 1);
INSERT INTO `sewing_tasks` VALUES (14, '2024-03-18 00:00:00', '2024-04-08 00:00:00', 2, 14, 120, 120, 1);
INSERT INTO `sewing_tasks` VALUES (15, '2024-03-26 00:00:00', '2024-04-09 00:00:00', 2, 15, 185, 185, 1);
INSERT INTO `sewing_tasks` VALUES (16, '2024-04-10 00:00:00', '2024-05-07 00:00:00', 8, 16, 200, 200, 2);
INSERT INTO `sewing_tasks` VALUES (17, '2024-03-25 00:00:00', '2024-04-22 00:00:00', 7, 17, 175, 175, 2);
INSERT INTO `sewing_tasks` VALUES (18, '2024-04-07 00:00:00', '2024-04-21 00:00:00', 7, 18, 200, 200, 2);
INSERT INTO `sewing_tasks` VALUES (19, '2024-04-12 00:00:00', '2024-04-23 00:00:00', 7, 19, 95, 95, 1);
INSERT INTO `sewing_tasks` VALUES (2, '2024-02-02 00:00:00', '2024-02-15 00:00:00', 9, 2, 240, 240, 1);
INSERT INTO `sewing_tasks` VALUES (20, '2024-04-15 00:00:00', '2024-05-07 00:00:00', 8, 20, 90, 90, 1);
INSERT INTO `sewing_tasks` VALUES (21, '2024-04-04 00:00:00', '2024-04-12 00:00:00', 8, 21, 85, 85, 1);
INSERT INTO `sewing_tasks` VALUES (22, '2024-04-09 00:00:00', '2024-04-22 00:00:00', 8, 22, 115, 60, 0);
INSERT INTO `sewing_tasks` VALUES (23, '2024-04-19 00:00:00', '2024-05-01 00:00:00', 7, 23, 110, 80, 0);
INSERT INTO `sewing_tasks` VALUES (24, '2024-04-23 00:00:00', '2024-05-20 00:00:00', 2, 24, 105, 105, 0);
INSERT INTO `sewing_tasks` VALUES (25, '2024-05-14 00:00:00', '2024-06-03 00:00:00', 8, 25, 75, 75, 0);
INSERT INTO `sewing_tasks` VALUES (26, '2024-05-04 00:00:00', '2024-05-15 00:00:00', 9, 26, 70, 70, 0);
INSERT INTO `sewing_tasks` VALUES (27, '2024-05-04 00:00:00', '2024-05-15 00:00:00', 7, 27, 60, 60, 0);
INSERT INTO `sewing_tasks` VALUES (28, '2024-05-12 00:00:00', '2024-05-28 00:00:00', 7, 28, 210, 210, 1);
INSERT INTO `sewing_tasks` VALUES (29, '2024-05-11 00:00:00', '2024-05-19 00:00:00', 7, 29, 180, 180, 1);
INSERT INTO `sewing_tasks` VALUES (3, '2024-01-19 00:00:00', '2024-02-08 00:00:00', 9, 3, 150, 150, 1);
INSERT INTO `sewing_tasks` VALUES (30, '2024-04-26 00:00:00', '2024-05-15 00:00:00', 2, 30, 195, 195, 1);
INSERT INTO `sewing_tasks` VALUES (31, '2024-05-26 00:00:00', '2024-06-04 00:00:00', 10, 31, 260, 260, 1);
INSERT INTO `sewing_tasks` VALUES (32, '2024-06-17 00:00:00', '2024-07-14 00:00:00', 9, 32, 150, 0, 0);
INSERT INTO `sewing_tasks` VALUES (33, '2024-07-17 00:00:00', '2024-08-03 00:00:00', 8, 33, 120, 0, 0);
INSERT INTO `sewing_tasks` VALUES (34, '2024-07-10 00:00:00', '2024-07-20 00:00:00', 10, 34, 330, 0, 0);
INSERT INTO `sewing_tasks` VALUES (4, '2024-01-17 00:00:00', '2024-01-30 00:00:00', 2, 4, 220, 220, 1);
INSERT INTO `sewing_tasks` VALUES (5, '2024-02-02 00:00:00', '2024-02-25 00:00:00', 2, 5, 260, 260, 1);
INSERT INTO `sewing_tasks` VALUES (6, '2024-03-20 00:00:00', '2024-04-07 00:00:00', 8, 6, 95, 95, 1);
INSERT INTO `sewing_tasks` VALUES (7, '2024-03-06 00:00:00', '2024-03-22 00:00:00', 8, 7, 110, 110, 1);
INSERT INTO `sewing_tasks` VALUES (8, '2024-03-08 00:00:00', '2024-04-05 00:00:00', 7, 8, 50, 50, 1);
INSERT INTO `sewing_tasks` VALUES (9, '2024-03-06 00:00:00', '2024-03-20 00:00:00', 8, 9, 80, 80, 1);

-- ----------------------------
-- Table structure for warehouse
-- ----------------------------
DROP TABLE IF EXISTS `warehouse`;
CREATE TABLE `warehouse`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'warehouse ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'warehouse Name',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of warehouse
-- ----------------------------
INSERT INTO `warehouse` VALUES (1, 'Main Warehouse');
INSERT INTO `warehouse` VALUES (2, 'Auxiliary warehouse');

-- ----------------------------
-- Table structure for warehouse_material
-- ----------------------------
DROP TABLE IF EXISTS `warehouse_material`;
CREATE TABLE `warehouse_material`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'warehouse Material ID',
  `warehouse_id` int UNSIGNED NOT NULL COMMENT 'warehouse ID',
  `material_id` int UNSIGNED NOT NULL COMMENT 'Material ID',
  `total_number` int(11) NOT NULL DEFAULT 0 COMMENT 'Total Material Inventory Quantity',
  `left_number` int(11) NOT NULL DEFAULT 0 COMMENT 'Remaining Material Inventory Quantity',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `warehouse_id`(`warehouse_id`) USING BTREE,
  INDEX `material_id`(`material_id`) USING BTREE,
  CONSTRAINT `warehouse_material_ibfk_1` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `warehouse_material_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of warehouse_material
-- ----------------------------
INSERT INTO `warehouse_material` VALUES (1, 1, 1,   3500, 3500);
INSERT INTO `warehouse_material` VALUES (10, 2, 10, 1500, 1500);
INSERT INTO `warehouse_material` VALUES (11, 1, 11, 4500, 4500);
INSERT INTO `warehouse_material` VALUES (12, 2, 12, 3180, 3180);
INSERT INTO `warehouse_material` VALUES (13, 1, 13, 1230, 1230);
INSERT INTO `warehouse_material` VALUES (14, 2, 14, 2420, 2420);
INSERT INTO `warehouse_material` VALUES (2, 2, 2,   3200, 3200);
INSERT INTO `warehouse_material` VALUES (3, 1, 3,   4100, 4100);
INSERT INTO `warehouse_material` VALUES (4, 2, 4,   3550, 3550);
INSERT INTO `warehouse_material` VALUES (5, 1, 5,   1100, 1100);
INSERT INTO `warehouse_material` VALUES (6, 2, 6,   5400, 5400);
INSERT INTO `warehouse_material` VALUES (7, 1, 7,   2200, 2200);
INSERT INTO `warehouse_material` VALUES (8, 2, 8,   1300, 1300);
INSERT INTO `warehouse_material` VALUES (9, 1, 9,   2300, 2300);

-- ----------------------------
-- Table structure for warehouse_product
-- ----------------------------
DROP TABLE IF EXISTS `warehouse_product`;
CREATE TABLE `warehouse_product`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'warehouse product ID',
  `warehouse_id` int UNSIGNED NOT NULL COMMENT 'warehouse ID',
  `product_id` int UNSIGNED NOT NULL COMMENT 'product ID',
  `left_number` int(11) NOT NULL DEFAULT 0 COMMENT 'Remaining Product Inventory Quantity',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `warehouse_id`(`warehouse_id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  CONSTRAINT `warehouse_product_ibfk_1` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `warehouse_product_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of warehouse_product
-- ----------------------------
INSERT INTO `warehouse_product` VALUES (1, 1, 1, 0);
INSERT INTO `warehouse_product` VALUES (2, 2, 2, 0);

-- ----------------------------
-- Table structure for working_group
-- ----------------------------
DROP TABLE IF EXISTS `working_group`;
CREATE TABLE `working_group`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Working Group ID',
  `type` enum('sew','cut') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Working Group type，Sewing group、Cutting group',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Working Group Name',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of working_group
-- ----------------------------
INSERT INTO `working_group` VALUES (1, 'cut', 'Precision Cutters');
INSERT INTO `working_group` VALUES (10, 'sew', 'Elite Sewers');
INSERT INTO `working_group` VALUES (2, 'sew', 'Master Sewers');
INSERT INTO `working_group` VALUES (3, 'cut', 'Master Cutters');
INSERT INTO `working_group` VALUES (4, 'cut', 'Expert Cutters');
INSERT INTO `working_group` VALUES (5, 'cut', 'Professional Cutters');
INSERT INTO `working_group` VALUES (6, 'cut', 'Advanced Cutters');
INSERT INTO `working_group` VALUES (7, 'sew','Skilled Sewers');
INSERT INTO `working_group` VALUES (8, 'sew', 'Advanced Sewers');
INSERT INTO `working_group` VALUES (9, 'sew', 'Premier Sewers');

-- ----------------------------
-- Table structure for product_material
-- ----------------------------
DROP TABLE IF EXISTS `product_material`;
CREATE TABLE `product_material`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Product Material ID',
  `product_id` int UNSIGNED NOT NULL COMMENT 'Product ID',
  `material_id` int UNSIGNED NOT NULL COMMENT 'Material ID',
  `number` int(11) NOT NULL DEFAULT 0.0 COMMENT 'Required Quantity of material',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  CONSTRAINT `product_material_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `product_material_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of working_group
-- ----------------------------
INSERT INTO `product_material` VALUES
(1, 1, 10, 2), (2, 1, 2, 4), (3, 10, 8, 3), (4, 10, 12, 1), (5, 10, 6, 5),
(6, 11, 4, 3), (7, 11, 2, 2 ), (8, 12, 8, 4), (9, 12, 6, 2), (10, 12, 10, 1),
(11, 13, 10, 3), (12, 13, 12, 4), (13, 14, 2, 2), (14, 14, 4, 3), (15, 14, 6, 1),
(16, 15, 8, 5), (17, 15, 10, 2), (18, 16, 2, 3), (19, 16, 6, 1), (20, 17, 4, 2),
(21, 17, 12, 3), (22, 18, 10, 4), (23, 18, 6, 1), (24, 18, 2, 3), (25, 19, 2, 2),
(26, 19, 12, 5), (27, 2, 6, 2), (28, 2, 4, 1), (29, 20, 2, 3), (30, 20, 6, 4),
(31, 21, 12, 2), (32, 21, 8, 3), (33, 22, 10, 1), (34, 22, 12, 2), (35, 23, 4, 3),
(36, 23, 2, 1), (37, 24, 10, 2), (38, 24, 8, 5), (39, 25, 4, 4), (40, 25, 6, 3),
(41, 26, 12, 1), (42, 26, 2, 3), (43, 27, 6, 4), (44, 27, 10, 2), (45, 28, 6, 3),
(46, 28, 8, 2), (47, 29, 10, 4), (48, 29, 12, 1), (49, 3, 4, 3), (50, 3, 8, 2),
(51, 30, 2, 5), (52, 30, 10, 1), (53, 4, 12, 3), (54, 4, 8, 2), (55, 5, 4, 4),
(56, 5, 10, 1), (57, 6, 6, 2), (58, 6, 8, 3), (59, 7, 12, 5), (60, 7, 6, 2),
(61, 8, 2, 1), (62, 8, 4, 3), (63, 9, 12, 4), (64, 9, 10, 2);

-- ----------------------------
-- Table structure for product_material
-- ----------------------------
DROP TABLE IF EXISTS `wip_material`;
CREATE TABLE `wip_material`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Product Material ID',
  `wip_id` int UNSIGNED NOT NULL COMMENT 'Wip material ID',
  `origin_material_id` int UNSIGNED NOT NULL COMMENT 'Original Material ID',
  `number` float NOT NULL DEFAULT 0.0 COMMENT 'Required Quantity of material',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `wip_id`(`wip_id`) USING BTREE,
  CONSTRAINT `wip_material_ibfk_1` FOREIGN KEY (`wip_id`) REFERENCES `materials` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `wip_material_ibfk_2` FOREIGN KEY (`origin_material_id`) REFERENCES `materials` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of working_group
-- ----------------------------
INSERT INTO `wip_material` VALUES
(1, 10, 9, 0.6),   (2, 10, 1, 0.35),  (3, 10, 13, 0.8),  (4, 12, 11, 0.7),  (5, 12, 1, 0.5),
(6, 2, 1, 0.4),    (7, 2, 11, 0.65),  (8, 2, 3, 0.2),    (9, 4, 3, 0.5),    (10, 4, 14, 0.15),
(11, 4, 13, 0.3),  (12, 6, 5, 0.75),  (13, 6, 1, 0.4),   (14, 8, 7, 1.0),   (15, 8, 9, 0.2),
(16, 8, 5, 0.1);
SET FOREIGN_KEY_CHECKS = 1;
