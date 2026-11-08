import struct
import unittest
from datetime import datetime, timezone

from gopro_gps import (
    GpsBlock,
    GpmfRecord,
    _decode_gps_stream,
    _parse_gpmf_records,
    expand_gps_blocks,
)


def record(key, data_type, structure_size, repeat, payload):
    header = key.encode("ascii") + data_type.encode("ascii")
    header += bytes([structure_size]) + struct.pack(">H", repeat)
    padding = b"\x00" * ((-len(payload)) % 4)
    return header + payload + padding


class GoproGpsTests(unittest.TestCase):
    def test_decodes_gps5_scaling_and_status(self):
        gpsu = record("GPSU", "U", 16, 1, b"241214180124.799")
        gpsf = record("GPSF", "L", 4, 1, struct.pack(">I", 3))
        gpsp = record("GPSP", "S", 2, 1, struct.pack(">H", 106))
        scales = record(
            "SCAL",
            "l",
            4,
            5,
            struct.pack(">5i", 10000000, 10000000, 1000, 1000, 100),
        )
        gps5 = record(
            "GPS5",
            "l",
            20,
            1,
            struct.pack(">5i", 209224401, -1564363102, 10124, 3333, 337),
        )
        stream_payload = gpsu + gpsf + gpsp + scales + gps5
        stream = record("STRM", "\x00", 1, len(stream_payload), stream_payload)
        device = record("DEVC", "\x00", 1, len(stream), stream)

        decoded = _decode_gps_stream(_parse_gpmf_records(device)[0].children[0])

        self.assertEqual(decoded.gpsu_utc, datetime(2024, 12, 14, 18, 1, 24, 799000, tzinfo=timezone.utc))
        self.assertEqual(decoded.fix, 3)
        self.assertEqual(decoded.precision_raw, 106)
        self.assertAlmostEqual(decoded.gps_points[0][0], 20.9224401)
        self.assertAlmostEqual(decoded.gps_points[0][1], -156.4363102)
        self.assertAlmostEqual(decoded.gps_points[0][3], 3.333)
        self.assertAlmostEqual(decoded.gps_points[0][4], 3.37)

    def test_expands_sample_times_between_gpsu_blocks(self):
        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        blocks = [
            GpsBlock(start, ((1, 2, 3, 4, 5), (1, 2, 3, 4, 5)), 3, 100),
            GpsBlock(
                start.replace(second=1),
                ((1, 2, 3, 4, 5), (1, 2, 3, 4, 5)),
                3,
                100,
            ),
        ]

        points = expand_gps_blocks(blocks)

        self.assertEqual(len(points), 4)
        self.assertEqual((points[0].timestamp_utc - start).total_seconds(), 0)
        self.assertEqual((points[1].timestamp_utc - start).total_seconds(), 0.5)
        self.assertEqual((points[2].timestamp_utc - start).total_seconds(), 1)

    def test_no_fix_block_does_not_create_false_dated_points(self):
        invalid_time = datetime(2015, 10, 18, tzinfo=timezone.utc)
        valid_time = datetime(2024, 12, 14, tzinfo=timezone.utc)
        blocks = [
            GpsBlock(invalid_time, ((0, 0, 0, 0, 0),), 0, 9999),
            GpsBlock(valid_time, ((20, -156, 10, 3, 3),), 3, 106),
            GpsBlock(
                valid_time.replace(second=1),
                ((20, -156, 10, 3, 3),),
                3,
                106,
            ),
        ]

        points = expand_gps_blocks(blocks)

        self.assertIsNone(points[0].timestamp_utc)
        self.assertEqual(points[1].timestamp_utc, valid_time)
        self.assertEqual(points[2].timestamp_utc, valid_time.replace(second=1))

    def test_rejects_malformed_gpmf_record(self):
        with self.assertRaisesRegex(ValueError, "exceeds"):
            _parse_gpmf_records(b"GPS5l\x14\x00\x02" + b"\x00" * 20)


if __name__ == "__main__":
    unittest.main()
