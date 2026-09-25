import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const AshtakavargaPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="birth-chart" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Ashtakavarga & Shodhya Pinda Matrix</h1>
            <p className="text-xs text-slate-400 font-mono">
              337 Parashari Bindu Invariant & Trikona Shodhana Reductions
            </p>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
          <h3 className="text-sm font-bold text-amber-400 font-mono">Raw Sarvashtakavarga (SAV - 337 Points)</h3>
          <div className="grid grid-cols-6 md:grid-cols-12 gap-2 text-center text-xs font-mono">
            {['ARI (21)', 'TAU (25)', 'GEM (26)', 'CAN (35)', 'LEO (39)', 'VIR (27)', 'LIB (22)', 'SCO (24)', 'SAG (28)', 'CAP (26)', 'AQU (31)', 'PIS (33)'].map((s) => (
              <div key={s} className="p-2 bg-slate-800/40 rounded border border-slate-800 text-slate-200">
                {s}
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default AshtakavargaPage;
