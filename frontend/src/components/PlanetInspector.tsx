import React from 'react';
import { Planet } from '../types/astrology';

export interface PlanetInspectorProps {
  selectedPlanet: Planet | null;
}

export const PlanetInspector: React.FC<PlanetInspectorProps> = ({ selectedPlanet }) => {
  if (!selectedPlanet) {
    return (
      <div className="backdrop-blur-xl bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-2xl text-center text-slate-400">
        <div className="text-3xl mb-2 opacity-50">✨</div>
        <h4 className="text-sm font-semibold text-slate-300 mb-1">No Planet Selected</h4>
        <p className="text-xs text-slate-500">
          Click or hover over any planetary node on the natal wheel to inspect metrics.
        </p>
      </div>
    );
  }

  // Determine power progress bar color based on percentage
  const powerColor =
    selectedPlanet.functionalPowerPct >= 80
      ? 'bg-emerald-400'
      : selectedPlanet.functionalPowerPct >= 60
      ? 'bg-amber-400'
      : selectedPlanet.functionalPowerPct >= 40
      ? 'bg-sky-400'
      : 'bg-rose-400';

  return (
    <div className="backdrop-blur-xl bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-5 text-white transition-all duration-300">
      {/* Header Info */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center text-2xl text-amber-400 shadow-inner">
            {selectedPlanet.glyph || selectedPlanet.name.substring(0, 2)}
          </div>
          <div>
            <h3 className="text-lg font-bold font-serif text-white flex items-center gap-2">
              <span>{selectedPlanet.name}</span>
              {selectedPlanet.isRetrograde && (
                <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs font-mono font-bold">
                  Rx
                </span>
              )}
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              House {selectedPlanet.house} • {selectedPlanet.rashi}
            </p>
          </div>
        </div>

        <div className="text-right">
          <span className="text-xs text-slate-500 font-mono block">Abs Degree</span>
          <span className="text-sm font-mono font-bold text-sky-400">
            {selectedPlanet.degree.toFixed(2)}°
          </span>
        </div>
      </div>

      {/* Grid Metrics */}
      <div className="grid grid-cols-2 gap-3">
        <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800">
          <span className="text-[11px] text-slate-400 font-mono block mb-0.5">Sign Degree</span>
          <span className="text-sm font-mono font-bold text-slate-200">
            {selectedPlanet.signDegree.toFixed(2)}°
          </span>
        </div>

        <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800">
          <span className="text-[11px] text-slate-400 font-mono block mb-0.5">Nakshatra & Pada</span>
          <span className="text-sm font-mono font-bold text-amber-400">
            {selectedPlanet.nakshatra} (P{selectedPlanet.pada})
          </span>
        </div>
      </div>

      {/* Functional Power Progress Bar */}
      <div className="space-y-1.5 pt-1">
        <div className="flex justify-between items-center text-xs">
          <span className="text-slate-400 font-medium">Functional Power Index</span>
          <span className="font-mono font-bold text-amber-400">{selectedPlanet.functionalPowerPct}%</span>
        </div>
        <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden p-0.5 border border-slate-700/50">
          <div
            className={`h-full rounded-full ${powerColor} transition-all duration-700 ease-out`}
            style={{ width: `${Math.min(100, Math.max(0, selectedPlanet.functionalPowerPct))}%` }}
          />
        </div>
      </div>
    </div>
  );
};
