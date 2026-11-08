"""Extract GPS5 telemetry from GoPro MP4 files containing a GPMF track."""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import math
import statistics
import struct
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Box:
    start: int
    size: int
    kind: bytes
    header_size: int


@dataclass(frozen=True)
class GpmfRecord:
    key: str
    data_type: str
    structure_size: int
    repeat: int
    payload: bytes
    children: Tuple["GpmfRecord", ...] = ()


@dataclass(frozen=True)
class GpsBlock:
    gpsu_utc: datetime
    gps_points: Tuple[Tuple[float, float, float, float, float], ...]
    fix: Optional[int]
    precision_raw: Optional[int]


@dataclass(frozen=True)
class GpsPoint:
    timestamp_utc: datetime
    gpsu_utc: datetime
    block_index: int
    sample_in_block: int
    latitude: float
    longitude: float
    altitude_m: float
    speed_2d_m_s: float
    speed_3d_m_s: float
    fix: Optional[int]
    precision_raw: Optional[int]


def _read_box(source, position: int, parent_end: int) -> Optional[Box]:
    if position + 8 > parent_end:
        return None
    source.seek(position)
    header = source.read(8)
    if len(header) != 8:
        raise ValueError("Truncated MP4 box header at byte {}".format(position))
    size, kind = struct.unpack(">I4s", header)
    header_size = 8
    if size == 1:
        extended = source.read(8)
        if len(extended) != 8:
            raise ValueError("Truncated extended MP4 box header")
        size = struct.unpack(">Q", extended)[0]
        header_size = 16
    elif size == 0:
        size = parent_end - position
    if size < header_size or position + size > parent_end:
        raise ValueError(
            "Invalid {} MP4 box size {} at byte {}".format(
                kind.decode("latin1"), size, position
            )
        )
    return Box(position, size, kind, header_size)


def _iter_boxes(source, start: int, end: int) -> Iterable[Box]:
    position = start
    while position + 8 <= end:
        box = _read_box(source, position, end)
        if box is None:
            break
        yield box
        position += box.size


def _box_children(source, box: Box) -> List[Box]:
    start = box.start + box.header_size
    if box.kind == b"meta":
        start += 4
    return list(_iter_boxes(source, start, box.start + box.size))


def _child(source, box: Box, kind: bytes) -> Optional[Box]:
    return next((item for item in _box_children(source, box) if item.kind == kind), None)


def _box_payload(source, box: Box) -> bytes:
    source.seek(box.start + box.header_size)
    return source.read(box.size - box.header_size)


def _gpmf_sample_table(source, track: Box) -> List[Tuple[int, int]]:
    mdia = _child(source, track, b"mdia")
    if mdia is None:
        return []
    hdlr = _child(source, mdia, b"hdlr")
    if hdlr is None:
        return []
    source.seek(hdlr.start + hdlr.header_size + 8)
    if source.read(4) != b"meta":
        return []

    minf = _child(source, mdia, b"minf")
    stbl = _child(source, minf, b"stbl") if minf else None
    if stbl is None:
        return []
    stsd = _child(source, stbl, b"stsd")
    if stsd is None:
        return []
    source.seek(stsd.start + stsd.header_size + 4)
    count_data = source.read(4)
    if len(count_data) != 4:
        raise ValueError("Invalid MP4 sample description table")
    entry_count = struct.unpack(">I", count_data)[0]
    sample_entries = list(
        _iter_boxes(
            source,
            stsd.start + stsd.header_size + 8,
            stsd.start + stsd.size,
        )
    )
    if not any(entry.kind == b"gpmd" for entry in sample_entries[:entry_count]):
        return []

    stsz = _child(source, stbl, b"stsz")
    stsc = _child(source, stbl, b"stsc")
    offsets_box = _child(source, stbl, b"stco") or _child(source, stbl, b"co64")
    if stsz is None or stsc is None or offsets_box is None:
        raise ValueError("GPMF track is missing a required MP4 sample table")

    source.seek(stsz.start + stsz.header_size + 4)
    raw = source.read(8)
    if len(raw) != 8:
        raise ValueError("Invalid MP4 sample-size table")
    constant_size, sample_count = struct.unpack(">II", raw)
    if constant_size:
        sample_sizes = [constant_size] * sample_count
    else:
        raw = source.read(4 * sample_count)
        if len(raw) != 4 * sample_count:
            raise ValueError("Truncated MP4 sample-size table")
        sample_sizes = list(struct.unpack(">{}I".format(sample_count), raw))

    source.seek(stsc.start + stsc.header_size + 4)
    raw = source.read(4)
    if len(raw) != 4:
        raise ValueError("Invalid MP4 sample-to-chunk table")
    entry_count = struct.unpack(">I", raw)[0]
    raw = source.read(12 * entry_count)
    if len(raw) != 12 * entry_count:
        raise ValueError("Truncated MP4 sample-to-chunk table")
    chunk_map = [
        struct.unpack_from(">III", raw, index * 12)
        for index in range(entry_count)
    ]

    source.seek(offsets_box.start + offsets_box.header_size + 4)
    raw = source.read(4)
    if len(raw) != 4:
        raise ValueError("Invalid MP4 chunk-offset table")
    chunk_count = struct.unpack(">I", raw)[0]
    offset_width = 8 if offsets_box.kind == b"co64" else 4
    raw = source.read(offset_width * chunk_count)
    if len(raw) != offset_width * chunk_count:
        raise ValueError("Truncated MP4 chunk-offset table")
    offset_format = "Q" if offset_width == 8 else "I"
    chunk_offsets = struct.unpack(">{}{}".format(chunk_count, offset_format), raw)

    if not chunk_map:
        raise ValueError("Empty MP4 sample-to-chunk table")
    locations: List[Tuple[int, int]] = []
    map_index = 0
    sample_index = 0
    for chunk_number, chunk_offset in enumerate(chunk_offsets, start=1):
        while (
            map_index + 1 < len(chunk_map)
            and chunk_map[map_index + 1][0] <= chunk_number
        ):
            map_index += 1
        samples_in_chunk = chunk_map[map_index][1]
        offset = chunk_offset
        for _ in range(samples_in_chunk):
            if sample_index >= sample_count:
                break
            sample_size = sample_sizes[sample_index]
            locations.append((offset, sample_size))
            offset += sample_size
            sample_index += 1
    if sample_index != sample_count:
        raise ValueError(
            "MP4 chunk table maps {} of {} GPMF samples".format(
                sample_index, sample_count
            )
        )
    return locations


def _gpmf_locations(source) -> List[Tuple[int, int]]:
    source.seek(0, 2)
    file_size = source.tell()
    top_level = list(_iter_boxes(source, 0, file_size))
    moov = next((box for box in top_level if box.kind == b"moov"), None)
    if moov is None:
        raise ValueError("No readable MP4 moov box found")
    locations: List[Tuple[int, int]] = []
    for track in (box for box in _box_children(source, moov) if box.kind == b"trak"):
        locations = _gpmf_sample_table(source, track)
        if locations:
            return locations
    raise ValueError("No GoPro GPMF (gpmd) telemetry track found")


def _parse_gpmf_records(data: bytes) -> Tuple[GpmfRecord, ...]:
    records: List[GpmfRecord] = []
    position = 0
    while position + 8 <= len(data):
        key_bytes = data[position : position + 4]
        data_type = chr(data[position + 4])
        structure_size = data[position + 5]
        repeat = struct.unpack_from(">H", data, position + 6)[0]
        payload_size = structure_size * repeat
        payload_start = position + 8
        payload_end = payload_start + payload_size
        if payload_end > len(data):
            raise ValueError(
                "GPMF record {} exceeds its containing payload".format(
                    key_bytes.decode("latin1")
                )
            )
        payload = data[payload_start:payload_end]
        try:
            key = key_bytes.decode("ascii")
        except UnicodeDecodeError as error:
            raise ValueError("Invalid GPMF key") from error
        children = (
            _parse_gpmf_records(payload) if data_type == "\x00" else ()
        )
        records.append(
            GpmfRecord(
                key, data_type, structure_size, repeat, payload, children
            )
        )
        position = payload_start + ((payload_size + 3) // 4) * 4
    if any(data[position:]):
        raise ValueError("Unexpected trailing bytes in GPMF payload")
    return tuple(records)


def _record_bytes(records: Sequence[GpmfRecord], key: str) -> Optional[bytes]:
    record = next((item for item in records if item.key == key), None)
    return record.payload if record is not None else None


def _decode_unsigned(records: Sequence[GpmfRecord], key: str) -> Optional[int]:
    record = next((item for item in records if item.key == key), None)
    if record is None or not record.payload:
        return None
    formats = {"B": "B", "S": "H", "L": "I"}
    fmt = formats.get(record.data_type)
    if fmt is None or len(record.payload) not in (1, 2, 4):
        raise ValueError("Unsupported {} GPMF value format".format(key))
    return struct.unpack(">" + fmt, record.payload)[0]


def _decode_gpsu(payload: bytes) -> datetime:
    text = payload.decode("ascii").strip("\x00 ")
    if len(text) < 15:
        raise ValueError("Invalid GPMF GPSU timestamp {!r}".format(text))
    try:
        year = 2000 + int(text[0:2])
        return datetime.strptime(
            "{:04d}{}".format(year, text[2:]), "%Y%m%d%H%M%S.%f"
        ).replace(tzinfo=timezone.utc)
    except ValueError as error:
        raise ValueError("Invalid GPMF GPSU timestamp {!r}".format(text)) from error


def _decode_gps_stream(stream: GpmfRecord) -> Optional[GpsBlock]:
    records = stream.children
    gps5 = next((record for record in records if record.key == "GPS5"), None)
    if gps5 is None:
        return None
    gpsu = next((record for record in records if record.key == "GPSU"), None)
    if gpsu is None:
        raise ValueError("GPS5 stream has no GPSU timestamp")

    gps5_index = records.index(gps5)
    scale_record = next(
        (
            record
            for record in reversed(records[:gps5_index])
            if record.key == "SCAL"
        ),
        None,
    )
    if scale_record is None or scale_record.data_type != "l":
        raise ValueError("GPS5 stream has no preceding signed-integer SCAL")
    if len(scale_record.payload) != 20:
        raise ValueError("GPS5 SCAL must contain five signed 32-bit scales")
    scales = struct.unpack(">5i", scale_record.payload)
    if any(scale == 0 for scale in scales):
        raise ValueError("GPS5 scale factors must be nonzero")
    if gps5.data_type != "l" or gps5.structure_size != 20:
        raise ValueError("Unsupported GPS5 record layout")
    if len(gps5.payload) != gps5.repeat * 20:
        raise ValueError("Invalid GPS5 payload length")

    raw_values = struct.unpack(">{}i".format(gps5.repeat * 5), gps5.payload)
    gps_points = []
    for index in range(gps5.repeat):
        values = raw_values[index * 5 : index * 5 + 5]
        gps_points.append(
            tuple(value / scale for value, scale in zip(values, scales))
        )
    return GpsBlock(
        _decode_gpsu(gpsu.payload),
        tuple(gps_points),
        _decode_unsigned(records, "GPSF"),
        _decode_unsigned(records, "GPSP"),
    )


def extract_gps(mp4_path: Path) -> Tuple[List[GpsBlock], Optional[str], int]:
    blocks: List[GpsBlock] = []
    camera_name: Optional[str] = None
    with mp4_path.open("rb") as source:
        locations = _gpmf_locations(source)
        for offset, size in locations:
            source.seek(offset)
            payload = source.read(size)
            if len(payload) != size:
                raise ValueError("Could not read a complete GPMF sample")
            for device in _parse_gpmf_records(payload):
                if device.key != "DEVC":
                    continue
                if camera_name is None:
                    name = _record_bytes(device.children, "DVNM")
                    if name:
                        camera_name = name.decode("ascii", "replace").rstrip("\x00 ")
                for stream in device.children:
                    if stream.key == "STRM":
                        block = _decode_gps_stream(stream)
                        if block is not None:
                            blocks.append(block)
    if not blocks:
        raise ValueError("GPMF track contains no decodable GPS5 records")
    return blocks, camera_name, len(locations)


def expand_gps_blocks(blocks: Sequence[GpsBlock]) -> List[GpsPoint]:
    if not blocks:
        return []
    ordered = sorted(blocks, key=lambda block: block.gpsu_utc)
    deltas = [
        (b.gpsu_utc - a.gpsu_utc).total_seconds()
        for a, b in zip(ordered, ordered[1:])
        if 0 < (b.gpsu_utc - a.gpsu_utc).total_seconds() <= 5
    ]
    fallback_delta = statistics.median(deltas) if deltas else 1.0
    result: List[GpsPoint] = []
    for block_index, block in enumerate(ordered):
        if block_index + 1 < len(ordered):
            next_block = ordered[block_index + 1]
            interval = (next_block.gpsu_utc - block.gpsu_utc).total_seconds()
            if interval <= 0 or interval > 5:
                interval = fallback_delta
        else:
            interval = fallback_delta
        count = len(block.gps_points)
        for sample_index, values in enumerate(block.gps_points):
            latitude, longitude, altitude, speed_2d, speed_3d = values
            timestamp = block.gpsu_utc + timedelta(
                seconds=interval * sample_index / count
            )
            result.append(
                GpsPoint(
                    timestamp,
                    block.gpsu_utc,
                    block_index,
                    sample_index,
                    latitude,
                    longitude,
                    altitude,
                    speed_2d,
                    speed_3d,
                    block.fix,
                    block.precision_raw,
                )
            )
    return result


def _percentile(values: Sequence[float], percentile: float) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def _summary(
    mp4_path: Path,
    camera_name: Optional[str],
    sample_count: int,
    blocks: Sequence[GpsBlock],
    points: Sequence[GpsPoint],
) -> Dict[str, object]:
    speeds_2d = [point.speed_2d_m_s for point in points]
    speeds_3d = [point.speed_3d_m_s for point in points]
    fixes: Dict[str, int] = {}
    for point in points:
        key = str(point.fix) if point.fix is not None else "missing"
        fixes[key] = fixes.get(key, 0) + 1
    start = min((point.timestamp_utc for point in points), default=None)
    end = max((point.timestamp_utc for point in points), default=None)

    def speed_stats(values: Sequence[float]) -> Dict[str, Optional[float]]:
        return {
            "median_m_s": _percentile(values, 0.5),
            "p90_m_s": _percentile(values, 0.9),
            "max_m_s": max(values) if values else None,
        }

    return {
        "source_file": str(mp4_path),
        "source_size_bytes": mp4_path.stat().st_size,
        "camera": camera_name,
        "gpmf_samples": sample_count,
        "gps_blocks": len(blocks),
        "gps_points": len(points),
        "start_utc_estimated": start.isoformat().replace("+00:00", "Z")
        if start
        else None,
        "end_utc_estimated": end.isoformat().replace("+00:00", "Z")
        if end
        else None,
        "gps_fix_counts": fixes,
        "gps_precision_raw_range": [
            min((p.precision_raw for p in points if p.precision_raw is not None), default=None),
            max((p.precision_raw for p in points if p.precision_raw is not None), default=None),
        ],
        "latitude_range": [
            min((p.latitude for p in points), default=None),
            max((p.latitude for p in points), default=None),
        ],
        "longitude_range": [
            min((p.longitude for p in points), default=None),
            max((p.longitude for p in points), default=None),
        ],
        "gps_speed_2d": speed_stats(speeds_2d),
        "gps_speed_3d": speed_stats(speeds_3d),
        "timing_note": (
            "Sub-sample timestamps are estimated by evenly spacing GPS5 fixes "
            "between successive GPSU packet timestamps."
        ),
        "vpp_note": (
            "GPS speed is ground-relative, not boat speed through water. "
            "No wind, heading, or current is present in these outputs."
        ),
    }


def _write_csv(path: Path, points: Sequence[GpsPoint]) -> None:
    fields = [
        "timestamp_utc_estimated",
        "gpsu_block_utc",
        "block_index",
        "sample_in_block",
        "latitude_deg",
        "longitude_deg",
        "altitude_m",
        "gps_speed_2d_m_s",
        "gps_speed_3d_m_s",
        "gps_fix",
        "gps_precision_raw",
    ]
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for point in points:
            writer.writerow(
                {
                    "timestamp_utc_estimated": point.timestamp_utc.isoformat().replace(
                        "+00:00", "Z"
                    ),
                    "gpsu_block_utc": point.gpsu_utc.isoformat().replace(
                        "+00:00", "Z"
                    ),
                    "block_index": point.block_index,
                    "sample_in_block": point.sample_in_block,
                    "latitude_deg": point.latitude,
                    "longitude_deg": point.longitude,
                    "altitude_m": point.altitude_m,
                    "gps_speed_2d_m_s": point.speed_2d_m_s,
                    "gps_speed_3d_m_s": point.speed_3d_m_s,
                    "gps_fix": point.fix,
                    "gps_precision_raw": point.precision_raw,
                }
            )


def _write_gpx(path: Path, points: Sequence[GpsPoint], name: str) -> None:
    namespace = "http://www.topografix.com/GPX/1/1"
    ET.register_namespace("", namespace)
    qname = lambda local: "{{{}}}{}".format(namespace, local)
    root = ET.Element(
        qname("gpx"), {"version": "1.1", "creator": "vpp-from-gopro"}
    )
    track = ET.SubElement(root, qname("trk"))
    ET.SubElement(track, qname("name")).text = name
    segment = ET.SubElement(track, qname("trkseg"))
    for point in points:
        node = ET.SubElement(
            segment,
            qname("trkpt"),
            {"lat": "{:.7f}".format(point.latitude), "lon": "{:.7f}".format(point.longitude)},
        )
        ET.SubElement(node, qname("ele")).text = "{:.3f}".format(point.altitude_m)
        ET.SubElement(node, qname("time")).text = (
            point.timestamp_utc.isoformat().replace("+00:00", "Z")
        )
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def extract_to_directory(mp4_path: Path, output_dir: Path) -> Dict[str, object]:
    blocks, camera_name, sample_count = extract_gps(mp4_path)
    points = expand_gps_blocks(blocks)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = mp4_path.stem
    csv_path = output_dir / (stem + "_gps.csv")
    gpx_path = output_dir / (stem + "_gps.gpx")
    summary_path = output_dir / (stem + "_summary.json")
    _write_csv(csv_path, points)
    _write_gpx(gpx_path, points, stem)
    summary = _summary(mp4_path, camera_name, sample_count, blocks, points)
    summary["outputs"] = {
        "csv": str(csv_path),
        "gpx": str(gpx_path),
        "summary_json": str(summary_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract GPS5 telemetry from a GoPro MP4 with GPMF data."
    )
    parser.add_argument("mp4", type=Path, help="GoPro MP4 source file")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data"),
        help="Directory for CSV, GPX, and summary outputs (default: ./data)",
    )
    args = parser.parse_args()
    summary = extract_to_directory(args.mp4, args.out_dir)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
