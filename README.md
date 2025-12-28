# SkyLogix: Logistics Weather Intelligence Pipeline

A Modern Data Engineering Ecosystem for Real-Time Fleet Optimization

---

##  Project Overview

SkyLogix Transportation manages a 1,200-vehicle logistics fleet across the high-growth hubs of Nairobi, Lagos, Accra, and Johannesburg. In these regions, weather isn't just a forecast—it's a critical operational variable. Unexpected storms or visibility issues directly impact delivery windows, vehicle maintenance, and driver safety.

This pipeline provides a robust, automated solution to ingest, normalize, and warehouse weather intelligence, transforming raw API data into actionable insights for the SkyLogix fleet.

---

##  Key Architectural Features

### 1. High-Fidelity Ingestion & Normalization
- **Modular ETL:** Decoupled architecture using dedicated Ingestion (API), Transformation (Schema Logic), and Load (Database) layers.
- **Schema Consistency:** Normalizes varying OpenWeather payloads into a structured format optimized for downstream analytics.

### 2. Scalable OLTP Storage
- **MongoDB Atlas:** Serves as the operational landing zone.
- **Efficient Upserts:** Uses a compound index (`city + observed_at`) to ensure idempotency and prevent duplicate records during frequent polling.

### 3. Incremental Analytical Sync (ELT)
Utilizing Airbyte, the pipeline moves data from MongoDB to DuckDB using a high-efficiency incremental sync pattern:

| Setting        | Value | Purpose |
|----------------|-------|---------|
| Cursor Field   | updatedAt | Tracks new/modified records since the last sync. |
| Primary Key    | _id       | Ensures record uniqueness in the warehouse. |
| Sync Mode      | IncrementalAppend + Deduped | Efficient incremental sync with deduplication. |

---

##  Setup & Installation

### 1. Environment Configuration
Create a `.env` file in the root directory to manage your secrets:

```bash
cp .env.example .env