# Assessment: can `505.gpx` produce accurate 505 polars?

## Decision

**Not by itself.** The supplied `C:\Users\dhaga\Downloads\505.gpx` is useful
for examining the boat's recorded ground track and deriving approximate
speed/course over ground. It does not contain the environmental and boat-state
measurements needed to build accurate true-wind-speed / true-wind-angle polars.

GPS can be a valuable part of a polar project, but it must be combined with
synchronized wind and heading measurements, current correction, configuration
records, and enough observations across conditions. This file alone cannot
identify the boat's optimum speed at a given wind angle and strength.

## What is in this file

The GPX contains 4,513 track fixes in one GPX track segment, spanning
2024-08-18 17:57:38Z to 19:44:19Z (6,401 seconds, or about 1 hour 47 minutes).
The median interval between consecutive fixes is one second. There are 12
intervals longer than two seconds, 11 longer than ten seconds, and the longest
gap is 433 seconds (about 7 minutes 13 seconds).

Using great-circle distances between consecutive fixes gives an approximate
sampled path length of 17.7 km. This sum includes gaps and is not a water-track
distance. The analysis script's 10-second displacement summary (endpoints
within two seconds of 10 seconds) gives a median speed over ground of about
3.7 m/s and a 90th percentile of about 7.6 m/s. These are descriptive
ground-speed estimates, not validated boat speeds; GPS noise, current,
maneuvers, and gaps affect them.

The track points contain latitude, longitude, timestamps, and elevation. The
file does not record wind speed/direction, apparent wind, heading, current,
boat identity/class, sail plan, crew weight, or setup. Its filename alone does
not prove the track is from a 505.

## Why these data are insufficient for a polar

A VPP polar needs performance indexed by true wind speed and true wind angle.
This file provides neither:

- **No wind observation:** Positions and timestamps do not determine true wind
  speed or direction. Course-over-ground cannot be converted to true wind angle
  without a wind reference and boat heading.
- **Ground speed is not water speed:** GPS measures motion over ground. Current
  changes that motion, while a boat polar normally describes speed through the
  water.
- **Course is not heading:** Leeway, current, and maneuvering can make GPS
  course differ from the bow direction needed to calculate wind angle.
- **Race tracks are selected behavior:** The boat's route reflects tactics,
  starts, traffic, sail changes, and crew decisions. It does not systematically
  measure the best speed at every angle.
- **Configuration is unknown:** Crew, sails, rig, and setup affect performance
  and are not encoded here.
- **One outing has limited coverage:** Even with wind data, one track may not
  cover the required wind-speed, angle, and setup combinations.

## What can be produced from this GPX alone

It is reasonable to generate:

- A map and time-series view of the recorded track.
- Point-to-point and smoothed speed-over-ground summaries.
- Course-over-ground, duration, sampling-gap, and track-quality diagnostics.
- A preliminary observed-performance trace for this outing, clearly labeled as
  SOG/COG and not as a true-wind polar.

It is not reasonable to label those outputs as accurate 505 polars, infer the
boat's wind-optimal angles, or use the speed summary as calibrated speed
through water.

## Additional data needed

For an empirical polar, collect or match:

1. **Synchronized GPS and onboard measurements:** timestamps, apparent wind
   speed/angle, and heading/compass. Calibrate sensor alignment and clocks.
2. **Current estimate:** enough to convert GPS motion over ground to
   water-relative boat speed and to treat wind angles consistently.
3. **Boat/configuration record:** verify the hull is a 505; log sails, rig
   setup, crew mass, and relevant changes during each session.
4. **Condition coverage:** repeat sessions spanning useful TWS/TWA ranges,
   both tacks, and steady-state sailing; flag maneuvers and poor-quality
   intervals.
5. **Independent validation:** reserve separate sessions or races to check
   performance predictions instead of fitting and validating on the same
   samples.

If onboard wind instruments are unavailable, carefully matched local wind
observations may support a rough empirical analysis, but spatial/time mismatch,
heading/leeway, and current will lower confidence. A physical VPP can provide
a separate model-based estimate, but it still requires measured boat inputs
and calibration before being called accurate.

## Method and reproducibility

The file was parsed as GPX 1.1. Distances use the haversine great-circle
formula; SOG is distance divided by timestamp interval. The 10-second summary
uses the displacement between fixes closest to a 10-second interval, accepting
an endpoint difference within two seconds. Gaps are retained in the gap
statistics and are not interpolated. The scripts do not infer missing wind,
heading, current, boat identity, or configuration.

Run the analysis and tests as described in [`README.md`](README.md). The source
GPX stays at its original path; it is not copied into this folder.
