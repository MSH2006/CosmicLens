/**
 * Canonical TypeScript type definitions for SKYTRACE AI / CosmicLens
 * Aligned with NASA Space Apps Challenge 2026 specification.
 */

export const DISCLAIMER_TEXT = "SIMULATED DEMO DATA — NOT A REAL ASTRONOMICAL DISCOVERY";
export const ALGORITHM_VERSION = "v1.0.0-robust";

export interface SourceObservation {
  id: string;
  ra: number;
  dec: number;
  position_uncertainty_arcsec?: number;
  flux: number;
  flux_err: number;
  flag: string;
  psf_fwhm: number;
  band?: string;
  type?: string;
}

export interface Epoch {
  epoch_id?: string;
  timestamp: string;
  jd: number;
  wavelength: number;
  sources: SourceObservation[];
  background_median?: number;
  background_rms?: number;
}

export interface Region {
  id: string;
  name: string;
  data_provenance?: string;
  disclaimer?: string;
  ra_center: number;
  dec_center: number;
  fov_arcmin: number;
  description: string;
  epochs: Epoch[];
}

export interface DetectorResult {
  detector_id: string;
  dimension: string;
  score: number;
  is_significant: boolean;
  metrics: Record<string, any>;
  description: string;
}

export interface QualityCheckItem {
  name: string;
  status: 'PASS' | 'CAUTION' | 'FAIL' | 'UNKNOWN' | 'NOT EVALUATED';
  details: string;
}

export interface CatalogCheckResult {
  status: 'MATCH FOUND' | 'NO MATCH FOUND IN QUERIED CATALOGS' | 'NOT CHECKED';
  catalogs_checked: string[];
  search_radius_arcsec: number;
  matches: Array<Record<string, any>>;
  limitations: string;
}

export interface EvidenceConfidence {
  tier: 'LOW' | 'MODERATE' | 'HIGH' | 'INSUFFICIENT DATA';
  numeric_value: number;
  reasons: string[];
}

export interface ClassificationHypothesis {
  category: string;
  label: string;
  probability: number;
  rationale: string;
}

export interface SEDPoint {
  wavelength_um: number;
  flux_ujy: number;
  flux_err_ujy: number;
  band_id: number;
  spectral_feature?: string | null;
}

export interface FalseAlarmInvestigation {
  checks: QualityCheckItem[];
  possible_alternatives: string[];
  assessment: string;
}

export interface DataQualitySummary {
  available_flags: string[];
  missing_metadata: string[];
  assessment: string;
}

export interface PositionAndMotion {
  trajectory: Array<Record<string, any>>;
  total_motion_arcsec: number;
  apparent_speed_arcsec_yr: number;
  trajectory_linearity: number;
  assessment: string;
}

export interface PhotometrySummary {
  measurements: Array<Record<string, any>>;
  fractional_variability: number;
  reduced_chi_squared: number;
  delta_magnitude: number;
  assessment: string;
}

export interface SpectralFingerprint {
  wavelength_um: number[];
  flux: number[];
  uncertainty: number[];
  spectral_changes: string[];
  assessment: string;
}

export interface ScientificDiscoveryPassport {
  passport_id: string;
  data_provenance: string;
  disclaimer: string;
  source_identity: {
    source_id: string;
    iau_designation?: string;
    region_id?: string;
    region_name?: string;
    observation_span: string;
    usable_epoch_count: number;
    ra_mean_deg?: number;
    dec_mean_deg?: number;
  };
  position_and_motion: PositionAndMotion;
  photometry: PhotometrySummary;
  spectral_fingerprint: SpectralFingerprint;
  data_quality: DataQualitySummary;
  false_alarm_investigation: FalseAlarmInvestigation;
  known_object_cross_check: CatalogCheckResult;
  analysis: {
    algorithm_version: string;
    component_scores: Record<string, number>;
    interestingness_score: number;
    evidence_confidence: EvidenceConfidence;
    scientific_priority: string;
    why_interesting: string[];
  };
  follow_up_suggestions: string[];
  generated_at: string;
  limitations: string[];
  fits_header_card?: string;
}

export interface AnalysisResult {
  object_id: string;
  data_provenance: string;
  disclaimer: string;
  algorithm_version: string;
  interestingness_score: number;
  evidence_confidence: EvidenceConfidence;
  scientific_priority: 'HIGH' | 'MODERATE' | 'LOW' | 'UNASSESSED';
  primary_classification: ClassificationHypothesis;
  classification_breakdown: ClassificationHypothesis[];
  dimensional_scores: Record<string, number>;
  detector_results: Record<string, DetectorResult>;
  quality_checks: QualityCheckItem[];
  false_alarm_investigation: FalseAlarmInvestigation;
  known_object_cross_check: CatalogCheckResult;
  why_interesting: string[];
  astrophysical_narrative: string;
  sed_profile: SEDPoint[];
  follow_up_suggestions: string[];
  limitations: string[];
}

export interface DiscoverySummary {
  object_id: string;
  data_provenance: string;
  ra_mean: number;
  dec_mean: number;
  interestingness_score: number;
  evidence_confidence_tier: string;
  evidence_confidence_numeric: number;
  scientific_priority: string;
  primary_classification: string;
  dominant_dimension: string;
  why_interesting_summary: string;
  motion_arcsec: number;
  flux_variability_pct: number;
  usable_epoch_count: number;
  quality_caveat: string;
  classification_category?: string;
}
