import React from 'react';
import { ChartPayload } from '../types/astrology';

export interface TransitDashboardProps {
  chartData: ChartPayload | null;
  websocketUrl?: string;
  isLiveConnected?: boolean;
}

export const TransitDashboard: React.FC<TransitDashboardProps> = ({
  chartData,
  isLiveConnected = true,
}) => {
  if (!chartData) {
    return (
      <div className="backdrop-blur-xl bg-slate-900/80 border border-slate-800 rounded-2xl p-6 text-center text-slate-400">
        <div className="spinner-border text-amber-400 mb-2" />
        <p className="text-xs font-mono">Loading transit activation data...</p>
      </div>
    );
  }

  return (
    <div className="backdrop-blur-xl bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-5 text-white">
      {/* Header & Status Indicator */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-xl font-bold font-serif text-sky-400">Real-Time Transit & Aspect Radar</h3>
          <p className="text-xs text-slate-400 font-mono">
            Active Gochara Movements • Precision Ephemeris Sync
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className={`w-3 h-3 rounded-full ${isLiveConnected ? 'bg-emerald-400 animate-ping' : 'bg-rose-500'}`} />
          <span className="text-xs font-mono font-bold text-slate-300">
            {isLiveConnected ? 'LIVE STREAMING' : 'DISCONNECTED'}
          </span>
        </div>
      </div>

      {/* Planetary Positions Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        {chartData.planets.map((planet) => (
          <div
            key={planet.id}
            className="p-3 bg-slate-800/40 border border-slate-800 rounded-xl hover:border-sky-500/40 transition-all flex flex-col justify-between"
          >
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold text-amber-400 flex items-center gap-1">
                <span>{planet.glyph}</span>
                <span>{planet.name}</span>
              </span>
              {planet.isRetrograde && (
                <span className="text-[10px] font-mono text-rose-400 font-bold bg-rose-500/10 px-1 rounded border border-rose-500/20">
                  Rx
                </span>
              )}
            </div>
            <div className="mt-2 text-sm font-mono font-bold text-white">
              {planet.signDegree.toFixed(2)}° <span className="text-xs font-normal text-slate-400">{planet.rashi}</span>
            </div>
            <div className="text-[10px] text-slate-400 font-mono mt-1 flex justify-between">
              <span>House {planet.house}</span>
              <span className="text-emerald-400">{planet.functionalPowerPct}%</span>
            </div>
          </div>
        ))}
      </div>

      {/* Active Aspect Alerts */}
      <div className="pt-2 border-t border-slate-800 space-y-3">
        <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider font-mono">
          Active Aspect Configurations ({chartData.aspects.length})
        </h4>

        <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
          {chartData.aspects.map((aspect, idx) => {
            const isBenefic = aspect.aspectType === 'trine' || aspect.aspectType === 'sextile';
            const isFriction = aspect.aspectType === 'square' || aspect.aspectType === 'opposition';

            const badgeColor = isBenefic
              ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
              : isFriction
              ? 'bg-rose-500/20 text-rose-300 border-rose-500/30'
              : 'bg-amber-500/20 text-amber-300 border-amber-500/30';

            return (
              <div
                key={idx}
                className="p-2.5 bg-slate-800/30 rounded-lg border border-slate-800 flex items-center justify-between text-xs"
              >
                <div className="flex items-center gap-2">
                  <span className="font-bold text-white">{aspect.sourcePlanet}</span>
                  <span className="text-slate-500 font-mono">⟷</span>
                  <span className="font-bold text-white">{aspect.targetPlanet}</span>
                </div>

                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded border font-mono font-bold text-[10px] uppercase ${badgeColor}`}>
                    {aspect.aspectType}
                  </span>
                  <span className="text-[10px] text-slate-400 font-mono">
                    (Orb: {aspect.orbDegree.toFixed(1)}°)
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
