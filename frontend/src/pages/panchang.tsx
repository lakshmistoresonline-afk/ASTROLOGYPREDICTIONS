import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const PanchangPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="transits" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Panchang, Gowri & Muhurta Radar</h1>
            <p className="text-xs text-slate-400 font-mono">
              Tithi, Vara, Nakshatra, Yoga, Karana & Auspicious Timing Windows
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
          <div className="p-4 backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl shadow-2xl">
            <span className="text-slate-400 block mb-1">Tithi</span>
            <span className="text-amber-400 font-bold text-sm">Shukla Ekadashi</span>
          </div>
          <div className="p-4 backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl shadow-2xl">
            <span className="text-slate-400 block mb-1">Nakshatra</span>
            <span className="text-sky-400 font-bold text-sm">Pushya</span>
          </div>
          <div className="p-4 backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl shadow-2xl">
            <span className="text-slate-400 block mb-1">Yoga</span>
            <span className="text-emerald-400 font-bold text-sm">Siddha</span>
          </div>
          <div className="p-4 backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl shadow-2xl">
            <span className="text-slate-400 block mb-1">Karana</span>
            <span className="text-amber-400 font-bold text-sm">Bava</span>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default PanchangPage;
