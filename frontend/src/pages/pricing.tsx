import React from 'react';

export const PricingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-8 flex flex-col justify-between" style={{ backgroundImage: 'radial-gradient(circle at top right, rgba(30, 27, 75, 0.4), rgba(15, 23, 42, 0.8))' }}>
      <div className="max-w-5xl mx-auto w-full space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold font-serif text-white">Astrological Intelligence Pricing Tiers</h1>
          <p className="text-xs text-slate-400 font-mono">100% Deterministic Ephemeris Calculations & Confluence Engine</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
            <h3 className="text-lg font-bold text-white">FREE TIER</h3>
            <p className="text-2xl font-bold font-mono text-sky-400">$0 / mo</p>
            <ul className="text-xs text-slate-300 space-y-2 font-mono">
              <li>✓ Full Natal Chart Calculation</li>
              <li>✓ Basic Dasha Periods</li>
              <li>✓ Daily Gochara Transits</li>
            </ul>
          </div>

          <div className="backdrop-blur-xl bg-slate-900/80 border border-amber-500/40 rounded-2xl p-6 shadow-2xl space-y-4 relative">
            <span className="absolute -top-3 right-6 px-3 py-0.5 rounded-full bg-amber-500 text-slate-950 text-[10px] font-mono font-bold">MOST POPULAR</span>
            <h3 className="text-lg font-bold text-amber-400">PRO CELESTIAL</h3>
            <p className="text-2xl font-bold font-mono text-amber-400">$19 / mo</p>
            <ul className="text-xs text-slate-300 space-y-2 font-mono">
              <li>✓ 16-Domain Confluence Forecasts</li>
              <li>✓ 80-Year Life Atlas Roadmap</li>
              <li>✓ Unlimited PDF Report Exports</li>
            </ul>
          </div>

          <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
            <h3 className="text-lg font-bold text-white">ENTERPRISE API</h3>
            <p className="text-2xl font-bold font-mono text-sky-400">$99 / mo</p>
            <ul className="text-xs text-slate-300 space-y-2 font-mono">
              <li>✓ Sub-15ms Anycast Edge API</li>
              <li>✓ Kyber-1024 Quantum Vault</li>
              <li>✓ Custom Webhook & Stream Bus</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;
