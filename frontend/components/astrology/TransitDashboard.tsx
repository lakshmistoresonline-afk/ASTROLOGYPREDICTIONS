import React from 'react';
import { useLiveTransits } from '../../hooks/useLiveTransits';

export interface TransitDashboardProps {
  websocketUrl?: string;
}

export const TransitDashboard: React.FC<TransitDashboardProps> = ({
  websocketUrl = 'ws://localhost:5000/ws/transits/live'
}) => {
  const { transits, timestamp, isConnected, error, reconnectAttempts } = useLiveTransits(websocketUrl);

  return (
    <div className="backdrop-blur-md bg-slate-900/60 border border-slate-800/80 shadow-2xl rounded-2xl p-6 text-white space-y-4">
      {/* Header & Status Indicator */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-xl font-bold font-serif text-cyan-400">Real-Time Transit Dashboard</h3>
          <p className="text-xs text-slate-400 font-mono">
            WebSocket Stream • 1Hz High-Precision Ephemeris Sync
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className={`w-3 h-3 rounded-full ${isConnected ? 'bg-emerald-400 animate-ping' : 'bg-rose-500'}`} />
            <span className="text-xs font-mono font-bold text-slate-300">
              {isConnected ? 'LIVE STREAMING' : reconnectAttempts > 0 ? `RECONNECTING (${reconnectAttempts}/5)` : 'DISCONNECTED'}
            </span>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-xl text-xs font-mono">
          ⚠️ {error}
        </div>
      )}

      {/* Timestamp Bar */}
      {timestamp && (
        <div className="text-xs text-slate-400 font-mono flex justify-between bg-slate-800/40 p-2 px-3 rounded-lg border border-slate-800">
          <span>UTC Timestamp: <strong className="text-white">{timestamp}</strong></span>
          <span className="text-amber-400 fw-bold">Live Kakshya & Vedha Radar Active</span>
        </div>
      )}

      {/* Planetary Positions Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        {transits ? (
          Object.entries(transits).map(([planet, lon]) => {
            const rashiIdx = Math.floor(lon / 30);
            const deg = lon % 30;
            const rashiNames = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];

            return (
              <div
                key={planet}
                className="p-3 bg-slate-800/50 border border-slate-700/60 rounded-xl hover:border-cyan-500/40 transition-all flex flex-col justify-between"
              >
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-amber-400">{planet}</span>
                  <span className="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-1.5 py-0.5 rounded border border-cyan-500/20">
                    {rashiNames[rashiIdx]}
                  </span>
                </div>
                <div className="mt-2 text-lg font-mono font-bold text-white">
                  {deg.toFixed(2)}°
                </div>
                <div className="text-[10px] text-slate-400 font-mono mt-1">
                  Absolute: {lon.toFixed(2)}°
                </div>
              </div>
            );
          })
        ) : (
          <div className="col-span-full py-8 text-center text-slate-400 text-xs font-mono">
            Awaiting WebSocket transit stream payload...
          </div>
        )}
      </div>

      {/* Real-Time SBC Vedha & Kakshya Pulse Indicators */}
      <div className="pt-2 border-t border-slate-800 flex flex-wrap justify-between items-center gap-3 text-xs text-slate-300">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
          <span>Kakshya BAV Bindu Active (High-Confluence)</span>
        </div>
        <div class="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-amber-400" />
          <span>SBC Vedha Clear Flow</span>
        </div>
      </div>
    </div>
  );
};
