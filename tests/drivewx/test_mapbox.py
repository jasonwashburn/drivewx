import json
from unittest.mock import AsyncMock

import pytest
from httpx import Response

from drivewx.mapbox import build_url, get_route_info
from drivewx.models import Coord, Route


def test_build_mapbox_url(mocker) -> None:
    mocker.patch.dict(
        "os.environ",
        {"MAPBOX_ACCESS_TOKEN": "mocked_secret_access_token"},
    )

    coords = [Coord(lon=1.0, lat=2.0), Coord(lon=3.0, lat=4.0)]
    url = build_url(coords)
    assert url == (
        "https://api.mapbox.com/directions/v5/mapbox/driving/1.0,2.0;3.0,4.0?&geometries=geojson&overview=full&annotations=duration&access_token=mocked_secret_access_token"
    )


@pytest.mark.asyncio
async def test_get_route_info(mocker, mock_mapbox_response) -> None:
    # Mock the httpx.AsyncClient and its get method
    mocked_client = AsyncMock()
    content = mock_mapbox_response
    mocked_client.get = AsyncMock(
        return_value=Response(status_code=200, content=content)
    )
    # Mock the build_url function
    build_url_mock = mocker.patch("drivewx.mapbox.build_url")
    build_url_mock.return_value = "http://example.com"

    # Patch the httpx.AsyncClient context manager
    mocked_async_client = mocker.patch("drivewx.mapbox.httpx.AsyncClient")
    mocked_async_client.return_value.__aenter__.return_value = mocked_client

    # Define the test data
    coords = [Coord(lon=0.0, lat=0.0), Coord(lon=1.0, lat=1.0)]

    # Call the function being tested
    result = await get_route_info(coords)
    route = Route(**json.loads(mock_mapbox_response)["routes"][0])

    # Assertions
    assert result == route
    build_url_mock.assert_called_once_with(coords)
    mocked_client.get.assert_called_once_with("http://example.com")
