import React from 'react';

export interface ScoreDialProps {
  score: number; // 0 to 100
  label: string;
  size?: number;
}

export const ScoreDial: React.FC<ScoreDialProps> = ({ score, label, size = 120 }) => {
  const strokeWidth = 10;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  // Color gradient based on score threshold
  const strokeColor =
    score >= 80 ? '#34D399' : score >= 60 ? '#FBBF24' : score >= 40 ? '#38BDF8' : '#F87171';

  return (
    <div className="flex flex-col items-center justify-center p-3">
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background Track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth={strokeWidth}
            fill="none"
          />
          {/* Active Score Ring */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-xl font-bold font-mono text-white">{Math.round(score)}%</span>
        </div>
      </div>
      <span className="mt-2 text-xs font-semibold text-slate-300 font-sans text-center">{label}</span>
    </div>
  );
};
