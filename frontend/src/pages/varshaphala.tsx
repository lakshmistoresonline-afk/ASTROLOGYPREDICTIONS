import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const VarshaphalaPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="forecasts" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Tajika Varshaphala (Annual Solar Return)</h1>
            <p className="text-xs text-slate-400 font-mono">
              Varsheshwara Lord, Mudda Dasha & Annual Return Chart
            </p>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-3 text-xs font-mono">
          <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-800 flex justify-between items-center">
            <div>
              <span className="text-amber-400 font-bold block text-sm">Target Year: 2026 Solar Return</span>
              <span className="text-slate-400">Varsheshwara Year Lord: Venus</span>
            </div>
            <span className="px-3 py-1 rounded bg-amber-500/20 text-amber-300 font-bold border border-amber-500/30">
              HIGH YEAR STRENGTH
            </span>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default VarshaphalaPage;
