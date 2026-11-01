# Cosmiclens— Complete Project Specification and 24-Hour Build Workflow

**Purpose:** Canonical self-contained brief for any AI coding assistant or developer (Claude, Antigravity, DeepSeek, Manus, Copilot, or similar). Read this file before planning, coding, or changing project scope.

**Working name:** SKYTRACE AI (recommended for clarity). Alternatives: ASTRAEON (distinctive brand), COSMIC-TRACE (name used in the supplied workflow), and the original Resonant Worlds Explorer (which sounds more focused on exoplanets/astrobiology). Choose one final name and use it consistently. Suggested repository slug: `skytrace-ai`.

**Target challenge:** NASA Space Apps Challenge 2026 — “Planet X and SPHEREx.” Verify the current official challenge statement and judging/submission requirements before implementation.

**Tagline:** *An Explainable AI Scientific Discovery Engine for the Changing Infrared Sky.*

---

## 1. Executive summary

SKYTRACE AI is a public-facing scientific discovery environment that helps people explore repeated observations from NASA’s SPHEREx mission and understand how astronomical sources change over time and across infrared wavelengths.

Its core journey is:

**Observe → Compare → Detect → Validate → Explain → Investigate**

Users explore a sky region and observation epochs, play them through a **Sky Time Machine**, select a source, inspect its position and brightness history, compare its spectral fingerprint, and see why its behavior may be scientifically interesting. The system then evaluates available data-quality information, investigates possible false alarms, checks relevant known-object catalogs where practical, separates **Scientific Interestingness** from **Evidence Confidence**, and creates a **Scientific Discovery Passport** and evidence-based report.

The differentiator is not simply another SPHEREx viewer. NASA/IPAC IRSA already provides archive access and tools for source discovery, moving-object search, spectra, cutouts, mosaics, and related tasks. SKYTRACE should add an explainable **discovery, validation, prioritization, and storytelling layer**, not recreate those existing services.

The hackathon strategy is to build a complete end-to-end demo first. If real data access is difficult, use a deterministic, clearly labeled synthetic SPHEREx-like dataset. Never present synthetic measurements as actual NASA observations.

### One-sentence definition

> SKYTRACE AI is an explainable AI-powered platform that helps people explore repeated SPHEREx observations, identify potentially interesting changes in the infrared sky, investigate possible artifacts and known-object explanations, and turn the evidence into understandable candidate profiles.

### Core judge-demo story

1. Open the Interactive Sky Explorer.
2. Select a demo region and move through four observation epochs.
3. Watch illustrative sources change position, brightness, or spectral shape.
4. Select a candidate and inspect motion, photometry, spectrum, and time-series plots.
5. Review transparent anomaly components and their underlying evidence.
6. Inspect quality checks and possible false-alarm explanations.
7. Review catalog cross-check results and limitations.
8. Compare interestingness with evidence confidence.
9. Open the candidate's Scientific Discovery Passport.
10. Generate an HTML/PDF report.

---

## 2. Challenge alignment and boundaries

### Direct fit

The app must visibly help users explore repeated SPHEREx observations and understand how source properties change over time. Verify the official challenge page and current NASA/IPAC IRSA documentation before coding; release names, product schemas, units, quality flags, and endpoints must not be guessed.

### The app is / is not

**It is:** an interactive astronomy exploration tool, temporal comparison interface, explainable anomaly-triage assistant, evidence organizer, and candidate-prioritization prototype.

**It is not:** a claim to have discovered Planet X, a planet, or extraterrestrial life; a replacement for professional analysis; a replacement for IRSA archive tools; a requirement to download the whole SPHEREx archive; or permission to invent observations or scientific conclusions.

### Differentiation

Focus on:
- Time-oriented exploration and synchronized views.
- Linked positional, temporal, photometric, and spectral evidence.
- Explainable anomaly scores.
- Data-quality and false-alarm investigation.
- Separate interestingness and confidence.
- Candidate passports and reproducible reports.
- Guided usability for non-specialists.

Link to existing NASA/IPAC tools when they already provide a function better than the hackathon app can.

---

## 3. Scientific context and guardrails

SPHEREx is a NASA all-sky near-infrared spectroscopic survey mission. Its data cover approximately 0.75–5 micrometres in 102 spectral bands. Treat these as background context; verify exact product coverage, units, schemas, uncertainty columns, flags, release names, and access methods from official documentation for the specific data being used.

Mandatory guardrails:
1. A statistical anomaly is not automatically a physical discovery.
2. “No catalog match” does not mean “unknown object”; a query may be incomplete or limited by coverage, epoch, sensitivity, radius, or service availability.
3. Label all synthetic records persistently: **SIMULATED DEMO DATA — NOT A REAL ASTRONOMICAL DISCOVERY**.
4. Never claim the app has detected Planet X.
5. The former exoplanet/biosignature idea is optional and outside the core challenge. O₂ + CH₄ alone does not prove life; atmospheric interpretation requires context, uncertainty, and abiotic false-positive analysis.
6. The original “Modulus” exact-math engine claimed to solve physics/chemistry without numerical error. That is an extraordinary claim and is not an MVP requirement. If retained later, document its precise algorithm, guarantees, benchmarks, and limits; call it experimental until demonstrated.
7. Do not present a heuristic score as a calibrated probability.
8. Distinguish raw observations, derived measurements, algorithmic scores, AI-generated explanations, and future suggestions.
9. If metadata needed for a check are unavailable, show “UNKNOWN” or “NOT EVALUATED,” not an invented pass.
10. A language model may explain computed evidence but must not invent fluxes, uncertainties, catalog matches, or scientific interpretations.

### Provenance modes

Use `REAL_ARCHIVE_DATA`, `SYNTHETIC_DEMO_DATA`, or `MIXED_DATA`. Store product/source identifier, source URL where available, retrieval time, release/version, units, and caveats. Never silently mix real and synthetic data.

---

## 4. Product goals and acceptance criteria

### Users
- Space Apps judges and the public.
- Citizen scientists and astronomy learners.
- Students learning data-driven astronomy.
- Researchers as a future candidate-triage audience.

### Hackathon success criteria
- Runs locally from documented instructions.
- Loads a small region with four demo epochs.
- Displays interactive sources and allows epoch selection/playback.
- Shows at least one deliberately designed candidate anomaly.
- Plots motion/position, brightness over time, and multi-band spectral fingerprint.
- Calculates transparent anomaly components.
- Explains why a candidate was flagged.
- Shows data-quality/false-alarm checks.
- Separates interestingness and evidence confidence.
- Generates a structured passport and report.
- Clearly labels synthetic data.
- Includes tests, documentation, and a rehearsed presentation.

---

## 5. Features and priorities

### 5.1 MUST — Interactive SPHEREx Sky Explorer

- Show a selected sky region as an interactive 2D sky map.
- Plot source positions; allow click-to-select and hover details.
- Highlight the selected source in linked views.
- Show source ID, RA, Dec, epoch, and selected measurement.
- Choose an epoch and filter candidates by priority, anomaly dimension, or provenance.
- Provide coordinate units, legend, and a simple demo-region selector.
- Use Canvas or SVG for the MVP. If using a schematic map or decorative star background, do not imply it is a calibrated telescope image.
- Document any coordinate-to-screen projection and handle celestial coordinates correctly.

### 5.2 MUST — Sky Time Machine (signature feature)

- Timeline with all available epochs, play/pause, manual selection, and timestamps.
- Smoothly update source positions, brightness indicators, selected-source details, and plots.
- Keep source identity consistent across epochs where the data supports matching.
- Show elapsed time and make clear that observations are discrete, not continuous.
- The supplied workflow uses four synthetic epochs in March, May, August, and October 2026. These are demo timestamps, not claims about actual SPHEREx coverage.

### 5.3 MUST — AI Anomaly Reasoner

Analyze five dimensions:
1. **Motion:** positional change relative to uncertainty and expected behavior.
2. **Photometry:** brightness variation accounting for flux errors.
3. **Spectral:** unusual spectral shape/color or changes across epochs.
4. **Temporal:** unusual time-series patterns, emergence/disappearance, or acceleration only when sampling and precision justify it.
5. **Context:** outlier behavior relative to a suitable population of compatible sources.

Initial workflow weights (configurable demo assumptions, not universal scientific truths):
- Motion 30%
- Photometry 25%
- Spectral 20%
- Temporal 15%
- Context 10%

Use transparent robust statistics first: median/MAD robust z-scores, uncertainty-aware positional displacement, error-aware flux variation, and uncertainty-normalized spectral differences. Isolation Forest or other scikit-learn models are optional. Do not add neural networks before the baseline works.

Normalize available components to a documented 0–100 scale. If a component is missing, do not silently treat it as zero: either renormalize valid weights under a documented rule or mark the total incomplete. Store score weights and algorithm version with every result. The score is a prioritization heuristic, not a probability of discovery.

### 5.4 MUST — False Alarm Investigator

Where metadata permit, check:
- Measurement uncertainty and signal-to-noise.
- Missing epochs/bands.
- Supplied data-quality flags.
- Saturation/detector flags if present.
- Possible bad pixels, PSF/measurement concerns, or neighboring-source contamination where supported.
- Whether apparent changes are small relative to uncertainty.
- Whether one questionable epoch dominates the result.
- Whether cadence/coverage support the interpretation.
- Ambiguous cross-matches.

Use documented states such as `PASS`, `CAUTION`, `FAIL`, `UNKNOWN`. Do not output a numeric “artifact probability” unless a defined and validated probabilistic model exists. If metadata are unavailable, state that the check could not be evaluated.

### 5.5 MUST — “Why Is This Interesting?”

Create evidence-linked explanations from computed values, for example:
- “Position changed by X arcseconds; this is Y times the estimated combined positional uncertainty.”
- “Flux varied by X%; uncertainty is shown on the light curve.”
- “The strongest spectral difference occurs in these bands.”
- “The spectral component drives this score; motion remains inconclusive.”
- “Confidence is limited because only N usable epochs are available.”
- “A quality flag may explain the apparent change.”

Each explanation should link to the chart/table/flag that supports it. An LLM can paraphrase structured evidence, never invent measurements.

### 5.6 MUST — Separate Interestingness and Evidence Confidence

- **Scientific Interestingness:** unusualness under the documented scoring method.
- **Evidence Confidence:** reliability/completeness based on data quality, uncertainties, usable epochs, consistency, and validation.
- **Scientific Priority:** a triage category, not proof that a source is real or important.

Show them separately. A highly interesting but low-confidence candidate is a valid outcome. If numeric confidence is not calibrated, use tiers (`LOW`, `MODERATE`, `HIGH`, `INSUFFICIENT DATA`) with reasons instead of a percentage.

### 5.7 MUST — Scientific Discovery Passport

A stable, structured profile for each candidate. Use Pydantic or equivalent schema validation.

Suggested JSON structure (schema example only; values are not real results):

```json
{
  "passport_id": "ST-001-DEMO-001",
  "data_provenance": "SYNTHETIC_DEMO_DATA",
  "source_identity": {
    "source_id": "DEMO-001",
    "region_id": "region_001",
    "observation_span": "derived from available epochs",
    "usable_epoch_count": 4
  },
  "position_and_motion": {
    "trajectory": [],
    "total_motion_arcsec": null,
    "assessment": ""
  },
  "photometry": {
    "measurements": [],
    "fractional_variability": null,
    "assessment": ""
  },
  "spectral_fingerprint": {
    "wavelength_um": [],
    "flux": [],
    "uncertainty": [],
    "spectral_changes": [],
    "assessment": ""
  },
  "data_quality": {
    "available_flags": [],
    "missing_metadata": [],
    "assessment": ""
  },
  "false_alarm_investigation": {
    "checks": [],
    "possible_alternatives": [],
    "assessment": ""
  },
  "known_object_cross_check": {
    "catalogs_checked": [],
    "matches": [],
    "limitations": ""
  },
  "analysis": {
    "algorithm_version": "",
    "component_scores": {},
    "interestingness_score": null,
    "evidence_confidence": null,
    "scientific_priority": "UNASSESSED",
    "why_interesting": []
  },
  "follow_up_suggestions": [],
  "generated_at": "",
  "limitations": []
}
```

Include provenance, observation span, usable epochs, motion, photometry/light curve, spectral fingerprint/change, quality checks, false-alarm investigation, actual catalog query status, component scores, algorithm version, interestingness, confidence, priority, limitations, timestamp, and suggested follow-up. Suggestions must not be presented as confirmed requirements.

### 5.8 SHOULD — Spectral Fingerprint Viewer

- Plot wavelength in μm against flux in the correct documented units.
- Show uncertainties/error bars if available.
- Hover values, epoch selection/overlays, missing-band indicators, and optional normalized spectra.
- Distinguish measured values from interpolation or normalization.
- Inspect actual product schema first: do not assume every SPHEREx product is a simple 102-point spectrum.
- IRSA already provides spectral-related tools; add interpretation and epoch comparison rather than only a line chart.

### 5.9 SHOULD — Spectral Change Detector

Compare compatible spectra across epochs. Show epoch A/B, difference spectrum, optional uncertainty-normalized differences, bands contributing to the score, missing data, and whether differences exceed uncertainty. Do not infer molecules from broad-band changes without a suitable model.

### 5.10 SHOULD — Known-Object Cross-Check

Potential services/catalogs include Gaia, 2MASS, VizieR, or other relevant sources, but verify each API and its matching semantics before implementing. Show catalogs actually checked, search radius, counterpart and angular separation, returned metadata, query time/status, ambiguous matches, and limitations.

Statuses should distinguish `MATCH FOUND`, `NO MATCH FOUND IN QUERIED CATALOGS`, and `NOT CHECKED`. Never conclude “not a known object” from a limited failed query.

### 5.11 SHOULD — Candidate ranking/feed

Rank candidates by transparent triage criteria. Show interestingness, confidence/tier, dominant dimension, provenance, usable epoch count, quality caveat, and why the source is listed. Filters may include spectral variability, motion-like behavior, photometric variability, quality, confidence, and provenance. This is a triage queue, not a list of confirmed discoveries.

### 5.12 SHOULD — Discovery Report Generator

Generate HTML first; PDF is optional. Include identity/provenance, observation span, motion and light-curve plots, spectral plots, score components and method, quality/false-alarm checks, catalog checks, separate interestingness/confidence, alternatives, limitations, follow-up suggestions, sources, retrieval time, algorithm version, and generation timestamp. Build the report from the passport; label synthetic data prominently.

### 5.13 NICE — Cross-Mission Evidence Graph

Connect actual SPHEREx data, source, temporal/spectral analyses, quality checks, catalog counterparts, and suggested follow-up. Potential external evidence includes Gaia astrometry, 2MASS infrared data, and VizieR records if relevant. Each edge must represent a real relationship or be labeled as a suggestion. If a query was not run, show “not queried.”

### 5.14 NICE — AI Discovery Chain

Make analysis auditable:

`Observation → source association → temporal comparison → motion → photometry → spectral analysis → quality checks → false-alarm investigation → catalog cross-check → candidate assessment → passport/report`

Each step shows inputs, computation, output, caveats, status, and supporting evidence.

### 5.15 NICE — Human + AI Discovery Mode

Offer AI-assisted candidate ranking and human-led exploration. Users can select region, epoch, source, wavelength range, or measurement before asking for analysis. Let users inspect raw evidence and challenge an AI interpretation.

### 5.16 NICE — Natural-Language Astronomy Search

Example requests: “Show strong brightness variation,” or “Find spectral variability with acceptable quality.” The LLM must convert language into a validated allow-listed filter object; the backend executes deterministic queries. Never run arbitrary model-generated SQL or invent results. Core app must work without paid LLM API keys; secrets belong in environment variables, never Git.

### 5.17 OPTIONAL — Atmosphere/biosignature extension

This belongs to the original Resonant Worlds Explorer concept, not the core challenge. Add only with suitable verified data and after the MVP. Potential molecule analysis (H₂O, CO₂, CH₄, O₂, O₃) requires suitable data/models and abiotic false-positive analysis. Do not assume SPHEREx survey data alone supports detailed characterization of a particular exoplanet atmosphere.

### 5.18 OPTIONAL — Modulus research engine

Only add if the method, guarantees, benchmarks, and limitations are precise and reproducible. Keep it separate and experimental; do not claim zero numerical error or superior atmospheric accuracy without evidence.

---

## 6. Technical architecture and stack

### Data flow

```text
NASA / NASA-IPAC IRSA SPHEREx data
       ↓
Data acquisition and provenance
       ↓
Parsing / normalization / source association
       ↓
Observation, source, epoch, photometry, spectrum
       ↓
Temporal + positional analysis / photometric + spectral analysis
       ↓
Explainable anomaly engine
       ↓
Data-quality + false-alarm checks
       ↓
Known-object cross-check (optional)
       ↓
Evidence aggregation and candidate triage
       ↓
Scientific Discovery Passport + report
       ↓
Next.js web interface
```

### Recommended stack

**Frontend:** Next.js, React, TypeScript, Tailwind CSS; SVG/Canvas for MVP sky view; Recharts, Plotly, or D3 for plots (choose one to reduce dependencies).

**Backend:** Python, FastAPI, Uvicorn, Pydantic, NumPy, SciPy, pandas; scikit-learn optional; Astropy for astronomy coordinates/FITS; Astroquery only after verifying support for the required current IRSA query; ReportLab if PDF export is implemented.

**Data:** official NASA/IPAC IRSA products when feasible; small sample region; local caching; synthetic data fallback. Do not download the entire archive. JSON is fine for MVP; Parquet/object storage may help later.

**Database:** JSON files or SQLite are enough for a 24-hour MVP. Later PostgreSQL tables could include `observations`, `sources`, `source_positions`, `photometry`, `spectra`, `quality_flags`, `anomaly_features`, `anomaly_results`, `catalog_matches`, `evidence_links`, and `discovery_reports`.

**Deployment:** local frontend/backend first. Docker Compose after the core works. Possible deployment: Vercel frontend plus Render/Railway or equivalent backend; verify current service limits and configure the deployed API URL correctly. The app must still run locally if deployment fails.

### Suggested repository layout

```text
skytrace-ai/
├── README.md
├── PROJECT_SPEC.md
├── ARCHITECTURE.md
├── DEVELOPMENT.md
├── ALGORITHM.md
├── API.md
├── DEMO.md
├── DEPLOYMENT.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── data_generator.py
│   ├── data_loader.py
│   ├── anomaly_engine.py
│   ├── false_alarm.py
│   ├── discovery_passport.py
│   ├── report_generator.py
│   ├── irsa_client.py
│   ├── catalog_client.py
│   ├── cache.py
│   ├── requirements.txt
│   └── tests/
└── frontend/
    ├── app/{page.tsx,layout.tsx,globals.css}
    ├── components/
    │   ├── SkyExplorer.tsx
    │   ├── Timeline.tsx
    │   ├── CandidateDetail.tsx
    │   ├── SpectraViewer.tsx
    │   ├── LightCurve.tsx
    │   ├── FalseAlarmPanel.tsx
    │   ├── DiscoveryPassport.tsx
    │   ├── ReportModal.tsx
    │   ├── EvidenceGraph.tsx
    │   └── ErrorBoundary.tsx
    ├── hooks/{useRegionData.ts,useAnalysis.ts}
    ├── lib/api.ts
    └── package.json
```

This is a guide, not a requirement to create every file immediately. Keep the first vertical slice small.

---

## 7. Synthetic demo dataset and scoring

### Dataset

The supplied workflow proposes one synthetic region, four epochs (example dates March, May, August, October 2026), three designed candidate behaviors, and 10–20 background sources per epoch. Include flux errors, position uncertainty, quality flags, and at least one ambiguous/low-quality source. Use a deterministic random seed.

Suggested candidates:
- `DEMO-001`: motion-like behavior.
- `DEMO-002`: brightness/photometric variability.
- `DEMO-003`: spectral/color change.

Older workflow identifiers `RW-001`, `RW-002`, `RW-003` can be retained internally, but `DEMO-*` makes synthetic provenance clearer.

Illustrative record:

```json
{
  "region_id": "region_001",
  "name": "Synthetic Demo Region",
  "data_provenance": "SYNTHETIC_DEMO_DATA",
  "epochs": [
    {
      "epoch_id": "epoch_001",
      "timestamp": "2026-03-01T00:00:00Z",
      "sources": [
        {
          "source_id": "DEMO-001",
          "ra_deg": 282.74,
          "dec_deg": -5.52,
          "position_uncertainty_arcsec": 0.5,
          "measurements": [
            {
              "wavelength_um": 1.1,
              "flux": 42.0,
              "flux_uncertainty": 2.0,
              "flux_unit": "DEMO_UNIT",
              "quality_flags": []
            }
          ]
        }
      ]
    }
  ]
}
```

This is a schema example, not actual NASA data. Adapt to the real product schema if integrating archive data. Use coherent units; never mix incompatible measurements without justified transformations.

### Score definitions

- Motion: angular separation on the celestial sphere; account for RA wrap/declination; compare with combined position uncertainty and elapsed time.
- Photometry: light curve and variability with flux uncertainties, non-detections, and missing epochs.
- Spectral: compatible-band differences with uncertainty; show which bands drive the score.
- Temporal: consider cadence and sampling; do not overclaim periodicity/acceleration from four points.
- Context: compare to an adequate, compatible population; if too small/biased, mark unavailable or low-reliability.

Initial configurable weights: motion .30, photometry .25, spectral .20, temporal .15, context .10. Store the weights and algorithm version. The output score is a heuristic, not a probability.

Illustrative response:

```json
{
  "source_id": "DEMO-001",
  "data_provenance": "SYNTHETIC_DEMO_DATA",
  "interestingness_score": 89,
  "evidence_confidence": {
    "tier": "MODERATE",
    "numeric_value": null,
    "reasons": ["Four usable synthetic epochs", "One quality limitation remains"]
  },
  "component_scores": {
    "motion": 92,
    "photometry": 75,
    "spectral": 68,
    "temporal": 61,
    "context": 54
  },
  "why_interesting": [
    {
      "dimension": "motion",
      "claim": "A position change is present in the available measurements.",
      "measurement_refs": ["position_series"],
      "limitations": ["Synthetic demonstration values"]
    }
  ],
  "quality_checks": [],
  "catalog_checks": {"status": "NOT_CHECKED", "catalogs": []},
  "algorithm_version": "demo-0.1"
}
```

Example scores are illustrative only. Do not hard-code them as actual findings.

---

## 8. API and UI requirements

### Minimum FastAPI endpoints

- `GET /api/health` — health and active data mode.
- `GET /api/regions` — regions and provenance.
- `GET /api/region/{region_id}` — metadata and source/epoch summary.
- `GET /api/region/{region_id}/epochs` — epochs.
- `GET /api/region/{region_id}/sources` — source list/filter/pagination.
- `GET /api/source/{source_id}` — source details and measurements.
- `POST /api/analyze/object` — analyze a validated source.
- `GET /api/discoveries?region_id=...&limit=10` — ranked candidate list.
- `GET /api/passport/{passport_id}` — passport.
- `POST /api/report/{passport_id}` — optional report.
- `POST /api/search/nlp` — optional NL filters.

Validate inputs and use typed response schemas. Do not expose arbitrary file paths or unrestricted archive queries. Configure CORS for expected frontend origins.

### Frontend main layout

- Header: product name, challenge label, data provenance, about/source links.
- Main panel: Sky Explorer.
- Timeline panel: Sky Time Machine.
- Detail panel: selected source, interestingness, evidence confidence, dominant anomaly, explanation, quality caveats.
- Secondary views: light curve, spectrum, false-alarm checks, passport, report.

Required states: loading, API error/retry, no source selected, missing data, playback, selected-source highlight. Use accessible labels, keyboard navigation, responsive layout, and clear units. Avoid controls that do nothing.

Visual style: polished mission-control/scientific visualization, dark background if desired, restrained accent colors, readable charts, clear provenance. Avoid decorative visuals that could be mistaken for telescope imagery.

---

## 9. Full 24-hour workflow

### Strategy

One developer with AI assistants and open-source tools. Build the end-to-end story first; the goal is a credible demo, not a production archive platform. Do not spend the first half on deep learning, full-archive ingestion, or architecture perfection.

### Phase 0 — Setup (Hour 0–1)

1. Create Git repo, README, `.gitignore`, and a license if appropriate.
2. Scaffold Next.js + TypeScript + Tailwind.
3. Create FastAPI backend.
4. Verify frontend-to-backend communication.
5. Add `.env.example`; never commit `.env`.
6. Make AI coding assistants read this file.
7. Add Docker Compose only if it does not delay a working local run.

Example commands:

```bash
# Frontend
npx create-next-app@latest frontend --typescript --tailwind

# Backend
mkdir backend
cd backend
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install fastapi uvicorn numpy pandas scipy scikit-learn pydantic
pip freeze > requirements.txt
```

Adapt to the existing repository; do not create duplicate nested folders.

Files: `README.md`, `PROJECT_SPEC.md`, `.gitignore`, `.env.example`, `backend/requirements.txt`, optional `docker-compose.yml`, optional `.github/workflows/ci.yml`.

### Phase 1 — Core discovery story (Hours 1–8)

**Goal:** complete working demo, even if synthetic.

#### 1.1 Data generator (1–1.5 h)
File: `backend/data_generator.py`.
- One synthetic region, four epochs, three designed behaviors, 10–20 background sources per epoch.
- Flux errors, position uncertainty, quality flags, one low-quality source.
- JSON-serializable, deterministic output.
- Stable IDs and provenance at region/source level.

Checks: same seed gives same data; timestamps ordered; missing values represented; frontend can load it.

#### 1.2 Anomaly engine (2–2.5 h)
File: `backend/anomaly_engine.py`.
- Implement motion, photometry, spectral, temporal, and optional context components.
- Normalize components and combine with configurable weights.
- Produce separate interestingness and evidence-confidence assessments.
- Generate evidence-linked structured explanations.
- Start with robust statistics/MAD; do not start with a neural network.

Checks: each designed candidate ranks high in its intended dimension; low-quality source gets a caution; missing data never silently becomes zero/normal; outputs are finite and within documented ranges; results are deterministic.

#### 1.3 Passport generator (about 1 h)
File: `backend/discovery_passport.py`.
- Pydantic schema and JSON serialization.
- Include identity, provenance, epochs, motion, photometry, spectrum, quality, false-alarm checks, catalog status, component scores, algorithm version, interestingness, confidence, priority, limitations, timestamp, follow-up suggestions.

Checks: schema validates, synthetic provenance present, no invented catalog results.

#### 1.4 FastAPI backend (about 1 h)
File: `backend/main.py`.
Implement health, regions, region detail, epochs, source detail, analysis, discoveries, and passport endpoints. Load demo data predictably, validate IDs, provide useful errors, and configure local CORS. Keep real-data integration separate.

#### 1.5 Frontend Sky Explorer + Time Machine (about 2 h)
Build:
- `app/page.tsx`, `layout.tsx`, `globals.css`
- `components/SkyExplorer.tsx`, `Timeline.tsx`, `CandidateDetail.tsx`
- `hooks/useRegionData.ts`, `useAnalysis.ts`
- `lib/api.ts`

Use Canvas/SVG map, clickable sources, hover details, four-epoch timeline, play/pause, selected candidate, scores, explanation, and basic plots if possible. Fetch from backend rather than duplicate data in frontend. Add loading/error states and a persistent synthetic-data warning.

**Phase 1 exit gate:** A user can load the demo, play epochs, select a candidate, inspect analysis, and open its passport. Do not proceed to optional ML or real archive work until this works.

### Phase 2 — Polish and enhancements (Hours 8–16)

#### 2.1 UI polish (about 3 h)
Improve source selection, map, plots, candidate ranking/filters, responsive layout, keyboard navigation/ARIA, quality/provenance indicators, error states, and restrained animations. Add `SpectraViewer.tsx`, `LightCurve.tsx`, `ReportModal.tsx`, `ErrorBoundary.tsx` as needed.

#### 2.2 Classical ML (1–2 h; optional)
Recommended: remain statistical unless ML adds demonstrable value. Optional Isolation Forest for contextual outliers if enough representative samples exist. Optional autoencoder only if there is time to evaluate it; a model trained on a tiny synthetic dataset is not scientifically validated.

Illustrative skeleton:

```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class ContextOutlierModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IsolationForest(contamination=0.1, random_state=42)

    def fit(self, features):
        self.model.fit(self.scaler.fit_transform(features))

    def predict(self, features):
        return self.model.predict(self.scaler.transform(features))
```

`contamination=0.1` is a configurable demo assumption, not the true anomaly rate of the sky.

#### 2.3 Lite real IRSA integration (2–3 h; optional bonus)
File: `backend/irsa_client.py`.
1. Verify current official docs and product availability.
2. Select one small product/region.
3. Implement one narrow query/download.
4. Parse actual schema/units.
5. Cache locally.
6. Preserve product ID, release, source URL, retrieval time, provenance.
7. Handle timeouts/API failures and fall back to synthetic mode.

Do not assume a generic Astroquery catalog name or `spherex_qr3` endpoint works without verification; that name/query in the supplied workflow was illustrative pseudocode, not a guaranteed endpoint. Failure of real data must not break demo mode.

#### 2.4 Docker/deployment (1–2 h)
Do this after local end-to-end works.

Example Compose shape (adapt as needed):

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      PYTHONUNBUFFERED: "1"
    volumes:
      - ./backend:/app
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: "http://localhost:8000"
```

Do not assume browser-side `localhost` points to a deployed backend. Set production API URLs correctly and never put secrets in `NEXT_PUBLIC_*`. Potential hosts include Vercel for frontend and Render/Railway or equivalent backend; verify current limits before choosing.

#### 2.5 Tests (1–1.5 h)
Backend: pytest tests for deterministic data, coordinate math, component scoring, missing data, quality flags, score normalization, passport, API errors. Frontend: test rendering, selection, epoch updates, provenance label, loading/error states.

Example test intent:
```python
def test_motion_candidate_is_flagged():
    # Create deterministic candidate with known motion.
    # Run actual anomaly engine and assert the motion component crosses
    # a documented test threshold.
    ...

def test_missing_quality_metadata_is_unknown():
    # Required metadata are absent; status must be UNKNOWN/NOT EVALUATED.
    ...
```

Test behavior, not arbitrary sample scores such as exactly `91`, unless the formula guarantees that value.

#### 2.6 Documentation (about 1 h)
Complete `README.md`, `ARCHITECTURE.md`, `DEVELOPMENT.md`, `ALGORITHM.md`, `API.md`, `DEPLOYMENT.md`, `DEMO.md`.

### Phase 3 — Advanced features (Hours 16–20; only if stable)

Pick at most one or two:
- **Evidence graph (2–3 h):** actual catalog matches only, with query status/separation/limits.
- **Natural-language search (~2 h):** LLM to validated filters; deterministic fallback; no arbitrary SQL.
- **Report generation (1–2 h):** HTML first, PDF with ReportLab if time.
- **Spectral visualizations (1–2 h):** error bars, epoch overlays, difference spectra, missing-band handling.
- **Autoencoder (2–3 h):** only with evaluation and baseline comparison.
- **Real-time ingestion:** last priority; only with verified update mechanism. Do not call periodic polling “real-time streaming.”

### Phase 4 — Final demo and presentation (Hours 20–24)

Reserve final time for rehearsal, slides, and fixes. Cut optional features instead of sacrificing demo reliability.

**10–15 minute demo:**
1. Landing page and challenge fit (30 sec).
2. Open synthetic region and show four epochs (1 min).
3. Play Sky Time Machine and pause on change (1–1.5 min).
4. Select candidate; show component scores and confidence (1 min).
5. Explain evidence for motion/brightness/spectral change (2 min).
6. Show quality/false-alarm checks and caveats (1 min).
7. Show actual catalog result or clearly say “not checked” (1 min).
8. Open Discovery Passport (1 min).
9. Generate report (30 sec).
10. Explain impact and future work (1 min).

**5–10 slide deck:**
1. Title/tagline.
2. Problem.
3. Challenge alignment/users.
4. Solution workflow.
5. Demo screenshots.
6. Architecture/data flow.
7. Explainable scoring and false-alarm investigation.
8. Provenance/scientific limitations.
9. Differentiation and impact.
10. Future work.

Key messaging:
> “SKYTRACE AI helps humans explore, compare, and investigate changes in SPHEREx observations. Rather than presenting a black-box claim of discovery, it exposes the measurements, quality checks, alternative explanations, and uncertainty behind every flagged candidate.”

### Time budget summary

| Task | Approx. time | Priority |
|---|---:|---|
| Setup | 1 h | MUST |
| Data generator | 1–1.5 h | MUST |
| Anomaly engine + tests | 2–2.5 h | MUST |
| Passport | 1 h | MUST |
| FastAPI | 1 h | MUST |
| Sky Explorer + timeline + detail | 2 h | MUST |
| UI polish/plots/ranking | 3 h | SHOULD |
| Classical ML | 1–2 h | NICE |
| Lite IRSA integration | 2–3 h | NICE |
| Docker/deploy | 1–2 h | SHOULD |
| Tests/docs | 1–1.5 h | SHOULD |
| Optional advanced features | 2–4 h total | NICE |
| Rehearsal/slides/fixes | 2–4 h | MUST |

These estimates are planning aids, not guarantees. A solo developer should not attempt every optional feature.

---

## 10. AI coding assistant operating instructions

Any coding assistant must:

### Before coding
1. Read this entire `PROJECT_SPEC.md`.
2. Inspect the current repository before creating/replacing files.
3. If web access exists, verify official NASA Space Apps challenge requirements and official SPHEREx/IRSA docs.
4. Report what already works and what is missing.
5. Propose a small ordered plan and first vertical slice.
6. Identify assumptions needing verification (product schema, units, flags, endpoints, deployment).
7. Do not begin with optional features.

### While coding
- Work in small, testable increments.
- Prefer simple maintainable code over speculative abstractions.
- Preserve working code; explain before major rewrites.
- Use real data only with verified provenance/schema.
- Keep deterministic synthetic fallback.
- Add tests with core modules and run tests/build after meaningful changes.
- Keep API contracts explicit.
- Use `.env.example`; never commit secrets.
- Never claim a test, deployment, data query, or scientific validation succeeded unless actually verified.
- Do not download/commit huge archives.
- Do not create controls that do nothing.

### Scientific correctness
- Never call synthetic sources real detections.
- Never claim Planet X or extraterrestrial life was discovered.
- Never present an uncalibrated score as a probability.
- Never say “not a known object” based only on a limited no-match result.
- Never invent measurements, quality flags, catalog matches, or citations.
- State when a check cannot be performed.
- Keep algorithm version and provenance with each result.

### Scope cuts if behind schedule
Cut in this order:
1. Real-time ingestion.
2. Neural network/autoencoder.
3. Natural-language search.
4. Cross-mission graph.
5. Real-data integration beyond one verified sample.
6. PDF report (keep HTML/structured passport).

Do **not** cut the working demo, Sky Explorer, epoch comparison, candidate selection, transparent scoring, false-alarm panel, provenance labels, passport, documentation, or rehearsal.

### Expected first response from the assistant
Before modifying code, summarize the project, inspect repository state, list verified official challenge/data facts and links if available, propose MVP steps, identify files to change, and list blockers/unverified assumptions. Then proceed incrementally if implementation is requested.

---

## 11. Git, licensing, and data management

- Use Git from the start.
- `.gitignore` should exclude `.env`, virtual environments, `__pycache__/`, `*.pyc`, `node_modules/`, `.next/`, build output, local databases, logs, OS metadata, caches, and large downloaded products.
- Commit `.env.example`, never real `.env`.
- Choose a license only after deciding how the code will be shared. MIT is a common permissive option, but the team must agree and ensure third-party code/assets are compatible.
- Check terms/attribution for NASA data, logos, screenshots, external catalogs, fonts, icons, and assets separately.
- Do not commit large SPHEREx archives. Use `data/README.md` for official sources, retrieval instructions, expected schema, and cache location.
- Test README instructions from a clean clone.

---

## 12. Test checklist

**Data**
- [ ] Deterministic synthetic generator.
- [ ] Provenance at region/source level.
- [ ] Units explicit and timestamps ordered.
- [ ] Missing values/quality flags represented.
- [ ] Real/synthetic data never silently confused.

**Science**
- [ ] Spherical angular separation or justified approximation.
- [ ] Uncertainty used where available.
- [ ] Photometric variation accounts for flux errors.
- [ ] Spectral comparisons use compatible measurements.
- [ ] Missing components handled explicitly.
- [ ] Weighting/normalization documented.
- [ ] Interestingness and confidence separate.
- [ ] Missing quality metadata means UNKNOWN/NOT EVALUATED.
- [ ] Explanations refer to computed evidence.
- [ ] No unsupported discovery claims.

**API/UI**
- [ ] Health, region, source, analysis, and passport endpoints work.
- [ ] Invalid IDs return useful errors.
- [ ] App works offline from external services using synthetic data.
- [ ] Epoch selection/playback updates map and linked views.
- [ ] Charts include units and uncertainty when available.
- [ ] Provenance warning visible.
- [ ] Loading/error/empty states work.
- [ ] Responsive and keyboard-usable controls.

**Delivery**
- [ ] Passport validates and serializes.
- [ ] Report includes provenance, limitations, algorithm version.
- [ ] Fresh-clone setup tested.
- [ ] README and slides match implemented features.
- [ ] Demo rehearsed.
- [ ] Official submission rules followed.

---

## 13. Research extension after the hackathon

Potential research questions:
- How well do scores recover known or controlled changes?
- What are false-positive rates under simulated noise, missing epochs, and crowding?
- How does performance change with cadence and signal-to-noise?
- Does the interface improve human triage compared with a basic archive viewer?
- How does it perform on verified real SPHEREx products?
- How accurate are cross-catalog matches?
- Can confidence be calibrated against a labeled evaluation set?

A credible paper requires a clear research question, reproducible data, baselines, metrics, error analysis, and careful claims. A polished hackathon demo alone does not establish scientific validity or guarantee publication.

---

## 14. Final MVP definition

The minimum successful version contains:
1. Next.js frontend and FastAPI backend.
2. Deterministic synthetic SPHEREx-like dataset with four epochs and explicit provenance.
3. Interactive sky map and Sky Time Machine.
4. Source selection and linked candidate detail.
5. Motion, photometry, spectral, temporal, and optional context scoring.
6. Documented weighted score.
7. Evidence-linked “Why is this interesting?” explanation.
8. Data-quality/false-alarm checks with UNKNOWN states.
9. Separate interestingness and evidence-confidence assessments.
10. Scientific Discovery Passport.
11. Candidate ranking/feed.
12. Tests and documentation.
13. Rehearsed demo and slides.

Real-data integration, catalog cross-checks, reports, and deployment are valuable bonuses, but must not break the core demo.

## 15. Immediate next actions

1. Inspect the existing repository; do not overwrite working code.
2. Verify official challenge requirements and current SPHEREx/IRSA access.
3. Set up the smallest frontend/backend skeleton.
4. Build deterministic synthetic data with provenance labels.
5. Implement and test transparent anomaly scoring.
6. Define the passport schema.
7. Build API endpoints.
8. Connect Sky Explorer, Time Machine, and candidate details.
9. Demonstrate one end-to-end candidate investigation.
10. Add quality checks, plots, and report.
11. Integrate a real product only if verified and feasible.
12. Rehearse, document, and submit.

**Do not begin with a neural network, a full archive download, a complex database, or real-time streaming. Make the core discovery story work first.**
