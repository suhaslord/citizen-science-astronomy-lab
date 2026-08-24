"""Reproducible aperture-photometry check of NASA/EXOTIC HAT-P-32 b sample data.

This is an independent, lightweight training analysis.  It is not an EXOTIC
replacement and must not be used to claim a new exoplanet result.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
from skimage.registration import phase_cross_correlation

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "EXOTIC_sampledata" / "HatP32Dec202017"
OUT = ROOT / "results"
TARGET = (424, 286)
COMPS = [(465, 183), (512, 263)]
RADIUS, R_IN, R_OUT = 6.0, 11.0, 17.0


def net_counts(image, positions):
    """Background-subtracted circular-aperture counts for each position."""
    apertures = CircularAperture(positions, r=RADIUS)
    annuli = CircularAnnulus(positions, r_in=R_IN, r_out=R_OUT)
    ap = aperture_photometry(image, apertures)["aperture_sum"].value
    ann = aperture_photometry(image, annuli)["aperture_sum"].value
    background_per_pixel = ann / annuli.area
    return ap - background_per_pixel * apertures.area


def observation_time(header):
    # These MicroObservatory files expose a UTC timestamp with a numeric timezone
    # suffix (e.g. ``-0000``), which Astropy's strict ``isot`` parser rejects.
    # Removing the zero offset preserves the UTC clock time.
    if "UT-OBS" in header:
        value = str(header["UT-OBS"])
        if value.endswith(("-0000", "+0000")):
            value = value[:-5]
        return Time(value, format="isot", scale="utc").jd
    for key in ("DATE-OBS", "DATEOBS"):
        if key in header:
            return Time(header[key], format="isot", scale="utc").jd
    raise KeyError("No DATE-OBS/DATEOBS in FITS header")


def main():
    OUT.mkdir(exist_ok=True)
    files = sorted(RAW.glob("*.FITS"))
    if not files:
        raise FileNotFoundError(f"No FITS files in {RAW}")
    rows = []
    reference = None
    for path in files:
        with fits.open(path) as hdul:
            image = np.asarray(hdul[0].data, dtype=float)
            header = hdul[0].header
            # The telescope field drifts substantially across the raw sequence.
            # Register every frame to the first image before placing apertures.
            clipped = np.clip(image - np.median(image), 0, np.percentile(image, 99.7))
            if reference is None:
                reference = clipped
                dy, dx = 0.0, 0.0
            else:
                (dy, dx), _, _ = phase_cross_correlation(reference, clipped, upsample_factor=10)
            positions = [(x - dx, y - dy) for x, y in [TARGET, *COMPS]]
            values = net_counts(image, positions)
            rows.append((observation_time(header), *values, path.name, dx, dy))
    rows.sort()
    jd = np.array([r[0] for r in rows])
    target = np.array([r[1] for r in rows])
    comps = np.array([[r[2], r[3]] for r in rows])
    comp_sum = comps.sum(axis=1)
    rel_flux = target / comp_sum
    # Reject frames whose comparison-star flux is implausibly low; this is an
    # explicit quality filter, not a data alteration, and raw measurements stay
    # in the CSV for review.
    comp_floor = 0.25 * np.median(comp_sum[comp_sum > 0])
    valid = np.isfinite(rel_flux) & (target > 0) & (comp_sum > comp_floor)
    if valid.sum() < 80:
        raise RuntimeError("Too few quality-controlled frames; inspect registration.")
    jd, target, comps, comp_sum, rel_flux = (a[valid] for a in (jd, target, comps, comp_sum, rel_flux))
    baseline = np.median(np.r_[rel_flux[:25], rel_flux[-25:]])
    normalized = rel_flux / baseline
    minutes = (jd - np.median(jd)) * 24 * 60
    # Centered 60-minute window is a transparent training proxy for in-transit.
    in_transit = np.abs(minutes) < 30
    depth = 1 - np.median(normalized[in_transit])
    residual_scatter = np.std(normalized[~in_transit] - 1, ddof=1)
    with (OUT / "photometry.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["jd_utc", "minutes_from_series_midpoint", "target_counts", "comparison_1_counts", "comparison_2_counts", "raw_relative_flux", "filename", "quality_control", "registration_dx_px", "registration_dy_px"])
        for i, row in enumerate(rows):
            original_flux = row[1] / (row[2] + row[3])
            writer.writerow([f"{row[0]:.8f}", "", f"{row[1]:.3f}", f"{row[2]:.3f}", f"{row[3]:.3f}", f"{original_flux:.8f}", row[4], "kept" if valid[i] else "rejected_low_or_invalid_comparison_flux", f"{row[5]:.2f}", f"{row[6]:.2f}"])
    fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)
    ax.scatter(minutes, normalized, s=17, color="#1f77b4", label="6 px aperture photometry")
    ax.axhline(1, color="0.35", lw=1, ls="--", label="out-of-transit baseline")
    ax.axhline(1-depth, color="#d62728", lw=1.4, label=f"central-window median (depth ≈ {depth*100:.2f}%)")
    ax.set(xlabel="Minutes from data-series midpoint", ylabel="Normalized target / comparison flux", title="HAT-P-32 b — official EXOTIC training sample")
    ax.legend(frameon=False)
    fig.savefig(OUT / "lightcurve.png", dpi=180)
    (OUT / "summary.md").write_text(
        f"# HAT-P-32 b training analysis\n\n"
        f"- Files analyzed: {len(files)} FITS images\n"
        f"- Method: phase-correlated frame registration to the first image; fixed 6-pixel aperture; annular local background (11–17 pixels); target `(424, 286)`; comparison stars `(465, 183)`, `(512, 263)`.\n"
        f"- Quality control: {valid.sum()} / {len(files)} frames kept when target and comparison counts were positive and comparison flux exceeded 25% of its positive median. Raw values and registration shifts are retained in `photometry.csv`.\n"
        f"- Reference: official EXOTIC `inits.json` target/comparison coordinates.\n"
        f"- Baseline: median of first and last 25 frames.\n"
        f"- Training proxy transit depth: **{depth*100:.2f}%** (central ±30-minute median comparison).\n"
        f"- Out-of-window residual scatter: **{residual_scatter*100:.2f}%**.\n\n"
        f"## Limitations\n\n"
        f"This is a reproducible exploratory training analysis, not the official EXOTIC fitted result. It does not optimize aperture/comparison stars, correct airmass/systematics, calculate a BJD_TDB mid-transit time, or derive formal parameter uncertainties. It must not be described as a discovery or as a submitted observation.\n",
        encoding="utf-8",
    )
    print((OUT / "summary.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
