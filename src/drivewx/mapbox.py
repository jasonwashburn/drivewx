import os

import httpx

from drivewx.models import Coord, Route


def build_url(coords: list[Coord]) -> str:
    return (
        "https://api.mapbox.com/directions/v5/mapbox/driving/"
        + ";".join([f"{coord.lon},{coord.lat}" for coord in coords])
        + "?&geometries=geojson&overview=full&annotations=duration&access_token="
        + os.getenv("MAPBOX_ACCESS_TOKEN", "none")
    )


async def get_route_info(coords: list[Coord]) -> Route | None:
    async with httpx.AsyncClient() as client:
        resp = await client.get(build_url(coords))
    route = Route(**resp.json()["routes"][0])
    return route
