import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const PredictionsPage: React.FC = () => {
  const predictions = [
    { domain: 'Career & Authority', eventType: 'PROMOTION', score: 88.5, strength: 'PEAK', peakDate: '2026-10-20', summary: 'Major executive promotion and leadership expansion under active Venus Mahadasha.' },
    { domain: 'Marriage & Relationships', eventType: 'RELATIONSHIP_BEGINNING', score: 85.0, strength: 'PEAK', peakDate: '2026-10-12', summary: 'Matrimonial union and long-term partnership commitment window.' },
    { domain: 'Foreign Settlement', eventType: 'VISA_APPROVAL', score: 82.0, strength: 'MAJOR', peakDate: '2026-11-21', summary: 'Overseas relocation, international residency, and visa approval.' },
    { domain: 'Education & Knowledge', eventType: 'ACADEMIC_ENROLLMENT', score: 79.0, strength: 'MAJOR', peakDate: '2026-10-01', summary: 'Certification, academic absorption, and technical mastery phase.' }
  ];

  return (
    <DashboardLayout activeRoute="forecasts" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Confluent Predictions (16 Life Domains)</h1>
            <p className="text-xs text-slate-400 font-mono">
              Deterministic Multi-Engine Evidence Graph Analysis
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {predictions.map((p) => (
            <div key={p.domain} className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs font-mono font-bold text-amber-400 uppercase">{p.domain}</span>
                <span className="px-2.5 py-1 rounded-full bg-amber-500/20 text-amber-300 font-mono text-xs font-bold border border-amber-500/30">
                  {p.score}% MATCH
                </span>
              </div>
              <h3 className="text-lg font-bold text-white">{p.eventType.replace('_', ' ')}</h3>
              <p className="text-xs text-slate-300 leading-relaxed">{p.summary}</p>
              <div className="pt-2 border-t border-slate-800/80 flex justify-between text-xs font-mono">
                <span className="text-slate-400">Peak Date: <strong className="text-sky-400">{p.peakDate}</strong></span>
                <span className="text-emerald-400 font-bold">{p.strength}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default PredictionsPage;
