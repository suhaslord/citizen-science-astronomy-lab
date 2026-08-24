# Citizen-Science Astronomy Lab

Reproducible training analyses using public astronomy data. This repository is
careful about scientific scope: neither project presents a discovery claim.

## Projects

### Planet Hunters TESS — known-transit reproduction

`planet-hunters-tess/` retrieves a public TESS Sector 56 SPOC light curve for
the already known planet HD 209458 b, runs a blind box-least-squares search,
and then compares the recovered period with the NASA Exoplanet Archive catalog.
The committed result used 18,791 cleaned cadences and recovered the period to
within roughly 0.51 minutes. Raw files are deliberately downloaded locally,
not versioned.

### NASA Exoplanet Watch / EXOTIC — sample-data setup

`exoplanet-watch/` provides a transparent aperture-photometry diagnostic for
the official HAT-P-32 b sample observation. It is intentionally labeled as a
training diagnostic rather than a publishable EXOTIC fit. Use the official
EXOTIC environment/tutorial before interpreting parameters.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\planet-hunters-tess\reproduce_hd209458b.py
```

For the Exoplanet Watch sample project, clone the official sample-data
repository into `exoplanet-watch/EXOTIC_sampledata/`, then run its script.

## Sources

- NASA Exoplanet Watch: https://science.nasa.gov/citizen-science/exoplanet-watch/
- EXOTIC: https://github.com/rzellem/EXOTIC
- EXOTIC sample data: https://github.com/rzellem/EXOTIC_sampledata
- TESS data at MAST: https://mast.stsci.edu/
- NASA Exoplanet Archive: https://exoplanetarchive.ipac.caltech.edu/

## Research integrity

Scripts record their data source, method, limitations, and reproduction path.
Raw data remain separate from derived results. Any apparent detection must be
treated as a known-object reproduction unless independently verified by the
relevant scientific collaboration.
