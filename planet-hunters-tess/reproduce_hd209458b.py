"""Reproduce a known HD 209458 b transit in public TESS data; never a discovery claim."""
from pathlib import Path
import csv, io, json
from datetime import datetime, timezone
from urllib.request import urlopen
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
RAW, OUT = ROOT / "data" / "raw", ROOT / "output"
TARGET, SECTOR = "HD 209458", 56
CATALOG_URL = ("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="
               "select%20pl_name,pl_orbper,pl_tranmid,pl_radj%20from%20pscomppars%20where%20pl_name%3D%27HD%20209458%20b%27&format=csv")

def fetch_lightcurve():
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / "hd209458_tess_s56_spoc_120s.fits"
    if path.exists(): return lk.read(path), path
    result = lk.search_lightcurve(TARGET, mission="TESS", sector=SECTOR, author="SPOC", exptime=120)
    if len(result) != 1: raise RuntimeError(f"Expected one SPOC product, found {len(result)}")
    lc = result.download(); lc.to_fits(path=path, overwrite=True)
    return lc, path

def fetch_catalog():
    raw = urlopen(CATALOG_URL, timeout=60).read().decode("utf-8")
    path = RAW / "nasa_exoplanet_archive_hd209458b.csv"; path.write_text(raw, encoding="utf-8")
    return next(csv.DictReader(io.StringIO(raw))), path

def main():
    OUT.mkdir(exist_ok=True)
    lc, lc_path = fetch_lightcurve(); catalog, cat_path = fetch_catalog()
    catalog_period = float(catalog["pl_orbper"])
    clean = lc.remove_nans().remove_outliers(sigma=8).normalize()
    flattened = clean.flatten(window_length=401, polyorder=2)
    bls = flattened.to_periodogram(method="bls", period=np.linspace(3.35, 3.70, 7001), duration=np.linspace(.08, .18, 11))
    period = float(bls.period_at_max_power.value)
    duration = float(bls.duration_at_max_power.value)
    epoch = float(bls.transit_time_at_max_power.value)
    folded = flattened.fold(period=period, epoch_time=epoch)
    hours, flux = folded.time.value * 24, folded.flux.value
    in_transit, out_transit = np.abs(hours) < duration * 12, np.abs(hours) > duration * 18
    depth = float(1 - np.nanmedian(flux[in_transit]) / np.nanmedian(flux[out_transit]))
    scatter_ppm = float(np.nanstd(flux[out_transit] - 1, ddof=1) * 1e6)
    result = {"target": TARGET, "known_planet": catalog["pl_name"], "sector": SECTOR,
              "cadences_after_cleaning": int(len(clean)), "catalog_period_days": catalog_period,
              "bls_detected_period_days": period, "period_difference_minutes": (period-catalog_period)*1440,
              "bls_duration_hours": duration*24, "bls_mid_transit_btjd": epoch,
              "simple_in_vs_out_depth_percent": depth*100, "out_of_transit_scatter_ppm": scatter_ppm}
    fig, (a, b) = plt.subplots(2, 1, figsize=(11,8), constrained_layout=True)
    fig.suptitle("HD 209458 — public TESS Sector 56 SPOC 120-second photometry", x=.125, y=.99, ha="left", fontsize=16, fontweight="bold")
    a.scatter(clean.time.value, clean.flux.value, s=.5, color="#5784ba", alpha=.3, rasterized=True)
    a.set(xlabel="TESS time (BTJD)", ylabel="Normalized PDCSAP flux")
    a.spines[["top","right"]].set_visible(False)
    b.scatter(hours, flux, s=2, color="#5784ba", alpha=.24, rasterized=True, label="Individual cadences")
    edges=np.linspace(-5,5,101); centers=(edges[:-1]+edges[1:])/2; indices=np.digitize(hours,edges)
    b.plot(centers,[np.nanmedian(flux[indices==i]) for i in range(1,len(edges))],color="#d55e00",lw=2,label="Median in 0.1-hour bins")
    b.axvspan(-duration*12,duration*12,color="#d55e00",alpha=.1,label="BLS duration")
    b.set(xlim=(-5,5), xlabel="Hours from BLS mid-transit", ylabel="Flattened normalized flux", title=f"BLS: {period:.8f} d  |  NASA catalog: {catalog_period:.8f} d")
    b.legend(frameon=False,ncol=3,fontsize=9); b.spines[["top","right"]].set_visible(False)
    fig.savefig(OUT / "hd209458b_tess_transit.png", dpi=220)
    (OUT / "result.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    log = "# Known-transit reproduction log\n\n## Question\nCan a blind BLS search recover HD 209458 b’s known period from public TESS data?\n\n## Dataset\nPublic TESS Sector 56 SPOC 120-second light curve for TIC 420814525, retained as raw FITS.\n\n## Method\nPDCSAP flux was normalized; NaNs and 8-sigma outliers removed; a 401-cadence second-order flattening filter applied. BLS searched 3.35–3.70 days and 0.08–0.18-day durations without using the catalog period as a fit constraint.\n\n## Result\n```json\n" + json.dumps(result,indent=2) + "\n```\n\n## Limitations\nThis is a known-planet training reproduction, not discovery evidence. Flattening can distort transit shape; grid resolution, red noise, and systematics are not fully modeled. Depth/scatter are diagnostics, not formal fitted parameters or uncertainties.\n\n## Sources\n- TESS/MAST: https://mast.stsci.edu/\n- Lightkurve: https://docs.lightkurve.org/\n- NASA Exoplanet Archive query: " + CATALOG_URL + "\n- Generated: " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC") + "\n"
    (OUT / "RESEARCH_LOG.md").write_text(log, encoding="utf-8")
    print(json.dumps(result,indent=2)); print(f"Raw: {lc_path}\nCatalog: {cat_path}")

if __name__ == "__main__": main()
