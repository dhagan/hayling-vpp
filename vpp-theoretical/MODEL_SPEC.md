# First-principles model specification

## Intended output

For a defined 505, crew, rig, sail set, and water condition, solve for boat
speed through water, leeway, heel, and VMG over a grid of true wind speed
(TWS) and true wind angle (TWA). Produce separate modes for upwind/reaching
main+jib and downwind spinnaker. Predictions must include input provenance,
configuration, and sensitivity/uncertainty.

## Force and moment balance

At each candidate speed and attitude:

1. Compute apparent wind from the true-wind vector and boat velocity relative
   to the water.
2. Compute sail drive and side force from apparent-wind dynamic pressure and
   sail-specific lift/drag coefficients:
   `q = 0.5 * rho_air * V_app^2`, `F = q * A * C`.
3. Resolve aerodynamic forces into boat-axis drive and lateral components.
4. Compute hull and appendage resistance/side force as functions of speed,
   heel, and leeway. The model must cover displacement and planing regimes;
   this requires an actual hull geometry or measured resistance data.
5. Solve the coupled equilibrium: drive force balances resistance; lateral
   forces balance; and heeling moment does not exceed available righting
   moment. Reject unstable or nonphysical solutions.
6. Compute VMG from the solved boat velocity and wind-axis direction; find
   upwind/downwind angles that maximize VMG.

This is a solver outline, not yet a complete calibrated VPP. The available
class limits do not define full sail shapes, force coefficients, hull
resistance, hydrostatics, or a particular crew configuration.

See [`EQUATIONS_AND_SOLVER.md`](EQUATIONS_AND_SOLVER.md) for coordinate and
wind conventions, explicit force/moment equations, solver checks, and a
review of the unsupported numerical claims in the earlier draft.

## Righting moment

There is no single class-wide righting-moment constant. For an upright,
quasi-static crew contribution, the initial approximation is:

`RM_crew = g * sum(m_i * y_i)`

where `m_i` is a crew member's mass and `y_i` is the horizontal transverse
lever arm from the centerline. `crew_righting_moment.py` implements only this
term. It does not account for heel-dependent crew geometry, hull buoyancy,
the boat's center of gravity, waves, or dynamic motion.

A complete righting-moment model needs the target hull's hydrostatic
righting-arm curve and the complete mass/position state. Do not describe the
crew-only calculation as the boat's total stability or allowable sail force.

## Hull plan and hydrodynamic model

Rule 5.2.1 requires the hull to conform to designer drawings and offsets. The
public measurement PDF provides class control stations/templates but not a
complete hull lines plan for all compliant designs. Therefore:

- identify the target boat and obtain its designer/build offsets or a measured
  hull scan;
- derive hydrostatics and wetted geometry from that plan;
- use measured/towed resistance or a documented resistance method for
  displacement and planing regimes;
- parameterize foils from target measurements, not merely the class maximum
  centerboard extension.

If a complete hull plan cannot be sourced, stop short of claiming a
hull-specific analytical polar; retain an uncertainty-bounded empirical or
heuristic estimate instead.

## Calibration and release gates

- **Input gate:** current rules checked; target hull, sail geometry, crew
  scenario, displacement, and units documented.
- **Physics gate:** force/drag relationships and solver tested for physical
  consistency and convergence.
- **Calibration gate:** use only suitable 505 tracks/trials matched to wind,
  heading, current, and configuration.
- **Validation gate:** test on separate races/sessions; report errors and
  coverage by wind/angle bin.
- **Release gate:** publish model predictions separately from observed GPS
  summaries and any 470/49er transferred priors.

No numerical polar is released from this initial scaffold.
