# Equation framework for a 505 VPP

**Status:** formulation and input contract only. This is not a calibrated,
executable VPP, and it does not support publishing numerical 505 polars yet.

This document develops the force-balance outline in [`MODEL_SPEC.md`](MODEL_SPEC.md)
into explicit equations and conventions. The earlier
[`../chatgptwithequations.md`](../chatgptwithequations.md) is retained as
historical research material, not as validated data or a model result.

## 1. Coordinate and wind conventions

Use SI units internally. Let the horizontal boat axes be \(x\) forward and
\(y\) to starboard. Define \(\mathbf e_f\) as a unit vector pointing from the
boat toward the direction the wind comes **from**; this is the upwind
direction. Thus the wind velocity vector points downwind:

\[
\mathbf u_{T,g}=-W\mathbf e_f
\]

where \(W\) is true-wind speed and the subscript \(g\) denotes a ground-fixed
reference frame. Let \(\mathbf v_{B,w}\) be boat velocity through the water
and \(\mathbf u_c\) the water-current velocity over ground. Then

\[
\mathbf v_{B,g}=\mathbf v_{B,w}+\mathbf u_c,\qquad
\mathbf u_A=\mathbf u_{T,g}-\mathbf v_{B,g}.
\]

\(\mathbf u_A\) is apparent-air velocity relative to the boat. Equivalently,
with wind expressed relative to the water,
\(\mathbf u_{T,w}=\mathbf u_{T,g}-\mathbf u_c\), so
\(\mathbf u_A=\mathbf u_{T,w}-\mathbf v_{B,w}\). These forms must not be mixed
with inconsistent wind/current conventions.

True wind angle is the angle between the boat's heading and \(\mathbf e_f\);
zero is head-to-wind and 180 degrees is directly downwind. Leeway is the angle
between heading and the through-water velocity vector. A polar must state this
TWA convention and whether its speed is through-water or over-ground. The
model output should be through-water speed; current is reported separately.

## 2. Aerodynamic loads

For apparent-air speed \(V_A=\lVert\mathbf u_A\rVert\), air density
\(\rho_A\), and dynamic pressure \(q_A\):

\[
q_A=\tfrac12\rho_A V_A^2.
\]

For each modeled sail or rig element \(j\), a coefficient representation is:

\[
\mathbf F_{A,j}
=q_A A_{j,\mathrm{ref}}\left(
C_{L,j}\mathbf e_{L,j}+C_{D,j}\mathbf e_{D,j}
\right),\qquad
\mathbf F_A=\sum_j\mathbf F_{A,j}.
\]

The reference area, force directions, and coefficient convention must be
defined consistently. \(C_L\) and \(C_D\) depend on apparent-wind angle, sail
trim and shape, heel, rig state, and Reynolds number; class-rule maximum
dimensions do not provide these coefficients or an actual sail outline.
Mast, rigging, and crew windage must either be modeled as additional elements
or explicitly excluded.

For each force applied at position \(\mathbf r_j\) relative to the chosen
moment origin, its moment is

\[
\mathbf M_A=\sum_j\mathbf r_j\times\mathbf F_{A,j}.
\]

Application points and the origin must be specified before using the roll,
pitch, or yaw components.

## 3. Hydrodynamic loads

The water force on the hull and each appendage can likewise be represented as

\[
\mathbf F_{H,i}
=\tfrac12\rho_W U^2 S_{i,\mathrm{ref}}\,
\mathbf C_{H,i}(U,\beta,\phi,\tau,\delta,\ldots),
\qquad \mathbf F_H=\sum_i\mathbf F_{H,i},
\]

where \(U=\lVert\mathbf v_{B,w}\rVert\), \(\rho_W\) is water density,
\(\beta\) is leeway, \(\phi\) is heel, \(\tau\) denotes trim state, and
\(\delta\) may represent rudder angle. The coefficient vector must include
the chosen reference axes and sign convention. A useful resistance
decomposition may separate hull friction/residual resistance and appendage
drag, but terms must not be counted twice. Foil side force and its induced
drag must be represented consistently.

Useful nondimensional coordinates include

\[
\mathrm{Re}=\frac{UL}{\nu_W},\qquad
\mathrm{Fr}=\frac{U}{\sqrt{gL}},
\]

with reference length \(L\) and water kinematic viscosity \(\nu_W\). These
numbers describe operating conditions; they do not supply a resistance
curve. Hull offsets/hydrostatics and validated resistance or force data are
still required. The class measurement templates are not a substitute for the
target hull's geometry.

## 4. Equilibrium and stability

For each fixed TWS, TWA, boat configuration, and control policy, solve the
steady horizontal force balance in boat axes:

\[
\mathbf R_F=
\begin{bmatrix}
(\mathbf F_A+\mathbf F_H)\cdot\mathbf e_x\\
(\mathbf F_A+\mathbf F_H)\cdot\mathbf e_y
\end{bmatrix}
=\mathbf 0.
\]

At minimum, the coupled unknowns include boat speed through water, leeway,
and heel. Sail trim and rudder angle are control variables and require a
declared policy or an optimization with realistic bounds. If the modeled
state includes yaw or pitch, also enforce the corresponding moment balance;
for example, yaw equilibrium is
\((\mathbf M_A+\mathbf M_H)\cdot\mathbf e_z=0\). Do not imply those balances
are solved if the model omits them.

Roll equilibrium requires the aerodynamic and hydrodynamic heeling moments to
balance the restoring moment:

\[
R_M=M_{\mathrm{heel}}-M_{\mathrm{restore}}(\phi)=0.
\]

The restoring model must use a target-boat hydrostatic righting-arm curve and
a consistent mass/crew-position state. If \(GZ(\phi)\) is defined for the
complete modeled displacement \(\Delta\), its hydrostatic contribution is
\(\Delta gGZ(\phi)\). Add explicit crew moments only when they are not already
included in that curve or mass model. For upright, quasi-static crew
positions, the simplified crew-only term is

\[
M_{\mathrm{crew},0}=g\sum_i m_i y_i,
\]

where signed \(y_i\) is the transverse lever arm. This is the limited
calculation in `crew_righting_moment.py`, not total boat stability. At finite
heel, crew locations and the hydrostatic curve must be evaluated in the
heeled geometry.

Accept only roots within physical input bounds and with a restoring response
to small heel perturbations. Check moment signs with simple test cases before
interpreting stability. Multiple mathematical roots may exist; report the
selection rule rather than silently accepting the first converged root.

## 5. VMG and polar construction

For the through-water velocity vector \(\mathbf v_{B,w}\), define positive
upwind and downwind VMG as

\[
\mathrm{VMG}_{up}=\mathbf v_{B,w}\cdot\mathbf e_f,\qquad
\mathrm{VMG}_{down}=-\mathbf v_{B,w}\cdot\mathbf e_f.
\]

At each true-wind speed, first solve the force/moment equilibrium at specified
headings/TWAs. Then optimize the appropriate VMG over heading and the
declared trim/rudder controls. Do not equate maximum boat speed with maximum
VMG. Output the full speed-through-water grid, the VMG optima, the selected
control state, convergence residuals, and input provenance.

## 6. Solver workflow and checks

1. Validate units, wind/TWA convention, current reference, and the complete
   boat/configuration identifier.
2. Compute apparent wind and aerodynamic loads for a candidate state.
3. Evaluate hull and appendage loads and righting moment from documented
   target-specific functions or data.
4. Solve the coupled residual equations using bounded states and controls.
   Use continuation across adjacent wind/angle points, but also check for
   alternate roots and failed convergence.
5. Reject nonphysical or unstable states. Store residuals and failure reasons;
   never replace a failed solution with a plausible-looking speed.
6. Run sensitivity checks for uncertain measured inputs and model
   coefficients. Calibrate only on suitable 505 trials/tracks, then validate
   on separate sessions.

Before any output is called a 505 polar, implementation tests should cover
unit/vector conventions, zero-current equivalence of the two apparent-wind
expressions, force/moment residual tolerances, bound handling, and repeatable
solutions. The resulting model still needs independent performance validation.

## 7. Input gate and relation to the earlier draft

This equation set does not close the model without: target hull offsets or a
measured scan; hydrostatics/righting-arm curve; all-up mass and CG; actual
appendage and sail geometry; aerodynamic and hydrodynamic force data; and
documented crew/configuration scenarios. None should be silently replaced by
generic values.

The earlier `chatgptwithequations.md` includes a purported South African
target-speed table without a recoverable primary source, synthetic numbers
whose generation is not reproducible, claimed error bars unsupported by
validation, and placeholder/contradictory table entries. These are not inputs
to this formulation and must not be treated as measured facts or tuning
targets. The document is preserved for provenance, with a warning and link
to this corrected equation framework.

## References and scope

- International 505 Association, [Hull Measurements](https://int505.org/about-the-505/resources-for-sailors/class-rules/hull-measurements/): class conformity requirements; not a target hull lines plan.
- Dane Hull, [Speed Sailing Design and Velocity Prediction Program](https://www.foils.org/wp-content/uploads/2017/10/Speed-Sailing-Design-and-Velocity-Prediction-Program-Dane-Hull.pdf): methodological background for another boat, not a source of 505 coefficients.
- [`SOURCES.md`](SOURCES.md): full source register and limitations.

The equations are standard force, moment, and dimensional-analysis forms
applied here as a model specification. They are not evidence that the missing
505-specific coefficients or geometry are known.
