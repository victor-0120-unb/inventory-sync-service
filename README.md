Integrate warehouse API, poller, cache, and query endpoint (Day 3 spec)

Fixes:
- db.py: correct DB name mismatch (warehouse_api_db -> warehouse_db)
- db.py: fix get_inventory() query to match actual schema.sql columns;
  join products/warehouses to expose sku + warehouse_code
- db.py: move DB credentials to env vars, drop hardcoded password

Adds:
- response_format.py: uniform {status, data|message} envelope for all routes
- app.py: GET /inventory/<sku> endpoint, reads from stock_cache with
  DB fallback if sku hasn't been polled yet

Changes:
- poller.py: now writes polled results into stock_cache via
  update_stock() instead of just logging the response; points at the
  real warehouse API (port 5000) instead of the standalone mock

Removes:
- Retired standalone mock warehouse API (port 5001) — Victor's
  DB-backed API is now the single source of truth

No changes: stock_cache.py, cache_schema.sql, schema.sql
