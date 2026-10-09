# SKYTRACE AI — Scientific Algorithms & Scoring Method

## 1. Astrometric Proper Motion
Angular displacement between epochs on the celestial sphere, accounting for declination curvature:
$$\Delta \theta = \sqrt{(\Delta \alpha \cos \bar{\delta})^2 + (\Delta \delta)^2}$$
Total displacement is tested against the combined positional uncertainty $\sigma_{\text{pos}}$.

Trajectory linearity is evaluated from the variance of step direction vectors to distinguish smooth Keplerian tracks from astrometric jitter.

## 2. Photometric Variability
Tested against the null hypothesis of constant flux using reduced chi-squared:
$$\chi^2_\nu = \frac{1}{N - 1} \sum_{i=1}^N \frac{(F_i - \bar{F})^2}{\sigma_{F_i}^2}$$
Fractional variability amplitude:
$$\frac{\sigma_F}{\bar{F}} = \frac{\sqrt{\frac{1}{N}\sum (F_i - \bar{F})^2}}{\bar{F}}$$

## 3. Infrared Spectral Energy Distribution (SED)
SPHEREx observes in 102 contiguous spectral bands from 0.75 to 5.0 micrometers.
- Infrared color index: $[-2.5 \log_{10}(F_{\lambda_2} / F_{\lambda_1})]$
- Water Ice ($H_2O$) absorption trough: evaluated at $3.05\,\mu\text{m}$ ($FWHM \approx 0.35\,\mu\text{m}$)
- Carbon Dioxide Ice ($CO_2$) absorption trough: evaluated at $4.27\,\mu\text{m}$ ($FWHM \approx 0.15\,\mu\text{m}$)

## 4. Contextual Field Outliers
Robust departure from local reference stars:
$$\text{Robust } z = \frac{|F - \text{median}(F_{\text{field}})|}{1.4826 \times \text{MAD}(F_{\text{field}})}$$

## 5. False-Alarm Vetting & PSF Diffraction Limit
The optical diffraction limit for SPHEREx near-infrared optics is $\text{FWHM} \approx 1.8''$.
- Direct cosmic ray hits deposit charge into silicon pixels, producing sharp sub-diffraction profiles ($\text{FWHM} < 1.0''$).
- Sources with $\text{FWHM} < 0.6 \times \text{diffraction limit}$ are flagged with state `FAIL` for cosmic ray contamination.

## 6. Composite Interestingness Score
$$S_{\text{composite}} = \sum_{i} w_i \times S_i \quad \text{where } \sum w_i = 1.0$$
Standard baseline weights: Motion (30%), Photometry (25%), Spectral (20%), Temporal (15%), Context (10%).
