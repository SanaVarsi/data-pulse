import dlt
import requests

STOP_ID = "900100003"  # S+U Alexanderplatz
API_URL = f"https://v6.bvg.transport.rest/stops/{STOP_ID}/departures"


@dlt.resource(name="departures")
def bvg_departures(results: int = 10):
    response = requests.get(API_URL, params={"results": results})
    response.raise_for_status()

    data = response.json()
    departures = data if isinstance(data, list) else data.get("departures", [])

    for departure in departures:
        yield {
            "trip_id": departure.get("tripId"),
            "line_name": departure.get("line", {}).get("name"),
            "line_mode": departure.get("line", {}).get("mode"),
            "direction": departure.get("direction"),
            "planned_when": departure.get("plannedWhen"),
            "when": departure.get("when"),
            "delay_seconds": departure.get("delay"),
            "stop_id": departure.get("stop", {}).get("id"),
            "stop_name": departure.get("stop", {}).get("name"),
        }


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="bvg_departures",
        destination="duckdb",
        dataset_name="bvg",
    )

    load_info = pipeline.run(bvg_departures())
    print(load_info)
