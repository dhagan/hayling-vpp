# GPX workstream summary

**Updated:** 2026-11-09

## Completed

- Assessed the supplied `C:\Users\dhaga\Downloads\505.gpx`: 4,513 fixes in one
  segment, spanning about 1 hour 47 minutes, with a longest gap of 433 seconds.
- Added `gpx_analysis.py` for track/timing/gap and ground-speed diagnostics and
  `export_track_csv.py` for exporting fixes with derived SOG/COG.
- Added `test_gpx_analysis.py`, `README.md`, `ASSESSMENT.md`, and this summary.
  The scripts use the Python standard library and leave the source GPX in place.

## Finding

The file supports descriptive track and speed-over-ground analysis, not an
accurate true-wind-speed/true-wind-angle 505 polar. It contains no wind,
heading, current, confirmed boat identity, sail plan, crew mass, or setup.
Course over ground is not heading, and speed over ground is not speed through
the water.

## Needed for a defensible empirical polar

Combine synchronized GPS with apparent-wind speed/angle, heading, current
estimates, verified 505 and configuration records, and repeated coverage
across wind/angle conditions. Keep observed race performance distinct from
model predictions and validate on independent sessions.

## Project context

The overall 505 effort uses a hybrid approach: build a transparent theoretical
model, use comparison-boat data only as labeled context, then calibrate and
validate against suitable 505 measurements. GPS-only results are not polar
targets.
