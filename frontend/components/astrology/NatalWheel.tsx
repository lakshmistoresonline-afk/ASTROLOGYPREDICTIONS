import React, { useState, useRef } from 'react';

export interface PlanetGlyph {
  planet: string;
  longitude: number;
  rashi: number;
  degree_in_rashi: number;
  house: number;
  dignity: string;
  is_retrograde: boolean;
  nakshatra_name?: string;
  nakshatra_pada?: number;
  sub_lord?: string;
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
  const [zoomLevel, setZoomLevel] = useState<number>(1.0);
  const [hoveredPlanet, setHoveredPlanet] = useState<PlanetGlyph | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);

  const rashiNames = [
    'Aries', 'Taurus', 'Gemini', 'Cancer',
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
  ];

  const handleDownloadSVG = () => {
    if (!svgRef.current) return;
    const svgData = new XMLSerializer().serializeToString(svgRef.current);
    const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${profileName}_Natal_Chart_Wheel.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="backdrop-blur-md bg-slate-900/60 border border-slate-800/80 shadow-2xl rounded-2xl p-6 text-white space-y-4">
      {/* Header & Controls */}
      <div className="flex flex-wrap justify-between items-center gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-xl font-bold font-serif text-amber-400">{profileName}'s Natal Celestial Chart</h3>
          <p className="text-xs text-slate-400 font-mono">
            Ascendant: {ascendantLongitude.toFixed(2)}° • Double-Ring Placidus Wheel
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Zoom Controls */}
          <div className="flex items-center bg-slate-800/80 rounded-lg p-1 border border-slate-700">
            <button
              onClick={() => setZoomLevel(prev => Math.max(0.8, prev - 0.1))}
              className="px-2 py-0.5 text-xs font-bold hover:text-amber-400"
              title="Zoom Out"
            >
              -
            </button>
            <span className="text-xs font-mono px-2 text-slate-300">{Math.round(zoomLevel * 100)}%</span>
            <button
              onClick={() => setZoomLevel(prev => Math.min(1.5, prev + 0.1))}
              className="px-2 py-0.5 text-xs font-bold hover:text-amber-400"
              title="Zoom In"
            >
              +
            </button>
          </div>

          {/* View Mode Toggle */}
          <div className="flex bg-slate-800/80 rounded-lg p-1 border border-slate-700">
            <button
              onClick={() => setViewMode('wheel')}
              className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
                viewMode === 'wheel' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-300 hover:text-white'
              }`}
            >
              Visual Wheel
            </button>
            <button
              onClick={() => setViewMode('tabular')}
              className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
                viewMode === 'tabular' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-300 hover:text-white'
              }`}
            >
              Tabular House View
            </button>
          </div>

          {/* SVG Export Download Button */}
          <button
            onClick={handleDownloadSVG}
            className="px-3 py-1.5 bg-cyan-600/30 hover:bg-cyan-600/50 border border-cyan-500/40 text-cyan-300 rounded-lg text-xs font-bold transition-all flex items-center gap-1"
          >
            <span>SVG Export</span>
          </button>
        </div>
      </div>

      {/* Main Wheel View or Tabular View */}
      {viewMode === 'wheel' ? (
        <div className="relative mx-auto my-4 flex justify-center items-center overflow-hidden" style={{ width: '380px', height: '380px' }}>
          <svg
            ref={svgRef}
            width="380"
            height="380"
            viewBox="0 0 380 380"
            className="drop-shadow-2xl transition-transform duration-200"
            style={{ transform: `scale(${zoomLevel})` }}
          >
            {/* Outer Zodiac Sign Ring */}
            <circle cx="190" cy="190" r="180" fill="none" stroke="rgba(6, 182, 212, 0.4)" strokeWidth="3" />
            <circle cx="190" cy="190" r="145" fill="none" stroke="rgba(245, 158, 11, 0.3)" strokeWidth="2" />

            {/* Inner House Cusps Ring */}
            <circle cx="190" cy="190" r="110" fill="none" stroke="rgba(255, 255, 255, 0.15)" strokeWidth="1" />
            <circle cx="190" cy="190" r="45" fill="none" stroke="rgba(139, 92, 246, 0.3)" strokeWidth="1.5" />

            {/* 12 House Spoke Lines */}
            {houseCusps.map((cusp, idx) => {
              const rad = (cusp - ascendantLongitude) * (Math.PI / 180);
              const x2 = 190 + 180 * Math.cos(rad);
              const y2 = 190 - 180 * Math.sin(rad);
              return (
                <line
                  key={`spoke-${idx}`}
                  x1="190"
                  y1="190"
                  x2={x2}
                  y2={y2}
                  stroke="rgba(255, 255, 255, 0.12)"
                  strokeWidth="1"
                  strokeDasharray={idx % 3 === 0 ? 'none' : '2,2'}
                />
              );
            })}

            {/* Planetary Aspect Connecting Lines */}
            {planetGlyphs.map((p1, idx1) =>
              planetGlyphs.slice(idx1 + 1).map((p2, idx2) => {
                const diff = Math.abs(p1.longitude - p2.longitude) % 360;
                const angle = diff > 180 ? 360 - diff : diff;
                // Trine (120 deg) or Opposition (180 deg) or Conjunction (0 deg)
                if (Math.abs(angle - 120) <= 6 || Math.abs(angle - 180) <= 6 || angle <= 6) {
                  const rad1 = (p1.longitude - ascendantLongitude) * (Math.PI / 180);
                  const rad2 = (p2.longitude - ascendantLongitude) * (Math.PI / 180);
                  const x1 = 190 + 130 * Math.cos(rad1);
                  const y1 = 190 - 130 * Math.sin(rad1);
                  const x2 = 190 + 130 * Math.cos(rad2);
                  const y2 = 190 - 130 * Math.sin(rad2);
                  return (
                    <line
                      key={`aspect-${idx1}-${idx2}`}
                      x1={x1}
                      y1={y1}
                      x2={x2}
                      y2={y2}
                      stroke={Math.abs(angle - 120) <= 6 ? 'rgba(52, 211, 153, 0.35)' : 'rgba(248, 113, 113, 0.35)'}
                      strokeWidth="1"
                    />
                  );
                }
                return null;
              })
            )}

            {/* Planet Glyphs Positioned on Inner Ring */}
            {planetGlyphs.map((p, idx) => {
              const rad = (p.longitude - ascendantLongitude) * (Math.PI / 180);
              const px = 190 + 130 * Math.cos(rad);
              const py = 190 - 130 * Math.sin(rad);
              return (
                <g
                  key={`planet-${idx}`}
                  className="cursor-pointer hover:scale-125 transition-transform"
                  onMouseEnter={() => setHoveredPlanet(p)}
                  onMouseLeave={() => setHoveredPlanet(null)}
                >
                  <circle cx={px} cy={py} r="14" fill="#0F172A" stroke="#F59E0B" strokeWidth="1.8" />
                  <text x={px} y={py + 4} textAnchor="middle" fill="#F59E0B" fontSize="10" fontWeight="bold">
                    {p.planet.substring(0, 2)}
                  </text>
                  {p.is_retrograde && (
                    <text x={px + 10} y={py - 8} fill="#EF4444" fontSize="9" fontWeight="bold">
                      R
                    </text>
                  )}
                </g>
              );
            })}
          </svg>

          {/* Interactive Popover Card */}
          {hoveredPlanet && (
            <div className="absolute top-4 left-4 backdrop-blur-md bg-slate-900/90 border border-amber-500/40 p-4 rounded-xl text-xs shadow-2xl space-y-1 font-sans">
              <div className="font-bold text-amber-400 text-sm flex items-center justify-between">
                <span>{hoveredPlanet.planet}</span>
                {hoveredPlanet.is_retrograde && (
                  <span className="text-red-400 bg-red-500/10 px-1.5 py-0.5 rounded border border-red-500/20">Retrograde (Rx)</span>
                )}
              </div>
              <div className="text-slate-200">
                Sign: <strong className="text-white">{rashiNames[hoveredPlanet.rashi]}</strong> ({hoveredPlanet.degree_in_rashi.toFixed(2)}°)
              </div>
              <div className="text-slate-300">
                House: House {hoveredPlanet.house} • Dignity: <span className="text-cyan-300">{hoveredPlanet.dignity}</span>
              </div>
              {hoveredPlanet.nakshatra_name && (
                <div className="text-slate-400 font-mono text-[11px]">
                  Nakshatra: {hoveredPlanet.nakshatra_name} (Pada {hoveredPlanet.nakshatra_pada || 1})
                </div>
              )}
              {hoveredPlanet.sub_lord && (
                <div className="text-amber-300/90 font-mono text-[11px]">
                  KP Sub-Lord: {hoveredPlanet.sub_lord}
                </div>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left text-slate-300">
            <thead className="text-amber-400 bg-slate-800/80 uppercase font-mono">
              <tr>
                <th className="p-3">Planet</th>
                <th className="p-3">Longitude</th>
                <th className="p-3">Sign</th>
                <th className="p-3">House</th>
                <th className="p-3">Dignity</th>
                <th className="p-3">Nakshatra & Pada</th>
              </tr>
            </thead>
            <tbody>
              {planetGlyphs.map((p, idx) => (
                <tr key={idx} className="border-b border-slate-800/60 hover:bg-slate-800/40">
                  <td className="p-3 font-bold text-white flex items-center gap-2">
                    <span>{p.planet}</span>
                    {p.is_retrograde && <span className="text-xs text-red-400 font-mono">(Rx)</span>}
                  </td>
                  <td className="p-3 font-mono text-cyan-300">{p.longitude.toFixed(2)}°</td>
                  <td className="p-3">{rashiNames[p.rashi]} ({p.degree_in_rashi.toFixed(2)}°)</td>
                  <td className="p-3">House {p.house}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">
                      {p.dignity}
                    </span>
                  </td>
                  <td className="p-3 font-mono text-slate-400">
                    {p.nakshatra_name ? `${p.nakshatra_name} (Pada ${p.nakshatra_pada || 1})` : 'Pushya'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
