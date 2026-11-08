# GoPro GPS telemetry for 505 VPP work

This folder extracts GPS telemetry stored in GoPro MP4 files as GPMF metadata.
The source videos stay in place; only compact derived CSV, GPX, and JSON files
are written here.

## Extract telemetry

From this directory, run the script on each source video:

```powershell
python .\gopro_gps.py "G:\My Drive\gopro\2024\GX010922.MP4" --out-dir .\data
python .\gopro_gps.py "G:\My Drive\gopro\2024\GX030922.MP4" --out-dir .\data
python -m unittest -v
```

For each MP4, the script writes:

- `*_gps.csv`: one row per GPS5 position fix, including coordinates, altitude,
  camera GPS 2D/3D speed, fix status, and timing provenance.
- `*_gps.gpx`: a track derived from those fixes, with estimated timestamps.
- `*_summary.json`: counts, time span, coordinate bounds, fix status, and speed
  summaries.

Sub-sample timestamps are estimated by spacing the GPS5 fixes evenly between
successive GPSU timestamps. The raw per-block GPSU timestamp is retained in the
CSV; verify this alignment against a trusted logger before sub-second timing
is used for performance calculations. GPS speed is over ground, not through
water. This extraction does not derive wind, heading, or current.

## Implementation scope

`gopro_gps.py` reads the MP4 index and decodes the GPMF `GPS5` stream using the
standard library. It is intentionally limited to GoPro-style MP4 files with an
indexed `gpmd` telemetry track and the five-integer GPS5 record layout; it is
not a full GPMF implementation.

The GPMF structure and metadata conventions are documented by GoPro's
[GPMF-parser](https://github.com/gopro/gpmf-parser) project. Use that parser
when handling other GPMF data types or unusual container layouts.

See [`TELEMETRY_FINDINGS.md`](TELEMETRY_FINDINGS.md) for findings from the
provided 2024 GoPro files and implications for 505 polars.
