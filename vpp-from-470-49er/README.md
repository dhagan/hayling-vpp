# Flying Dutchman / 470 / 49er comparison workstream

This workstream evaluates whether public Flying Dutchman (FD), 470, and 49er
performance data can provide bounds or priors for a 505 polar. It is not a
direct scaling exercise: the boats differ in hull form, righting power, rig,
sail plan, and planing behavior.

## Intended approach

- Find published or measured polars with provenance, wind definitions,
  configuration, and conditions; keep specifications, crew data, and speed
  claims distinct from polar observations.
- Verify each source and record whether its speed is measured through water or
  over ground.
- Compare like-for-like wind and sail modes; do not merge values from different
  measurement conventions.
- Use comparative data only as a prior/range or reasonableness check for the
  505-specific model. Keep transferred values labeled and uncertainty explicit.
- Do not infer a 505 polar by simply interpolating the 470 and 49er tables.

## Status

The source inventory is in `DOWNLOADS.md`. The FD class site provides
dimensions, sail areas, weights, trim guides, and a 2011 equipment/crew review,
but no verified FD polar. Its top-speed claim is not a measured polar point.
No raw numeric 470 polar has been verified; the 2020 470 paper remains a
technical lead with access and redistribution limitations. Two public 49er
`.pol` tables and
2018/2020 spreadsheet variants are downloaded, but the associated workbook
instructions identify Regatta Game as the spreadsheet input source; the `.pol`
files' lineage is not established. Treat the workbooks as game-derived and the
`.pol` tables as unverified candidate data, not measured 49er performance or a
validated class VPP. Tactical Sailing publishes 470/49er diagrams but no raw
numeric table. The BLUR index and public SailGrib/QtVlm file index yielded no
FD or 470 polar, and the World Sailing Paris 2024 tracking page exposed no raw
470/49er tracks. The 49er class tracking URL also yielded only a heading, with
no downloadable race tracks visible.

Theoretical 505 inputs and the primary 505 model are being developed in the
sibling `vpp-theoretical` directory.
