# Work record

**Updated:** 2026-11-08

## Objective

Determine whether published or measured Flying Dutchman (FD), 470, and 49er
performance data can responsibly inform a 505 polar as bounded context or
priors.

## Current status

- Created the transfer scope and acceptance criteria in `TRANSFER_METHOD.md`.
- Downloaded the 49er 2018/2020 `.pol` tables and their `.xlsx`/`.ods`
  workbooks; recorded sizes and SHA-256 hashes in `DOWNLOADS.md`.
- The `.pol` matrices pass structural checks (37 TWA rows, 15 TWS columns,
  expected 5-degree/5-unit grids, finite nonnegative values). The workbook
  HOWTO identifies Regatta Game as the spreadsheet input source; the
  spreadsheets are game-derived, while the `.pol` files' exact lineage remains
  unverified. Neither is verified real-world 49er performance.
- Found Tactical Sailing's 470/49er polar diagrams, but no raw numeric tables.
  No numerical 470 polar has been verified or downloaded.
- Extended the search to the Flying Dutchman. The IFDCO class page provides
  dimensions, sail areas, and hull/ready-to-sail weights; its "up to 20 knots"
  statement has no measurement conditions and is not a polar datum. The IFDCO
  also links a 2011 championship equipment/crew review with age, height, and
  weight analysis; it is potential crew-context evidence, not boat-speed data.
- Checked the public BLUR polars index; it lists no FD, 470, or 49er polar.
  The public SailGrib/QtVlm index lists 49er 2018/2020 only. SailGrib's separate
  400+ polar product page returned HTTP 403, so class availability there is
  unverified.
- Checked the World Sailing Paris 2024 tracking page; it exposed no
  downloadable 470/49er raw tracks. This does not establish that no underlying
  event data exist elsewhere.
- Checked the 49er class tracking URL; the fetched page exposed only a
  "Tracking" heading and no downloadable tracks. Dynamic or non-indexed content
  may not be represented by the page fetch.
- Direct interpolation or simple sail-area scaling is explicitly out of scope.

## Next steps

1. Ask the 49er polar host to confirm the `.pol` files' units, original method,
   and reuse terms; check whether the public tables are derived from the
   Regatta Game spreadsheets.
2. Obtain authorized access to the 470 research paper and/or request numeric
   470/FD data from class associations, Tactical Sailing, or Seapilot with
   provenance and terms.
3. If useful for crew-mass priors, extract and cite the FD review's crew
   statistics separately from the 505 parameter data; do not treat FD
   competitors as a substitute for 505 measurements.
4. Verify wind/speed definitions, conditions, and configuration before any
   comparison; provide only labeled, uncertain context to `vpp-theoretical`,
   never transferred values as measured 505 data.
