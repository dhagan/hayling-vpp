# GoPro GPS telemetry investigation

## Finding

The two readable 2024 GoPro MP4s contain an indexed GPMF metadata track with
GPS5 position/speed records. **GPS telemetry can be extracted from these MP4s.**
The GPS track is useful for reconstructing when and where the camera/boat
moved, and for obtaining GPS-reported speed over ground. It is not, by itself,
enough to generate accurate 505 VPP polars.

## Source files and inspection

The files inspected in `G:\My Drive\gopro\2024` were:

| File | Size | Result |
|---|---:|---|
| `GX010922.MP4` | about 4.01 GB | Readable; GPMF `gpmd` track present |
| `GX030922.MP4` | about 4.00 GB | Readable; GPMF `gpmd` track present |
| `GX020896.MP4` | about 4.00 GB reported by the filesystem | Not readable during inspection: reads returned no MP4 bytes, so it could not be parsed |

Both readable clips identify the camera in GPMF as **HERO10 Black**. Their
GPS5 payloads contain repeated five-value records: latitude, longitude,
altitude, 2D speed, and 3D speed. GPS coordinates and speeds are scaled by the
SCAL record. The samples also include GPSU UTC timestamps, GPSF fix status, and
GPSP precision values.

The extractor writes the GPS fixes to CSV and GPX without copying the
multi-gigabyte source videos. The CSV preserves raw GPSU packet time and
per-fix sample index. Its per-fix timestamps are estimated by evenly spacing
the repeated GPS5 records between consecutive GPSU timestamps; this
sub-second alignment should be verified before high-precision timing use.
`GPSP` is retained as a raw value and is not assigned an undocumented unit.

## Suitability for 505 VPP polars

These tracks can provide a useful **position and ground-speed data layer**.
They do not supply:

- True or apparent wind speed and direction.
- Boat heading (GPS course over ground is not heading and does not resolve
  leeway).
- Current, needed to distinguish speed over ground from speed through water.
- Verified boat identity, sails, rig setup, or crew configuration.

Consequently, a GPS-only analysis can summarize the observed route and speed
over ground, but cannot bin performance by true wind speed and angle or identify
the optimum polar. The GoPro may be mounted on a different boat or position, so
the camera track must also be matched to the specific 505 before using it as
boat-performance evidence.

For empirical polars, combine these GPS records with synchronized masthead
apparent-wind speed/angle, heading, and current estimates; record the 505's
configuration; and collect repeated sessions across wind/angle ranges. Keep
observed race performance separate from modeled VPP predictions and validate
on sessions not used to calibrate the model.

## Reproducibility

Run the commands in [`README.md`](README.md) to create the per-video CSV, GPX,
and JSON files in `data\`. The source video paths are stored in the JSON
summaries. The unreadable `GX020896.MP4` is excluded until it is fully
available as a readable local file.

GPMF format reference: [GoPro GPMF-parser](https://github.com/gopro/gpmf-parser).
