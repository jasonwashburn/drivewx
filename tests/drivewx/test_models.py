import json

from drivewx.models import Route


def test_route_get_durations(simple_route_fixture) -> None:
    durations = simple_route_fixture.get_durations()
    assert durations == [1.0, 2.0, 2.0, 5.0]


def test_route_get_coords(simple_route_fixture) -> None:
    coords = simple_route_fixture.get_coords()
    assert coords == [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]


def test_route_model_loads_route() -> None:
    with open("tests/test_route.json") as f:
        route_json = json.load(f)["routes"][0]
        route = Route.parse_obj(route_json)

    assert isinstance(route, Route)
