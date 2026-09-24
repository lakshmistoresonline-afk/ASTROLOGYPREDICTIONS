import React from 'react';

export interface LandingProps {
  onLoginClick?: () => void;
}

export const Landing: React.FC<LandingProps> = ({ onLoginClick }) => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans relative overflow-hidden flex flex-col justify-between">
      {/* Ambient Background Gradient */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[700px] h-[700px] bg-indigo-900/20 rounded-full blur-[150px]" />
        <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-amber-900/10 rounded-full blur-[150px]" />
      </div>

      {/* Header Bar */}
      <header className="relative z-10 max-w-7xl w-full mx-auto px-6 py-6 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black flex items-center justify-center text-xl shadow-lg shadow-amber-500/20">
            ॐ
          </div>
          <span className="text-lg font-bold font-serif tracking-widest text-white">ASTRO PREDICTIONS</span>
        </div>

        <button
          onClick={onLoginClick}
          className="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow-lg shadow-amber-500/20 transition-all"
        >
          LAUNCH APP DASHBOARD
        </button>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 max-w-5xl mx-auto px-6 py-16 text-center space-y-6 my-auto">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/80 border border-amber-500/30 text-xs font-mono text-amber-400">
          <span>✨ SWISS EPHEMERIS V3.36 HARDENED ENGINE</span>
        </div>

        <h1 className="text-4xl sm:text-6-xl font-extrabold font-serif text-white tracking-tight leading-tight">
          Deterministic Astrological Intelligence <br />
          <span className="bg-gradient-to-r from-amber-400 via-sky-400 to-indigo-400 bg-clip-text text-transparent">
            Powered by Quantum Precision
          </span>
        </h1>

        <p className="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
          Multi-layer predictive synthesis combining Parashari Vedic Dashas, KP Sub-Lord Promises, Jaimini Chara Karakas, and Bhrigu Nandi Nadi transits down to 48-hour operational windows.
        </p>

        <div className="pt-4 flex justify-center gap-4">
          <button
            onClick={onLoginClick}
            className="px-8 py-3.5 rounded-2xl bg-gradient-to-r from-amber-500 to-amber-400 text-slate-950 font-bold text-sm shadow-xl shadow-amber-500/20 hover:scale-105 transition-all"
          >
            ENTER CELESTIAL DASHBOARD →
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 max-w-7xl w-full mx-auto px-6 py-6 text-center text-xs text-slate-500 font-mono border-t border-slate-900">
        Deterministic Swiss Ephemeris Architecture • 100% Verified Multi-Engine Confluence
      </footer>
    </div>
  );
};

export default Landing;
