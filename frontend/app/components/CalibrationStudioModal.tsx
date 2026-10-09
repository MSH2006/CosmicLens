'use client';

import React, { useState } from 'react';
import { DEFAULT_WEIGHTS } from '../lib/clientEngine';

interface CalibrationStudioModalProps {
  isOpen: boolean;
  onClose: () => void;
  weights: Record<string, number>;
  onApplyWeights: (newWeights: Record<string, number>) => void;
}

export default function CalibrationStudioModal({
  isOpen,
  onClose,
  weights,
  onApplyWeights,
}: CalibrationStudioModalProps) {
  const [localWeights, setLocalWeights] = useState<Record<string, number>>({ ...weights });

  if (!isOpen) return null;

  const handleSliderChange = (key: string, val: number) => {
    setLocalWeights((prev) => ({
      ...prev,
      [key]: val,
    }));
  };

  const handleReset = () => {
    setLocalWeights({ ...DEFAULT_WEIGHTS });
  };

  const handleApply = () => {
    // Normalize weights to sum to 1.0
    const total = Object.values(localWeights).reduce((a, b) => a + b, 0) || 1.0;
    const normalized: Record<string, number> = {};
    for (const [k, v] of Object.entries(localWeights)) {
      normalized[k] = Number((v / total).toFixed(3));
    }
    onApplyWeights(normalized);
    onClose();
  };

  const weightSliders = [
    {
      key: 'astrometric_motion',
      label: 'Astrometric Proper Motion',
      desc: 'Sensitivity to angular sky displacement and linear trajectory velocity.',
    },
    {
      key: 'photometric_variability',
      label: 'Photometric Flux Variability',
      desc: 'Sensitivity to fractional flux variance and reduced Chi-squared deviations.',
    },
    {
      key: 'spectral_anomaly',
      label: 'Infrared Spectral Excess & Ices',
      desc: 'Weight given to infrared color departures and 3.05 um H2O / 4.27 um CO2 ice dips.',
    },
    {
      key: 'temporal_dynamics',
      label: 'Temporal Evolution & Transients',
      desc: 'Weight for fast-rising explosive light curve derivatives and non-stationary profiles.',
    },
    {
      key: 'contextual_outlier',
      label: 'Local Neighborhood Outlier',
      desc: 'Weight for robust MAD z-score departures from surrounding reference stars.',
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-xl bg-[#030d17] border border-cyan-500/40 rounded-3xl p-6 shadow-2xl flex flex-col gap-5">
        {/* Header */}
        <div className="flex items-start justify-between border-b border-cyan-500/20 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] uppercase tracking-widest px-2 py-0.5 rounded bg-cyan-950 border border-cyan-500/40 text-cyan-300 font-mono">
                Extensibility Studio
              </span>
            </div>
            <h2 className="text-xl font-bold font-mono text-cyan-100 mt-1">
              Dynamic Detector Tuning & Weights
            </h2>
            <p className="text-xs font-mono text-cyan-400/70">
              Calibrate multi-dimensional sensitivity in real time with zero core pipeline friction.
            </p>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/20 flex items-center justify-center text-sm font-bold"
          >
            ✕
          </button>
        </div>

        {/* Sliders Container */}
        <div className="flex flex-col gap-4 text-xs font-mono max-h-[50vh] overflow-y-auto pr-1">
          {weightSliders.map((slider) => {
            const val = localWeights[slider.key] || 0.2;
            return (
              <div key={slider.key} className="bg-black/30 p-3 rounded-2xl border border-cyan-500/15 flex flex-col gap-1.5">
                <div className="flex justify-between items-center">
                  <span className="text-cyan-200 font-bold">{slider.label}</span>
                  <span className="text-amber-400 font-bold px-2 py-0.5 bg-black/50 rounded border border-cyan-500/20">
                    {(val * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="text-[11px] text-cyan-400/60">{slider.desc}</p>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={val}
                  onChange={(e) => handleSliderChange(slider.key, parseFloat(e.target.value))}
                  className="w-full accent-cyan-400 cursor-pointer mt-1"
                />
              </div>
            );
          })}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-cyan-500/20">
          <button
            onClick={handleReset}
            className="px-3 py-2 rounded-xl bg-cyan-950/60 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/20 font-mono text-xs"
          >
            RESET TO BASELINE
          </button>
          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-black/40 text-cyan-400 hover:text-white font-mono text-xs"
            >
              CANCEL
            </button>
            <button
              onClick={handleApply}
              className="px-4 py-2 rounded-xl bg-cyan-500 text-black font-mono text-xs font-bold hover:bg-cyan-400 transition-all shadow-lg"
            >
              APPLY & RE-RANK TARGETS
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
