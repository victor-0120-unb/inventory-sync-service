CREATE DATABASE IF NOT EXISTS warehouse_db;
USE warehouse_db;

-- =========================
-- WAREHOUSES
-- =========================
CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_code VARCHAR(20) UNIQUE NOT NULL,
    warehouse_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL
);

-- =========================
-- PRODUCTS
-- =========================
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(150) NOT NULL
);

-- =========================
-- INVENTORY
-- =========================
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id),
    UNIQUE (warehouse_id, product_id)
);

-- =========================
-- MOCK WAREHOUSE DATA
-- =========================
INSERT IGNORE INTO warehouses
(warehouse_code, warehouse_name, location)
VALUES
('WH-NRB', 'Nairobi Central Warehouse', 'Nairobi'),
('WH-MSA', 'Mombasa Distribution Center', 'Mombasa'),
('WH-ELD', 'Eldoret Warehouse', 'Eldoret'),
('WH-KSM', 'Kisumu Warehouse', 'Kisumu');

-- =========================
-- MOCK PRODUCT DATA
-- =========================
INSERT IGNORE INTO products
(sku, product_name)
VALUES
('SKU-1001', 'Wireless Mouse'),
('SKU-1002', 'USB Keyboard'),
('SKU-1003', 'Laptop Stand'),
('SKU-1004', 'USB-C Cable'),
('SKU-1005', 'Wireless Headphones'),
('SKU-1006', 'HD Webcam'),
('SKU-1007', 'Power Bank'),
('SKU-1008', 'Mechanical Keyboard');

-- =========================
-- MOCK INVENTORY DATA
-- =========================
INSERT IGNORE INTO inventory
(warehouse_id, product_id, quantity)
VALUES
(1, 1, 150), (1, 2, 85), (1, 3, 40), (1, 4, 200),
(1, 5, 65), (1, 6, 30), (1, 7, 90), (1, 8, 25),
(2, 1, 75), (2, 2, 50), (2, 3, 20), (2, 4, 100),
(2, 5, 40), (2, 6, 15), (2, 7, 55), (2, 8, 10),
(3, 1, 60), (3, 2, 45), (3, 3, 15), (3, 4, 80),
(3, 5, 25), (3, 6, 10), (3, 7, 35), (3, 8, 8),
(4, 1, 50), (4, 2, 30), (4, 3, 10), (4, 4, 65),
(4, 5, 20), (4, 6, 5), (4, 7, 25), (4, 8, 5);