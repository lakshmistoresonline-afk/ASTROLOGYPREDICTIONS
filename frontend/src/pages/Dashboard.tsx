import React, { useState } from 'react';
import { ChartPayload, Planet } from '../types/astrology';
import { NatalWheel } from '../components/NatalWheel';
import { PlanetInspector } from '../components/PlanetInspector';
import { TransitDashboard } from '../components/TransitDashboard';

// Out-of-the-box Mock Fallback Data Initialization (Mahatma Gandhi Chart Baseline)
const MOCK_FALLBACK_CHART: ChartPayload = {
  sha256Fingerprint: '0069d60b97901e5a254591b0a17cfea376a8a1fea00b3ef16f07037b798e0fc8',
  ascendantDegree: 186.79, // Tula (Libra) 6.79°
  planets: [
    { id: 'p-sun', name: 'Sun', glyph: '☉', degree: 166.90, signDegree: 16.90, rashi: 'Virgo', house: 12, nakshatra: 'Hasta', pada: 3, isRetrograde: false, functionalPowerPct: 60 },
    { id: 'p-moon', name: 'Moon', glyph: '☽', degree: 118.40, signDegree: 28.40, rashi: 'Cancer', house: 10, nakshatra: 'Ashlesha', pada: 4, isRetrograde: false, functionalPowerPct: 95 },
    { id: 'p-mars', name: 'Mars', glyph: '♂', degree: 206.37, signDegree: 26.37, rashi: 'Libra', house: 1, nakshatra: 'Vishakha', pada: 2, isRetrograde: false, functionalPowerPct: 75 },
    { id: 'p-mercury', name: 'Mercury', glyph: '☿', degree: 191.74, signDegree: 11.74, rashi: 'Libra', house: 1, nakshatra: 'Swati', pada: 2, isRetrograde: false, functionalPowerPct: 75 },
    { id: 'p-jupiter', name: 'Jupiter', glyph: '♃', degree: 28.14, signDegree: 28.14, rashi: 'Aries', house: 7, nakshatra: 'Krittika', pada: 1, isRetrograde: true, functionalPowerPct: 80 },
    { id: 'p-venus', name: 'Venus', glyph: '♀', degree: 204.41, signDegree: 24.41, rashi: 'Libra', house: 1, nakshatra: 'Vishakha', pada: 2, isRetrograde: false, functionalPowerPct: 90 },
    { id: 'p-saturn', name: 'Saturn', glyph: '♄', degree: 230.33, signDegree: 20.33, rashi: 'Scorpio', house: 2, nakshatra: 'Jyeshtha', pada: 2, isRetrograde: false, functionalPowerPct: 65 },
    { id: 'p-rahu', name: 'Rahu', glyph: '☊', degree: 102.15, signDegree: 12.15, rashi: 'Cancer', house: 10, nakshatra: 'Pushya', pada: 3, isRetrograde: true, functionalPowerPct: 85 },
    { id: 'p-ketu', name: 'Ketu', glyph: '☋', degree: 282.15, signDegree: 12.15, rashi: 'Capricorn', house: 4, nakshatra: 'Shravana', pada: 1, isRetrograde: true, functionalPowerPct: 55 }
  ],
  houseCusps: [
    { house: 1, degree: 186.79, rashi: 'Libra' },
    { house: 2, degree: 216.79, rashi: 'Scorpio' },
    { house: 3, degree: 246.79, rashi: 'Sagittarius' },
    { house: 4, degree: 276.79, rashi: 'Capricorn' },
    { house: 5, degree: 306.79, rashi: 'Aquarius' },
    { house: 6, degree: 336.79, rashi: 'Pisces' },
    { house: 7, degree: 6.79, rashi: 'Aries' },
    { house: 8, degree: 36.79, rashi: 'Taurus' },
    { house: 9, degree: 66.79, rashi: 'Gemini' },
    { house: 10, degree: 96.79, rashi: 'Cancer' },
    { house: 11, degree: 126.79, rashi: 'Leo' },
    { house: 12, degree: 156.79, rashi: 'Virgo' }
  ],
  aspects: [
    { sourcePlanet: 'Moon', targetPlanet: 'Rahu', aspectType: 'conjunction', orbDegree: 0.25 },
    { sourcePlanet: 'Mars', targetPlanet: 'Venus', aspectType: 'conjunction', orbDegree: 1.96 },
    { sourcePlanet: 'Jupiter', targetPlanet: 'Saturn', aspectType: 'trine', orbDegree: 2.19 },
    { sourcePlanet: 'Sun', targetPlanet: 'Jupiter', aspectType: 'opposition', orbDegree: 3.42 }
  ]
};

export const Dashboard: React.FC = () => {
  const [chartData] = useState<ChartPayload>(MOCK_FALLBACK_CHART);
  const [selectedPlanet, setSelectedPlanet] = useState<Planet | null>(MOCK_FALLBACK_CHART.planets[1]); // Default to Moon
  const [searchQuery, setSearchQuery] = useState<string>('');

  const handleSelectPlanet = (planet: Planet) => {
    setSelectedPlanet(planet);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-amber-500 selection:text-slate-950">
      {/* Background Ambient Glowing Halos */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute -top-40 -left-40 w-[600px] h-[600px] bg-sky-600/10 rounded-full blur-[140px]" />
        <div className="absolute top-1/3 -right-40 w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-[140px]" />
        <div className="absolute -bottom-40 left-1/3 w-[600px] h-[600px] bg-amber-600/10 rounded-full blur-[140px]" />
      </div>

      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Top Header Bar */}
        <header className="sticky top-0 z-40 backdrop-blur-xl bg-slate-900/80 border-b border-slate-800/80 px-6 py-4 flex flex-wrap items-center justify-between gap-4 shadow-xl">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black flex items-center justify-center text-xl shadow-lg shadow-amber-500/20">
              ॐ
            </div>
            <div>
              <h1 className="text-lg font-bold font-serif text-white tracking-wider flex items-center gap-2">
                <span>ASTRO PREDICTIONS</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono">
                  V7.0 ENTERPRISE
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-mono">
                Swiss Ephemeris • Parashari & KP Sub-Lord Core
              </p>
            </div>
          </div>

          {/* Search Bar Input */}
          <div className="relative flex-1 max-w-md hidden md:block">
            <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
              🔍
            </span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search planets, rashis, houses, transits..."
              className="w-full pl-9 pr-4 py-2 bg-slate-800/50 border border-slate-700/80 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all"
            />
          </div>

          {/* System Status Indicator */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800/60 border border-slate-700/60 text-xs font-mono">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
              <span className="text-slate-300">ENGINE ONLINE</span>
            </div>
          </div>
        </header>

        {/* Main Dashboard Grid Workspace */}
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left / Center Section: Interactive Natal Wheel & Real-Time Radar */}
          <div className="lg:col-span-8 space-y-6">
            <div className="backdrop-blur-xl bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-2xl">
              <NatalWheel
                data={chartData}
                selectedPlanetId={selectedPlanet?.id}
                onSelectPlanet={handleSelectPlanet}
                size={520}
              />
            </div>

            {/* Real-Time Transit Dashboard */}
            <TransitDashboard chartData={chartData} isLiveConnected={true} />
          </div>

          {/* Right Side Panel: Planet Metrics Inspector & System Fingerprint */}
          <div className="lg:col-span-4 space-y-6">
            <PlanetInspector selectedPlanet={selectedPlanet} />

            {/* System Fingerprint Card */}
            <div className="backdrop-blur-xl bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-2xl space-y-2 text-xs font-mono">
              <div className="text-slate-400 flex justify-between">
                <span>Fingerprint:</span>
                <span className="text-amber-400 font-bold">
                  {chartData.sha256Fingerprint.substring(0, 12)}...
                </span>
              </div>
              <div className="text-slate-400 flex justify-between">
                <span>Ascendant:</span>
                <span className="text-sky-400 font-bold">
                  {chartData.ascendantDegree.toFixed(2)}°
                </span>
              </div>
              <div className="text-slate-400 flex justify-between">
                <span>Calculated Planets:</span>
                <span className="text-emerald-400 font-bold">{chartData.planets.length} Active Nodes</span>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
