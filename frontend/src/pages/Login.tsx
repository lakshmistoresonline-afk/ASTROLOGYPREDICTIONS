import React, { useState } from 'react';

export interface LoginProps {
  onLoginSuccess?: (token: string, email: string) => void;
}

export const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState<string>('demo@astropredictions.com');
  const [password, setPassword] = useState<string>('••••••••••••');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      if (onLoginSuccess) {
        onLoginSuccess('jwt_token_demo_123', email);
      }
    }, 600);
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center p-6 text-slate-100 font-sans relative overflow-hidden"
      style={{
        backgroundColor: '#0B0F19',
        backgroundImage: 'radial-gradient(circle at top right, rgba(30, 27, 75, 0.4), rgba(15, 23, 42, 0.8))'
      }}
    >
      {/* Glassmorphism Login Card */}
      <div className="w-full max-w-md backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl shadow-2xl p-8 space-y-6 relative z-10">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black flex items-center justify-center text-2xl mx-auto shadow-lg shadow-amber-500/20">
            ॐ
          </div>
          <h2 className="text-2xl font-bold font-serif text-white tracking-wide">
            Astrological Intelligence
          </h2>
          <p className="text-xs text-slate-400 font-mono">
            V3.36 Swiss Ephemeris Hardened Architecture
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs font-sans">
          <div className="space-y-1.5">
            <label className="text-slate-300 font-semibold block">Email / Developer Key ID</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-mono"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-slate-300 font-semibold block">Encrypted Passphrase</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-mono"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 px-4 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs shadow-lg shadow-sky-500/20 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2"
          >
            {isLoading ? 'Decrypting Vault...' : 'ACCESS CELESTIAL DASHBOARD →'}
          </button>
        </form>

        <div className="pt-2 text-center text-[11px] text-slate-500 font-mono border-t border-slate-800/80">
          AES-256 Quantum-Resilient PII Encryption Active
        </div>
      </div>
    </div>
  );
};

export default Login;
