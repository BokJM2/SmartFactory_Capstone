"""
SQLite DB setup script.
Run this ONCE before running the demo:
    python setup_db.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "fashion.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products_types (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    products_type_id INTEGER NOT NULL,
    attributes       TEXT NOT NULL,
    FOREIGN KEY (products_type_id) REFERENCES products_types(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    order_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS order_product (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id   INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    number     INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (order_id)   REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS working_group (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK(type IN ('sew','cut')),
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cutting_tasks (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time       TEXT NOT NULL DEFAULT (datetime('now')),
    end_time         TEXT NOT NULL DEFAULT (datetime('now')),
    working_group_id INTEGER NOT NULL,
    order_product_id INTEGER NOT NULL,
    produced_wip_id  INTEGER,
    planned_number   INTEGER NOT NULL DEFAULT 0,
    completed_number INTEGER NOT NULL DEFAULT 0,
    status           INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (working_group_id) REFERENCES working_group(id),
    FOREIGN KEY (order_product_id) REFERENCES order_product(id)
);

CREATE TABLE IF NOT EXISTS sewing_tasks (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time       TEXT NOT NULL DEFAULT (datetime('now')),
    end_time         TEXT NOT NULL DEFAULT (datetime('now')),
    working_group_id INTEGER NOT NULL,
    order_product_id INTEGER NOT NULL,
    planned_number   INTEGER NOT NULL DEFAULT 0,
    completed_number INTEGER NOT NULL DEFAULT 0,
    status           INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (working_group_id) REFERENCES working_group(id),
    FOREIGN KEY (order_product_id) REFERENCES order_product(id)
);

CREATE TABLE IF NOT EXISTS materials (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('wip','origin'))
);

CREATE TABLE IF NOT EXISTS warehouse (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouse_material (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_id INTEGER NOT NULL,
    material_id  INTEGER NOT NULL,
    total_number INTEGER NOT NULL DEFAULT 0,
    left_number  INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(id),
    FOREIGN KEY (material_id)  REFERENCES materials(id)
);

CREATE TABLE IF NOT EXISTS warehouse_product (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_id INTEGER NOT NULL,
    product_id   INTEGER NOT NULL,
    left_number  INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(id),
    FOREIGN KEY (product_id)   REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS product_material (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    number      INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id)  REFERENCES products(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
);

CREATE TABLE IF NOT EXISTS cutting_material_allocation (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_material_id INTEGER,
    cutting_task_id      INTEGER NOT NULL,
    allocated_num        INTEGER NOT NULL DEFAULT 0,
    is_allocated         INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (cutting_task_id)       REFERENCES cutting_tasks(id),
    FOREIGN KEY (warehouse_material_id) REFERENCES warehouse_material(id)
);

CREATE TABLE IF NOT EXISTS sewing_material_allocation (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_material_id INTEGER,
    sewing_task_id       INTEGER NOT NULL,
    allocated_num        INTEGER NOT NULL DEFAULT 0,
    is_allocated         INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (sewing_task_id)        REFERENCES sewing_tasks(id),
    FOREIGN KEY (warehouse_material_id) REFERENCES warehouse_material(id)
);
"""

SAMPLE_DATA = """
-- Customers
INSERT OR IGNORE INTO customers (id, customer_name) VALUES
(1, 'PolyU'),
(2, 'Alice'),
(3, 'Bob'),
(4, 'Michael'),
(5, 'Sophia'),
(6, 'Emma'),
(7, 'James');

-- Product types
INSERT OR IGNORE INTO products_types (id, description) VALUES
(1, 'T-shirt'),
(2, 'Skirt'),
(3, 'Sweater'),
(4, 'Shorts'),
(5, 'Jacket');

-- Products
INSERT OR IGNORE INTO products (id, products_type_id, attributes) VALUES
(1,  1, 'Red, M size'),
(2,  1, 'Blue, L size'),
(3,  1, 'White, S size'),
(4,  1, 'Black, XL size'),
(5,  2, 'Red, S size'),
(6,  2, 'Blue, M size'),
(7,  2, 'White, L size'),
(8,  4, 'Silver, S size'),
(9,  4, 'Grey, XL size'),
(10, 3, 'Red, M size'),
(11, 3, 'Blue, L size'),
(12, 5, 'Black, M size'),
(13, 5, 'Grey, L size'),
(25, 3, 'Blue, S size');

-- Orders
INSERT OR IGNORE INTO orders (id, user_id, order_name, created_at) VALUES
(1,  1, 'PolyU_Tshirt',          '2024-02-10 00:00:00'),
(2,  2, 'Alice_Jacket',           '2024-03-01 00:00:00'),
(3,  3, 'Bob_Sweater',            '2024-03-05 00:00:00'),
(4,  4, 'Michael_TshirtAndSkirt', '2024-03-10 00:00:00'),
(5,  5, 'Sophia_Jacket',          '2024-03-18 00:00:00'),
(6,  4, 'Michael_SweaterAndShorts','2024-04-01 00:00:00'),
(7,  6, 'Emma_Tshirt',            '2024-04-05 00:00:00'),
(8,  7, 'James_Shorts',           '2024-04-10 00:00:00'),
(9,  1, 'PolyU_Skirt',            '2024-04-15 00:00:00');

-- Order products
INSERT OR IGNORE INTO order_product (id, order_id, product_id, number) VALUES
(1,  1, 1,  50),
(2,  2, 12, 30),
(3,  3, 11, 40),
(4,  4, 2,  60),
(5,  4, 5,  45),
(6,  5, 13, 25),
(7,  6, 25, 115),
(8,  6, 8,  110),
(9,  6, 9,  105),
(10, 7, 3,  70),
(11, 8, 8,  80),
(12, 9, 6,  55);

-- Working groups (cut: 1-3, sew: 4-6)
INSERT OR IGNORE INTO working_group (id, type, name) VALUES
(1, 'cut', 'Cutting Group A'),
(2, 'cut', 'Cutting Group B'),
(3, 'cut', 'Cutting Group C'),
(4, 'sew', 'Sewing Group A'),
(5, 'sew', 'Sewing Group B'),
(6, 'sew', 'Sewing Group C');

-- Cutting tasks
INSERT OR IGNORE INTO cutting_tasks
    (id, working_group_id, order_product_id, produced_wip_id, planned_number, completed_number, status, start_time, end_time)
VALUES
(1, 1, 1,  NULL, 50,  50,  2, '2024-02-11 08:00:00', '2024-02-12 17:00:00'),
(2, 2, 2,  NULL, 30,  20,  1, '2024-03-02 08:00:00', '2024-03-10 17:00:00'),
(3, 3, 3,  NULL, 40,  40,  2, '2024-03-06 08:00:00', '2024-03-07 17:00:00'),
(4, 1, 4,  NULL, 60,  60,  2, '2024-03-11 08:00:00', '2024-03-13 17:00:00'),
(5, 2, 5,  NULL, 45,  30,  1, '2024-03-11 08:00:00', '2024-03-20 17:00:00'),
(6, 3, 6,  NULL, 25,  10,  1, '2024-03-19 08:00:00', '2024-04-01 17:00:00'),
(7, 1, 7,  NULL, 115, 115, 2, '2024-04-02 08:00:00', '2024-04-05 17:00:00'),
(8, 2, 8,  NULL, 110, 90,  1, '2024-04-02 08:00:00', '2024-04-15 17:00:00'),
(9, 3, 9,  NULL, 105, 0,   0, '2024-04-10 08:00:00', '2024-04-20 17:00:00'),
(10,1, 10, NULL, 70,  70,  2, '2024-04-06 08:00:00', '2024-04-08 17:00:00'),
(11,2, 11, NULL, 80,  60,  1, '2024-04-11 08:00:00', '2024-04-20 17:00:00'),
(12,3, 12, NULL, 55,  55,  2, '2024-04-16 08:00:00', '2024-04-18 17:00:00');

-- Sewing tasks
INSERT OR IGNORE INTO sewing_tasks
    (id, working_group_id, order_product_id, planned_number, completed_number, status, start_time, end_time)
VALUES
(1, 4, 1,  50,  50,  2, '2024-02-13 08:00:00', '2024-02-15 17:00:00'),
(2, 5, 2,  30,  15,  1, '2024-03-05 08:00:00', '2024-03-15 17:00:00'),
(3, 6, 3,  40,  40,  2, '2024-03-08 08:00:00', '2024-03-10 17:00:00'),
(4, 4, 4,  60,  60,  2, '2024-03-14 08:00:00', '2024-03-16 17:00:00'),
(5, 5, 5,  45,  20,  1, '2024-03-14 08:00:00', '2024-03-25 17:00:00'),
(6, 6, 6,  25,  5,   1, '2024-03-22 08:00:00', '2024-04-05 17:00:00'),
(7, 4, 7,  115, 60,  1, '2024-04-06 08:00:00', '2024-04-20 17:00:00'),
(8, 5, 8,  110, 80,  1, '2024-04-06 08:00:00', '2024-04-20 17:00:00'),
(9, 6, 9,  105, 0,   0, '2024-04-12 08:00:00', '2024-04-25 17:00:00'),
(10,4, 10, 70,  70,  2, '2024-04-09 08:00:00', '2024-04-12 17:00:00'),
(11,5, 11, 80,  40,  1, '2024-04-14 08:00:00', '2024-04-25 17:00:00'),
(12,6, 12, 55,  55,  2, '2024-04-19 08:00:00', '2024-04-21 17:00:00');

-- Materials
INSERT OR IGNORE INTO materials (id, name, unit, type) VALUES
(1,  'Cotton Fabric',      'meter', 'origin'),
(2,  'Polyester Fabric',   'meter', 'origin'),
(3,  'Red Dye',            'liter', 'origin'),
(4,  'Blue Dye',           'liter', 'origin'),
(5,  'Silver Thread',      'meter', 'origin'),
(6,  'Zipper',             'piece', 'origin'),
(7,  'Button',             'piece', 'origin'),
(8,  'Cut Cotton Piece',   'piece', 'wip'),
(9,  'Cut Polyester Piece','piece', 'wip');

-- Warehouse
INSERT OR IGNORE INTO warehouse (id, name) VALUES
(1, 'Main Warehouse'),
(2, 'Secondary Warehouse');

-- Warehouse materials
INSERT OR IGNORE INTO warehouse_material (id, warehouse_id, material_id, total_number, left_number) VALUES
(1, 1, 1, 5000, 2000),
(2, 1, 2, 3000, 1500),
(3, 1, 3, 200,  100),
(4, 1, 4, 200,  80),
(5, 1, 5, 1000, 500),
(6, 2, 6, 500,  300),
(7, 2, 7, 2000, 1200),
(8, 2, 8, 300,  100),
(9, 2, 9, 300,  150);

-- Warehouse products (finished goods)
INSERT OR IGNORE INTO warehouse_product (id, warehouse_id, product_id, left_number) VALUES
(1, 1, 1,  50),
(2, 1, 2,  0),
(3, 1, 11, 40),
(4, 2, 5,  0),
(5, 2, 13, 0);
"""


def _exec_sql_block(cursor, sql_block):
    """Execute a block of SQL, skipping blank lines and comment-only lines."""
    import re
    for stmt in sql_block.split(";"):
        # Remove comment lines from the statement
        lines = [l for l in stmt.splitlines() if not l.strip().startswith("--")]
        clean = "\n".join(lines).strip()
        if clean:
            try:
                cursor.execute(clean)
            except Exception as e:
                print(f"Warning: {e}\nSQL: {clean[:100]}")


def setup():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing DB: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    _exec_sql_block(cursor, SCHEMA)
    _exec_sql_block(cursor, SAMPLE_DATA)

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")
    print("Tables: customers, orders, order_product, products, products_types,")
    print("        working_group, cutting_tasks, sewing_tasks, materials,")
    print("        warehouse, warehouse_material, warehouse_product")


if __name__ == "__main__":
    setup()
