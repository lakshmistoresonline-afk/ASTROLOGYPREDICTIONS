import React, { useState } from 'react';
import { ChartPayload, Planet } from '../types/astrology';

export interface NatalWheelProps {
  data: ChartPayload;
  selectedPlanetId?: string | null;
  onSelectPlanet?: (planet: Planet) => void;
  size?: number;
}

const ZODIAC_SIGNS = [
  { name: 'Aries', abbr: 'ARI', glyph: '♈' },
  { name: 'Taurus', abbr: 'TAU', glyph: '♉' },
  { name: 'Gemini', abbr: 'GEM', glyph: '♊' },
  { name: 'Cancer', abbr: 'CAN', glyph: '♋' },
  { name: 'Leo', abbr: 'LEO', glyph: '♌' },
  { name: 'Virgo', abbr: 'VIR', glyph: '♍' },
  { name: 'Libra', abbr: 'LIB', glyph: '♎' },
  { name: 'Scorpio', abbr: 'SCO', glyph: '♏' },
  { name: 'Sagittarius', abbr: 'SAG', glyph: '♐' },
  { name: 'Capricorn', abbr: 'CAP', glyph: '♑' },
  { name: 'Aquarius', abbr: 'AQU', glyph: '♒' },
  { name: 'Pisces', abbr: 'PIS', glyph: '♓' },
];

export const NatalWheel: React.FC<NatalWheelProps> = ({
  data,
  selectedPlanetId,
  onSelectPlanet,
  size = 500,
}) => {
  const [hoveredPlanet, setHoveredPlanet] = useState<Planet | null>(null);

  const center = size / 2;
  const outerRadius = size * 0.46;
  const zodiacInnerRadius = size * 0.38;
  const houseInnerRadius = size * 0.28;
  const aspectRadius = size * 0.14;

  const ascendantDegree = data.ascendantDegree || 0;

  // Converts 360° total longitude to fixed-precision polar (x,y) coordinates relative to Ascendant
  // Fixed 3-decimal precision prevents float representation mismatches between SSR and Client Hydration
  const degreeToPolar = (deg: number, radius: number) => {
    const angleRad = ((ascendantDegree - deg + 180) * Math.PI) / 180;
    const x = Number((center + radius * Math.cos(angleRad)).toFixed(3));
    const y = Number((center - radius * Math.sin(angleRad)).toFixed(3));
    return { x, y };
  };

  const handlePlanetClick = (planet: Planet) => {
    if (onSelectPlanet) {
      onSelectPlanet(planet);
    }
  };

  const rOut = Number(outerRadius.toFixed(3));
  const rIn = Number(zodiacInnerRadius.toFixed(3));

  return (
    <div className="relative flex flex-col items-center justify-center p-4">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="drop-shadow-[0_0_35px_rgba(56,189,248,0.15)] transition-all duration-300"
        suppressHydrationWarning
      >
        <defs>
          <radialGradient id="celestialBg" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#0F172A" />
            <stop offset="100%" stopColor="#0B0F19" />
          </radialGradient>

          <filter id="amberGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>

          <filter id="cyanGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Outer Background Rim */}
        <circle
          cx={center}
          cy={center}
          r={rOut}
          fill="url(#celestialBg)"
          stroke="#1E293B"
          strokeWidth="2"
        />

        {/* 12 Polar Zodiac Sectors (30° Each) */}
        {ZODIAC_SIGNS.map((sign, idx) => {
          const startDeg = idx * 30;
          const midDeg = startDeg + 15;
          const endDeg = startDeg + 30;

          const pStart = degreeToPolar(startDeg, outerRadius);
          const pEnd = degreeToPolar(endDeg, outerRadius);
          const pInnerStart = degreeToPolar(startDeg, zodiacInnerRadius);
          const pInnerEnd = degreeToPolar(endDeg, zodiacInnerRadius);

          const midPos = degreeToPolar(midDeg, (outerRadius + zodiacInnerRadius) / 2);

          const arcPath = `M ${pStart.x} ${pStart.y} A ${rOut} ${rOut} 0 0 1 ${pEnd.x} ${pEnd.y} L ${pInnerEnd.x} ${pInnerEnd.y} A ${rIn} ${rIn} 0 0 0 ${pInnerStart.x} ${pInnerStart.y} Z`;

          return (
            <g key={sign.name}>
              <path
                d={arcPath}
                fill={idx % 2 === 0 ? 'rgba(30, 41, 59, 0.4)' : 'rgba(15, 23, 42, 0.6)'}
                stroke="rgba(255, 255, 255, 0.08)"
                strokeWidth="1"
                className="transition-colors duration-200 hover:fill-slate-800/60"
                suppressHydrationWarning
              />
              <text
                x={midPos.x}
                y={midPos.y + 4}
                textAnchor="middle"
                fill="#F59E0B"
                fontSize={size > 400 ? '12' : '10'}
                fontWeight="bold"
                className="select-none font-mono"
              >
                {sign.abbr} {sign.glyph}
              </text>
            </g>
          );
        })}

        {/* Zodiac Inner Boundary Circle */}
        <circle
          cx={center}
          cy={center}
          r={rIn}
          fill="none"
          stroke="#38BDF8"
          strokeOpacity="0.3"
          strokeWidth="1.5"
        />

        {/* House Division Lines (12 Radiating Vectors) */}
        {data.houseCusps.map((cusp) => {
          const pOuter = degreeToPolar(cusp.degree, zodiacInnerRadius);
          const pInner = degreeToPolar(cusp.degree, aspectRadius);

          return (
            <g key={`house-${cusp.house}`}>
              <line
                x1={pOuter.x}
                y1={pOuter.y}
                x2={pInner.x}
                y2={pInner.y}
                stroke={cusp.house === 1 || cusp.house === 10 ? '#F59E0B' : 'rgba(255, 255, 255, 0.12)'}
                strokeWidth={cusp.house === 1 || cusp.house === 10 ? '2' : '1'}
                strokeDasharray={cusp.house === 1 || cusp.house === 10 ? 'none' : '3,3'}
              />
              {/* House Number Indicator */}
              {(() => {
                const labelPos = degreeToPolar(cusp.degree + 15, (zodiacInnerRadius + houseInnerRadius) / 2);
                return (
                  <text
                    x={labelPos.x}
                    y={labelPos.y + 4}
                    textAnchor="middle"
                    fill="#94A3B8"
                    fontSize="9"
                    fontWeight="600"
                    className="select-none font-mono opacity-70"
                  >
                    H{cusp.house}
                  </text>
                );
              })()}
            </g>
          );
        })}

        {/* House Inner Boundary Ring */}
        <circle
          cx={center}
          cy={center}
          r={Number(houseInnerRadius.toFixed(3))}
          fill="none"
          stroke="rgba(255, 255, 255, 0.08)"
          strokeWidth="1"
        />

        {/* Aspect Lines Between Planetary Nodes */}
        {data.aspects.map((aspect, idx) => {
          const source = data.planets.find((p) => p.name === aspect.sourcePlanet);
          const target = data.planets.find((p) => p.name === aspect.targetPlanet);

          if (!source || !target) return null;

          const p1 = degreeToPolar(source.degree, aspectRadius);
          const p2 = degreeToPolar(target.degree, aspectRadius);

          const strokeColor =
            aspect.aspectType === 'trine' || aspect.aspectType === 'sextile'
              ? '#34D399' // Green (Benefic)
              : aspect.aspectType === 'square' || aspect.aspectType === 'opposition'
              ? '#F87171' // Red (Friction)
              : '#FBBF24'; // Gold (Conjunction)

          return (
            <line
              key={`aspect-${idx}`}
              x1={p1.x}
              y1={p1.y}
              x2={p2.x}
              y2={p2.y}
              stroke={strokeColor}
              strokeOpacity="0.4"
              strokeWidth="1"
              strokeDasharray="2,2"
            />
          );
        })}

        {/* Center Aspect Circle Boundary */}
        <circle
          cx={center}
          cy={center}
          r={Number(aspectRadius.toFixed(3))}
          fill="#0B0F19"
          stroke="#1E293B"
          strokeWidth="1.5"
        />

        {/* Planetary Nodes Plotted Accurately in 360° Polar Space */}
        {data.planets.map((planet) => {
          const pos = degreeToPolar(planet.degree, (zodiacInnerRadius + houseInnerRadius) / 2);
          const isSelected = selectedPlanetId === planet.id;
          const isHovered = hoveredPlanet?.id === planet.id;

          return (
            <g
              key={planet.id}
              className="cursor-pointer transition-transform duration-200"
              onClick={() => handlePlanetClick(planet)}
              onMouseEnter={() => setHoveredPlanet(planet)}
              onMouseLeave={() => setHoveredPlanet(null)}
            >
              {/* Selection / Hover Glowing Pulse Outer Ring */}
              {(isSelected || isHovered) && (
                <circle
                  cx={pos.x}
                  cy={pos.y}
                  r="18"
                  fill="none"
                  stroke={isSelected ? '#F59E0B' : '#38BDF8'}
                  strokeWidth="2"
                  filter={isSelected ? 'url(#amberGlow)' : 'url(#cyanGlow)'}
                  className="animate-pulse"
                />
              )}

              {/* Node Circle Background */}
              <circle
                cx={pos.x}
                cy={pos.y}
                r="13"
                fill="#0F172A"
                stroke={isSelected ? '#F59E0B' : isHovered ? '#38BDF8' : '#334155'}
                strokeWidth={isSelected || isHovered ? '2' : '1.5'}
              />

              {/* Planet Glyph or Symbol */}
              <text
                x={pos.x}
                y={pos.y + 4}
                textAnchor="middle"
                fill={isSelected ? '#F59E0B' : isHovered ? '#38BDF8' : '#F8FAFC'}
                fontSize="11"
                fontWeight="bold"
                className="select-none font-sans"
              >
                {planet.glyph || planet.name.substring(0, 2)}
              </text>

              {/* Retrograde Indicator Badge (Rx) */}
              {planet.isRetrograde && (
                <text
                  x={pos.x + 10}
                  y={pos.y - 7}
                  fill="#F87171"
                  fontSize="8"
                  fontWeight="900"
                  className="select-none font-mono"
                >
                  R
                </text>
              )}
            </g>
          );
        })}
      </svg>

      {/* Floating Centered Tooltip Modal */}
      {hoveredPlanet && (
        <div className="absolute top-6 right-6 backdrop-blur-xl bg-slate-900/90 border border-slate-700/80 p-4 rounded-2xl shadow-2xl text-xs space-y-1.5 z-20 min-w-[200px] pointer-events-none animate-fadeIn">
          <div className="flex items-center justify-between border-b border-slate-800 pb-1.5">
            <span className="font-bold text-amber-400 text-sm flex items-center gap-1.5">
              <span>{hoveredPlanet.glyph}</span>
              <span>{hoveredPlanet.name}</span>
            </span>
            {hoveredPlanet.isRetrograde && (
              <span className="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-400 border border-rose-500/30 text-[10px] font-mono font-bold">
                Rx
              </span>
            )}
          </div>
          <div className="text-slate-300 flex justify-between">
            <span className="text-slate-400">Sign:</span>
            <span className="font-semibold text-white">{hoveredPlanet.rashi} ({hoveredPlanet.signDegree.toFixed(2)}°)</span>
          </div>
          <div className="text-slate-300 flex justify-between">
            <span className="text-slate-400">Placement:</span>
            <span className="font-semibold text-cyan-300">House {hoveredPlanet.house}</span>
          </div>
          <div className="text-slate-300 flex justify-between">
            <span className="text-slate-400">Nakshatra:</span>
            <span className="font-mono text-slate-200">{hoveredPlanet.nakshatra} (P{hoveredPlanet.pada})</span>
          </div>
          <div className="text-slate-300 flex justify-between pt-1 border-t border-slate-800/80">
            <span className="text-slate-400">Functional Power:</span>
            <span className="font-mono font-bold text-emerald-400">{hoveredPlanet.functionalPowerPct}%</span>
          </div>
        </div>
      )}
    </div>
  );
};
