import React, { useState } from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { NatalWheel } from '../components/NatalWheel';
import { PlanetInspector } from '../components/PlanetInspector';

export const KundliPage: React.FC = () => {
  const [selectedPlanet, setSelectedPlanet] = useState<any>(null);

  return (
    <DashboardLayout activeRoute="birth-chart" userProfileName="Subramanian T S">
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold font-serif text-white">Interactive Birth Chart (Kundli)</h1>
            <p className="text-xs text-slate-400 font-mono">
              Precision Swiss Ephemeris Placidus Double-Ring Vector Visualizer
            </p>
          </div>

          <div className="flex gap-2">
            <span className="px-3 py-1.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/30 text-xs font-mono font-bold">
              VARGA: D1 (NATAL)
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <div className="lg:col-span-8 backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl">
            <NatalWheel
              data={{
                sha256Fingerprint: 'ad1a10ab1ce7448c0d9f4b13246982e5536112d84c28f31c40a95f6841c9144c',
                ascendantDegree: 311.19,
                planets: [
                  { id: 'p-sun', name: 'Sun', glyph: '☉', degree: 161.35, signDegree: 11.35, rashi: 'Virgo', house: 8, nakshatra: 'Hasta', pada: 2, isRetrograde: false, functionalPowerPct: 60 },
                  { id: 'p-moon', name: 'Moon', glyph: '☽', degree: 96.38, signDegree: 6.38, rashi: 'Cancer', house: 6, nakshatra: 'Pushya', pada: 1, isRetrograde: false, functionalPowerPct: 95 },
                  { id: 'p-mars', name: 'Mars', glyph: '♂', degree: 270.85, signDegree: 0.85, rashi: 'Capricorn', house: 12, nakshatra: 'Uttara Ashadha', pada: 2, isRetrograde: false, functionalPowerPct: 85 },
                  { id: 'p-mercury', name: 'Mercury', glyph: '☿', degree: 178.10, signDegree: 28.10, rashi: 'Virgo', house: 8, nakshatra: 'Chitra', pada: 2, isRetrograde: false, functionalPowerPct: 90 },
                  { id: 'p-jupiter', name: 'Jupiter', glyph: '♃', degree: 321.95, signDegree: 21.95, rashi: 'Aquarius', house: 1, nakshatra: 'Purva Bhadrapada', pada: 1, isRetrograde: true, functionalPowerPct: 80 },
                  { id: 'p-venus', name: 'Venus', glyph: '♀', degree: 201.63, signDegree: 21.63, rashi: 'Libra', house: 9, nakshatra: 'Vishakha', pada: 1, isRetrograde: false, functionalPowerPct: 90 },
                  { id: 'p-saturn', name: 'Saturn', glyph: '♄', degree: 221.51, signDegree: 11.51, rashi: 'Scorpio', house: 10, nakshatra: 'Anuradha', pada: 3, isRetrograde: false, functionalPowerPct: 70 },
                  { id: 'p-rahu', name: 'Rahu', glyph: '☊', degree: 357.83, signDegree: 27.83, rashi: 'Pisces', house: 2, nakshatra: 'Revati', pada: 4, isRetrograde: true, functionalPowerPct: 85 },
                  { id: 'p-ketu', name: 'Ketu', glyph: '☋', degree: 177.83, signDegree: 27.83, rashi: 'Virgo', house: 8, nakshatra: 'Chitra', pada: 2, isRetrograde: true, functionalPowerPct: 55 }
                ],
                houseCusps: [
                  { house: 1, degree: 311.19, rashi: 'Aquarius' },
                  { house: 2, degree: 341.19, rashi: 'Pisces' },
                  { house: 3, degree: 11.19, rashi: 'Aries' },
                  { house: 4, degree: 41.19, rashi: 'Taurus' },
                  { house: 5, degree: 71.19, rashi: 'Gemini' },
                  { house: 6, degree: 101.19, rashi: 'Cancer' },
                  { house: 7, degree: 131.19, rashi: 'Leo' },
                  { house: 8, degree: 161.19, rashi: 'Virgo' },
                  { house: 9, degree: 191.19, rashi: 'Libra' },
                  { house: 10, degree: 221.19, rashi: 'Scorpio' },
                  { house: 11, degree: 251.19, rashi: 'Sagittarius' },
                  { house: 12, degree: 281.19, rashi: 'Capricorn' }
                ],
                aspects: [
                  { sourcePlanet: 'Jupiter', targetPlanet: 'Sun', aspectType: 'trine', orbDegree: 0.60 },
                  { sourcePlanet: 'Mars', targetPlanet: 'Saturn', aspectType: 'sextile', orbDegree: 0.66 }
                ]
              }}
              onSelectPlanet={(p) => setSelectedPlanet(p)}
              size={520}
            />
          </div>

          <div className="lg:col-span-4 space-y-6">
            <PlanetInspector selectedPlanet={selectedPlanet} />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default KundliPage;
