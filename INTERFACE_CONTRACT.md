# Interface Contract — Stock Cache Service

Owner: [your name] — cache/storage layer
For: whoever builds the warehouse-side webhook trigger, and whoever builds the chat frontend

Base URL (local dev): `http://127.0.0.1:5002`

---

## 1. Writing a stock update (warehouse → cache)

**Whoever triggers stock-change events on the warehouse side calls this.**

```
POST /webhook/stock-update
Content-Type: application/json
```

Request body:
```json
{
  "sku": "SKU001",
  "warehouse_code": "WH-NRB",
  "quantity": 12
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `sku` | string | yes | Product identifier as known by the warehouse |
| `warehouse_code` | string | yes | e.g. `WH-NRB`, `WH-MSA` |
| `quantity` | integer | yes | Must be >= 0 |

Responses:
- `200` — cached successfully:
  ```json
  { "status": "cached", "sku": "SKU001", "warehouse_code": "WH-NRB", "quantity": 12 }
  ```
- `400` — missing field, non-integer quantity, or negative quantity:
  ```json
  { "error": "quantity cannot be negative" }
  ```

Sending the same `sku` + `warehouse_code` again **overwrites** the previous quantity (it's always "latest known stock", not a history log).

---

## 2. Reading stock for one sku (chat frontend → cache)

**The support chatbot calls this to answer "is X in stock?"**

```
GET /stock/<sku>
```

Example: `GET /stock/SKU001`

Response `200`:
```json
[
  {
    "sku": "SKU001",
    "warehouse_code": "WH-NRB",
    "quantity": 12,
    "last_updated": "2026-08-20 10:41:03"
  }
]
```

Note: it's a **list**, one row per warehouse that has reported stock for that sku. Sum `quantity` across rows for a total, or show per-warehouse detail — frontend's call.

Response `404` if the sku has never been reported:
```json
{ "error": "No cached stock found for sku 'SKU999'" }
```

---

## 3. Reading everything cached (debugging / dashboard)

```
GET /stock
```

Response `200`: array of every `{sku, warehouse_code, quantity, last_updated}` row currently cached.

---

## 4. What NOT to assume

- There's no push notification back to the frontend — it's pull-based. The chatbot should call `GET /stock/<sku>` fresh on every user question, not cache a copy client-side.
- `last_updated` reflects when *the cache* last wrote that row, not necessarily the moment the real-world stock changed — good enough to show "as of X" in the chat reply.
- No auth on `/webhook/stock-update` yet (flagged as deferred in the Scope Delta Analysis) — don't expose this service to the public internet as-is.
