# Transfer method and acceptance criteria

## Candidate data

For each 470 or 49er data source, record:

- URL, author/organization, publication date, and whether values are measured,
  modeled, or target polars.
- TWS/TWA definitions, units, averaging window, boat speed convention, and
  sail/crew configuration.
- Wind range, sea state, current treatment, sample count, and uncertainty.

Reject sources that do not identify their wind and speed conventions or cannot
be traced to a credible publisher.

## How to compare

1. Normalize units and angle conventions.
2. Compare only similar modes (upwind, reaching, downwind/spinnaker) and
   condition ranges.
3. Use dimensionless or normalized comparisons only after documenting the
   scaling assumptions; sail area, crew righting moment, displacement, hull
   resistance, and planing behavior do not scale as one simple multiplier.
4. Treat the 470 and 49er values as separate lower/upper context only where
   their verified characteristics justify that interpretation. Do not assume
   either boat bounds the 505 in every condition.
5. Keep transferred values outside the measured-505 dataset and label them as
   priors until a 505 test supports them.

## Deliverable

A source catalog and a comparison table with confidence grades. No synthetic
505 table should be generated from this workstream alone.
