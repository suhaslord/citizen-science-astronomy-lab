# Planet Hunters TESS — known-transit reproduction

This extension uses public TESS Sector 56 data for the known planet HD 209458 b. It runs a blind BLS period search, then compares the recovered period to a NASA Exoplanet Archive catalog value.

Run:

```powershell
..\exoplanet-watch\.venv\Scripts\python.exe .\reproduce_hd209458b.py
```

Outputs retain raw light-curve/catalog data, a plot, numerical result, and research log. This is a known-planet training reproduction, not a discovery or physical parameter-fit pipeline.
