import tempfile
import unittest
from pathlib import Path

from gpx_analysis import load_track, point_rows, summarize


SAMPLE_GPX = """<?xml version="1.0"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1">
  <trk><trkseg>
    <trkpt lat="0" lon="0"><ele>1</ele><time>2024-01-01T00:00:00Z</time></trkpt>
    <trkpt lat="0.0001" lon="0"><ele>2</ele><time>2024-01-01T00:00:10Z</time></trkpt>
  </trkseg><trkseg>
    <trkpt lat="0.0002" lon="0"><time>2024-01-01T00:01:40Z</time></trkpt>
    <trkpt lat="0.0003" lon="0"><time>2024-01-01T00:01:50Z</time></trkpt>
  </trkseg></trk></gpx>
"""


class GpxAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.gpx_path = Path(self.temp_dir.name) / "sample.gpx"
        self.gpx_path.write_text(SAMPLE_GPX, encoding="utf-8")
        self.points = load_track(self.gpx_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_loads_points_and_preserves_segment_boundaries(self):
        self.assertEqual(len(self.points), 4)
        self.assertEqual([point.segment for point in self.points], [0, 0, 1, 1])

    def test_motion_is_derived_only_within_segment(self):
        rows = point_rows(self.points)
        self.assertIsNone(rows[0]["sog_m_s"])
        self.assertAlmostEqual(rows[1]["sog_m_s"], 1.11, places=1)
        self.assertIsNone(rows[2]["sog_m_s"])
        self.assertAlmostEqual(rows[3]["sog_knots"], 2.16, places=1)

    def test_summary_excludes_time_between_gpx_segments(self):
        result = summarize(self.points, window_seconds=10)
        self.assertEqual(result["segments"], 2)
        self.assertEqual(result["valid_intervals"], 2)
        self.assertEqual(result["intervals_over_10s"], 0)
        self.assertEqual(result["window_sog"]["count"], 2)

    def test_rejects_gpx_without_track_segments(self):
        empty_path = Path(self.temp_dir.name) / "empty.gpx"
        empty_path.write_text(
            '<gpx xmlns="http://www.topografix.com/GPX/1/1"></gpx>',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "no track segments"):
            load_track(empty_path)


if __name__ == "__main__":
    unittest.main()
