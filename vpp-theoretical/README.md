# 505 theoretical VPP

This workstream builds a 505-specific, physics-based velocity prediction
program from traceable class limits, a real hull definition, rig/sail inputs,
hydrostatics, and crew righting-moment scenarios.

## Current state

- `parameters.json` records verified class-rule dimensions and marks
  boat-specific/model inputs that are still missing.
- `MODEL_SPEC.md` defines the force-balance approach and the inputs required
  before a polar can be trusted.
- `crew_righting_moment.py` computes the **crew's upright transverse moment**
  from explicit masses and lever arms. It is not a complete boat righting-moment
  or stability model.
- No complete hull plan, measured hydrostatic curve, sail-force coefficients,
  or resistance curves have been obtained. Therefore this folder does not yet
  claim to generate accurate polar values.

## Run the crew-moment component

```powershell
python .\crew_righting_moment.py --crew helm:80:0.35 --crew crew:80:1.10
python -m unittest -v
```

Each crew entry is `name:mass_kg:lateral_lever_m`. The lever arm is measured
transversely from the boat centerline. Use measured crew positions for the
target heel/condition; the example values above are illustrative only.

See [`SOURCES.md`](SOURCES.md), [`PARAMETERS.md`](PARAMETERS.md), and
[`MODEL_SPEC.md`](MODEL_SPEC.md) for source status, assumptions, and the next
technical inputs required.
