'use client';

import React from 'react';
import { Epoch } from '../lib/types';

interface TimeMachineBarProps {
  epochs: Epoch[];
  selectedEpoch: number;
  onSelectEpoch: (index: number) => void;
  playing: boolean;
  onTogglePlay: () => void;
  playbackSpeed: number;
  onChangeSpeed: (speed: number) => void;
}

export default function TimeMachineBar({
  epochs,
  selectedEpoch,
  onSelectEpoch,
  playing,
  onTogglePlay,
  playbackSpeed,
  onChangeSpeed,
}: TimeMachineBarProps) {
  const handlePrev = () => {
    onSelectEpoch((selectedEpoch - 1 + epochs.length) % epochs.length);
  };

  const handleNext = () => {
    onSelectEpoch((selectedEpoch + 1) % epochs.length);
  };

  return (
    <div className="w-full bg-[#07131e]/90 border border-cyan-500/20 rounded-2xl p-3.5 backdrop-blur-md shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
      {/* Playback Controls */}
      <div className="flex items-center gap-2">
        <button
          onClick={handlePrev}
          className="w-9 h-9 rounded-xl bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/20 flex items-center justify-center transition-all"
          title="Previous Epoch"
        >
          ⏮
        </button>
        <button
          onClick={onTogglePlay}
          className={`px-4 h-9 rounded-xl font-mono text-sm font-semibold flex items-center gap-2 transition-all shadow-md ${
            playing
              ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30'
              : 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 hover:bg-cyan-500/30'
          }`}
        >
          <span>{playing ? '⏸ PAUSE' : '▶ PLAY'}</span>
        </button>
        <button
          onClick={handleNext}
          className="w-9 h-9 rounded-xl bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/20 flex items-center justify-center transition-all"
          title="Next Epoch"
        >
          ⏭
        </button>

        {/* Speed Selector */}
        <div className="flex items-center bg-black/40 rounded-xl p-0.5 border border-cyan-500/20 ml-2">
          {[0.5, 1.0, 2.0].map((s) => (
            <button
              key={s}
              onClick={() => onChangeSpeed(s)}
              className={`px-2 py-1 rounded-lg text-xs font-mono transition-all ${
                playbackSpeed === s
                  ? 'bg-cyan-500 text-black font-bold shadow'
                  : 'text-cyan-400 hover:text-white'
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>

      {/* Epoch Step Items */}
      <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto py-1">
        {epochs.map((epoch, idx) => {
          const isActive = idx === selectedEpoch;
          return (
            <button
              key={epoch.timestamp}
              onClick={() => onSelectEpoch(idx)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl border transition-all text-xs font-mono whitespace-nowrap ${
                isActive
                  ? 'bg-cyan-500/20 border-cyan-400 text-cyan-200 shadow-[0_0_15px_rgba(56,189,248,0.3)]'
                  : 'bg-black/30 border-cyan-500/10 text-cyan-400/70 hover:bg-cyan-500/10 hover:border-cyan-500/30'
              }`}
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  isActive ? 'bg-amber-400 animate-ping' : 'bg-cyan-600'
                }`}
              />
              <span className="font-bold">T{idx + 1}</span>
              <span className="text-[11px] opacity-75">{epoch.timestamp}</span>
              <span className="text-[10px] px-1.5 py-0.2 bg-cyan-950/80 rounded border border-cyan-500/20 text-cyan-300">
                {epoch.wavelength} μm
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
