import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const HistoryPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="vault" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Temporal Vault & Saved Profiles</h1>
            <p className="text-xs text-slate-400 font-mono">
              User-Scoped Encrypted Birth Chart Profiles & Audit Records
            </p>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl">
          <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-800 flex justify-between items-center text-xs">
            <div>
              <h3 className="font-bold text-white text-sm">Subramanian T S</h3>
              <p className="text-slate-400 font-mono mt-0.5">1986-09-28 • 16:30 • Palakkad, Kerala, India</p>
            </div>
            <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono font-bold border border-emerald-500/30">
              ACTIVE PROFILE
            </span>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default HistoryPage;
