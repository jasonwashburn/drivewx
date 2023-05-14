import datetime

from drivewx.route import create_times_from_durations, split_coords_by_duration_interval


def test_split_coords_by_duration_interval() -> None:
    coords = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0], [9.0, 10.0]]
    durations = [10.0, 5.0, 14.0, 2.0, 3.0]
    interval = 15
    expected_coords = [[3, 4], [7, 8], [9, 10]]
    expected_durations = [15, 16, 3]
    coords, durations = split_coords_by_duration_interval(coords, durations, interval)
    assert coords == expected_coords
    assert durations == expected_durations


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
