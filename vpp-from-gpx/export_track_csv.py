"""Export track fixes and derived speed/course over ground to CSV."""

import argparse
import csv
from pathlib import Path

from gpx_analysis import load_track, point_rows


FIELDS = [
    "timestamp_utc",
    "latitude",
    "longitude",
    "elevation_m",
    "segment",
    "interval_s",
    "distance_from_previous_m",
    "sog_m_s",
    "sog_knots",
    "cog_deg",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export GPX fixes; derived speed/course are over ground."
    )
    parser.add_argument("gpx", type=Path, help="Input GPX file")
    parser.add_argument("csv", type=Path, help="Output CSV file")
    args = parser.parse_args()

    rows = point_rows(load_track(args.gpx))
    with args.csv.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote {} fixes to {}".format(len(rows), args.csv))


if __name__ == "__main__":
    main()
