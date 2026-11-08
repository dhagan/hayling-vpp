# VPP feasibility from GPX

This folder contains a small, dependency-free investigation toolkit for checking
what can be learned from a GPS track when considering 505 dinghy VPP polars.

## Conclusion

A GPX file containing only positions and timestamps is not enough to create an
accurate true-wind-speed / true-wind-angle polar. It supports track inspection
and approximate speed/course-over-ground summaries. It does not provide true
wind, boat heading, water-relative speed, boat identity, or sail/crew setup.

Use the scripts here to inspect and export a track; do not treat their output as
a polar or as boat speed through the water.

## Run

The scripts use only the Python standard library. From this folder, run:

```powershell
python .\gpx_analysis.py C:\Users\dhaga\Downloads\505.gpx
python .\export_track_csv.py C:\Users\dhaga\Downloads\505.gpx .\505-track.csv
python -m unittest -v
```

`gpx_analysis.py` prints JSON with track counts, timing, gaps, sampled path
distance, and point-to-point / 10-second-window speed-over-ground summaries.
The 10-second window accepts endpoints within two seconds of the requested
interval. `export_track_csv.py` writes one row per track fix; derived speed and
course are over ground (SOG/COG), not through water.

## Files

- `ASSESSMENT.md` records the findings for the supplied `505.gpx` and the
  feasibility decision.
- `gpx_analysis.py` parses GPX track segments and computes track diagnostics.
- `export_track_csv.py` exports the fixes and derived SOG/COG values.
- `test_gpx_analysis.py` covers parsing, segment boundaries, calculations, and
  malformed/empty input behavior.

The scripts read the GPX from the path supplied on the command line; they do
not copy the input file into this folder.
