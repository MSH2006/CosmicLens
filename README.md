# CosmicLens: Explainable AI for Discovering and Understanding Change in the Infrared Sky

[![NASA Space Apps Challenge](https://img.shields.io/badge/NASA%20Space%20Apps-Challenge%20Submission-0B3D91?style=for-the-badge&logo=nasa)](https://www.spaceappschallenge.org/)
[![Mission](https://img.shields.io/badge/Mission-SPHEREx%20%7C%20JWST%20%7C%20NEOWISE-0ea5e9?style=for-the-badge)](https://spherex.caltech.edu/)
[![Status](https://img.shields.io/badge/Status-Submission%20Ready%20%7C%20Full%20Production-10b981?style=for-the-badge)]()

**CosmicLens** is a submission-ready, production-grade Explainable AI (XAI) discovery platform designed for all-sky time-domain infrared astrophysics, specifically tailored for NASA's **SPHEREx** (Spectro-Photometer for the History of the Universe, Epoch of Reionization, and Ices Explorer) mission, alongside JWST and NEOWISE time-domain surveys.

Unlike traditional black-box machine learning approaches that output uninterpretable anomaly scores, CosmicLens pairs **multi-dimensional physical detectors** with **transparent statistical reasoning**, **false-alarm vetting against instrumental artifacts**, and **automated NASA Scientific Discovery Passports with standard FITS headers**.

---

## 🌟 Key Highlights & Architectural Strengths

### 1. Zero-Friction Extensible Detector Architecture
Built from the ground up for researchers and teams to integrate new features, new detectors, and increase accuracy effortlessly with zero pipeline friction:
- **Registry Pattern (`@register_detector`)**: Any developer or astronomer can create a new detector in a standalone file by subclassing `BaseAnomalyDetector` and applying the decorator `@register_detector`.
- **Dynamic Auto-Discovery**: The pipeline discovers, normalizes weights, and incorporates the new detector dynamically into the API, composite scoring, and UI radar visualizations without modifying any core engine code.
- **Runtime Weight & Threshold Calibration**: Astronomers and evaluators can adjust detector weights and sensitivity thresholds in real time via the UI **Calibration Studio** or REST API (`POST /api/detectors/weights`).

### 2. Multi-Dimensional Astronomical Detectors
CosmicLens evaluates celestial sources across 5 fundamental physical dimensions:
- **Astrometric Proper Motion**: Quantifies sky displacement, proper motion velocity vector ($\text{arcsec/yr}$), and linear orbital trajectory consistency ($\chi^2$) to identify Solar System moving objects (Near-Earth Asteroids, Centaurs, Trojans).
- **Photometric Flux Variability**: Computes reduced $\chi^2_\nu$ against constant flux, fractional amplitude ($\Delta F / \bar{F}$), Stetson $J$-index, and magnitude swings ($\Delta m$) to detect pulsating variables (Mira, Cepheids) and accretion flares.
- **Infrared Spectral & SED Analysis**: Analyzes infrared color indices ($[1.1] - [2.5]\,\mu m$), spectral slope $\beta$, and extracts molecular ice absorption signatures (specifically $3.05\,\mu m$ $\text{H}_2\text{O}$ ice and $4.27\,\mu m$ $\text{CO}_2$ ice absorption troughs) across 102 continuous SPHEREx spectrophotometric bands ($0.75 - 5.0\,\mu m$).
- **Temporal Dynamics**: Evaluates flux time derivatives ($dF/dt$), light curve morphology, and rise/decay asymmetry to isolate explosive transients (supernovae, novae, tidal disruption events).
- **Contextual Field Departure**: Measures robust MAD (Median Absolute Deviation) $z$-scores against local reference field stars to filter broad survey systematics.

### 3. Vetting & False-Alarm Auditor
Infrared space telescopes produce non-astrophysical artifacts such as cosmic ray charge deposits, bad pixel spikes, and diffraction spikes. CosmicLens incorporates:
- **PSF Diffraction Limit Audit**: Compares Point Spread Function FWHM against the telescope's optical diffraction limit. Sub-diffraction spikes ($< 1.0''$) are flagged as cosmic ray hits.
- **Evidence Confidence Metric**: Dynamically penalizes anomaly scores by the calculated artifact probability, preventing false alarms and prioritizing high-value telescope time.

### 4. Automated NASA Scientific Discovery Passports & FITS Cards
- Generates official IAU-style source designations (e.g. `SPHEREx J185057.6-053112`).
- Produces standard 80-character **FITS header cards** directly importable into Astropy, DS9, TOPCAT, or Aladin.
- Synthesizes actionable follow-up proposals for premier observatories (JWST NIRSpec, Roman Space Telescope, IAU Minor Planet Center).

---

## 🚀 Interactive Mission Control Dashboard

The frontend is a futuristic, responsive NASA-grade dashboard:
- **Interactive Celestial Sky Canvas**: Pan, zoom, celestial coordinates grid (RA/Dec), flux-scaled stellar halos, animated proper motion vector trails across survey passes, and click-to-select interaction on any celestial source.
- **Sky Time Machine**: Scrub between observation epochs, play/pause automated playback, and control animation speed ($0.5\times, 1.0\times, 2.0\times$).
- **Multi-Epoch Photometric Light Curve**: Interactive SVG plot with $\pm 1\sigma$ measurement error bars, baseline median reference line, and variability metrics.
- **102-Band SPHEREx Spectral SED Viewer**: Continuous infrared spectrum ($0.75 - 5.0\,\mu m$) with interactive wavelength cursor and highlighted molecular ice absorption bands.
- **5-Dimensional Radar / Spider Chart**: Visual breakdown of Astrometry, Photometry, Spectroscopy, Temporal, and Context scores.
- **Discovery Catalog & Triage Table**: Filter by candidate type (All, High Priority, Moving Asteroids, Variable Stars, Transients, Ice Cores, Artifacts), search, and sort.
- **Live Extensibility Studio**: Adjust detector weights in real time and watch candidate rankings re-calculate live.
- **Synthetic Anomaly Injector**: Inject custom moving asteroids or flaring transients into any survey field to benchmark detection capabilities.
- **Custom Survey Data Ingestion**: Upload or paste multi-epoch survey JSON datasets.

---

## 🛠️ Project Architecture

```text
CosmicLens/
├── backend/
│   ├── app/
│   │   ├── classifiers/
│   │   │   └── astrophysical_classifier.py  # Probabilistic Bayesian candidate classifier
│   │   ├── detectors/
│   │   │   ├── base.py                      # BaseAnomalyDetector ABC & DetectorRegistry
│   │   │   ├── motion_detector.py           # Astrometric proper motion & trajectory fit
│   │   │   ├── photometry_detector.py       # Reduced chi-sq & fractional flux variance
│   │   │   ├── spectral_detector.py         # 102-band SED & 3.05um/4.27um ice absorption
│   │   │   ├── temporal_detector.py         # Transient derivative & light curve dynamics
│   │   │   ├── context_detector.py          # Local stellar neighborhood MAD z-scores
│   │   │   └── artifact_vetter.py           # PSF diffraction limit & cosmic ray auditor
│   │   ├── models/
│   │   │   └── schemas.py                   # Pydantic schemas for data integrity
│   │   ├── services/
│   │   │   ├── data_service.py              # Survey field provider, ingestion, & injector
│   │   │   ├── engine.py                    # Orchestrator & explainable AI synthesizer
│   │   │   └── passport_service.py          # NASA Discovery Passport & FITS card generator
│   │   ├── anomaly_engine.py                # Backward compatibility layer
│   │   ├── data_generator.py                # Backward compatibility layer
│   │   ├── discovery_passport.py            # Backward compatibility layer
│   │   └── main.py                          # FastAPI RESTful API & OpenAPI documentation
│   ├── tests/
│   │   └── test_anomaly_pipeline.py         # Scientific unit test suite
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   ├── AnomalyInjectorModal.tsx     # Synthetic anomaly injection modal
│   │   │   ├── CalibrationStudioModal.tsx   # Live weight tuning & sensitivity sliders
│   │   │   ├── CelestialSkyCanvas.tsx       # Interactive 2D pan/zoom sky map & trails
│   │   │   ├── DataIngestModal.tsx          # Custom survey JSON ingestion modal
│   │   │   ├── DiscoveryCatalogTable.tsx    # Multi-epoch triage ranking table
│   │   │   ├── DiscoveryPassportModal.tsx   # Formal NASA Discovery Passport & FITS viewer
│   │   │   ├── LightCurveViewer.tsx         # Multi-epoch light curve with error bars
│   │   │   ├── RadarBreakdown.tsx           # 5-axis SVG radar chart & vetting meters
│   │   │   ├── SpectralSEDViewer.tsx        # 102-channel SPHEREx infrared SED viewer
│   │   │   └── TimeMachineBar.tsx           # Epoch timeline scrub bar & player
│   │   ├── lib/
│   │   │   ├── clientEngine.ts              # Standalone high-fidelity client engine
│   │   │   └── types.ts                     # TypeScript data interfaces
│   │   ├── globals.css                      # Futuristic dark-sky visual design
│   │   ├── layout.tsx
│   │   └── page.tsx                         # Mission Control master page
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── docker-compose.yml
└── README.md
```

---

## ⚡ How to Add a New Detector with Zero Drawbacks

Adding a new scientific anomaly detector or machine learning model takes under 15 lines of code:

```python
# backend/app/detectors/polarization_detector.py
from app.detectors.base import BaseAnomalyDetector, register_detector
from app.models.schemas import DetectorResult

@register_detector
class PolarizationDetector(BaseAnomalyDetector):
    @property
    def detector_id(self) -> str:
        return "infrared_polarization"

    @property
    def name(self) -> str:
        return "Dust Polarization Degree Detector"

    @property
    def dimension(self) -> str:
        return "spectral"

    @property
    def default_weight(self) -> float:
        return 0.15

    def calculate(self, epochs, context, config=None) -> DetectorResult:
        # Your custom astrophysics logic here
        pol_degree = 0.08  # Example calculation
        score = min(100.0, pol_degree * 500.0)
        return DetectorResult(
            detector_id=self.detector_id,
            dimension=self.dimension,
            score=score,
            is_significant=pol_degree > 0.05,
            metrics={"polarization_fraction": pol_degree},
            description=f"Polarization degree: {pol_degree*100:.1f}%",
        )
```
Upon file import, the detector is **automatically registered** in `DetectorRegistry`, exposed in the API, incorporated into composite score weighting, and visualized in the UI with zero code changes elsewhere!

---

## 💻 Quick Start & Running Locally

### 1. Run the Backend API

```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Interactive OpenAPI documentation will be accessible at: `http://localhost:8000/docs`

### 2. Run the Frontend Dashboard

```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

### 3. Run with Docker Compose

```bash
docker compose up --build
```

---

## 📊 Scientific Test Suite

To run the scientific test suite validating astrometric motion vectors, reduced $\chi^2$ variability tests, ice absorption detection, and artifact vetting:

```bash
cd backend
pytest tests/
```

---

## 🪐 NASA Challenge Alignment

- **Challenge**: NASA Space Apps Challenge (SPHEREx / Time-Domain Infrared Astronomy).
- **Target Science Cases**: Solar System Near-Earth Asteroids, Variable Stars (Mira, Cepheid, YSO), Infrared Transients (Supernovae, Tidal Disruption Events), Interstellar Ices ($\text{H}_2\text{O}$ and $\text{CO}_2$), and False-Alarm Artifact Vetting.
- **Mission Ready**: End-to-end operational software, no demo mockups, full FITS-compliant export.
