-- =========================
-- STOCK CACHE (Day 4 pivot)
-- =========================
--
-- Storage layer for the webhook push model. This table holds the LATEST
-- known stock level per (sku, warehouse_code), as pushed by the warehouse
-- system, decoupled from the original `inventory` table (which stays
-- untouched, per the Assignment 2 requirement not to break existing
-- features). Keyed by the natural identifiers the webhook payload carries
-- (sku, warehouse_code) rather than internal auto-increment IDs, since
-- the external warehouse system does not know our internal product_id /
-- warehouse_id values.
--
-- Run this after schema.sql (it uses the same database).

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
