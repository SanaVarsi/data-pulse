# Data Pulse — End-to-End Pipeline Plan

## Overview

A generic data pipeline repo that ingests data from public APIs, stores and transforms it,
and serves it through dashboards and ML models. Designed to support any data source.

## Pipeline Flow

```
Source API
  ↓
pipelines/<source>/   (dlt — fetch & load raw data into DuckDB)
  ↓
DuckDB                (raw data stored locally)
  ↓
transforms/<source>/  (dbt — clean, rename, aggregate)
  ↓
dashboards/<source>/  (visualize trends and insights)
  ↓
ml/<source>/          (predictions, anomaly detection)
```

## Layers Explained

### 1. Source — Any Public API
Any public API that provides structured data — transport, weather, crypto, finance etc.
One pipeline per source, all following the same pattern.

### 2. Extract & Load — dlt
Fetches data from the source API on a schedule and loads it raw into DuckDB.
One pipeline script per data source under `pipelines/`.

### 3. Storage — DuckDB
Local database that stores all raw ingested data.
Acts as the single source of truth for all downstream layers.

### 4. Transform — dbt
Cleans and models the raw data into analysis-ready tables.
Examples: aggregations, type casting, renaming, calculated fields.

### 5. Dashboard
Visualizations on top of the transformed data.
Shows trends, comparisons, and patterns over time.

### 6. ML / AI
Machine learning models trained on historical data.
Use cases: predictions, anomaly detection, alerting.

## Repo Structure

```
data-pulse/
├── pipelines/
│   └── <source>/
│       └── <source>_pipeline.py
├── transforms/
│   └── <source>/
├── dashboards/
│   └── <source>/
├── ml/
│   └── <source>/
└── docs/
    ├── <source>/
    │   └── <source>-api-investigation.md
    └── pipeline-plan.md
```

## Adding a New Source

Adding a new data source means:
1. Creating a new folder under each layer (`pipelines/`, `transforms/`, `dashboards/`, `ml/`)
2. Writing an API investigation doc under `docs/<source>/`
3. Following the same pipeline pattern
