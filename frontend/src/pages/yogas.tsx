import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const YogasPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="birth-chart" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">50+ Classical Yogas & Raja Yoga Detector</h1>
            <p className="text-xs text-slate-400 font-mono">
              Parashari, Jaimini, and Tajika Combinations Analysis
            </p>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-3 text-xs font-mono">
          <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800 flex justify-between items-center">
            <span className="font-bold text-amber-400">Gaja Kesari Yoga</span>
            <span className="text-emerald-400 font-bold">ACTIVE (HIGH STRENGTH)</span>
          </div>
          <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800 flex justify-between items-center">
            <span className="font-bold text-sky-400">Raja Yoga (Kendra/Trikona Lords)</span>
            <span className="text-emerald-400 font-bold">ACTIVE (VERY HIGH)</span>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default YogasPage;
