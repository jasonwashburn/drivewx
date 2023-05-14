from __future__ import annotations

from pydantic import BaseModel, Field


class Annotation(BaseModel):
    duration: list[float]


class Admin(BaseModel):
    iso_3166_1_alpha3: str
    iso_3166_1: str


class Coord(BaseModel):
    lat: float
    lon: float


class Leg(BaseModel):
    via_waypoints: list
    annotation: Annotation
    admins: list[Admin]
    weight: float
    duration: float
    steps: list
    distance: float
    summary: str


class Geometry(BaseModel):
    coordinates: list[list[float]]
    geometry_type: str = Field(..., alias="type")


class Route(BaseModel):
    weight_name: str
    weight: float
    duration: float
    distance: float
    legs: list[Leg]
    geometry: Geometry

    def get_durations(self) -> list[float]:
        return self.legs[0].annotation.duration

    def get_coords(self) -> list[list[float]]:
        return self.geometry.coordinates


class Waypoint(BaseModel):
    distance: float
    name: str
    location: list[float]


class Model(BaseModel):
    routes: list[Route]
    waypoints: list[Waypoint]
    code: str
    uuid: str
