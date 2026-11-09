# Theoretical VPP workstream summary

**Updated:** 2026-11-09

## Completed

- Created a 505-specific parameter register (`parameters.json` and
  `PARAMETERS.md`) with rule-backed hull, rig, and sail limits and explicit
  missing/model-dependent inputs.
- Cross-checked rule text against an official-hosted 2024 Class Rules PDF.
  The class-rules index still links a 2014 PDF, so the 2024 document has not
  been confirmed as the latest consolidated edition.
- Added `MODEL_SPEC.md` and `EQUATIONS_AND_SOLVER.md` to define force/moment
  balance, wind/boat reference frames, VMG, solver checks, and release gates.
- Added `crew_righting_moment.py`, which calculates only the upright crew
  transverse moment from supplied masses and lever arms; it is not a complete
  boat stability or righting-moment model.
- Marked the unsupported numerical claims in the older
  `chatgptwithequations.md` draft as unverified. The theoretical component
  tests previously passed (3 tests); `parameters.json` parsed successfully.

## Current limitation

This is a documented model scaffold, not a functioning or calibrated
numerical VPP. The target boat's complete hull lines/offsets, hydrostatics,
all-up mass and center of gravity, actual sail shapes, force coefficients,
resistance/foil data, and validated 505 observations are still missing. The
class minimum weight is not all-up sailing displacement, and there is no
single class-wide righting-moment value.

## Next technical inputs

1. Confirm the current class-rule edition and obtain the target hull's design
   offsets or a measured scan.
2. Measure the actual boat/rig/sails and crew mass/position scenarios.
3. Establish hydrostatics and documented aerodynamic/hydrodynamic force or
   resistance models before implementing a coupled equilibrium solver.
4. Calibrate and validate with synchronized 505 wind, heading, current, and
   speed data; keep predictions separate from observations and comparison
   priors.
