# Natural Language to SQL — Design

## What it does

A text box on the dashboard where users type questions in plain English. An LLM converts the question to SQL, DuckDB runs it against the gold table, and the answer is shown as a table.

**Example:**
> User types: "which day was windiest last month?"
> LLM writes: `SELECT date, max_wind_speed_kmh FROM gold_weather_daily ORDER BY max_wind_speed_kmh DESC LIMIT 1`
> Result shown on dashboard.

---

## Flow

```
User types question
        ↓
Question + table schema sent to LLM
        ↓
LLM returns a SELECT query
        ↓
DuckDB runs the query (read-only)
        ↓
Result displayed as a table on dashboard
```

---

## Implementation

```python
import anthropic
import duckdb

SCHEMA = """
Table: gold_weather_daily
Columns: date, avg_temp_c, max_temp_c, min_temp_c,
         avg_wind_speed_kmh, max_wind_speed_kmh,
         total_precipitation_mm, avg_cloud_cover_pct, hour_count
"""

def ask(question: str) -> str:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"Given this table schema:\n{SCHEMA}\nWrite a single SQL SELECT query to answer: {question}\nReturn only the SQL, nothing else."
        }]
    )
    sql = message.content[0].text.strip()
    conn = duckdb.connect("bright_sky_weather.duckdb", read_only=True)
    return conn.execute(sql).df()
```

---

## Safety

- DuckDB connection is `read_only=True` — no writes possible
- Only SELECT queries should be allowed — add a guard in production:
  ```python
  if not sql.strip().upper().startswith("SELECT"):
      raise ValueError("Only SELECT queries allowed")
  ```

---

## Why deferred

Requires a paid LLM API key (Claude or OpenAI) to work when deployed on Streamlit Cloud. For local use, Ollama (free, runs locally) is an alternative but does not work for deployed apps.
