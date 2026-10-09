'use client';

import React from 'react';
import { AnalysisResult } from '../lib/types';

interface RadarBreakdownProps {
  analysis: AnalysisResult;
}

export default function RadarBreakdown({ analysis }: RadarBreakdownProps) {
  const scores = analysis.dimensional_scores || {};
  const dimensions = [
    { key: 'motion', label: 'Astrometry', score: scores.motion || 0 },
    { key: 'photometry', label: 'Photometry', score: scores.photometry || 0 },
    { key: 'spectral', label: 'Spectroscopy', score: scores.spectral || 0 },
    { key: 'temporal', label: 'Temporal', score: scores.temporal || 0 },
    { key: 'context', label: 'Context', score: scores.context || 0 },
  ];

  const size = 180;
  const center = size / 2;
  const radius = 68;

  const getCoordinates = (value: number, index: number) => {
    const angle = (Math.PI * 2 * index) / dimensions.length - Math.PI / 2;
    const r = (value / 100) * radius;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle),
    };
  };

  const radarPolygonPoints = dimensions
    .map((d, i) => {
      const { x, y } = getCoordinates(d.score, i);
      return `${x},${y}`;
    })
    .join(' ');

  const conf = analysis.evidence_confidence;
  const failCount = analysis.quality_checks.filter((c) => c.status === 'FAIL').length;
  const cautionCount = analysis.quality_checks.filter((c) => c.status === 'CAUTION').length;

  return (
    <div className="bg-[#050f19] border border-cyan-500/20 rounded-2xl p-4 shadow-xl flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-amber-400" />
          <h4 className="text-xs font-mono tracking-wider uppercase text-cyan-200">
            5-Dimensional Anomaly Breakdown
          </h4>
        </div>
        <span className="text-[11px] font-mono text-cyan-400/80">Multi-Component Evidence</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
        {/* SVG Radar Chart */}
        <div className="flex justify-center">
          <svg width={size} height={size} className="select-none overflow-visible">
            {[0.25, 0.5, 0.75, 1.0].map((frac, idx) => (
              <circle
                key={idx}
                cx={center}
                cy={center}
                r={radius * frac}
                fill="none"
                stroke="#38bdf8"
                strokeOpacity={idx === 3 ? '0.3' : '0.1'}
                strokeDasharray={idx < 3 ? '2 2' : 'none'}
              />
            ))}

            {dimensions.map((d, i) => {
              const { x, y } = getCoordinates(100, i);
              return (
                <line
                  key={i}
                  x1={center}
                  y1={center}
                  x2={x}
                  y2={y}
                  stroke="#38bdf8"
                  strokeOpacity="0.2"
                />
              );
            })}

            <polygon
              points={radarPolygonPoints}
              fill="rgba(56, 189, 248, 0.25)"
              stroke="#38bdf8"
              strokeWidth="2"
            />

            {dimensions.map((d, i) => {
              const { x, y } = getCoordinates(d.score, i);
              return (
                <circle
                  key={i}
                  cx={x}
                  cy={y}
                  r="3.5"
                  fill="#f59e0b"
                  stroke="#fff"
                  strokeWidth="1"
                />
              );
            })}

            {dimensions.map((d, i) => {
              const { x, y } = getCoordinates(125, i);
              return (
                <text
                  key={i}
                  x={x}
                  y={y + 3}
                  textAnchor="middle"
                  fill="#7dd3fc"
                  fontSize="8.5"
                  fontFamily="monospace"
                  fontWeight="bold"
                >
                  {d.label}
                </text>
              );
            })}
          </svg>
        </div>

        {/* Dimension Meters */}
        <div className="flex flex-col gap-2">
          {dimensions.map((d) => (
            <div key={d.key} className="flex flex-col gap-0.5">
              <div className="flex justify-between text-[11px] font-mono">
                <span className="text-cyan-300">{d.label}</span>
                <span className="text-cyan-100 font-bold">{d.score.toFixed(0)}/100</span>
              </div>
              <div className="w-full h-1.5 rounded-full bg-cyan-950/60 overflow-hidden border border-cyan-500/20">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-amber-400 transition-all duration-500"
                  style={{ width: `${Math.min(100, Math.max(2, d.score))}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Discrete False-Alarm & Quality Check Status Strip */}
      <div className="pt-3 border-t border-cyan-500/15 flex flex-col md:flex-row items-start md:items-center justify-between gap-2 text-xs font-mono">
        <div className="flex items-center gap-2">
          <span className="text-cyan-400/80">Quality Status:</span>
          {failCount > 0 ? (
            <span className="px-2 py-0.5 rounded bg-rose-500/20 border border-rose-500/40 text-rose-300 font-bold">
              {failCount} CHECKS FAILED
            </span>
          ) : cautionCount > 0 ? (
            <span className="px-2 py-0.5 rounded bg-amber-500/20 border border-amber-500/40 text-amber-300 font-bold">
              {cautionCount} QUALITY CAVEATS
            </span>
          ) : (
            <span className="px-2 py-0.5 rounded bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 font-bold">
              ALL CHECKS PASSED
            </span>
          )}
        </div>
        <div className="text-[11px] text-cyan-300 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-500/20">
          Confidence Tier: <strong>{conf.tier}</strong> ({conf.numeric_value.toFixed(0)}%)
        </div>
      </div>
    </div>
  );
}
