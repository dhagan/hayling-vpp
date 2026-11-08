# 505 Dinghy VPP Polars: Options and Work Plan

## Executive recommendation

Build a **hybrid polar**: start with a transparent sailing-performance model, use comparable-boat data only as a prior, then calibrate and validate it with 505 measurements and GPS tracks that have trustworthy wind observations. Keep the model's predicted optimum separate from the speeds actually observed in races.

GPS race data is useful, but **GPS alone is not enough to recover a defensible true-wind-speed/true-wind-angle polar**. It records motion over ground, not wind, current, heading, sail trim, or whether the crew was at the boat's speed optimum. GPS-only analysis can yield observed speed-versus-course summaries and useful quality checks; it cannot reliably identify the boat's performance envelope without environmental data and additional assumptions.

## What the product should contain

Define the first deliverable as a family of tables or files indexed by true wind speed (TWS) and true wind angle (TWA), reporting:

- Predicted boat speed through the water, with a confidence or quality indicator.
- Upwind and downwind VMG, plus the angles that maximize each.
- The assumptions and configuration for each result: boat/rig, sail plan, crew weight, and water state.
- Separate observed-data summaries from model predictions.

Treat a polar as conditional on configuration and conditions, not as one timeless curve. Record units and angle convention explicitly (for example, TWA in degrees from the bow, 0–180°).

## Options

| Option | Inputs and method | What it can deliver | Main limitations | Effort / confidence |
|---|---|---|---|---|
| **1. GPS-only race summaries** | Parse TracTrac tracks; segment upwind/downwind legs and summarize speed over ground by course/leg. | A first look at observed race performance, track quality, and relative consistency. | No wind reference; speed over ground includes current; course over ground is not heading; tactical choices and maneuvers bias the sample. Not a true VPP polar. | Low effort / low confidence as a polar |
| **2. GPS plus race-area wind** | Join tracks to time- and location-matched shore/station wind, ideally with direction and gust information; estimate current and filter maneuvers. | Coarse empirical speed versus estimated TWS/TWA; useful for calibration if coverage is good. | A distant or land-affected sensor may not represent wind at the boat. Current and heading/leeway remain important errors. | Low–medium / low–medium |
| **3. GPS plus onboard instruments** | Combine GPS with masthead apparent wind, compass/heading, and preferably an IMU; use current estimates to convert ground motion to water-relative motion and apparent to true wind. | Strongest empirical polar route; can reveal performance by sail, tack, and crew configuration. | Instrument offsets, calibration, leeway, sea state, and uneven condition coverage still matter. | Medium / medium–high with good data |
| **4. Controlled 505 trials** | Sail repeatable upwind/downwind legs across wind ranges with GPS, calibrated apparent wind/heading instruments, and recorded configuration. | Cleaner measurements and deliberate coverage of angles missing from race tracks. | Requires organized sailing sessions; wind/current can change during a run and perfect steady-state tests are difficult. | Medium / high for measured conditions |
| **5. Analytical / semi-empirical VPP** | Assemble hull, appendage, rig, sail, displacement, and crew data; calculate aerodynamic driving force and hydrodynamic resistance, then solve for equilibrium speed and heel/leeway. | A predicted performance envelope and explicit what-if comparisons. | Requires accurate 505 geometry, sail/rig inputs, and force models; tuning without measurements can produce precise-looking but wrong answers. | High / medium until calibrated |
| **6. Hybrid model (recommended)** | Build a modest physical model, use similar-boat information only as an initial prior, calibrate against instrumented 505 data, and reserve independent races/trials for validation. | Both an interpretable optimum and a reality-checked performance range; uncertainty can be made explicit. | More setup than a data-only chart; quality depends on measurement coverage and model discipline. | Medium–high / best balance |
| **7. Transfer from another dinghy or published polar** | Adapt a known polar from a similar boat, adjusting for displacement, sail area, hull/rig differences, and crew. | A quick provisional baseline for planning or testing the pipeline. | Small design differences and source uncertainty can dominate; not a 505 VPP unless the source is genuinely comparable. | Low / low–medium; label provisional |
| **8. CFD or detailed fluid simulation** | Simulate hull/appendage flow and possibly sails, then combine forces in a sailing equilibrium solver. | Detailed design investigation under well-specified conditions. | Very high geometry, meshing, solver, and validation cost; free-surface, waves, sails, and crew make the full problem difficult. | Very high / not a first step |
| **9. Existing rating or commercial VPP tools** | Investigate whether a tool exposes a relevant 505 model, inputs, and usable outputs. | Potentially a rapid independent benchmark or hull/rig calculation. | Access, licensing, model assumptions, and class-specific coverage may prevent use; a rating output is not automatically a boat polar. | Unknown until feasibility check |

### GPS race-data feasibility

The existing `inspect_tractrac.py` is a useful starting point for checking what the selected TracTrac event exposes. It currently observes the page, selected race-data responses, and websocket URLs; it does not yet establish a reusable track-data export or a complete schema.

Before investing in a parser, verify for a small sample:

1. Whether the event provides actual timestamped positions for the target 505, not only leaderboard/race metadata.
2. Sampling interval, missing-data behavior, timestamp/time-zone convention, coordinate reference, boat identifier stability, and whether positions are raw or smoothed.
3. Whether track history can be retrieved consistently and lawfully under the event/service terms. Do not rely on reverse-engineered endpoints until their stability and permitted use are clear.
4. Whether the same timestamps can be matched to trustworthy wind measurements and, ideally, current estimates.

If only position, timestamp, and boat ID are available, the useful output is an **observed-track analysis**, not a full polar. The key measurement distinctions are:

- GPS gives speed/course over ground. A polar normally describes speed through the water; current must be accounted for.
- Course over ground is not heading. Leeway and maneuvering make the difference material, especially upwind.
- True wind cannot be obtained from GPS alone. It requires a wind observation or apparent-wind and heading/boat-velocity measurements.
- Race tracks sample tactical choices, not every angle at the best speed. Tacks, starts, traffic, waves, and sail changes need to be identified or excluded from steady-state estimates.

## Work plan

### Phase 0 — Define the target and success criteria

- Choose the target use: tactical reference for one boat, class-level reference, or design-comparison VPP. These are different products.
- Fix conventions and outputs: units, TWA sign/range, TWS bins, speed through water versus ground, and whether each cell represents a mean, median, high percentile, or modeled optimum.
- Select an initial scope: one representative 505 configuration and a practical wind range, expanding only when data supports it.
- **Gate:** no analysis is called a validated polar unless its wind and water-relative speed inputs are sufficiently supported.

### Phase 1 — Data and feasibility audit

**Track-data workstream**
- Use the current inspection script to document what the chosen event actually returns.
- Obtain a small sample through an approved, repeatable export path if available; preserve the original data and document provenance.
- Check frequency, gaps, duplicate/out-of-order times, coordinate quality, boat identity, and event conditions.
- Build a minimal parser and produce a map/time-series plot before scaling to more races.

**Environmental-data workstream**
- Inventory available onboard wind/heading logs, race-committee or nearby station records, weather observations, and current information.
- Match clocks and locations; quantify time/location offset and wind representativeness.
- Treat gridded hindcasts (for example, ERA5) as coarse context or a fallback, not as precise dinghy-scale race-course wind.

**Boat-definition workstream**
- Collect 505 hull/appendage geometry, displacement, rig dimensions, sail measurements, sail inventory, crew mass, and relevant setup.
- Record the source, units, and uncertainty for every input; distinguish class limits from the actual test boat.

**Gate:** choose the empirical route if wind and tracks align well; otherwise proceed with a provisional physical baseline and plan instrumented trials.

### Phase 2 — Build a trustworthy observed-performance dataset

- Normalize timestamps, coordinates, units, and identifiers; retain raw data separately.
- Derive smoothed position, speed/course over ground, and acceleration with a documented method.
- Segment legs and flag starts, maneuvers, tacks/gybes, stops, traffic, and obvious GPS artifacts. Do not silently interpret these as steady-state sailing.
- Join wind and current observations with explicit match tolerances and quality flags.
- Where heading is available, estimate TWA consistently; where it is not, mark angle as course-based and lower its quality.
- Produce coverage plots by TWS/TWA and boat/configuration. Identify empty or sparse bins instead of filling them with unjustified precision.
- Compare multiple races and both tacks to expose calibration bias, current, and asymmetry.

### Phase 3 — Create the first polar candidate

Run two candidates in parallel where inputs allow:

1. **Empirical candidate:** aggregate quality-filtered, water-relative speed by wind/angle bins; report sample counts, spread, and observed percentiles. Keep it explicitly labeled “observed.”
2. **Model candidate:** implement the simplest transparent equilibrium model supported by the available 505 inputs. Start with established aerodynamic and resistance relationships; expose assumptions and avoid adding CFD-level complexity prematurely.

If a comparable dinghy polar or rating-tool output is found, use it only as a labeled reasonableness check or prior, never as ground truth. If usable wind data is absent, limit the empirical candidate to GPS-only summaries and prioritize a measurement session.

### Phase 4 — Calibration and validation

- Calibrate model parameters on a defined subset of races/trials; do not tune against every available sample.
- Hold out at least one separate session or race for validation. Split by session/event, not random individual GPS points, to avoid leakage from the same conditions.
- Compare predicted and observed speeds only for matched conditions/configurations, report errors by wind/angle bin, and show sample counts and uncertainty.
- Investigate systematic residuals (for example, wind calibration, current, sail configuration, sea state, or model resistance) before changing coefficients.
- Run controlled trials to fill sparse bins and to test the predicted optimum angles.
- **Gate:** publish a validated range only for conditions with independent supporting data; label extrapolated bins and configurations clearly.

### Phase 5 — Deliver and maintain

- Export a human-readable polar table/plot and machine-readable CSV/JSON with metadata and version.
- Include data provenance, assumptions, calibration/validation split, uncertainty, and known limitations.
- Keep separate layers for (a) observed race performance, (b) calibrated model prediction, and (c) any provisional transferred baseline.
- Version the input data and model so new sessions can be added without obscuring prior results.

## Suggested parallel workstreams

These can start independently after the target product is agreed:

1. **TracTrac/data feasibility:** inspect one event, confirm track availability/schema/terms, and report sampling and identity quality.
2. **505 inputs and model survey:** assemble the test boat's geometry/rig/sail/crew inputs and identify candidate VPP or comparable-boat references.
3. **Wind/current plan:** find available race-area/onboard environmental data and assess what is sufficiently local and synchronized.
4. **Processing and validation design:** specify track cleaning, leg segmentation, quality flags, bins, and an event-level holdout strategy.

Then combine findings at the Phase 1 gate. Avoid building a large ingestion pipeline or calibrating a model before confirming the data can answer the intended question.

## Initial decision

Start with a **small feasibility spike** on one TracTrac race plus one representative 505 data inventory. If track timestamps and trustworthy wind/heading data can be matched, proceed to empirical analysis and hybrid calibration. If not, create only a GPS observed-performance summary, arrange controlled instrumented trials, and treat any standalone model or transferred polar as provisional until validated.

## Reference starting points

- The existing project probe: [`inspect_tractrac.py`](inspect_tractrac.py).
- TracTrac event viewer/data path referenced by that probe: [live.tractrac.com](https://live.tractrac.com/).
- ECMWF ERA5 reanalysis overview (useful for broad environmental context, not fine-scale dinghy wind): [ECMWF ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5).
- NOAA National Data Buoy Center (potential nearby observations; station proximity and exposure must be checked): [NDBC](https://www.ndbc.noaa.gov/).

