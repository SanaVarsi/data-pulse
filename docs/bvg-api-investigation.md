# BVG API Investigation

## What is it?

The BVG REST API is an open-source community-built API created by developer Jannis R (derhuerst).
It wraps the official BVG HAFAS backend — the same system that powers the BVG mobile app —
and exposes it as a clean, easy-to-use REST API.

The data is official BVG realtime data. The API itself is free and requires no authentication.

## Base URL

```
https://v6.bvg.transport.rest
```

## License

ISC License — free to use, modify, and build on top of. No restrictions for portfolio or commercial use.

## Authentication

No API key required. Openly accessible.

## Rate Limit

100 requests per minute.

## Data Coverage

- All local transport in Berlin & Brandenburg (U-Bahn, S-Bahn, Bus, Tram)
- Some long-distance trains running through the area
- Realtime delays and service disruptions

## Available Endpoints

### 1. Search for a Stop
```
GET /locations?query=<stop_name>&poi=false&addresses=false
```
Returns stop name, ID, coordinates, and available transport types.

---

### 2. Get Departures from a Stop
```
GET /stops/<stop_id>/departures?results=<number>
```
Returns upcoming departures including line, direction, planned time, actual time, and delay.

**Example:**
```bash
curl 'https://v6.bvg.transport.rest/stops/900100003/departures?results=5'
```

**Key fields:**
| Field | Description |
|-------|-------------|
| `line.name` | Line name e.g. U2, S5, Bus 100 |
| `direction` | Final destination of the line |
| `plannedWhen` | Scheduled departure time |
| `when` | Actual departure time (includes delay) |
| `delay` | Delay in seconds |

---

### 3. Get Journey from A to B
```
GET /journeys?from=<stop_id>&to=<stop_id>&departure=<time>&results=<number>
```
Returns full route with legs, transfers, and delays.

---

## Data Format

All responses are JSON. Timestamps are in ISO 8601 format with timezone offset.
Delays are in seconds.

## Legal

- API built on top of BVG's HAFAS system
- ISC licensed — no restrictions on use
- Data originates from BVG's official backend
- No terms of service violations for storing or analyzing the data

## Verdict

This API is suitable for our data pipeline. The departures endpoint is the most valuable —
it gives us realtime delay data per line per station, which we can store over time and
analyze for patterns, trends, and anomalies.

**Chosen endpoint for pipeline:** `/stops/<id>/departures`
