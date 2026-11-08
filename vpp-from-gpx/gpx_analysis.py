"""Summarize what can be measured from a GPX track, without calling it a polar."""

from __future__ import annotations

import argparse
import bisect
import json
import math
import statistics
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class TrackPoint:
    timestamp: Optional[datetime]
    latitude: float
    longitude: float
    elevation_m: Optional[float]
    segment: int


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _child_text(element: ET.Element, name: str) -> Optional[str]:
    for child in element:
        if _local_name(child.tag) == name:
            return child.text
    return None


def _parse_timestamp(value: Optional[str], point_number: int) -> Optional[datetime]:
    if value is None or not value.strip():
        return None
    try:
        timestamp = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(
            "Invalid GPX timestamp at track point {}".format(point_number)
        ) from error
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc)


def load_track(path: Path) -> List[TrackPoint]:
    """Load GPX trackpoints, preserving track-segment boundaries."""
    root = ET.parse(str(path)).getroot()
    segments = [element for element in root.iter() if _local_name(element.tag) == "trkseg"]
    if not segments:
        raise ValueError("GPX contains no track segments")

    points: List[TrackPoint] = []
    for segment_number, segment in enumerate(segments):
        for element in segment:
            if _local_name(element.tag) != "trkpt":
                continue
            point_number = len(points) + 1
            try:
                latitude = float(element.attrib["lat"])
                longitude = float(element.attrib["lon"])
            except (KeyError, ValueError) as error:
                raise ValueError(
                    "Invalid coordinates at track point {}".format(point_number)
                ) from error
            if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                raise ValueError(
                    "Coordinates out of range at track point {}".format(point_number)
                )

            timestamp = _parse_timestamp(_child_text(element, "time"), point_number)
            elevation_text = _child_text(element, "ele")
            try:
                elevation = float(elevation_text) if elevation_text else None
            except ValueError as error:
                raise ValueError(
                    "Invalid elevation at track point {}".format(point_number)
                ) from error
            points.append(
                TrackPoint(timestamp, latitude, longitude, elevation, segment_number)
            )

    if not points:
        raise ValueError("GPX contains no trackpoints")
    return points


def _distance_m(a: TrackPoint, b: TrackPoint) -> float:
    earth_radius_m = 6371000.0
    lat_a = math.radians(a.latitude)
    lat_b = math.radians(b.latitude)
    delta_lat = lat_b - lat_a
    delta_lon = math.radians(b.longitude - a.longitude)
    haversine = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat_a) * math.cos(lat_b) * math.sin(delta_lon / 2) ** 2
    )
    return 2 * earth_radius_m * math.asin(math.sqrt(min(1.0, haversine)))


def _bearing_deg(a: TrackPoint, b: TrackPoint) -> float:
    lat_a = math.radians(a.latitude)
    lat_b = math.radians(b.latitude)
    delta_lon = math.radians(b.longitude - a.longitude)
    y = math.sin(delta_lon) * math.cos(lat_b)
    x = (
        math.cos(lat_a) * math.sin(lat_b)
        - math.sin(lat_a) * math.cos(lat_b) * math.cos(delta_lon)
    )
    return (math.degrees(math.atan2(y, x)) + 360.0) % 360.0


def point_rows(points: Sequence[TrackPoint]) -> List[Dict[str, Optional[float]]]:
    """Return one row per fix, with motion over ground from the preceding fix."""
    rows: List[Dict[str, Optional[float]]] = []
    previous: Optional[TrackPoint] = None
    for point in points:
        row: Dict[str, Optional[float]] = {
            "timestamp_utc": (
                point.timestamp.isoformat().replace("+00:00", "Z")
                if point.timestamp
                else None
            ),
            "latitude": point.latitude,
            "longitude": point.longitude,
            "elevation_m": point.elevation_m,
            "segment": point.segment,
            "interval_s": None,
            "distance_from_previous_m": None,
            "sog_m_s": None,
            "sog_knots": None,
            "cog_deg": None,
        }
        if (
            previous is not None
            and previous.segment == point.segment
            and previous.timestamp is not None
            and point.timestamp is not None
        ):
            interval = (point.timestamp - previous.timestamp).total_seconds()
            if interval > 0:
                distance = _distance_m(previous, point)
                sog_m_s = distance / interval
                row.update(
                    {
                        "interval_s": interval,
                        "distance_from_previous_m": distance,
                        "sog_m_s": sog_m_s,
                        "sog_knots": sog_m_s * 1.943844492,
                        "cog_deg": _bearing_deg(previous, point),
                    }
                )
        rows.append(row)
        previous = point
    return rows


def _percentile(values: Sequence[float], percentile: float) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def _window_speeds(
    points: Sequence[TrackPoint], window_seconds: int, tolerance_seconds: int = 2
) -> List[float]:
    by_segment: Dict[int, List[TrackPoint]] = {}
    for point in points:
        by_segment.setdefault(point.segment, []).append(point)

    speeds: List[float] = []
    for segment_points in by_segment.values():
        timestamps = [point.timestamp for point in segment_points]
        if any(timestamp is None for timestamp in timestamps):
            continue
        times = [timestamp for timestamp in timestamps if timestamp is not None]
        if any(b <= a for a, b in zip(times, times[1:])):
            continue
        for start_index, start in enumerate(segment_points):
            if start.timestamp is None:
                continue
            target = start.timestamp + timedelta(seconds=window_seconds)
            insertion = bisect.bisect_left(times, target, lo=start_index + 1)
            candidates = []
            if insertion < len(segment_points):
                candidates.append(insertion)
            if insertion - 1 > start_index:
                candidates.append(insertion - 1)
            if not candidates:
                continue
            end_index = min(
                candidates,
                key=lambda index: abs(
                    (segment_points[index].timestamp - start.timestamp).total_seconds()
                    - window_seconds
                ),
            )
            end = segment_points[end_index]
            if end.timestamp is None:
                continue
            interval = (end.timestamp - start.timestamp).total_seconds()
            if abs(interval - window_seconds) <= tolerance_seconds:
                speeds.append(_distance_m(start, end) / interval)
    return speeds


def summarize(points: Sequence[TrackPoint], window_seconds: int = 10) -> Dict[str, object]:
    if window_seconds <= 0:
        raise ValueError("window_seconds must be positive")

    rows = point_rows(points)
    valid_intervals = [
        row["interval_s"] for row in rows if row["interval_s"] is not None
    ]
    distances = [
        row["distance_from_previous_m"]
        for row in rows
        if row["distance_from_previous_m"] is not None
    ]
    speeds = [row["sog_m_s"] for row in rows if row["sog_m_s"] is not None]
    timed_points = [point.timestamp for point in points if point.timestamp is not None]
    smoothed_speeds = _window_speeds(points, window_seconds)
    segment_numbers = {point.segment for point in points}

    def speed_statistics(values: Sequence[float]) -> Dict[str, Optional[float]]:
        return {
            "count": len(values),
            "min_m_s": min(values) if values else None,
            "median_m_s": _percentile(values, 0.5),
            "p90_m_s": _percentile(values, 0.9),
            "max_m_s": max(values) if values else None,
        }

    return {
        "points": len(points),
        "segments": len(segment_numbers),
        "start_utc": min(timed_points).isoformat().replace("+00:00", "Z")
        if timed_points
        else None,
        "end_utc": max(timed_points).isoformat().replace("+00:00", "Z")
        if timed_points
        else None,
        "duration_s": (max(timed_points) - min(timed_points)).total_seconds()
        if timed_points
        else None,
        "points_without_time": sum(point.timestamp is None for point in points),
        "valid_intervals": len(valid_intervals),
        "median_interval_s": statistics.median(valid_intervals)
        if valid_intervals
        else None,
        "intervals_over_2s": sum(interval > 2 for interval in valid_intervals),
        "intervals_over_10s": sum(interval > 10 for interval in valid_intervals),
        "sampled_path_distance_km": sum(distances) / 1000.0,
        "latitude_range": [min(p.latitude for p in points), max(p.latitude for p in points)],
        "longitude_range": [
            min(p.longitude for p in points),
            max(p.longitude for p in points),
        ],
        "point_to_point_sog": speed_statistics(speeds),
        "window_sog": {
            "window_seconds": window_seconds,
            "endpoint_tolerance_seconds": 2,
            **speed_statistics(smoothed_speeds),
        },
        "limitations": [
            "Derived speeds and courses are over ground, not through water.",
            "No wind, heading, current, boat identity, or sailing configuration is inferred.",
            "A GPX track alone cannot produce a true-wind-speed/true-wind-angle VPP polar.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize a GPX track; output is not a VPP polar."
    )
    parser.add_argument("gpx", type=Path, help="Input GPX file")
    parser.add_argument(
        "--window-seconds",
        type=int,
        default=10,
        help="Displacement interval used for a smoothed SOG summary (default: 10)",
    )
    args = parser.parse_args()
    result = summarize(load_track(args.gpx), args.window_seconds)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
