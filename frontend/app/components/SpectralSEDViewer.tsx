'use client';

import React, { useState } from 'react';
import { SEDPoint } from '../lib/types';

interface SpectralSEDViewerProps {
  sedProfile: SEDPoint[];
}

export default function SpectralSEDViewer({ sedProfile }: SpectralSEDViewerProps) {
  const [hoveredPoint, setHoveredPoint] = useState<SEDPoint | null>(null);

  if (!sedProfile || sedProfile.length === 0) {
    return (
      <div className="h-44 flex items-center justify-center text-xs font-mono text-cyan-400/50">
        No SPHEREx 102-channel SED spectrum available.
      </div>
    );
  }

  const fluxes = sedProfile.map((p) => p.flux_ujy);
  const minFlux = Math.max(0, Math.min(...fluxes) * 0.7);
  const maxFlux = Math.max(...fluxes) * 1.25;
  const rangeFlux = maxFlux - minFlux || 1.0;

  const minWl = 0.75;
  const maxWl = 5.0;
  const rangeWl = maxWl - minWl;

  const svgWidth = 460;
  const svgHeight = 170;
  const padding = { top: 22, right: 25, bottom: 30, left: 45 };
  const plotWidth = svgWidth - padding.left - padding.right;
  const plotHeight = svgHeight - padding.top - padding.bottom;

  const getX = (wl: number) => {
    return padding.left + ((wl - minWl) / rangeWl) * plotWidth;
  };

  const getY = (val: number) => {
    return padding.top + plotHeight - ((val - minFlux) / rangeFlux) * plotHeight;
  };

  const pathD = sedProfile
    .map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${getX(p.wavelength_um)} ${getY(p.flux_ujy)}`)
    .join(' ');

  // Area under curve fill
  const areaD = `${pathD} L ${getX(sedProfile[sedProfile.length - 1].wavelength_um)} ${padding.top + plotHeight} L ${getX(sedProfile[0].wavelength_um)} ${padding.top + plotHeight} Z`;

  // Molecular Ice Feature Markers
  const iceFeatures = sedProfile.filter((p) => p.spectral_feature);

  return (
    <div className="bg-[#050f19] border border-cyan-500/20 rounded-2xl p-4 shadow-xl">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-teal-400" />
          <h4 className="text-xs font-mono tracking-wider uppercase text-cyan-200">
            SPHEREx 102-Band Infrared Spectrum (0.75 - 5.0 μm)
          </h4>
        </div>
        <div className="text-[11px] font-mono text-cyan-400/80">
          {hoveredPoint ? (
            <span className="text-amber-300 font-bold">
              λ: {hoveredPoint.wavelength_um.toFixed(2)} μm | F: {hoveredPoint.flux_ujy.toFixed(1)} μJy
            </span>
          ) : (
            <span>Resolving Power R ≈ 35 - 130</span>
          )}
        </div>
      </div>

      {/* SVG Spectrum Plot */}
      <div className="relative w-full overflow-hidden">
        <svg
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          className="w-full h-auto select-none"
          onMouseLeave={() => setHoveredPoint(null)}
        >
          <defs>
            <linearGradient id="spectrumGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#2dd4bf" stopOpacity="0.35" />
              <stop offset="100%" stopColor="#0f766e" stopOpacity="0.02" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          {[1.0, 2.0, 3.0, 4.0, 5.0].map((wl) => {
            const xVal = getX(wl);
            return (
              <g key={wl}>
                <line
                  x1={xVal}
                  y1={padding.top}
                  x2={xVal}
                  y2={padding.top + plotHeight}
                  stroke="#38bdf8"
                  strokeOpacity="0.1"
                  strokeDasharray="2 2"
                />
                <text
                  x={xVal}
                  y={svgHeight - 12}
                  textAnchor="middle"
                  fill="#7dd3fc"
                  fontSize="9"
                  fontFamily="monospace"
                  opacity="0.6"
                >
                  {wl} μm
                </text>
              </g>
            );
          })}

          {/* Shaded Area */}
          <path d={areaD} fill="url(#spectrumGradient)" />

          {/* 3.05 um H2O Ice Absorption Highlight Zone */}
          <rect
            x={getX(2.85)}
            y={padding.top}
            width={getX(3.35) - getX(2.85)}
            height={plotHeight}
            fill="#38bdf8"
            fillOpacity="0.08"
          />

          {/* 4.27 um CO2 Ice Absorption Highlight Zone */}
          <rect
            x={getX(4.15)}
            y={padding.top}
            width={getX(4.40) - getX(4.15)}
            height={plotHeight}
            fill="#f59e0b"
            fillOpacity="0.08"
          />

          {/* Spectral Line */}
          <path d={pathD} fill="none" stroke="#2dd4bf" strokeWidth="2.2" />

          {/* Feature Markers */}
          {iceFeatures.map((feat, idx) => {
            const fx = getX(feat.wavelength_um);
            const fy = getY(feat.flux_ujy);
            return (
              <g key={idx}>
                <line x1={fx} y1={padding.top} x2={fx} y2={fy} stroke="#f59e0b" strokeWidth="1" strokeDasharray="2 2" />
                <circle cx={fx} cy={fy} r="4" fill="#f59e0b" stroke="#fff" strokeWidth="1" />
                <text
                  x={fx}
                  y={padding.top - 5}
                  textAnchor="middle"
                  fill="#fcd34d"
                  fontSize="8"
                  fontFamily="monospace"
                  fontWeight="bold"
                >
                  {feat.wavelength_um > 4.0 ? 'CO2 Ice' : 'H2O Ice'}
                </text>
              </g>
            );
          })}

          {/* Interactive Mouse Hover Overlay Points */}
          {sedProfile.map((pt, idx) => (
            <circle
              key={idx}
              cx={getX(pt.wavelength_um)}
              cy={getY(pt.flux_ujy)}
              r="7"
              fill="transparent"
              className="cursor-pointer"
              onMouseEnter={() => setHoveredPoint(pt)}
            />
          ))}

          {/* Active Hover Marker */}
          {hoveredPoint && (
            <g>
              <line
                x1={getX(hoveredPoint.wavelength_um)}
                y1={padding.top}
                x2={getX(hoveredPoint.wavelength_um)}
                y2={padding.top + plotHeight}
                stroke="#fff"
                strokeWidth="1"
                strokeOpacity="0.4"
              />
              <circle
                cx={getX(hoveredPoint.wavelength_um)}
                cy={getY(hoveredPoint.flux_ujy)}
                r="5"
                fill="#38bdf8"
                stroke="#fff"
                strokeWidth="2"
              />
            </g>
          )}
        </svg>
      </div>

      {/* Detected Molecular Signatures Legend */}
      <div className="flex flex-wrap items-center gap-2 mt-2 pt-2 border-t border-cyan-500/15 text-[11px] font-mono">
        <span className="text-cyan-400/70">LABELED BANDS:</span>
        <span className="px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30 text-cyan-300">
          3.05 μm H₂O Ice Libration
        </span>
        <span className="px-2 py-0.5 rounded bg-amber-950/60 border border-amber-500/30 text-amber-300">
          4.27 μm CO₂ Ice Stretch
        </span>
        <span className="px-2 py-0.5 rounded bg-purple-950/60 border border-purple-500/30 text-purple-300">
          3.3 μm PAH Emission
        </span>
      </div>
    </div>
  );
}
