CREATE TABLE `customers` (
  `customer_id` uuid PRIMARY KEY,
  `customer_name` varchar(255)
);

CREATE TABLE `orders` (
  `id` uuid PRIMARY KEY,
  `user_id` uuid,
  `order_name` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `products_types` (
  `id` uuid PRIMARY KEY,
  `description` varchar(255)
);

CREATE TABLE `products` (
  `id` uuid PRIMARY KEY,
  `products_type_id` uuid,
  `attributes` varchar(255)
);

CREATE TABLE `materials` (
  `id` uuid PRIMARY KEY,
  `name` varchar(255),
  `unit` varchar(255),
  `type` enum(wip,origin)
);

CREATE TABLE `order_product` (
  `id` uuid PRIMARY KEY,
  `order_id` uuid,
  `product_id` uuid,
  `number` integer
);

CREATE TABLE `working_group` (
  `id` uuid PRIMARY KEY,
  `type` enum(sew,cut),
  `name` varchar(255)
);

CREATE TABLE `cutting_tasks` (
  `id` uuid PRIMARY KEY,
  `start_time` timestamp,
  `end_time` timestamp,
  `working_group_id` uuid,
  `order_product_id` uuid,
  `produced_wip_id` uuid,
  `planned_number` integer,
  `completed_number` integer,
  `status` integer
);

CREATE TABLE `sewing_tasks` (
  `id` uuid PRIMARY KEY,
  `start_time` timestamp,
  `end_time` timestamp,
  `working_group_id` uuid,
  `order_product_id` uuid,
  `planned_number` integer,
  `completed_number` integer,
  `status` integer
);

CREATE TABLE `cutting_material_allocation` (
  `id` uuid PRIMARY KEY,
  `warehouse_material_id` uuid,
  `cutting_task_id` uuid,
  `allocated_num` integer,
  `is_allocated` bool
);

CREATE TABLE `sewing_material_allocation` (
  `id` uuid PRIMARY KEY,
  `warehouse_material_id` uuid,
  `sewing_task_id` uuid,
  `allocated_num` integer,
  `is_allocated` bool
);

CREATE TABLE `warehouse` (
  `id` uuid PRIMARY KEY,
  `name` varchar(255)
);

CREATE TABLE `warehouse_product` (
  `id` uuid PRIMARY KEY,
  `warehouse_id` uuid,
  `product_id` uuid,
  `left_number` integer
);

CREATE TABLE `warehouse_material` (
  `id` uuid PRIMARY KEY,
  `warehouse_id` uuid,
  `material_id` uuid,
  `left_number` integer
);

CREATE TABLE `product_material` (
  `id` uuid PRIMARY KEY,
  `product_id` uuid,
  `material_id` uuid,
  `amount` float
);

CREATE TABLE `wip_material` (
  `id` uuid PRIMARY KEY,
  `wip_material_id` uuid,
  `origin_material_id` uuid,
  `amount` float
);

ALTER TABLE `orders` ADD FOREIGN KEY (`user_id`) REFERENCES `customers` (`customer_id`);

ALTER TABLE `product_material` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

ALTER TABLE `product_material` ADD FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`);

ALTER TABLE `wip_material` ADD FOREIGN KEY (`wip_material_id`) REFERENCES `materials` (`id`);

ALTER TABLE `wip_material` ADD FOREIGN KEY (`origin_material_id`) REFERENCES `materials` (`id`);

ALTER TABLE `products` ADD FOREIGN KEY (`products_type_id`) REFERENCES `products_types` (`id`);

ALTER TABLE `order_product` ADD FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

ALTER TABLE `order_product` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

ALTER TABLE `warehouse_product` ADD FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`);

ALTER TABLE `warehouse_material` ADD FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`);

ALTER TABLE `warehouse_material` ADD FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`);

ALTER TABLE `sewing_tasks` ADD FOREIGN KEY (`working_group_id`) REFERENCES `working_group` (`id`);

ALTER TABLE `cutting_tasks` ADD FOREIGN KEY (`working_group_id`) REFERENCES `working_group` (`id`);

ALTER TABLE `cutting_tasks` ADD FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`);

ALTER TABLE `cutting_tasks` ADD FOREIGN KEY (`produced_wip_id`) REFERENCES `materials` (`id`);

ALTER TABLE `warehouse_product` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

ALTER TABLE `sewing_material_allocation` ADD FOREIGN KEY (`sewing_task_id`) REFERENCES `sewing_tasks` (`id`);

ALTER TABLE `cutting_material_allocation` ADD FOREIGN KEY (`cutting_task_id`) REFERENCES `cutting_tasks` (`id`);

ALTER TABLE `cutting_material_allocation` ADD FOREIGN KEY (`warehouse_material_id`) REFERENCES `warehouse_material` (`id`);

ALTER TABLE `sewing_material_allocation` ADD FOREIGN KEY (`warehouse_material_id`) REFERENCES `warehouse_material` (`id`);

ALTER TABLE `sewing_tasks` ADD FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`);

ALTER TABLE `order_product` ADD FOREIGN KEY (`product_id`) REFERENCES `order_product` (`id`);
