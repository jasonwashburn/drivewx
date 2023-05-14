from datetime import datetime, timedelta


def split_coords_by_duration_interval(
    coords: list[list[float]], durations: list[float], interval: int
) -> tuple[list, list]:
    stepped_coords = []
    stepped_durations = []
    sum_duration = 0.0
    for idx, duration in enumerate(durations):
        sum_duration += duration
        if sum_duration >= interval:
            stepped_coords.append(coords[idx])
            stepped_durations.append(sum_duration)
            sum_duration = 0
        if idx == len(durations) - 1 and sum_duration > 0:
            stepped_coords.append(coords[idx])
            stepped_durations.append(sum_duration)
    return stepped_coords, stepped_durations


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
