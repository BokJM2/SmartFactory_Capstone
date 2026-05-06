import re
import os
import pandas as pd
from config import cfg
from sqlite_db import SQLiteDB
from fruit_shop_schema import tables


def get_table_info(create_table_sql):
    # Regex to match 'CREATE TABLE' followed by the table name
    pattern = r"CREATE TABLE (\w+)"
    match = re.search(pattern, create_table_sql, re.IGNORECASE)
    table_name = match.group(1)

    # Regex to match the column definitions starting with a lowercase letter
    # This pattern matches a word at the start of the line, followed by a space, followed by another word
    pattern = r"^\s*([a-z]\w*)\s+(\w+)"
    matches = re.findall(pattern, create_table_sql, re.MULTILINE)

    # The matches list now contains tuples with the column name and data type
    column_names = []
    column_types = []
    for column_name, data_type in matches:
        column_names.append(column_name)
        column_types.append(data_type)

    return table_name, column_names, column_types


def get_database_info(tables):
    database_info = dict()
    for tab in tables:
        table_name, column_names, column_types = get_table_info(tab)
        database_info[table_name] = {
            "column_names": column_names,
            "column_types": column_types,
        }
    return database_info


database_info = get_database_info(tables)
# table_details = "\n".join(tables)
table_details = """
-- ----------------------------
-- Table structure for customers
-- ----------------------------
CREATE TABLE `customers`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Customer ID',
  `customer_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Customer Name',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for cutting_material_allocation
-- ----------------------------
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
-- Table structure for cutting_tasks
-- ----------------------------
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
-- Table structure for materials
-- ----------------------------
CREATE TABLE `materials`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Material ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Material Name',
  `unit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Material Unit',
  `type` enum('wip','origin') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Material Type',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;



-- ----------------------------
-- Table structure for order_product
-- ----------------------------
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
-- Table structure for orders
-- ----------------------------
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
-- Table structure for products
-- ----------------------------
CREATE TABLE `products`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'product ID',
  `products_type_id` int UNSIGNED NOT NULL COMMENT 'product typeID',
  `attributes` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'product 属性',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `products_type_id`(`products_type_id`) USING BTREE,
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`products_type_id`) REFERENCES `products_types` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for products_types
-- ----------------------------
CREATE TABLE `products_types`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'product typeID',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'product type描述',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sewing_material_allocation
-- ----------------------------
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
-- Table structure for sewing_tasks
-- ----------------------------
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
-- Table structure for warehouse
-- ----------------------------
CREATE TABLE `warehouse`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'warehouse ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'warehouse Name',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for warehouse_material
-- ----------------------------
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
-- Table structure for warehouse_product
-- ----------------------------
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
-- Table structure for working_group
-- ----------------------------
CREATE TABLE `working_group`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Working Group ID',
  `type` enum('sew','cut') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Working Group type，Sewing group、Cutting group',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Working Group Name',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for product_material
-- ----------------------------
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
-- Table structure for product_material
-- ----------------------------
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
"""
# print("*****************table details*****************")
# print(table_details)

def init_database(database_info=None, db_name=None):
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(project_root, "fashion.db")
    return SQLiteDB(db_path=db_path)
    # print(mysqldb)
    # mysqldb.create_database(db_name)
    # for tab_crate_cmd in tables:
    #     mysqldb.execute_sql(tab_crate_cmd)
    # from sqlalchemy import create_engine
    # from urllib.parse import quote

    # create database engine
    # connect_str = "mysql+pymysql://{user}:{pw}@{host}/{db}".format(user=cfg.mysql_user,
    #                                pw=quote(cfg.mysql_password),
    #                                host=cfg.mysql_host,
    #                                db=db_name)
    # print(connect_str)
    # engine = create_engine(connect_str)
    # print(database_info)
    # read csv data
    # conn = pymysql.connect(
    #         host=cfg.mysql_host,
    #         port=cfg.mysql_port,
    #         user=cfg.mysql_user,
    #         password=cfg.mysql_password,
    #         database=db_name
    #     )
    # for tab_name in database_info.keys():
    #     df = pd.read_csv(f'csvs/{tab_name}.csv')
    #     # write data to MySQL database
    #     df.to_sql(tab_name, con=conn, if_exists='append', index=False)
    # return mysqldb

# def init_database(database_info, db_name):
#     # global mysqldb
#     mysqldb = MySQLDB(host=cfg.mysql_host, user=cfg.mysql_user, password=cfg.mysql_password,
#                       port=cfg.mysql_port, database=None)
#     # print(mysqldb)
#     mysqldb.create_database(db_name)
#     for tab_crate_cmd in tables:
#         mysqldb.execute_sql(tab_crate_cmd)

#     # create database engine
#     engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
#                            .format(user=cfg.mysql_user,
#                                    pw=quote(cfg.mysql_password),
#                                    host=cfg.mysql_host,
#                                    db=db_name))

#     # Create a configured "Session" class
#     Session = sessionmaker(bind=engine)

#     # Create a Session
#     session = Session()

#     try:
#         # read csv data and write to MySQL database using the session connection
#         for tab_name in database_info.keys():
#             df = pd.read_csv(f'csvs/{tab_name}.csv')
#             df.to_sql(tab_name, con=session.connection(), if_exists='append', index=False)
        
#         session.commit()
        
#     except Exception as e:
#         session.rollback()
#         raise e
    
#     finally:
#         session.close()

#     return mysqldb


if __name__ == '__main__':
    print(database_info)
    print(table_details)
    # test_db_name = "try1024"
    # init_database(database_info, test_db_name)
