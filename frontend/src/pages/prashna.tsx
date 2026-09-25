import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const PrashnaPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="forecasts" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">1–249 KP Seed Prashna (Horary) Engine</h1>
            <p className="text-xs text-slate-400 font-mono">
              Krishnamurti Paddhati Horary Cusp Sub-Lord Verdicts
            </p>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-3 text-xs font-mono">
          <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-800 flex justify-between items-center">
            <div>
              <span className="text-amber-400 font-bold block text-sm">KP Seed #108 Selected</span>
              <span className="text-slate-400">Lagna Sub-Lord: Saturn</span>
            </div>
            <span className="px-3 py-1 rounded bg-rose-500/20 text-rose-300 font-bold border border-rose-500/30">
              VERDICT: NO
            </span>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default PrashnaPage;
