# Work record

**Updated:** 2026-11-08

## Objective

Assess whether the supplied `C:\Users\dhaga\Downloads\505.gpx` can support
accurate 505 VPP polars, and preserve a repeatable, local GPX inspection
workflow.

## Completed

- Inspected the GPX: 4,513 fixes, one segment, mostly one-second intervals,
  spanning about 1 hour 47 minutes; 11 gaps exceed ten seconds.
- Added `gpx_analysis.py` to summarize track quality and ground-speed estimates.
- Added `export_track_csv.py` to export fixes and derived SOG/COG.
- Added `test_gpx_analysis.py`, `README.md`, and `ASSESSMENT.md`.
- Ran the analyzer and CSV exporter against the supplied file; outputs are
  reproducible without copying the source GPX into this folder.

## Conclusion

This GPX supports observed speed/course-over-ground summaries, not accurate
true-wind-speed / true-wind-angle polars. It lacks wind, heading, current,
verified boat identity, and boat configuration. Accurate empirical polars
require synchronized environmental and boat-state data plus condition coverage
and independent validation.

## Next step

The sibling `vpp-from-gopro` work has extracted 14,203 GPS5 fixes from two
readable HERO10 clips. Those tracks add position and GPS speed-over-ground
observations, but still lack synchronized wind, heading, current, and verified
boat/configuration context. They therefore do not change the conclusion:
neither this GPX nor the GoPro GPS alone can support accurate true-wind polars.
