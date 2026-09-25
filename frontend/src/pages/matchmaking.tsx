import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const MatchmakingPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="compatibility" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Ashtakoota Matchmaking & Compatibility</h1>
            <p className="text-xs text-slate-400 font-mono">
              36-Guna Synchronicity Analysis & Nadi/Bhakoot Overrides
            </p>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <h3 className="text-lg font-bold text-amber-400">Ashtakoota 36-Guna Breakdown</h3>
            <span className="text-xl font-mono font-bold text-sky-400">28.5 / 36 POINTS</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
            <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800">
              <span className="text-slate-400 block mb-1">Nadi Kuta</span>
              <span className="text-emerald-400 font-bold text-sm">8 / 8 (PASS)</span>
            </div>
            <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800">
              <span className="text-slate-400 block mb-1">Bhakoot Kuta</span>
              <span className="text-emerald-400 font-bold text-sm">7 / 7 (PASS)</span>
            </div>
            <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800">
              <span className="text-slate-400 block mb-1">Gana Kuta</span>
              <span className="text-amber-400 font-bold text-sm">5 / 6 (PASS)</span>
            </div>
            <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800">
              <span className="text-slate-400 block mb-1">Graha Maitri</span>
              <span className="text-emerald-400 font-bold text-sm">5 / 5 (PASS)</span>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default MatchmakingPage;
