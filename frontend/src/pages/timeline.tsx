import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export const TimelinePage: React.FC = () => {
  const events = [
    { date: '1986-10-12', domain: 'Foreign Settlement', event: 'VISA_APPROVAL', age: 0, magnitude: 'MAJOR' },
    { date: '2006-10-25', domain: 'Career & Authority', event: 'PROMOTION', age: 20, magnitude: 'MAJOR' },
    { date: '2016-10-24', domain: 'Career & Authority', event: 'PROMOTION', age: 30, magnitude: 'PEAK' },
    { date: '2026-10-12', domain: 'Marriage & Relationships', event: 'RELATIONSHIP_BEGINNING', age: 40, magnitude: 'PEAK' },
    { date: '2026-10-20', domain: 'Career & Authority', event: 'PROMOTION', age: 40, magnitude: 'PEAK' },
    { date: '2046-10-14', domain: 'Foreign Settlement', event: 'VISA_APPROVAL', age: 60, magnitude: 'MAJOR' }
  ];

  return (
    <DashboardLayout activeRoute="life-atlas" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Life Atlas Milestone Roadmap (Age 0 - 80)</h1>
            <p className="text-xs text-slate-400 font-mono">
              Deterministic Lifespan Dasha & Transit Confluence Mapping
            </p>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-sans">
              <thead>
                <tr className="border-b border-slate-800 text-amber-400 font-mono uppercase">
                  <th className="pb-3">Peak Date</th>
                  <th className="pb-3">Domain</th>
                  <th className="pb-3">Event Type</th>
                  <th className="pb-3">Age</th>
                  <th className="pb-3 text-right">Magnitude</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {events.map((ev, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/30 transition-all">
                    <td className="py-3.5 font-mono text-sky-400 font-bold">{ev.date}</td>
                    <td className="py-3.5 text-white font-semibold">{ev.domain}</td>
                    <td className="py-3.5 text-slate-300">{ev.event.replace('_', ' ')}</td>
                    <td className="py-3.5 font-mono text-slate-400">{ev.age} yrs</td>
                    <td className="py-3.5 text-right font-mono">
                      <span className="px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-bold border border-amber-500/30 text-[11px]">
                        {ev.magnitude}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default TimelinePage;
