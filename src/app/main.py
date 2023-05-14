from datetime import UTC, datetime

from fastapi import FastAPI

from drivewx.mapbox import get_route_info
from drivewx.models import Coord
from drivewx.route import create_times_from_durations, split_coords_by_duration_interval

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/route/")
async def route(
    start: str, end: str, interval: int = 900, start_time: datetime | None = None
) -> dict[str, list | str]:
    lon, lat = start.split(",")
    start_coord = Coord(lat=float(lat), lon=float(lon))
    lon, lat = end.split(",")
    end_coord = Coord(lat=float(lat), lon=float(lon))
    if start_time is None:
        start_time = datetime.now(tz=UTC)

    if route := await get_route_info([start_coord, end_coord]):
        coords = route.get_coords()
        durations = route.get_durations()
        stepped_coords, stepped_durations = split_coords_by_duration_interval(
            coords, durations, interval
        )
        times = create_times_from_durations(
            start=start_time, durations=stepped_durations
        )
        return {
            "coords": stepped_coords,
            "durations": stepped_durations,
            "times": times,
        }
    else:
        return {"error": "No route found"}
