# International 505 Dinghy — VPP, Polar and Tracking Research

**Compiled:** 8 November 2026  
**Purpose:** Consolidated record of the 505 VPP/polar research discussion, research instructions preserved in the available conversation context, and the final research findings available from the completed Deep Research run.

> **Completeness note:** This is a comprehensive reconstruction from the conversation material available to the assistant, not a platform-level verbatim export. It preserves the substantive requests, constraints, additions, findings, and caveats available in context. Some original intermediate messages, exact tool payloads, and the full original Deep Research report text were not available for verbatim reproduction. Those gaps are identified rather than invented.

---

## 1. Conversation history and user requests

### 1.1 Initial objective: actual 505 polars

The user wanted actual International 505 polar data comparable to the polar tables available for classes such as the 49er and 470. The request emphasized usable sources and links that work, not broken or speculative references.

The user supplied a possible lead:

**“VPPs - SAPSailing - International 505 Polar Target Table (Knots)”**

The table was described as having wind-speed bands of 6, 10, 14, 18, and 22+ knots, with target values for:
- Upwind: optimal true wind angle (TWA), boat speed (BSP), and VMG
- Beam reach
- Broad reach
- Downwind: optimal TWA, BSP, and VMG

The important research question was whether this exact SAPSailing table existed and could be verified. It was not to be treated as official, measured, or authoritative merely because it was presented as a target table.

### 1.2 Expanded objective: best data-based VPP available online

The user expanded the task to:

> “best data-based VPP for 505 based what's out there on the web”

The requested research was to:
- Search official class/rules sources and reliable technical references.
- Establish the 505's geometry, sail area/configuration, crew/trapeze arrangement, hull characteristics, and planing behaviour.
- Look for actual 505 VPPs, polar tables, and measured performance data.
- Compare with relevant 49er, 470, and other trapeze-dinghy polars only where useful, with assumptions and scaling made explicit.
- Develop a defensible synthetic VPP if direct 505 data were unavailable.
- Explain equations, assumptions, and parameter choices.
- Produce a wind-speed / TWA grid, upwind and downwind VMG-optimal angles, reaching speeds, and interpolation guidance.
- Separate sourced facts, inferred parameters, and synthetic outputs.
- Include confidence/uncertainty estimates and clear caveats.
- Prefer official sources and verify URLs.
- If possible, produce CSV/spreadsheet polar data and charts.
- Explain how to validate and calibrate the model using GPS tracks, TWS/TWA, boat speed, crew weight, sea state, and sail configuration.

### 1.3 Added requirement: use tracking data from major events

The user explicitly added:

> “use tracking data from major events as well”

The research scope was therefore expanded to investigate GPS/live-tracking data from major 505 events, including (where available):
- 505 World Championships
- European Championships
- North American Championships
- Australian Nationals
- Other major 505 regattas

Platforms and sources to investigate included Sailmon, TracTrac, MetaSail, SAP Sailing, RegattaNetwork, and event-specific tracking pages.

The requested approach was:
- Find raw GPS or replay data where available.
- Extract or estimate speed and VMG only when tracking and wind context support it.
- Account for boat-to-boat differences, current, sea state, manoeuvres, fleet traffic, and data gaps.
- Distinguish GPS speed over ground (SOG) from through-water boat speed (BSP).
- If raw data are not publicly downloadable, document the access limitations and provide a reproducible extraction/calibration method.
- Verify links rather than inventing them.

### 1.4 Request to export the conversation as Markdown

The user asked:

> “can you dump the history ad responses from this chat into an *.md”

A Markdown transcript was drafted in the conversation, titled **“International 505 Dinghy – VPP & Polar Research”**. It included the main requests and a summary of the research instructions, and noted that skipped/unavailable messages could not be reproduced.

The user then asked whether it contained everything, including prompts. The answer clarified that the first draft was not guaranteed to be a complete verbatim export and might omit:
- Exact original wording of Deep Research prompts
- Intermediate assistant responses and tool calls
- Full instructions from updates/restarts
- Messages not available in the conversation context

The user accepted an offer to revise it into a more comprehensive record. An attempt was made to start a Deep Research task for that revision, but it did not produce the Markdown file. The user was later told that the task had not completed and that the better route was to author the Markdown record directly.

### 1.5 User asked whether research was still running

The user asked:
- “are you still working”
- “still working?”

The subsequent research status showed the 505 VPP research run as **completed**, not still running. The user later said they could not see the Deep Research panel. The response clarified that the report was available in the conversation context and that the panel need not be visible to access the results.

---

## 2. Deep Research run — status and scope

The final status available from the research run was **completed**.

The status details showed:

| Workstream | Status shown | Available result |
|---|---|---|
| Published 505 polar/VPP sources, including SAPSailing | Completed | Sources investigated; no official 505 polar/VPP located |
| GPS tracking from major events | In progress at last step update | Live tracking was found, but no publicly downloadable raw 505 GPS dataset was obtained |
| Physics-based synthetic VPP | In progress at last step update | First-pass model design and approximate synthetic values |
| Polar tables, CSVs, plots, confidence bands | In progress at last step update | Preliminary grid/table drafted; final CSV and polished plots not completed |
| Sources, assumptions, reproducible calibration | Pending at last step update | Not completed as a full reproducible package |

Although the overall research run was marked **completed**, several substeps were unfinished. The status must not be read as meaning that every requested deliverable was produced.

---

## 3. Research findings available from the completed run

### 3.1 No official 505 polar/VPP found

The central finding was:

**No official International 505 polar table or validated 505 VPP was found in the sources investigated.**

The SAPSailing lead did not establish the existence of a published, official, complete 505 target-polar table matching the wind-speed/TWA/BSP/VMG grid described by the user.

### 3.2 Class and boat specifications

The report referenced the 505 class overview on Wikipedia for basic specifications, including:
- Length overall: approximately 5.05 m
- Beam: approximately 1.88 m
- Minimum hull weight: approximately 127.4 kg
- Upwind sail area: approximately 17.3 m²

**Important specification caveat:** The report's sail-area figures were not sufficiently reconciled. It also cited a downwind/spinnaker area of 44.3 m², which appears questionable as a standalone spinnaker figure and may reflect a combined or differently defined area. Do not use that number as a verified sail measurement without checking the current class measurement rules and authoritative class documentation.

The final report's class-spec reference:
- https://en.wikipedia.org/wiki/505_(dinghy)

This is a secondary reference, not a substitute for the class rules or official measurement documentation.

### 3.3 Qualitative 505 performance information

The USA 505 class material titled “Getting Around the Racecourse” was cited as discussing the value of polar diagrams and the way optimal downwind angles vary with wind and waves. It is qualitative guidance, not a numeric polar data set.

Source:
- https://usa505.org/library/improve-your-505-sailing/getting-around-the-racecourse/

### 3.4 North Sails tuning information

The North Sails 505 tuning guide was identified as a useful rig-tuning reference. It provides tuning guidance but does not supply a validated numeric 505 polar table.

Source:
- https://www.northsails.com/en-us/blogs/north-sails-blog/505-tuning-guide

### 3.5 SAP Sailing / 2018 505 Worlds

The report identified a SAP Sailing page for the 2018 505 Worlds. It indicated 10 races and reported a maximum speed of 20.9 knots for boat POL 8812.

Source:
- https://505worlds2018.sapsailing.com/

**Interpretation:** A single maximum-speed value is an anecdotal performance observation. It is not a polar, does not identify the wind angle or duration, and does not establish repeatable speed at a given TWS/TWA.

### 3.6 2026 505 Worlds tracking

The report identified an event page indicating TracTrac live tracking for the 2026 505 World Championship races.

Source:
- https://int505.org/2026-505-world-championships-hayling/race-tracking/

However, the research did not obtain a public raw downloadable GPS dataset from that tracking source. Live replay availability does not automatically mean the underlying tracks can be exported or used for quantitative VPP calibration.

### 3.7 VPP methodology reference

A paper discussing VPP methods for the Moth class was cited. It describes a method using TracTrac-derived boat speed/TWA data and weather observations as inputs.

Source:
- https://www.foils.org/wp-content/uploads/2017/10/Speed-Sailing-Design-and-Velocity-Prediction-Program-Dane-Hull.pdf

This is a methodological reference, not a 505-specific VPP. It supports the general idea of combining race tracking and wind observations, but the boat-specific model and calibration would still need to be developed for the 505.

### 3.8 General polar-diagram reference

Source:
- https://en.wikipedia.org/wiki/Polar_diagram_(sailing)

This is general background on sailing polar diagrams, not 505 performance data.

---

## 4. Preliminary synthetic polar values reported

The completed research report included the following first-pass synthetic speed grid. These values are reproduced because they appeared in the report, **not because they were empirically validated**.

**Units:** knots  
**Rows:** true wind speed (TWS)  
**Columns:** true wind angle (TWA)

| TWS \ TWA | 30° | 60° | 90° | 120° | 150° | 180° |
|---:|---:|---:|---:|---:|---:|---:|
| 6 kt | 3.5 | 4.5 | 5.2 | 5.0 | 4.2 | 3.8 |
| 10 kt | 4.5 | 6.2 | 7.8 | 8.2 | 6.5 | 5.5 |
| 14 kt | 5.3 | 8.4 | 10.5 | 11.8 | 9.0 | 7.5 |
| 18 kt | 5.9 | 10.4 | 13.0 | 14.5 | 11.5 | 9.0 |
| 22 kt | 6.5 | 11.6 | 14.5 | 15.5 | 13.0 | 10.0 |

### 4.1 Critical limitations of this table

These are **synthetic, preliminary estimates**, not:
- Measured 505 speeds
- A published SAP Sailing target table
- A class-approved VPP
- A validated performance target
- A statistically calibrated prediction interval

The report mentioned uncertainty of approximately ±10–15%, but this was not demonstrated as a statistically estimated confidence interval. Treat it as an informal uncertainty indication only, not a measured confidence band.

The table is sparse and should not be interpolated into a detailed polar without a defensible model. It also does not capture:
- Waves and sea state
- Current and leeway
- Crew weight, skill, and righting moment
- Rig and sail setup
- Spinnaker trim and gybe manoeuvres
- Planing transition and dynamic stability
- Differences between GPS SOG and through-water BSP

### 4.2 Other optimum-angle claims in the report

The report also stated:
- Upwind optimum around 36–38°
- An upwind speed of approximately 7.1 kt at 22 kt TWS
- Broad-reach maximum around 120°
- Lower speed at dead downwind (180°) than on a broad reach

These values were not transparently derived from the sparse grid above. In particular, the stated upwind speed at 36–38° cannot be independently reproduced from the table as shown. They should be treated as unverified model claims, not established 505 targets.

---

## 5. Preliminary modelling approach described

The report described a first-pass physics-based model built around a balance of:
- Aerodynamic force from the sails
- Hydrodynamic resistance, including frictional and planing-related drag
- Crew righting moment
- Boat equilibrium at a given TWS and TWA

It mentioned an assumed crew weight of approximately 160 kg and flat-water conditions.

This is a conceptual model outline, not a complete reproducible VPP specification. The available report did not provide a sufficiently complete, validated set of equations, coefficients, sail-force polars, hull resistance curves, righting-moment curves, or solver details to reproduce its output faithfully.

**Do not treat the reported grid as a rigorous VPP until the model is rebuilt with explicit equations, traceable parameters, and calibration data.**

---

## 6. Tracking-data findings and limitations

The major-event tracking investigation found that live tracking/replay exists for at least some major 505 events, including the 2026 Worlds. However, the run did not yield public raw downloadable GPS tracks suitable for direct analysis.

A useful future workflow would be:

1. Identify specific events and races with replay coverage.
2. Determine whether the tracking provider or event organizer can supply raw tracks or an export.
3. Preserve timestamp, boat identifier, latitude/longitude, and any recorded speed/heading fields.
4. Obtain wind observations with matching timestamps and location.
5. Convert GPS SOG to an estimate of through-water speed only when current data or a defensible current correction is available.
6. Estimate TWA from true wind direction and boat course/heading, correcting for current and leeway as possible.
7. Filter manoeuvres, starts, mark roundings, traffic effects, and low-quality GPS segments.
8. Bin clean steady-state observations by TWS and TWA.
9. Compare multiple boats and races, rather than treating one fast boat or one maximum-speed point as representative.
10. Report sample counts, dispersion, and conditions for every polar bin.

### Why the distinction between SOG and BSP matters

GPS generally measures speed over ground. A polar normally describes boat speed through the water. Current can make these materially different. A track-derived polar that does not account for current may misstate boat performance, particularly when comparing different legs, locations, or days.

---

## 7. What was not delivered by the research run

Despite the original request, the completed run did **not** provide:
- A verified official 505 polar table
- A validated 505 VPP
- A public raw GPS dataset from a major 505 event
- A finished downloadable CSV or spreadsheet
- Finished polar charts
- A statistically defensible confidence band
- A fully reproducible model implementation and calibration package

The report contained a preliminary synthetic grid and source leads, but the CSV and polished plots described as potential deliverables were not attached.

---

## 8. Recommended next technical steps

To turn the preliminary work into something useful for actual 505 performance analysis:

### 8.1 Verify class inputs first
Use the current International 505 class rules and measurement documentation to establish:
- Hull dimensions and measurement constraints
- Minimum hull weight and relevant appendage specifications
- Mainsail and jib measurement areas
- Spinnaker measurement area and definitions
- Mast, rig, and trapeze constraints

Resolve the sail-area discrepancy before modelling.

### 8.2 Build the model from explicit components
At minimum, document:
- Sail lift/drag or drive/side-force coefficients by apparent wind angle
- Apparent wind calculation
- Hull resistance versus speed, including displacement-to-planing transition
- Appendage drag and leeway
- Crew righting moment versus heel and crew position
- Equilibrium solution method
- Separate upwind, reaching, and spinnaker configurations

### 8.3 Calibrate from event tracks
Prioritize races where tracking, wind records, and course geometry overlap. Seek raw exports from event organizers or tracking providers if replay pages do not expose downloadable data.

### 8.4 Produce reproducible outputs
A useful deliverable should include:
- Source/parameter register
- Model equations and code
- CSV polar grid
- Separate measured and synthetic data
- Polar plots for each wind speed
- VMG-optimal upwind and downwind angles
- Sample counts and uncertainty by bin
- Conditions and limitations

### 8.5 Validate against independent data
Do not calibrate and validate on the same race segments. Use some events for fitting and separate races/events for validation. Compare predicted speeds and VMG against steady-state observed segments, and publish residuals and sample counts.

---

## 9. Source list preserved from the research report

1. 505 class overview — Wikipedia  
   https://en.wikipedia.org/wiki/505_(dinghy)

2. USA 505 — “Getting Around the Racecourse”  
   https://usa505.org/library/improve-your-505-sailing/getting-around-the-racecourse/

3. North Sails — 505 Tuning Guide  
   https://www.northsails.com/en-us/blogs/north-sails-blog/505-tuning-guide

4. SAP Sailing — 2018 505 World Championship  
   https://505worlds2018.sapsailing.com/

5. International 505 — 2026 World Championship race tracking  
   https://int505.org/2026-505-world-championships-hayling/race-tracking/

6. Dane Hull — VPP / speed-sailing methodology paper (Moth-focused)  
   https://www.foils.org/wp-content/uploads/2017/10/Speed-Sailing-Design-and-Velocity-Prediction-Program-Dane-Hull.pdf

7. Polar diagram (sailing) — Wikipedia  
   https://en.wikipedia.org/wiki/Polar_diagram_(sailing)

---

## 10. Bottom line

The research established a useful starting point, but not a finished 505 VPP.

- No official or validated 505 polar table was found.
- The SAP Sailing 2018 Worlds page provides a maximum-speed anecdote, not a polar.
- Major-event live tracking exists, but the run did not obtain public raw GPS tracks.
- A preliminary synthetic speed grid was reported, but its assumptions and optimum-angle claims were not sufficiently documented or calibrated.
- No finished CSV, spreadsheet, plots, or reproducible model were attached.

**The preliminary numbers should not be used as authoritative tuning targets.** The strongest path forward is to verify the class-rule inputs, obtain event tracking exports and matching wind data, and build a reproducible model that clearly separates observed performance from synthetic predictions.

## 11. Current two-path plan and workstream status (2026-11-08)

The current execution plan is recorded in [`POLAR_GENERATION_PLAN.md`](POLAR_GENERATION_PLAN.md):

1. **Empirical evidence:** analyze the GPX and GoPro tracks, then seek synchronized wind, heading, and current. Use 470/49er data only as traceable priors or bounds—not as 505 measurements.
2. **505-specific theoretical VPP:** assemble class-rule and boat-specific inputs, solve force balance, then calibrate and validate against independent 505 observations.

Work is organized in [`vpp-from-gpx`](vpp-from-gpx/), [`vpp-from-gopro`](vpp-from-gopro/), [`vpp-from-470-49er`](vpp-from-470-49er/), and [`vpp-theoretical`](vpp-theoretical/), each with its own work record. The theoretical directory now contains a sourced rule-parameter scaffold, model specification, and a crew-only righting-moment calculator; it does **not** yet contain a numerical VPP. The public [Hull Measurements rules page](https://int505.org/about-the-505/resources-for-sailors/class-rules/hull-measurements/) confirms that a compliant hull must match designer drawings and offsets, but its class measurement controls are not a complete target-boat lines plan. Actual hull geometry, hydrostatics, all-up mass/CG, sail outlines, and force coefficients remain prerequisites.

The existing GPX and GoPro speeds are ground-relative observations, not true-wind 505 polars. Keep them separate from any future model output, and do not use the report's preliminary synthetic grid as a tuning target.

---

## Appendix A — Original request wording preserved where available

The following short user phrases are preserved exactly as they appear in the available conversation summary:

- “use tracking data from major events as well”
- “can you dump the history ad responses from this chat into an *.md”
- “yes, revise it”
- “are you still working”
- “still working?”
- “I don't see the deep research panel”
- “create a complete downloadable md”

The initial exact wording of the original polar/VPP request and the complete Deep Research prompt payloads were not available verbatim in the context used to create this file. Their substantive requirements are reconstructed in Sections 1.1–1.3 and are explicitly labelled as such.

## Appendix B — Record integrity

This file combines:
1. User requests and phrases visible in the available conversation record.
2. Assistant summaries of the research scope and run status.
3. Findings and numerical values surfaced in the completed research report summary.
4. Editorial organization and explicit caveats added to prevent preliminary or weakly supported values from being mistaken for measured facts.

It is not a verbatim export of every platform message, tool call, hidden prompt, or Deep Research internal step.
