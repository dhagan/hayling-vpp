# Work record

**Updated:** 2026-11-08

## Objective

Start a 505-specific theoretical VPP from class specifications, sail/rig limits,
crew righting moment, and a target hull definition.

## Completed in this first pass

- Recorded official-hosted rule dimensions and limits in `parameters.json` and
  `PARAMETERS.md`.
- Linked the official measurement rules and rule pages in `SOURCES.md`.
- Documented that the available public rules require designer hull drawings
  and offsets but do not supply a complete hull plan for the target boat.
- Documented that 127.4 kg is a dry minimum hull sailing weight, not all-up
  displacement, and that no single class righting-moment value exists.
- Added a small parameterized crew-only moment calculator; it makes no
  unsupported crew-weight or trapeze-position assumptions.
- Defined the analytical force-balance model and release gates in
  `MODEL_SPEC.md`.
- Added `EQUATIONS_AND_SOLVER.md` with explicit reference frames,
  apparent-wind treatment, aerodynamic and hydrodynamic load forms,
  force/moment balance, righting-moment conventions, VMG definitions, and
  solver checks.
- Reviewed `chatgptwithequations.md`: its unverified target-speed table,
  synthetic polar, stated uncertainty, and claimed validation are not
  reproducible. Added a warning and linked it to the equation framework rather
  than carrying its numbers into the theoretical model.

## Follow-up: rule-backed rig and sail constraints

- Located an official-domain 2024 Class Rules PDF (PDF metadata creation date
  2024-09-08) and cross-checked textual rule limits in the parameter register
  against its clauses. Hull-template values remain separately attributed to
  the hosted measurement form.
- Recorded that the Association's class-rules index still links a 2014 PDF;
  no later amendment or confirmation of the latest consolidated edition was
  found. The register therefore remains subject to class/measurement-officer
  confirmation.
- Expanded `parameters.json` and `PARAMETERS.md` with rule-based sail widths,
  mast/boom limits, halyard/hoist ranges, and spinnaker-pole length. These are
  constraints only; they do not supply the target sails' actual shapes, areas,
  mast bend, or aerodynamic coefficients.

## Current limitation

This is an input/model scaffold, not a numerical VPP. The target hull lines,
hydrostatics, actual sail outlines, all-up mass/CG, crew positions, and
aerodynamic/hydrodynamic coefficients remain unprovided. The hosted
measurement form is not a full target-hull lines plan; current class amendments
also need confirmation.

## Next steps

1. Verify the current 505 class-rule edition and obtain the target boat's hull
   design/offsets or measured scan.
2. Measure target boat mass, rig/sail outlines, and crew mass/position ranges.
3. Derive or obtain hydrostatics and resistance/foil-force data, then implement
   and test the coupled equilibrium solver.
4. Calibrate and validate against 505 data with matching wind/heading/current;
   keep observed and modeled polars separate.
