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
      className="min-h-screen flex flex-col items-center justify-center p-6 text-slate-100 font-sans relative overflow-hidden"
      style={{
        backgroundColor: '#0B0F19',
        backgroundImage: 'radial-gradient(circle at top right, rgba(30, 27, 75, 0.4), rgba(15, 23, 42, 0.8))'
      }}
    >
      {/* Production Glassmorphism Login Card */}
      <div className="w-full max-w-md backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl shadow-2xl p-8 space-y-6 relative z-10">
        <div className="text-center space-y-1.5">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black flex items-center justify-center text-2xl mx-auto shadow-lg shadow-amber-500/20">
            ॐ
          </div>
          <h1 className="text-2xl font-bold font-serif text-white tracking-wider uppercase">
            ASTRO PREDICTIONS
          </h1>
          <p className="text-[10px] text-amber-400 font-mono font-bold tracking-widest uppercase">
            Dark Celestial AI
          </p>
        </div>

        <div className="text-center space-y-1 pt-2">
          <h2 className="text-lg font-bold text-white">Secure Sign In</h2>
          <p className="text-xs text-slate-400 font-sans">
            Secure access to your astrology workspace
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs font-sans">
          <div className="space-y-1.5 text-left">
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

          <div className="space-y-1.5 text-left">
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
  );
};

export default Login;
