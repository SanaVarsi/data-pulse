# Weather API Investigation — Bright Sky / DWD

## What is it?

Bright Sky is a free, open-source JSON API that wraps the Deutscher Wetterdienst (DWD) —
Germany's official national meteorological service. It exposes both historical observations
(from the DWD station network) and forecasts (the MOSMIX model) through one clean endpoint.

## Base URL

```
https://api.brightsky.dev
```

## Authentication

No API key required. Openly accessible.

## Rate Limit

Not officially documented. The API handles over 1 million requests per day in production,
indicating it is built for scale. No hard limit published — monitor usage and add back-off if needed.

## License

Bright Sky itself is MIT licensed. The underlying DWD data is open data:
free to use, share, and build on — including commercially — with attribution to DWD.

## Data Coverage

- All of Germany including Berlin
- Historical weather observations from DWD station network
- Future forecasts via the MOSMIX model
- Active weather alerts and warnings
- Precipitation radar data

## Available Endpoints

### 1. Current Weather
```
GET /current_weather?lat=<lat>&lon=<lon>
```
Returns the latest observation from the nearest DWD station.

### 2. Historical & Forecast Weather
```
GET /weather?lat=<lat>&lon=<lon>&date=<YYYY-MM-DD>&last_date=<YYYY-MM-DD>
```
Returns hourly weather records for a given location and date range.
Covers both past observations and future forecasts.

### 3. Weather Alerts
```
GET /alerts?lat=<lat>&lon=<lon>
```
Returns active DWD weather warnings for a given location.

### 4. Weather Radar
```
GET /radar?...
```
Returns radar precipitation data.

## Key Response Fields

| Field | Description |
|-------|-------------|
| `timestamp` | UTC timestamp of observation |
| `temperature` | Temperature in °C |
| `wind_speed` | Wind speed in km/h |
| `wind_direction` | Wind direction in degrees |
| `precipitation` | Precipitation in mm |
| `cloud_cover` | Cloud cover in % |
| `condition` | Human-readable condition e.g. dry, rain, snow |
| `source` | DWD station or forecast model used |

## Data Format

All responses are JSON. Timestamps are in ISO 8601 UTC format.

## Legal

- Bright Sky is MIT licensed — no restrictions on use
- DWD data is open data — free to use, store, and analyse
- Attribution to DWD required when publishing or sharing data publicly

## Verdict

Bright Sky is selected as the weather data source for data-pulse. It is reliable,
well-maintained, backed by official government data, requires no authentication,
and is free for all use cases. The historical and forecast endpoint is the most
useful for our pipeline — it allows us to build a historical dataset over time
and also query future forecasts.

**Chosen endpoint for pipeline:** `/weather` (historical & forecast)
