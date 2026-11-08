# Work record

**Updated:** 2026-11-08

## Objective

Inspect the MP4 files in `G:\My Drive\gopro\2024` for embedded GoPro GPS
telemetry and record how that data may (and may not) help build 505 VPP polars.

## Current status

- Found three MP4 files, each approximately 4 GB.
- Confirmed two readable 2024 files contain a GPMF `gpmd` telemetry track with
  `GPS5` records (latitude, longitude, altitude, and GPS 2D/3D speed), plus
  GPSU timestamps and fix-status fields.
- Added `gopro_gps.py` to extract GPS telemetry and write CSV, GPX, and JSON
  summary files without copying the source videos.
- Added `test_gopro_gps.py`, `README.md`, and `TELEMETRY_FINDINGS.md`.
- The older `GX020896.MP4` reports a large file size but returned no bytes when
  read, so it has not yet been parsed.

## In progress

Validate the parser against the two readable clips, export the extracted
telemetry under this folder's `data\` directory, and record the actual counts,
time spans, and GPS summaries here.

## VPP limitation

GPS-derived speed is over ground, not through water. The videos do not provide
wind, heading, current, confirmed 505 identity, or boat configuration, so the
extracted tracks alone cannot produce accurate true-wind polars.
