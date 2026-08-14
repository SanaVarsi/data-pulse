# data-pulse

A generic end-to-end data pipeline framework — ingest from any API, store in DuckDB, transform with dbt, and visualize on a dashboard.

Built as a portfolio project to demonstrate a real-world data engineering stack using open source tools.

## Live Dashboard

🔗 [https://data-pulse101.streamlit.app](https://data-pulse101.streamlit.app)

📄 [dbt Docs](https://sanavarsi.github.io/data-pulse)

## Dashboard Preview

![Dashboard Preview](docs/dashboard.gif)

---

## Architecture

```
Bright Sky API
      │
      ▼
  dlt pipeline
  (Python script)
      │
      ▼
DuckDB — landing.weather
      │
      ▼
  dbt models
  ┌─────────────────────────────┐
  │ Bronze → raw copy of data   │
  │ Silver → cleaned & typed    │
  │ Gold   → daily aggregations │
  └─────────────────────────────┘
      │
      ▼
Streamlit Dashboard
(charts + anomaly detection + 7-day forecast)
```

---

## Tools

| Tool | Purpose |
|---|---|
| **dlt** | Fetches weather data from Bright Sky API and loads it into DuckDB |
| **DuckDB** | Embedded database — stores all raw and transformed data |
| **dbt** | Transforms raw data through Bronze, Silver and Gold layers using SQL |
| **Streamlit** | Interactive dashboard built on top of the Gold table |
| **GitHub Actions** | Schedules the pipeline to run automatically every day |
| **scikit-learn** | Linear regression model for 7-day temperature forecast |
| **uv** | Python package manager |

---

## Project Structure

```
data-pulse/
  pipelines/
    weather/
      weather_pipeline.py    # fetches data from API, loads into DuckDB
  transforms/
    models/
      bronze/
        bronze_weather.sql   # raw copy of landing data
      silver/
        silver_weather.sql   # cleaned and properly typed
      gold/
        gold_weather_daily.sql    # daily aggregations
        gold_weather_anomalies.sql # rolling z-score anomaly detection
  dashboard/
    app.py                   # Streamlit dashboard
    forecast.py              # 7-day temperature forecast model
  .github/
    workflows/
      pipeline.yml           # GitHub Actions daily schedule
      ci.yml                 # dbt build on every PR
```

---

## Local Setup

**1. Install uv**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Install dependencies**
```bash
uv sync
```

**3. Run the pipeline**
```bash
uv run python pipelines/weather/weather_pipeline.py
```

**4. Run dbt models**
```bash
cd transforms
uv run dbt run --profiles-dir .
```

**5. Start the dashboard**
```bash
uv run streamlit run dashboard/app.py
```

---

## Data Source

Weather data is sourced from [Bright Sky](https://brightsky.dev) — a free API built on top of open data from the German Weather Service (DWD). Data covers Berlin (52.52°N, 13.405°E).

---

## What I Learned

- **Medallion architecture** — structuring data into Bronze, Silver and Gold layers keeps raw data safe and transformations clean and auditable
- **dbt** — writing SQL models that reference each other with `{{ ref() }}` and running them in the right order automatically
- **Data quality tests** — adding `not_null` and `unique` tests to catch bad data before it reaches the dashboard
- **GitHub Actions** — scheduling a pipeline to run daily and committing results back to the repo automatically
- **Anomaly detection** — using rolling z-scores to flag unusual weather days without any ML model
- **Linear regression forecasting** — using lag features (past temperatures) to predict future temperatures, and honestly evaluating the model with MAE
- **Git workflow** — working with branches, PRs and squash merges to keep a clean commit history

---

## Planned Features

- **Natural language to SQL** — a text box where users type questions in plain English, an LLM converts it to SQL, DuckDB runs it, and the answer is shown on the dashboard. See [design doc](docs/nl_to_sql_design.md) for implementation details. Deferred due to LLM API cost for deployment.

---

## Known Limitations

- **DuckDB stored in git** — the database file is committed to the repo daily by the pipeline. This works for a portfolio project but will grow over time. [MotherDuck](https://motherduck.com) (hosted DuckDB) is the natural next step for production use.
