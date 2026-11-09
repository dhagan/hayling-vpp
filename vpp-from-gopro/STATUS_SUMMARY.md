# GoPro telemetry workstream summary

**Updated:** 2026-11-09

## Completed

- Inspected three approximately 4 GB MP4s in `G:\My Drive\gopro\2024`.
- Confirmed two readable clips contain an indexed GPMF `gpmd` track with
  `GPS5` positions/speeds, GPS timestamps, and fix-status fields.
- Added `gopro_gps.py` to export per-fix CSV, GPX, and JSON summaries without
  copying the source videos; added `test_gopro_gps.py`,
  `TELEMETRY_FINDINGS.md`, and `README.md`.
- Extracted 7,106 GPS fixes from `GX010922.MP4` and 7,097 from
  `GX030922.MP4`; outputs are in `data\`. Parser tests passed.

## Findings and limits

`GX010922.MP4` includes 60 no-fix samples; the remaining 7,046 have fix status
3. `GX030922.MP4` has 7,097 valid fixes. The estimated UTC intervals are
2024-12-14 17:37:49–17:49:34 and 18:01:25–18:13:14, respectively. Per-fix
sub-second timestamps are estimated by spacing GPS5 samples between GPSU
timestamps and should be verified before high-precision use. The third clip,
`GX020896.MP4`, could not be read and remains unparsed.

The extracted speeds are GPS speed over ground, not water-relative boat speed.
The files do not establish true/apparent wind, heading, current, boat identity,
or configuration; they cannot alone produce a true-wind polar. The camera track
must also be matched to the specific 505 before it is treated as boat evidence.

## Project context

Use these tracks as a position/ground-speed layer only. Accurate empirical
polars still require synchronized wind and heading, current correction,
configuration records, broad condition coverage, and independent validation.
