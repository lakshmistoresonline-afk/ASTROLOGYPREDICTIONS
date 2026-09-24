import React, { useState } from 'react';

export interface LoginProps {
  onLoginSuccess?: (token: string, email: string) => void;
}

export const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState<string>('user@astropredictions.app');
  const [password, setPassword] = useState<string>('••••••••••••');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      if (onLoginSuccess) {
        onLoginSuccess(`token_${email.split('@')[0]}`, email);
      }
    }, 400);
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center p-6 text-slate-100 font-sans relative overflow-hidden"
      style={{
        backgroundColor: '#0B0F19',
        backgroundImage: 'radial-gradient(circle at top right, rgba(30, 27, 75, 0.4), rgba(15, 23, 42, 0.8))'
      }}
    >
      {/* Full Viewport Desktop 2-Column Glassmorphism Card */}
      <div className="w-full max-w-5xl backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl shadow-2xl p-8 sm:p-12 relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">

        {/* Left Column: Brand & Product Identity */}
        <div className="lg:col-span-6 space-y-5 text-left lg:border-r border-slate-800 lg:pr-8">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black flex items-center justify-center text-2xl shadow-lg shadow-amber-500/20 flex-shrink-0">
              ॐ
            </div>
            <div>
              <h1 className="text-2xl font-bold font-serif text-white tracking-wider uppercase">
                ASTRO PREDICTIONS
              </h1>
              <p className="text-[10px] text-amber-400 font-mono font-bold tracking-widest uppercase">
                Dark Celestial AI Engine
              </p>
            </div>
          </div>

          <p className="text-slate-300 text-xs sm:text-sm leading-relaxed">
            Deterministic Swiss Ephemeris calculation engine providing sub-arcsecond natal blueprints, 16-domain confluent life forecasts, 80-year Life Atlas roadmaps, and real-time Gochara transit alerts.
          </p>

          <div className="space-y-2 text-xs text-slate-200">
            <div className="flex items-center gap-2">
              <span className="text-amber-400 font-bold">✓</span>
              <span>Sub-arcsecond C-extension Swiss Ephemeris precision</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-amber-400 font-bold">✓</span>
              <span>16-Domain Confluent Predictions & 5-Level Dasha Timelines</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-amber-400 font-bold">✓</span>
              <span>Real-time Gochara Kakshya Transits & SBC Vedha Alerts</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-amber-400 font-bold">✓</span>
              <span>Post-Quantum Kyber-1024 Ephemeral Vault & Zero-Knowledge Privacy</span>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 text-[11px] font-mono text-slate-400 hidden sm:block">
            <span className="text-amber-400 font-bold">🛡️ ENTERPRISE SECURITY:</span> AES-256 PII Encryption • W3C Decentralized Identity
          </div>
        </div>

        {/* Right Column: Secure Authentication Controls */}
        <div className="lg:col-span-6 space-y-5 text-left lg:pl-4">
          <div className="space-y-1">
            <div className="inline-block px-3 py-1 rounded-full bg-slate-800 border border-amber-500/30 text-[10px] font-mono font-bold text-amber-400 mb-1">
              ✨ SECURE GATEWAY
            </div>
            <h2 className="text-xl font-bold text-white">Secure Sign In</h2>
            <p className="text-xs text-slate-400">
              Welcome back! Sign in to access your astrology workspace.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4 text-xs font-sans">
            <div className="space-y-1.5">
              <label className="text-slate-300 font-semibold font-mono text-[11px] uppercase">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="name@domain.com"
                className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-mono"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-slate-300 font-semibold font-mono text-[11px] uppercase">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Enter your password"
                className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-mono"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3.5 px-4 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs shadow-lg shadow-sky-500/20 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2"
            >
              {isLoading ? 'Signing In...' : 'Continue / Sign In →'}
            </button>
          </form>

          <div className="pt-2 text-center text-xs space-y-3 border-t border-slate-800/80">
            <div>
              <span className="text-slate-400">New user?</span>{' '}
              <a href="/profile/new" className="text-amber-400 font-bold hover:underline">
                Create birth profile →
              </a>
            </div>

            <div className="text-[11px] text-slate-500 font-mono flex justify-center gap-3">
              <a href="/marketing/privacy" className="hover:text-amber-400">Privacy Policy</a>
              <span>•</span>
              <a href="/marketing/terms" className="hover:text-amber-400">Terms of Service</a>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Login;
