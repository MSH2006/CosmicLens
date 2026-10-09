# SKYTRACE AI — Demo & Presentation Walkthrough

**10-Minute NASA Space Apps Challenge Judging Presentation Script**

---

### Step 1: Challenge Context & Landing View (Minute 0:00 - 1:00)
- **Action**: Open `http://localhost:3000`.
- **Narrative**:
  > "Welcome to SKYTRACE AI, built for the NASA Space Apps Challenge: Planet X and SPHEREx. SPHEREx will observe the entire sky in 102 infrared bands every 6 months. Rather than a black-box discovery claim, SKYTRACE AI provides an explainable discovery and prioritization engine that separates Scientific Interestingness from Evidence Confidence."
- **Point out**: The persistent guardrail banner: *SIMULATED DEMO DATA — NOT A REAL ASTRONOMICAL DISCOVERY*.

---

### Step 2: Sky Explorer & Time Machine (Minute 1:00 - 2:30)
- **Action**:
  1. Show the Serpens Demo Field.
  2. Press **▶ PLAY** on the Sky Time Machine.
  3. Watch the 4 discrete observation passes (March, May, August, October 2026).
  4. Notice candidate `DEMO-001` displacing systematically along a linear trajectory across epochs.

---

### Step 3: Candidate Inspection & Evidence Breakdown (Minute 2:30 - 4:30)
- **Action**: Click on `DEMO-001` (or select from the triage table).
- **Narrative**:
  > "We see candidate DEMO-001 flagged with high Scientific Interestingness (82/100) and High Evidence Confidence (92%). The Astrometric Proper Motion detector records 1.40 arcsec of total displacement, with 92% linear orbital consistency."
- **Show**: The Photometric Light Curve with error bars, and the continuous 102-band SPHEREx infrared spectrum.

---

### Step 4: False-Alarm & Quality Investigation (Minute 4:30 - 6:00)
- **Action**: Select candidate `DEMO-ART-99` (Cosmic Ray Artifact).
- **Narrative**:
  > "In infrared surveys, most transients are false alarms. Here, candidate DEMO-ART-99 flared to 95 μJy in epoch 2. But our False Alarm Investigator flags that its PSF FWHM is only 0.65 arcseconds—smaller than the SPHEREx optical diffraction limit of 1.8 arcseconds. The check status is FAIL, dropping confidence to 22% (LOW) and preventing false telescope alarm."

---

### Step 5: Spectral Ice Absorption (Minute 6:00 - 7:30)
- **Action**: Select candidate `DEMO-003` (Ice-Rich Protostellar Core).
- **Narrative**:
  > "Candidate DEMO-003 exhibits stationary astrometry but strong spectral deviation. Looking at the 102-channel SED, our spectral detector identifies the prominent 3.05 μm water ice and 4.27 μm carbon dioxide ice absorption troughs."

---

### Step 6: Scientific Discovery Passport & Report (Minute 7:30 - 9:00)
- **Action**:
  1. Click **VIEW PASSPORT**: show identity, discrete checks, and 80-column FITS header card.
  2. Click **GENERATE REPORT**: open the clean, printable HTML scientific report.
  3. Show the **Print / Save to PDF** capability.

---

### Step 7: Zero-Friction Extensibility & Conclusion (Minute 9:00 - 10:00)
- **Action**: Open the **CALIBRATE** modal. Show how detector weights can be tuned dynamically in real time.
- **Closing**:
  > "With our decoupled plugin registry, new detectors or machine learning models can be integrated in 15 lines of code with zero core drawbacks. SKYTRACE AI empowers human scientists to explore, understand, and validate the changing infrared sky."
