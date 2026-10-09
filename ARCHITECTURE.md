# SKYTRACE AI — System Architecture

## Overview

SKYTRACE AI uses a decoupled, modular architecture designed for rapid feature integration and zero-drawback extensibility.

```text
[ NASA SPHEREx Multi-Epoch Sky Data / Synthetic Simulator ]
                        ↓
             [ Fast API Backend Service ]
  ├── DetectorRegistry (Extensible @register_detector plugins)
  ├── 5D Anomaly Reasoner (Astrometry, Photometry, SED, Temporal, Context)
  ├── FalseAlarmInvestigator (PSF, SNR, flags, single-epoch dominance)
  ├── CatalogCrossCheckService (Gaia DR3 & 2MASS)
  ├── PassportService (Canonical JSON & FITS Header)
  └── ReportService (Self-contained HTML reports)
                        ↓
          [ Next.js 14 Web Mission Control ]
  ├── Interactive CelestialSkyCanvas (2D Pan/Zoom, Trajectories)
  ├── Sky Time Machine (4-epoch timeline player & scrub bar)
  ├── LightCurveViewer (SVG Photometric error bars & metrics)
  ├── SpectralSEDViewer (102-band SPHEREx 0.75-5.0 um spectrum)
  ├── RadarBreakdown (5-axis radar & quality check counts)
  ├── DiscoveryCatalogTable (Triage table & filters)
  ├── DiscoveryPassportModal (Tabs: Profile, Quality, Catalog, FITS, JSON)
  └── ReportModal (Print-to-PDF HTML report viewer)
```

## Zero-Friction Extensibility Pattern

To integrate a new detector or machine learning model without modifying the core pipeline:
1. Subclass `BaseAnomalyDetector` in `backend/app/detectors/`.
2. Decorate the class with `@register_detector`.
3. The detector is automatically registered, exposed in `/api/detectors`, integrated into composite score weighting, and visualized in the UI.
