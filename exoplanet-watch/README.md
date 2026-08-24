# NASA Exoplanet Watch — HAT-P-32 b training analysis

This workspace analyzes the official EXOTIC sample observation of HAT-P-32 b.
It is explicitly an **official training/sample observation analysis**, not a
personal telescope observation or an exoplanet discovery claim.

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\analyze_hatp32.py
```

Raw FITS files are in `EXOTIC_sampledata/`, cloned from the official sample-data
repository. The independent script writes `results/photometry.csv`,
`results/lightcurve.png`, and `results/summary.md`.

## Sources

- NASA Exoplanet Watch: https://science.nasa.gov/citizen-science/exoplanet-watch/
- EXOTIC pipeline: https://github.com/rzellem/EXOTIC
- Official sample data: https://github.com/rzellem/EXOTIC_sampledata

## Research-integrity notes

The script states its aperture, comparison stars, baseline, and deliberately
limited depth estimate. It does not substitute for EXOTIC’s systematics-aware
fit or publishable uncertainty treatment.
