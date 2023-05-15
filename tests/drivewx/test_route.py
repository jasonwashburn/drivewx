import datetime

from drivewx.route import (
    create_feature_collection,
    create_line_strings_from_segments,
    create_times_from_durations,
    split_coords_by_duration_interval,
    split_coords_into_segments,
)


def test_split_coords_by_duration_interval() -> None:
    coords = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0], [9.0, 10.0]]
    durations = [10.0, 5.0, 14.0, 2.0, 3.0]
    interval = 15
    expected_points = [[3, 4], [7, 8], [9, 10]]
    expected_durations = [15, 16, 3]
    expected_indexes = [1, 3, 4]
    points, durations, interval_indexes = split_coords_by_duration_interval(
        coords, durations, interval
    )
    assert points == expected_points
    assert durations == expected_durations
    assert interval_indexes == expected_indexes


def test_split_coords_into_segments() -> None:
    coords = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0], [9.0, 10.0]]
    indexes = [1, 3, 4]
    expected_segments = [
        [[1.0, 2.0], [3.0, 4.0]],
        [[3.0, 4.0], [5.0, 6.0], [7.0, 8.0]],
        [[7.0, 8.0], [9.0, 10.0]],
    ]
    segments = split_coords_into_segments(coords, indexes)
    assert segments == expected_segments


def test_create_line_strings_from_segments() -> None:
    segments = [
        [[1.0, 2.0], [3.0, 4.0]],
        [[3.0, 4.0], [5.0, 6.0], [7.0, 8.0]],
        [[7.0, 8.0], [9.0, 10.0]],
    ]
    expected = [
        {
            "properties": {},
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": segment},
        }
        for segment in segments
    ]
    line_strings = create_line_strings_from_segments(segments)
    assert line_strings == expected


def test_create_feature_collection() -> None:
    line_strings = [
        {
            "properties": {},
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": [[1.0, 2.0], [3.0, 4.0]]},
        },
        {
            "properties": {},
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[3.0, 4.0], [5.0, 6.0], [7.0, 8.0]],
            },
        },
        {
            "properties": {},
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[7.0, 8.0], [9.0, 10.0]],
            },
        },
    ]
    expected = {
        "type": "FeatureCollection",
        "features": line_strings,
    }
    feature_collection = create_feature_collection(line_strings)
    assert feature_collection == expected


def test_create_times_from_durations() -> None:
    start = datetime.datetime(
        year=2023,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
        tzinfo=datetime.timezone.utc,
    )
    durations = [15 * 60, 16 * 60, 17 * 60]
    excepted_times = [
        datetime.datetime(
            year=2023,
            month=1,
            day=1,
            hour=0,
            minute=15,
            second=0,
            tzinfo=datetime.timezone.utc,
        ),
        datetime.datetime(
            year=2023,
            month=1,
            day=1,
            hour=0,
            minute=31,
            second=0,
            tzinfo=datetime.timezone.utc,
        ),
        datetime.datetime(
            year=2023,
            month=1,
            day=1,
            hour=0,
            minute=48,
            second=0,
            tzinfo=datetime.timezone.utc,
        ),
    ]
    times = create_times_from_durations(start, durations)
    assert times == excepted_times
