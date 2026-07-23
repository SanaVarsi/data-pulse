import dlt
import requests
from datetime import date, timedelta

# Berlin coordinates
LAT = 52.52
LON = 13.405

BASE_URL = "https://api.brightsky.dev/weather"


@dlt.resource(name="weather", primary_key="timestamp", write_disposition="merge")
def bright_sky_weather(
    updated_at: dlt.sources.incremental[str] = dlt.sources.incremental(
        "timestamp", initial_value=(date.today() - timedelta(days=1)).isoformat()
    ),
):
    """
    Fetches hourly weather data from Bright Sky for Berlin.

    Uses dlt incremental loading on the timestamp field.
    - First run: fetches from yesterday (sample ~24 rows)
    - Subsequent runs: fetches only records newer than the last loaded timestamp
    This ensures we never re-fetch or duplicate data.
    """
    start_date = updated_at.last_value[:10]  # extract YYYY-MM-DD from timestamp
    end_date = date.today().isoformat()

    params = {
        "lat": LAT,
        "lon": LON,
        "date": start_date,
        "last_date": end_date,
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()
    records = data.get("weather", [])

    print(f"Fetched {len(records)} rows from {start_date} to {end_date}")

    for record in records:
        yield {
            "timestamp": record.get("timestamp"),
            "temperature": record.get("temperature"),
            "wind_speed": record.get("wind_speed"),
            "wind_direction": record.get("wind_direction"),
            "precipitation": record.get("precipitation"),
            "cloud_cover": record.get("cloud_cover"),
            "condition": record.get("condition"),
            "source_id": record.get("source_id"),
        }


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="bright_sky_weather",
        destination="duckdb",
        dataset_name="landing",
    )

    load_info = pipeline.run(bright_sky_weather())
    print(load_info)
