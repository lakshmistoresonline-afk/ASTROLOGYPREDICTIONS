import React, { useState } from 'react';

export interface PlanetGlyph {
  planet: string;
  longitude: number;
  rashi: number;
  degree_in_rashi: number;
  house: number;
  dignity: string;
  is_retrograde: bool;
}

export interface NatalWheelProps {
  ascendantLongitude: number;
  houseCusps: number[];
  planetGlyphs: PlanetGlyph[];
  profileName?: string;
}

export const NatalWheel: React.FC<NatalWheelProps> = ({
  ascendantLongitude,
  houseCusps,
  planetGlyphs,
  profileName = 'Native'
}) => {
  const [viewMode, setViewMode] = useState<'wheel' | 'tabular'>('wheel');
  const [hoveredPlanet, setHoveredPlanet] = useState<PlanetGlyph | null>(null);

  const rashiNames = [
    'Aries', 'Taurus', 'Gemini', 'Cancer',
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
  ];

  return (
    <div className="card-glass p-4 rounded-2xl border border-white/10 text-white">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="text-xl font-bold font-serif text-amber-400">{profileName}'s Natal Chart</h3>
          <p className="text-xs text-slate-400 font-mono">Ascendant: {ascendantLongitude.toFixed(2)}°</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('wheel')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              viewMode === 'wheel'
                ? 'bg-amber-500 text-slate-900 font-bold'
                : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Visual Wheel
          </button>
          <button
            onClick={() => setViewMode('tabular')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              viewMode === 'tabular'
                ? 'bg-amber-500 text-slate-900 font-bold'
                : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Tabular View
          </button>
        </div>
      </div>

      {viewMode === 'wheel' ? (
        <div className="relative mx-auto my-4 flex justify-center items-center" style={{ width: '320px', height: '320px' }}>
          {/* SVG Circular Chart Wheel */}
          <svg width="320" height="320" viewBox="0 0 320 320" className="drop-shadow-lg">
            <circle cx="160" cy="160" r="150" fill="none" stroke="rgba(251, 191, 36, 0.4)" strokeWidth="2" />
            <circle cx="160" cy="160" r="100" fill="none" stroke="rgba(255, 255, 255, 0.15)" strokeWidth="1" />
            <circle cx="160" cy="160" r="45" fill="none" stroke="rgba(251, 191, 36, 0.2)" strokeWidth="1" />

            {/* 12 House Spoke Lines */}
            {houseCusps.map((cusp, idx) => {
              const rad = (cusp - ascendantLongitude) * (Math.PI / 180);
              const x2 = 160 + 150 * Math.cos(rad);
              const y2 = 160 - 150 * Math.sin(rad);
              return (
                <line
                  key={`spoke-${idx}`}
                  x1="160"
                  y1="160"
                  x2={x2}
                  y2={y2}
                  stroke="rgba(255, 255, 255, 0.1)"
                  strokeWidth="1"
                />
              );
            })}

            {/* Planet Glyphs Positioned on Wheel */}
            {planetGlyphs.map((p, idx) => {
              const rad = (p.longitude - ascendantLongitude) * (Math.PI / 180);
              const px = 160 + 120 * Math.cos(rad);
              const py = 160 - 120 * Math.sin(rad);
              return (
                <g
                  key={`planet-${idx}`}
                  className="cursor-pointer hover:scale-125 transition-transform"
                  onMouseEnter={() => setHoveredPlanet(p)}
                  onMouseLeave={() => setHoveredPlanet(null)}
                >
                  <circle cx={px} cy={py} r="12" fill="#0F172A" stroke="#FBBF24" strokeWidth="1.5" />
                  <text x={px} y={py + 4} textAnchor="middle" fill="#FBBF24" fontSize="10" fontWeight="bold">
                    {p.planet.substring(0, 2)}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Interactive Hover Tooltip */}
          {hoveredPlanet && (
            <div className="absolute top-2 left-2 bg-slate-900/90 border border-amber-500/40 p-3 rounded-xl text-xs shadow-2xl backdrop-blur-md">
              <div className="font-bold text-amber-400">{hoveredPlanet.planet} {hoveredPlanet.is_retrograde ? '(Rx)' : ''}</div>
              <div>Rashi: {rashiNames[hoveredPlanet.rashi]} ({hoveredPlanet.degree_in_rashi.toFixed(2)}°)</div>
              <div>House: {hoveredPlanet.house} • Dignity: {hoveredPlanet.dignity}</div>
            </div>
          )}
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left text-slate-300">
            <thead className="text-amber-400 bg-slate-800/60 uppercase font-mono">
              <tr>
                <th className="p-2">Planet</th>
                <th className="p-2">Longitude</th>
                <th className="p-2">Sign</th>
                <th className="p-2">House</th>
                <th className="p-2">Dignity</th>
              </tr>
            </thead>
            <tbody>
              {planetGlyphs.map((p, idx) => (
                <tr key={idx} className="border-b border-white/5 hover:bg-white/5">
                  <td className="p-2 font-bold text-white">{p.planet} {p.is_retrograde ? '(Rx)' : ''}</td>
                  <td className="p-2 font-mono">{p.longitude.toFixed(2)}°</td>
                  <td className="p-2">{rashiNames[p.rashi]} ({p.degree_in_rashi.toFixed(2)}°)</td>
                  <td className="p-2">House {p.house}</td>
                  <td className="p-2"><span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">{p.dignity}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
