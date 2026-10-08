'use client';

import { useEffect, useState } from 'react';

type Source = {
  id: string;
  ra: number;
  dec: number;
  flux: number;
  flux_err: number;
  flag: string;
  psf_fwhm: number;
  type: string;
};

type Epoch = {
  timestamp: string;
  wavelength: number;
  sources: Source[];
};

type Region = {
  id: string;
  name: string;
  description: string;
  ra_center: number;
  dec_center: number;
  epochs: Epoch[];
};

type Analysis = {
  anomaly_score: number;
  evidence_confidence: number;
  why_interesting: string[];
  motion_anomaly: { is_significant: boolean; total_motion_arcsec: number };
  photometry_anomaly: { is_variable: boolean; fractional_variation: number };
  artifacts: Array<{ type: string; probability: number }>;
};

type Passport = {
  passport_id: string;
  identity: {
    source_id: string;
    region: string;
    observation_start: string;
    observation_end: string;
    epoch_count: number;
  };
  scientific_priority: string;
  recommendations: string[];
};

export default function HomePage() {
  const [region, setRegion] = useState<Region | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [passport, setPassport] = useState<Passport | null>(null);
  const [selectedEpoch, setSelectedEpoch] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch region data
  useEffect(() => {
    const fetchRegion = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/region/region_001');
        if (!res.ok) throw new Error('Failed to fetch region');
        const data = await res.json();
        setRegion(data);
        setSelectedEpoch(0);
        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setLoading(false);
      }
    };
    fetchRegion();
  }, []);

  // Analyze candidate object
  useEffect(() => {
    if (!region) return;

    const analyzeObject = async () => {
      try {
        const res = await fetch(
          `http://localhost:8000/api/analyze/object?region_id=${region.id}&object_id=RW-001`
        );
        if (!res.ok) throw new Error('Failed to analyze object');
        const data = await res.json();
        setAnalysis(data.analysis);
        setPassport(data.passport);
      } catch (err) {
        console.error('Analysis error:', err);
      }
    };

    analyzeObject();
  }, [region]);

  // Play timeline animation
  useEffect(() => {
    if (!playing || !region) return;

    const timer = setInterval(() => {
      setSelectedEpoch((prev) => (prev + 1) % region.epochs.length);
    }, 1200);

    return () => clearInterval(timer);
  }, [playing, region]);

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-content">
          <h1>CosmicLens</h1>
          <p>Loading infrared observations...</p>
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-screen">
        <div className="error-content">
          <h1>Connection Error</h1>
          <p>{error}</p>
          <p style={{ marginTop: '1rem', color: '#9db4d1' }}>
            Make sure the backend is running on http://localhost:8000
          </p>
        </div>
      </div>
    );
  }

  if (!region || !analysis || !passport) {
    return <div className="loading-screen">Loading...</div>;
  }

  const activeEpoch = region.epochs[selectedEpoch];
  const candidate = activeEpoch.sources.find((s) => s.id === 'RW-001');

  // Calculate position relative to map
  const relativeRa = (candidate?.ra ?? region.ra_center) - region.ra_center;
  const relativeDec = (candidate?.dec ?? region.dec_center) - region.dec_center;
  const motionX = 50 + relativeRa * 400;
  const motionY = 50 - relativeDec * 400;

  const artifactProb =
    analysis.artifacts.length > 0
      ? (analysis.artifacts.reduce((sum, a) => sum + a.probability, 0) /
          analysis.artifacts.length) *
        100
      : 0;

  return (
    <main className="app-container">
      <header className="topbar">
        <div className="topbar-left">
          <p className="eyebrow">NASA SPHEREx Discovery Prototype</p>
          <h1>CosmicLens</h1>
        </div>
        <button
          className="button-play"
          onClick={() => setPlaying((prev) => !prev)}
        >
          {playing ? '⏸ Pause' : '▶ Play Sky Time Machine'}
        </button>
      </header>

      <section className="grid-layout">
        {/* Left Panel: Sky Explorer */}
        <div className="panel sky-panel">
          <div className="panel-header">
            <div>
              <h2>{region.name}</h2>
              <p className="description">{region.description}</p>
            </div>
          </div>

          {/* Sky Map */}
          <div className="sky-map">
            <div
              className="object-dot"
              style={{
                left: `${Math.min(95, Math.max(5, motionX))}%`,
                top: `${Math.min(95, Math.max(5, motionY))}%`,
              }}
              title={`RW-001 at epoch ${selectedEpoch + 1}`}
            />
          </div>

          {/* Timeline */}
          <div className="timeline-container">
            <div className="timeline">
              {region.epochs.map((epoch, idx) => (
                <button
                  key={epoch.timestamp}
                  className={`timeline-item ${idx === selectedEpoch ? 'active' : ''}`}
                  onClick={() => {
                    setPlaying(false);
                    setSelectedEpoch(idx);
                  }}
                >
                  <span className="timeline-dot" />
                  <span className="timeline-label">T{idx + 1}</span>
                  <span className="timeline-date">{epoch.timestamp}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Panel: Analysis */}
        <aside className="panel detail-panel">
          {/* Candidate Header */}
          <div className="candidate-section">
            <div className="candidate-header">
              <div>
                <p className="eyebrow">Candidate Object</p>
                <h3>RW-001</h3>
              </div>
              <div className="score-badge">
                <span className="badge-label">Science Priority</span>
                <strong className="badge-value">
                  {Math.round(analysis.anomaly_score)}
                </strong>
              </div>
            </div>

            {/* Stats Row */}
            <div className="stats-row">
              <div className="stat-item">
                <label>Confidence</label>
                <strong>{Math.round(analysis.evidence_confidence)}%</strong>
              </div>
              <div className="stat-item">
                <label>Artifact Risk</label>
                <strong
                  style={{
                    color:
                      artifactProb < 20
                        ? '#7ce8b4'
                        : artifactProb < 50
                          ? '#ffce73'
                          : '#ff8d8d',
                  }}
                >
                  {artifactProb < 20 ? 'LOW' : artifactProb < 50 ? 'MED' : 'HIGH'}
                </strong>
              </div>
            </div>
          </div>

          {/* Why Interesting */}
          <div className="info-box">
            <h4>Why is this interesting?</h4>
            <ul className="reasons-list">
              {analysis.why_interesting.map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          </div>

          {/* Motion & Photometry */}
          <div className="info-box">
            <h4>Observations</h4>
            {analysis.motion_anomaly.is_significant && (
              <p className="observation">
                <strong>Motion:</strong> {analysis.motion_anomaly.total_motion_arcsec.toFixed(2)}
                {' arcsec'}
              </p>
            )}
            {analysis.photometry_anomaly.is_variable && (
              <p className="observation">
                <strong>Variability:</strong> {(analysis.photometry_anomaly.fractional_variation * 100).toFixed(1)}%
              </p>
            )}
            <p className="observation">
              <strong>Wavelength:</strong> {activeEpoch.wavelength.toFixed(1)} μm
            </p>
          </div>

          {/* Scientific Passport */}
          <div className="info-box passport-box">
            <h4>Scientific Passport</h4>
            <p className="passport-id">{passport.passport_id}</p>
            <p className="passport-detail">
              <strong>Priority:</strong> {passport.scientific_priority}
            </p>
            <p className="passport-detail">
              <strong>Observation span:</strong> {passport.identity.epoch_count} epochs
            </p>
            <p className="passport-detail" style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
              {passport.recommendations[0]}
            </p>
          </div>
        </aside>
      </section>
    </main>
  );
}
