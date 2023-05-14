import pytest

from drivewx.models import Admin, Annotation, Geometry, Leg, Route


@pytest.fixture
def simple_route_fixture() -> Route:
    test_route = Route(
        weight_name="auto",
        weight=1.0,
        duration=10.0,
        distance=10.0,
        legs=[
            Leg(
                via_waypoints=[],
                annotation=Annotation(duration=[1.0, 2.0, 2.0, 5.0]),
                admins=[
                    Admin(iso_3166_1_alpha3="USA", iso_3166_1="US"),
                ],
                weight=1.0,
                duration=10.0,
                steps=[],
                distance=10.0,
                summary="Summary",
            )
        ],
        geometry=Geometry(
            coordinates=[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
            type="LineString",
        ),
    )
    return test_route


@pytest.fixture
def mock_mapbox_response():
    with open("tests/test_route.json") as f:
        route_json = f.read()
    return route_json
