# SKYTRACE AI — Project Specification

**Challenge:** NASA Space Apps Challenge 2026 — *Planet X and SPHEREx: Discovering Change in the Infrared Sky*  
**Tagline:** *An Explainable AI Scientific Discovery Engine for the Changing Infrared Sky.*  
**Data Mode:** `SYNTHETIC_DEMO_DATA` (Deterministically generated SPHEREx-like infrared survey passes)  
**Mandatory Disclaimer:** **SIMULATED DEMO DATA — NOT A REAL ASTRONOMICAL DISCOVERY**

---

## 1. Executive Summary

SKYTRACE AI is an explainable AI-powered scientific discovery platform that enables users to explore multi-epoch infrared sky observations from NASA’s SPHEREx mission. It identifies changes across position, brightness, and infrared spectra, investigates possible instrumental false alarms, checks known catalogs, separates **Scientific Interestingness** from **Evidence Confidence**, and generates standardized **Scientific Discovery Passports**.

### The Core Discovery Journey
$$\textbf{Observe} \longrightarrow \textbf{Compare} \longrightarrow \textbf{Detect} \longrightarrow \textbf{Validate} \longrightarrow \textbf{Explain} \longrightarrow \textbf{Investigate}$$

---

## 2. Scientific Guardrails

1. **Synthetic Data Warning**: All demonstration data are explicitly labeled `SYNTHETIC_DEMO_DATA`.
2. **No Unwarranted Discovery Claims**: The app never claims to have detected Planet X, exoplanets, or biosignatures.
3. **Transparent Heuristic**: Anomaly scores are transparent triage heuristics, not physical probabilities of discovery.
4. **Catalog Disclaimers**: "No catalog match" does not imply an undiscovered object.
5. **Quality Failure Visibility**: Missing metadata or failed checks evaluate to `UNKNOWN` or `FAIL`, never an invented pass.

---

## 3. Five-Dimensional Anomaly Dimensions

1. **Astrometric Proper Motion (30%)**: Angular displacement and linear trajectory consistency.
2. **Photometric Variability (25%)**: Reduced $\chi^2$ against constant flux and fractional variation.
3. **Infrared Spectral & SED (20%)**: Color index departures and molecular ice absorption (3.05 μm $\text{H}_2\text{O}$ / 4.27 μm $\text{CO}_2$).
4. **Temporal Dynamics (15%)**: Light curve derivatives and explosive transient evolution.
5. **Contextual Neighborhood Outlier (10%)**: Robust MAD $z$-scores relative to local reference stars.

---

## 4. Canonical Demo Candidates

- `DEMO-001` (also `RW-001`): High-proper-motion Solar System moving object candidate.
- `DEMO-002` (also `RW-002`): Large-amplitude Mira pulsating variable candidate.
- `DEMO-003` (also `YSO-ICE-07`): Protostellar core with deep $\text{H}_2\text{O}$ and $\text{CO}_2$ ice absorption.
- `DEMO-ART-99` (also `ART-CR-99`): Cosmic ray charge deposit (sub-diffraction PSF FWHM $< 1.0''$).
