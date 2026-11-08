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

## Completed extraction

- `GX010922.MP4`: 7,106 GPS5 fixes; 7,046 have GPS fix status 3, with 60 no-fix
  samples excluded from the GPX route. Estimated valid interval:
  2024-12-14 17:37:49.429–17:49:33.999 UTC.
- `GX030922.MP4`: 7,097 GPS5 fixes, all with fix status 3. Estimated interval:
  2024-12-14 18:01:24.799–18:13:14.399 UTC.
- Per-file `_gps.csv`, `_gps.gpx`, and `_summary.json` outputs are in `data\`.
- Parser tests pass. Sub-second times are reconstructed from GPSU packet
  timestamps and should be treated as estimates.

## VPP limitation

GPS-derived speed is over ground, not through water. The videos do not provide
wind, heading, current, confirmed 505 identity, or boat configuration, so the
extracted tracks alone cannot produce accurate true-wind polars.
