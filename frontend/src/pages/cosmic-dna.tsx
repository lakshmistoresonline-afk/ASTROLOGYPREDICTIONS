import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const CosmicDnaPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="cosmic-dna" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Cosmic DNA & Cross-Conversant Synthesis</h1>
            <p className="text-xs text-slate-400 font-mono">
              Vedic Sidereal, Chinese BaZi Four Pillars & Human Design Gene Keys
            </p>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4 text-xs font-mono">
          <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-800 space-y-2">
            <h3 className="font-bold text-amber-400 text-sm">🇨🇳 CHINESE BAZI FOUR PILLARS</h3>
            <p className="text-slate-300">Year: Fire Tiger • Month: Wood Rooster • Day: Water Rat • Hour: Metal Monkey</p>
          </div>

          <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-800 space-y-2">
            <h3 className="font-bold text-sky-400 text-sm">🧬 HUMAN DESIGN GENE KEYS</h3>
            <p className="text-slate-300">Type: Generator • Profile: 5/1 Heretic/Investigator • Definition: Single Definition</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default CosmicDnaPage;
