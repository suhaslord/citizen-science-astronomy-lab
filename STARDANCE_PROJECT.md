# Stardance project plan — TESS Transit Validation Explorer

## Status

**Registered for Hack Club Stardance. Project not yet submitted/shipped on Stardance.**

This project will turn the existing public-data transit-validation work in this repository into a small, reproducible explorer for known exoplanets. It is a validation/reproduction project, not a planet-discovery claim.

## Goal

Make a tool that lets someone choose a confirmed exoplanet, retrieve or load its public TESS light curve, recover the known transit signal, and compare the measured result with a catalog value.

## Existing baseline

The repository already contains a reproducible known-transit example for **HD 209458 b** using public TESS data. Local work has also been used to test additional known targets; any target added to the shipped public version must have its inputs, outputs, and validation committed or otherwise reproducible before it is claimed here.

## Ship checklist

- [ ] Generalize the target configuration instead of hard-coding one system.
- [ ] Add at least three fully reproducible confirmed-planet examples to the public package.
- [ ] Produce one summary table with catalog period, recovered period, error, and data provenance.
- [ ] Export a clean folded-light-curve plot for each target.
- [ ] Add a simple user-facing entry point (notebook, CLI, or lightweight web view) that another person can actually try.
- [ ] Document failed/poor recoveries rather than hiding them.
- [ ] Add limitations and research-integrity wording to every public-facing result.
- [ ] Ship the finished open-source project on Stardance and request peer feedback.

## Stardance logging rule

Only log time actually spent working after the project is connected to Stardance/Hackatime as required by the platform. Do not backfill or invent hours. Stardance states that tracked time counts through devlogs and that certificate hours must be verified project work tied to a shipped project.

## Suggested devlog format

### What I worked on
- Concrete code/data/visualization changes made today.

### What changed
- Before/after behavior or measured result.

### Evidence
- Commit, plot, test output, or screenshot.

### Problems / failed attempts
- Anything that did not work and why.

### Next
- One or two specific next steps.

## Scientific scope

Good wording:

> Reproduces known exoplanet transit signals in public TESS data and compares recovered parameters with catalog/reference values.

Do not describe the project as discovering planets unless an independent scientific collaboration later validates an actually new candidate.
