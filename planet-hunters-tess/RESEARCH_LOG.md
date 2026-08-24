# Known-transit reproduction log

## Question
Can a blind BLS search recover HD 209458 b’s known period from public TESS data?

## Dataset
Public TESS Sector 56 SPOC 120-second light curve for TIC 420814525, retained as raw FITS.

## Method
PDCSAP flux was normalized; NaNs and 8-sigma outliers removed; a 401-cadence second-order flattening filter applied. BLS searched 3.35–3.70 days and 0.08–0.18-day durations without using the catalog period as a fit constraint.

## Result
```json
{
  "target": "HD 209458",
  "known_planet": "HD 209458 b",
  "sector": 56,
  "cadences_after_cleaning": 18791,
  "catalog_period_days": 3.52474859,
  "bls_detected_period_days": 3.5250999999999997,
  "period_difference_minutes": 0.5060303999992755,
  "bls_duration_hours": 2.4960000000000004,
  "bls_mid_transit_btjd": 2826.778629476596,
  "simple_in_vs_out_depth_percent": 1.531776148148034,
  "out_of_transit_scatter_ppm": 325.9118353811397
}
```

## Limitations
This is a known-planet training reproduction, not discovery evidence. Flattening can distort transit shape; grid resolution, red noise, and systematics are not fully modeled. Depth/scatter are diagnostics, not formal fitted parameters or uncertainties.

## Sources
- TESS/MAST: https://mast.stsci.edu/
- Lightkurve: https://docs.lightkurve.org/
- NASA Exoplanet Archive query: https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select%20pl_name,pl_orbper,pl_tranmid,pl_radj%20from%20pscomppars%20where%20pl_name%3D%27HD%20209458%20b%27&format=csv
- Generated: 2026-08-24 06:45 UTC
