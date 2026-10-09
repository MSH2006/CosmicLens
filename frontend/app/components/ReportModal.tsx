'use client';

import React, { useRef } from 'react';
import { ScientificDiscoveryPassport } from '../lib/types';

interface ReportModalProps {
  passport: ScientificDiscoveryPassport | null;
  isOpen: boolean;
  onClose: () => void;
}

export default function ReportModal({ passport, isOpen, onClose }: ReportModalProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  if (!isOpen || !passport) return null;

  const p = passport;
  const analysis = p.analysis;

  const checksRows = p.false_alarm_investigation.checks
    .map(
      (c) => `
      <tr>
        <td style="padding: 10px; border-bottom: 1px solid #1e3a5f; font-family: monospace;">${c.name}</td>
        <td style="padding: 10px; border-bottom: 1px solid #1e3a5f;">
          <span style="display: inline-block; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;
            background: ${c.status === 'PASS' ? '#064e3b; color: #34d399' : c.status === 'CAUTION' ? '#78350f; color: #fbbf24' : '#881337; color: #f87171'};">
            ${c.status}
          </span>
        </td>
        <td style="padding: 10px; border-bottom: 1px solid #1e3a5f; color: #cbd5e1; font-size: 12px;">${c.details}</td>
      </tr>`
    )
    .join('');

  const htmlDoc = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SKYTRACE AI Discovery Report — ${p.source_identity.source_id}</title>
  <style>
    body { background: #020813; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 30px; line-height: 1.6; }
    .report-container { max-width: 850px; margin: 0 auto; background: #061527; border: 1px solid #1e3a8a; border-radius: 16px; padding: 35px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
    .disclaimer-banner { background: #7c2d12; color: #fed7aa; border: 1px solid #ea580c; padding: 12px 18px; border-radius: 8px; font-weight: bold; font-size: 13px; text-align: center; margin-bottom: 25px; text-transform: uppercase; }
    h1, h2, h3 { color: #7dd3fc; font-family: monospace; }
    .header-meta { display: flex; justify-content: space-between; border-bottom: 2px solid #1e3a8a; padding-bottom: 16px; margin-bottom: 24px; }
    .score-box { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 24px; }
    .card { background: #020b18; border: 1px solid #1e3a5f; border-radius: 10px; padding: 14px; }
    .card-label { font-size: 11px; color: #94a3b8; text-transform: uppercase; font-family: monospace; }
    .card-value { font-size: 24px; font-weight: bold; color: #38bdf8; font-family: monospace; margin-top: 4px; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { background: #0a1f38; color: #7dd3fc; text-align: left; padding: 10px; font-family: monospace; font-size: 12px; }
    ul { margin: 0; padding-left: 20px; color: #cbd5e1; font-size: 13px; }
    li { margin-bottom: 6px; }
    .fits-box { background: #01060e; border: 1px solid #1e3a5f; border-radius: 8px; padding: 14px; font-family: monospace; font-size: 11px; color: #38bdf8; white-space: pre-wrap; overflow-x: auto; }
    @media print {
      body { background: #fff; color: #000; padding: 0; }
      .report-container { border: none; box-shadow: none; padding: 15px; }
      .disclaimer-banner { background: #fee2e2; color: #991b1b; border-color: #ef4444; }
      h1, h2, h3 { color: #0369a1; }
      .card { background: #f8fafc; border-color: #cbd5e1; }
      .card-value { color: #0284c7; }
      th { background: #e2e8f0; color: #0f172a; }
      .fits-box { background: #f1f5f9; color: #0f172a; }
    }
  </style>
</head>
<body>
  <div class="report-container">
    <div class="disclaimer-banner">⚠ ${p.disclaimer}</div>
    <div class="header-meta">
      <div>
        <h1 style="margin: 0;">SKYTRACE AI — Discovery Report</h1>
        <div style="font-family: monospace; color: #94a3b8; font-size: 13px; margin-top: 4px;">
          Candidate: <strong>${p.source_identity.source_id}</strong> (${p.source_identity.iau_designation || 'SPHEREx Source'})
        </div>
        <div style="font-family: monospace; color: #64748b; font-size: 12px;">ID: ${p.passport_id} | ${analysis.algorithm_version}</div>
      </div>
      <div style="text-align: right; font-family: monospace; font-size: 12px; color: #94a3b8;">
        <div>Field: ${p.source_identity.region_name || 'Survey Field'}</div>
        <div>Observation Span: ${p.source_identity.observation_span}</div>
        <div>Date: ${p.generated_at}</div>
      </div>
    </div>

    <div class="score-box">
      <div class="card">
        <div class="card-label">Scientific Interestingness</div>
        <div class="card-value" style="color: #fbbf24;">${analysis.interestingness_score.toFixed(1)} / 100</div>
      </div>
      <div class="card">
        <div class="card-label">Evidence Confidence</div>
        <div class="card-value">${analysis.evidence_confidence.numeric_value.toFixed(0)}%</div>
        <div style="font-size: 11px; color: #34d399; margin-top: 2px;">Tier: ${analysis.evidence_confidence.tier}</div>
      </div>
      <div class="card">
        <div class="card-label">Scientific Priority</div>
        <div class="card-value">${analysis.scientific_priority}</div>
      </div>
    </div>

    <div class="card" style="margin-bottom: 20px;">
      <h3>Astrophysical Summary & Evidence</h3>
      <p style="color: #cbd5e1; font-size: 13px; margin: 0 0 10px 0;">
        ${p.position_and_motion.assessment} ${p.photometry.assessment}
      </p>
      <ul>
        ${analysis.why_interesting.map((r) => `<li>${r}</li>`).join('')}
      </ul>
    </div>

    <div class="card" style="margin-bottom: 20px;">
      <h3>False-Alarm & Data Quality Checks</h3>
      <p style="font-size: 12px; color: #94a3b8; margin: 0 0 10px 0;">Assessment: <strong>${p.false_alarm_investigation.assessment}</strong></p>
      <table>
        <thead>
          <tr><th>Check</th><th>Status</th><th>Findings</th></tr>
        </thead>
        <tbody>
          ${checksRows}
        </tbody>
      </table>
    </div>

    <div class="card" style="margin-bottom: 20px;">
      <h3>Known-Object Catalog Cross-Check</h3>
      <p style="font-size: 12px; color: #94a3b8; margin: 0 0 8px 0;">
        Status: <strong>${p.known_object_cross_check.status}</strong> (Radius: ${p.known_object_cross_check.search_radius_arcsec.toFixed(1)}")
      </p>
      <p style="font-size: 11px; color: #94a3b8; font-style: italic; margin: 0;">
        ${p.known_object_cross_check.limitations}
      </p>
    </div>

    <div class="card" style="margin-bottom: 20px;">
      <h3>Follow-Up Suggestions</h3>
      <ul>
        ${p.follow_up_suggestions.map((s) => `<li>${s}</li>`).join('')}
      </ul>
    </div>

    <div class="card" style="margin-bottom: 20px;">
      <h3>Mandatory Scientific Limitations</h3>
      <ul>
        ${p.limitations.map((l) => `<li>${l}</li>`).join('')}
      </ul>
    </div>

    ${
      p.fits_header_card
        ? `<div class="card"><h3>Standard 80-Column FITS Header Card</h3><div class="fits-box">${p.fits_header_card}</div></div>`
        : ''
    }

    <div style="text-align: center; margin-top: 25px; font-size: 11px; color: #64748b; font-family: monospace;">
      NASA Space Apps Challenge 2026 — Planet X and SPHEREx | SKYTRACE AI
    </div>
  </div>
</body>
</html>`;

  const handlePrint = () => {
    if (iframeRef.current && iframeRef.current.contentWindow) {
      iframeRef.current.contentWindow.print();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-4xl h-[90vh] bg-[#030d17] border border-cyan-500/40 rounded-3xl p-6 shadow-2xl flex flex-col gap-4">
        {/* Modal Top Bar */}
        <div className="flex items-center justify-between border-b border-cyan-500/20 pb-3">
          <div className="flex items-center gap-3">
            <span className="text-xl">📄</span>
            <div>
              <h2 className="text-base font-bold font-mono text-cyan-100">
                Scientific Discovery Report — {p.source_identity.source_id}
              </h2>
              <span className="text-xs font-mono text-cyan-400/70">
                Self-contained, evidence-linked HTML scientific report
              </span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="px-4 py-2 rounded-xl bg-cyan-500 text-black font-mono text-xs font-bold hover:bg-cyan-400 transition-all flex items-center gap-1.5 shadow-lg"
            >
              <span>🖨</span>
              <span>PRINT / SAVE TO PDF</span>
            </button>
            <button
              onClick={onClose}
              className="w-8 h-8 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/20 flex items-center justify-center text-sm font-bold"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Embedded Iframe Preview */}
        <div className="w-full flex-1 rounded-2xl overflow-hidden border border-cyan-500/20 bg-[#020813]">
          <iframe
            ref={iframeRef}
            srcDoc={htmlDoc}
            title="Discovery Report Preview"
            className="w-full h-full border-none"
          />
        </div>
      </div>
    </div>
  );
}
