# data-pulse

A generic end-to-end data pipeline framework — ingest from any API, store, transform with dbt, visualize, and layer AI/ML on top.

## Pattern

```
API → Ingestion → Database → dbt (transforms) → Dashboard → AI/ML
```

## Projects built on this pattern

- [bvg-pulse](../bvg-pulse) — Berlin public transit data pipeline

## Local development setup
First you need to run these commands to install uv and required pakages 
```
curl -LsSf https://astral.sh/uv/install.sh | sh

uv sync

source .venv/bin/activate
```


