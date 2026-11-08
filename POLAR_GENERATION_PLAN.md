# Two-path plan for 505 polars

The goal is a useful, defensible 505 polar—not a precise-looking table built
from unsupported assumptions. Keep empirical observations and model
predictions separate until they have been calibrated and independently
validated.

1. **Empirical and heuristic path — `vpp-from-gpx`, `vpp-from-gopro`, and `vpp-from-470-49er`.** Extract GPS tracks and speeds; match them to synchronized local wind, boat heading, and current; filter maneuvers and poor fixes; then bin steady-state observations by true wind speed and angle. GPS without wind can only produce observed ground-track summaries, not a true-wind polar. Where 505 observations are sparse, use published 470/49er data and 505 tuning evidence only as labeled priors or bounds—not as 505 measurements. Report source, conditions, sample counts, and uncertainty.

2. **505-specific theoretical / analytical path — `vpp-theoretical`.** Build a parameterized model from the class measurement rules, actual hull drawings or measured offsets, rig and sail geometry, appendages, boat displacement, and crew righting-moment scenarios. Solve sail-force, hull/appendage resistance, heel, and leeway equilibrium over wind-speed/angle grids. Calibrate only against suitable 505 GPS-plus-wind data or controlled trials, then validate on held-out sessions. Do not publish a numerical VPP until the missing hull, force, and stability inputs are supplied or defensibly sourced.

The analytical workstream is the current priority. The comparative-boat workstream is a data inventory and cross-check, not a substitute for 505-specific physics or observations.
