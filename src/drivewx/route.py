from datetime import datetime, timedelta


def split_coords_by_duration_interval(
    coords: list[list[float]], durations: list[float], interval: int
) -> tuple[list, list, list]:
    stepped_points = []
    stepped_durations = []
    interval_indexes = []
    sum_duration = 0.0
    for idx, duration in enumerate(durations):
        sum_duration += duration
        if sum_duration >= interval:
            stepped_points.append(coords[idx])
            interval_indexes.append(idx)
            stepped_durations.append(sum_duration)
            sum_duration = 0
        if idx == len(durations) - 1 and sum_duration > 0:
            stepped_points.append(coords[idx])
            interval_indexes.append(idx)
            stepped_durations.append(sum_duration)
    return stepped_points, stepped_durations, interval_indexes


def create_times_from_durations(
    start: datetime, durations: list[int]
) -> list[datetime]:
    times = []
    last_time = start
    for duration in durations:
        new_time = last_time + timedelta(seconds=duration)
        times.append(new_time)
        last_time = new_time
    return times


def split_coords_into_segments(
    coords: list[list[float]], indexes: list[int]
) -> list[list[list[float]]]:
    segments = []
    prev_end = 0
    for index in indexes:
        segments.append(coords[prev_end : index + 1])
        prev_end = index
    return segments


def create_line_strings_from_segments(segments: list[list[list[float]]]) -> list[dict]:
    return [
        {
            "properties": {},
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": segment},
        }
        for segment in segments
    ]


def create_feature_collection(line_strings: list[dict]) -> dict:
    return {
        "type": "FeatureCollection",
        "features": line_strings,
    }
