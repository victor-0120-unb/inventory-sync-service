USE warehouse_db;

CREATE TABLE IF NOT EXISTS stock_cache (
    cache_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL,
    warehouse_code VARCHAR(20) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_sku_warehouse (sku, warehouse_code)
);