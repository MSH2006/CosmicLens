'use client';

import React, { useState } from 'react';
import { Region } from '../lib/types';

interface DataIngestModalProps {
  isOpen: boolean;
  onClose: () => void;
  onIngest: (region: Region) => void;
}

export default function DataIngestModal({
  isOpen,
  onClose,
  onIngest,
}: DataIngestModalProps) {
  const [jsonContent, setJsonContent] = useState('');
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleLoadSample = () => {
    const sample: Region = {
      id: `custom_survey_${Date.now()}`,
      name: 'JWST Cosmic Evolution Deep Field',
      ra_center: 189.2,
      dec_center: 62.2,
      fov_arcmin: 22.0,
      description: 'Ultra-deep multi-epoch infrared survey monitoring high-redshift transients and dusty starbursts.',
      epochs: [
        {
          timestamp: '2026-01-15',
          jd: 2460325.5,
          wavelength: 1.5,
          sources: [
            { id: 'TDE-CAND-01', ra: 189.2, dec: 62.2, flux: 12.0, flux_err: 1.2, flag: 'good', psf_fwhm: 2.0, type: 'transient' },
            { id: 'REF-STAR-01', ra: 189.215, dec: 62.21, flux: 45.0, flux_err: 1.5, flag: 'good', psf_fwhm: 1.95, type: 'star' },
          ],
        },
        {
          timestamp: '2026-03-30',
          jd: 2460400.5,
          wavelength: 2.8,
          sources: [
            { id: 'TDE-CAND-01', ra: 189.2, dec: 62.2, flux: 110.0, flux_err: 2.5, flag: 'good', psf_fwhm: 2.0, type: 'transient' },
            { id: 'REF-STAR-01', ra: 189.215, dec: 62.21, flux: 44.8, flux_err: 1.5, flag: 'good', psf_fwhm: 1.95, type: 'star' },
          ],
        },
        {
          timestamp: '2026-06-15',
          jd: 2460476.5,
          wavelength: 4.4,
          sources: [
            { id: 'TDE-CAND-01', ra: 189.2, dec: 62.2, flux: 65.0, flux_err: 2.1, flag: 'good', psf_fwhm: 2.0, type: 'transient' },
            { id: 'REF-STAR-01', ra: 189.215, dec: 62.21, flux: 45.2, flux_err: 1.5, flag: 'good', psf_fwhm: 1.95, type: 'star' },
          ],
        },
      ],
    };
    setJsonContent(JSON.stringify(sample, null, 2));
    setError(null);
  };

  const handleIngest = () => {
    try {
      const parsed = JSON.parse(jsonContent);
      if (!parsed.id || !parsed.epochs || parsed.epochs.length === 0) {
        throw new Error('Dataset must contain an "id" and an "epochs" array with at least one epoch.');
      }
      onIngest(parsed as Region);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Invalid JSON syntax');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-xl bg-[#030d17] border border-cyan-500/40 rounded-3xl p-6 shadow-2xl flex flex-col gap-4">
        {/* Header */}
        <div className="flex items-start justify-between border-b border-cyan-500/20 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] uppercase tracking-widest px-2 py-0.5 rounded bg-cyan-950 border border-cyan-500/40 text-cyan-300 font-mono">
                Data Pipeline
              </span>
            </div>
            <h2 className="text-xl font-bold font-mono text-cyan-100 mt-1">
              Ingest Custom Astronomical Survey
            </h2>
            <p className="text-xs font-mono text-cyan-400/70">
              Provide multi-epoch observations in JSON format for instant pipeline processing.
            </p>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/20 flex items-center justify-center text-sm font-bold"
          >
            ✕
          </button>
        </div>

        {/* Action Row */}
        <div className="flex items-center justify-between text-xs font-mono">
          <button
            onClick={handleLoadSample}
            className="px-3 py-1.5 rounded-xl bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/20"
          >
            Load Sample Template (JWST Deep Field)
          </button>
        </div>

        {/* JSON Editor */}
        <textarea
          value={jsonContent}
          onChange={(e) => {
            setJsonContent(e.target.value);
            setError(null);
          }}
          placeholder="Paste survey JSON schema here..."
          className="w-full h-56 bg-black/50 border border-cyan-500/30 rounded-2xl p-3 text-xs font-mono text-cyan-200 focus:outline-none focus:border-cyan-400 select-all"
        />

        {error && (
          <div className="p-3 rounded-xl bg-rose-950/50 border border-rose-500/40 text-rose-300 text-xs font-mono">
            {error}
          </div>
        )}

        {/* Footer Actions */}
        <div className="flex items-center justify-end gap-3 pt-3 border-t border-cyan-500/20">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-black/40 text-cyan-400 hover:text-white font-mono text-xs"
          >
            CANCEL
          </button>
          <button
            onClick={handleIngest}
            disabled={!jsonContent.trim()}
            className="px-4 py-2 rounded-xl bg-cyan-500 text-black font-mono text-xs font-bold hover:bg-cyan-400 disabled:opacity-50 transition-all shadow-lg"
          >
            INGEST & ANALYZE
          </button>
        </div>
      </div>
    </div>
  );
}
