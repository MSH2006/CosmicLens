'use client';

import React from 'react';
import { Epoch, AnalysisResult } from '../lib/types';

interface LightCurveViewerProps {
  objectId: string;
  epochs: Epoch[];
  analysis: AnalysisResult | null;
  selectedEpoch: number;
}

export default function LightCurveViewer({
  objectId,
  epochs,
  analysis,
  selectedEpoch,
}: LightCurveViewerProps) {
  // Extract object observation points
  const points = epochs.map((ep, idx) => {
    const src = ep.sources.find((s) => s.id === objectId);
    return {
      epochIdx: idx,
      timestamp: ep.timestamp,
      wavelength: ep.wavelength,
      flux: src ? src.flux : null,
      fluxErr: src ? src.flux_err : 1.0,
      flag: src ? src.flag : 'none',
    };
  }).filter((p) => p.flux !== null);

  if (points.length === 0) {
    return (
      <div className="h-48 flex items-center justify-center text-xs font-mono text-cyan-400/50">
        No photometric light curve data available.
      </div>
    );
  }

  // Calculate SVG bounds
  const fluxes = points.map((p) => p.flux as number);
  const minFlux = Math.max(0, Math.min(...fluxes) * 0.75);
  const maxFlux = Math.max(...fluxes) * 1.25;
  const rangeFlux = maxFlux - minFlux || 1.0;

  const svgWidth = 460;
  const svgHeight = 170;
  const padding = { top: 20, right: 25, bottom: 30, left: 45 };
  const plotWidth = svgWidth - padding.left - padding.right;
  const plotHeight = svgHeight - padding.top - padding.bottom;

  const getX = (idx: number) => {
    if (points.length <= 1) return padding.left + plotWidth / 2;
    return padding.left + (idx / (points.length - 1)) * plotWidth;
  };

  const getY = (val: number) => {
    return padding.top + plotHeight - ((val - minFlux) / rangeFlux) * plotHeight;
  };

  const meanFlux = fluxes.reduce((a, b) => a + b, 0) / fluxes.length;
  const meanY = getY(meanFlux);

  // SVG polyline path
  const pathD = points
    .map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${getX(idx)} ${getY(p.flux as number)}`)
    .join(' ');

  const photoMetrics = analysis?.detector_results?.photometric_variability?.metrics || {};

  return (
    <div className="bg-[#050f19] border border-cyan-500/20 rounded-2xl p-4 shadow-xl">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-cyan-400" />
          <h4 className="text-xs font-mono tracking-wider uppercase text-cyan-200">
            Multi-Epoch Photometric Light Curve
          </h4>
        </div>
        <div className="flex items-center gap-2 text-[11px] font-mono text-cyan-400/80">
          <span>Baseline: {meanFlux.toFixed(1)} μJy</span>
          {photoMetrics.delta_mag && (
            <span className="px-1.5 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-300">
              Δm: {photoMetrics.delta_mag.toFixed(2)} mag
            </span>
          )}
        </div>
      </div>

      {/* SVG Photometric Plot */}
      <div className="relative w-full overflow-hidden">
        <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} className="w-full h-auto select-none">
          {/* Grid lines */}
          {[0, 0.25, 0.5, 0.75, 1.0].map((frac, i) => {
            const yVal = padding.top + plotHeight * frac;
            const fluxLabel = maxFlux - frac * rangeFlux;
            return (
              <g key={i}>
                <line
                  x1={padding.left}
                  y1={yVal}
                  x2={svgWidth - padding.right}
                  y2={yVal}
                  stroke="#38bdf8"
                  strokeOpacity="0.1"
                  strokeDasharray="2 2"
                />
                <text
                  x={padding.left - 6}
                  y={yVal + 3}
                  textAnchor="end"
                  fill="#7dd3fc"
                  fontSize="9"
                  fontFamily="monospace"
                  opacity="0.6"
                >
                  {fluxLabel.toFixed(0)}
                </text>
              </g>
            );
          })}

          {/* Baseline Median Flux Line */}
          <line
            x1={padding.left}
            y1={meanY}
            x2={svgWidth - padding.right}
            y2={meanY}
            stroke="#f59e0b"
            strokeOpacity="0.4"
            strokeDasharray="4 4"
          />

          {/* Light curve continuous connector */}
          <path d={pathD} fill="none" stroke="#38bdf8" strokeWidth="2.5" className="drop-shadow-md" />

          {/* Error Bars and Data Points */}
          {points.map((p, idx) => {
            const cx = getX(idx);
            const cy = getY(p.flux as number);
            const errPixels = ((p.fluxErr as number) / rangeFlux) * plotHeight;
            const isCurrent = idx === selectedEpoch;

            return (
              <g key={idx}>
                {/* Vertical Error Bar */}
                <line
                  x1={cx}
                  y1={cy - errPixels}
                  x2={cx}
                  y2={cy + errPixels}
                  stroke="#38bdf8"
                  strokeWidth="1.5"
                  strokeOpacity="0.75"
                />
                <line
                  x1={cx - 3}
                  y1={cy - errPixels}
                  x2={cx + 3}
                  y2={cy - errPixels}
                  stroke="#38bdf8"
                  strokeWidth="1.5"
                  strokeOpacity="0.75"
                />
                <line
                  x1={cx - 3}
                  y1={cy + errPixels}
                  x2={cx + 3}
                  y2={cy + errPixels}
                  stroke="#38bdf8"
                  strokeWidth="1.5"
                  strokeOpacity="0.75"
                />

                {/* Point Marker */}
                <circle
                  cx={cx}
                  cy={cy}
                  r={isCurrent ? '6' : '4.5'}
                  fill={isCurrent ? '#f59e0b' : '#0284c7'}
                  stroke={isCurrent ? '#fff' : '#bae6fd'}
                  strokeWidth={isCurrent ? '2' : '1.5'}
                  className="transition-all"
                />

                {/* Epoch Date Label on X Axis */}
                <text
                  x={cx}
                  y={svgHeight - 10}
                  textAnchor="middle"
                  fill={isCurrent ? '#f59e0b' : '#7dd3fc'}
                  fontSize="9"
                  fontFamily="monospace"
                  fontWeight={isCurrent ? 'bold' : 'normal'}
                >
                  T{idx + 1}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Photometric Metrics Bar */}
      <div className="grid grid-cols-3 gap-2 mt-2 pt-2 border-t border-cyan-500/15 text-center text-xs font-mono">
        <div className="bg-black/30 p-1.5 rounded-lg border border-cyan-500/10">
          <span className="block text-[10px] text-cyan-400/70">VARIABILITY</span>
          <span className="text-cyan-200 font-bold">
            {photoMetrics.fractional_variation ? `${(photoMetrics.fractional_variation * 100).toFixed(1)}%` : '0.0%'}
          </span>
        </div>
        <div className="bg-black/30 p-1.5 rounded-lg border border-cyan-500/10">
          <span className="block text-[10px] text-cyan-400/70">REDUCED χ²</span>
          <span className="text-cyan-200 font-bold">
            {photoMetrics.reduced_chi_squared ? photoMetrics.reduced_chi_squared.toFixed(1) : '1.0'}
          </span>
        </div>
        <div className="bg-black/30 p-1.5 rounded-lg border border-cyan-500/10">
          <span className="block text-[10px] text-cyan-400/70">AMPLITUDE</span>
          <span className="text-cyan-200 font-bold">
            {photoMetrics.amplitude_ratio ? `${photoMetrics.amplitude_ratio.toFixed(1)}x` : '1.0x'}
          </span>
        </div>
      </div>
    </div>
  );
}
