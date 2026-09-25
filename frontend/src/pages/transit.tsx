import React from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { TransitDashboard } from '../components/TransitDashboard';

export const TransitPage: React.FC = () => {
  return (
    <DashboardLayout activeRoute="transits" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Transit Calendar & Gochara Radar</h1>
            <p className="text-xs text-slate-400 font-mono">
              Real-Time High-Precision Ephemeris Transit & Aspect Sync
            </p>
          </div>
        </div>

        <TransitDashboard
          chartData={{
            sha256Fingerprint: 'ad1a10ab1ce7448c0d9f4b13246982e5536112d84c28f31c40a95f6841c9144c',
            ascendantDegree: 311.19,
            planets: [
              { id: 'p-sun', name: 'Sun', glyph: '☉', degree: 161.35, signDegree: 11.35, rashi: 'Virgo', house: 8, nakshatra: 'Hasta', pada: 2, isRetrograde: false, functionalPowerPct: 60 },
              { id: 'p-moon', name: 'Moon', glyph: '☽', degree: 96.38, signDegree: 6.38, rashi: 'Cancer', house: 6, nakshatra: 'Pushya', pada: 1, isRetrograde: false, functionalPowerPct: 95 },
              { id: 'p-mars', name: 'Mars', glyph: '♂', degree: 270.85, signDegree: 0.85, rashi: 'Capricorn', house: 12, nakshatra: 'Uttara Ashadha', pada: 2, isRetrograde: false, functionalPowerPct: 85 },
              { id: 'p-venus', name: 'Venus', glyph: '♀', degree: 201.63, signDegree: 21.63, rashi: 'Libra', house: 9, nakshatra: 'Vishakha', pada: 1, isRetrograde: false, functionalPowerPct: 90 }
            ],
            houseCusps: [
              { house: 1, degree: 311.19, rashi: 'Aquarius' },
              { house: 2, degree: 341.19, rashi: 'Pisces' }
            ],
            aspects: [
              { sourcePlanet: 'Jupiter', targetPlanet: 'Sun', aspectType: 'trine', orbDegree: 0.60 }
            ]
          }}
          isLiveConnected={true}
        />
      </div>
    </DashboardLayout>
  );
};

export default TransitPage;
