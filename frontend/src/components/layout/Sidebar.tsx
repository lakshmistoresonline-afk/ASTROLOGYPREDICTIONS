import React from 'react';

export interface SidebarProps {
  activeRoute?: string;
  userProfileName?: string;
  onNavigate?: (route: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeRoute = 'dashboard',
  userProfileName = 'Subramanian T S',
  onNavigate
}) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '⚡', isPrimary: true },
    { id: 'birth-chart', label: 'Birth Chart', icon: '🧭' },
    { id: 'forecasts', label: 'Forecasts & Domains', icon: '🔮' },
    { id: 'life-atlas', label: 'Life Atlas', icon: '📅' },
    { id: 'cosmic-dna', label: 'Cosmic DNA', icon: '🧬' },
    { id: 'compatibility', label: 'Compatibility (Guna Milan)', icon: '💖' },
    { id: 'transits', label: 'Transit Calendar', icon: '🌕' },
    { id: 'export-pdf', label: 'Export PDF Report', icon: '📄', isGold: true },
    { id: 'vault', label: 'Vault & Profiles', icon: '📁', isDivider: true },
  ];

  const handleNavClick = (id: string) => {
    if (onNavigate) {
      onNavigate(id);
    }
  };

  return (
    <aside className="w-64 bg-slate-950/80 backdrop-blur-2xl border-r border-slate-800/80 min-h-screen flex flex-col justify-between p-4 sticky top-0 z-40">
      <div className="space-y-6">
        {/* Brand Logo Header */}
        <div className="flex items-center gap-3 px-2 py-1">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black flex items-center justify-center text-xl shadow-lg shadow-amber-500/20">
            ॐ
          </div>
          <div>
            <h1 className="text-sm font-bold font-serif text-white tracking-widest uppercase">
              ASTRO PREDICTIONS
            </h1>
            <p className="text-[10px] text-amber-400 font-mono font-semibold tracking-wider">
              DARK CELESTIAL AI
            </p>
          </div>
        </div>

        {/* Navigation Menu Links */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const isActive = activeRoute === item.id;
            return (
              <React.Fragment key={item.id}>
                {item.isDivider && <div className="my-3 border-t border-slate-800/80" />}
                <button
                  onClick={() => handleNavClick(item.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30 shadow-lg shadow-amber-500/5 font-bold'
                      : item.isGold
                      ? 'text-amber-300 hover:bg-amber-500/10 hover:border-amber-500/20 border border-transparent'
                      : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/40 border border-transparent'
                  }`}
                >
                  <span className="text-base">{item.icon}</span>
                  <span>{item.label}</span>
                </button>
              </React.Fragment>
            );
          })}
        </nav>
      </div>

      {/* User Profile Card Footer */}
      <div className="pt-3 border-t border-slate-800/80">
        <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2 overflow-hidden">
            <div className="w-8 h-8 rounded-full bg-amber-500 text-slate-950 font-bold flex items-center justify-center text-xs flex-shrink-0">
              {userProfileName[0].toUpperCase()}
            </div>
            <div className="truncate text-left">
              <div className="text-xs font-bold text-white truncate">{userProfileName}</div>
              <div className="text-[10px] text-slate-500 font-mono">V3.36 Active</div>
            </div>
          </div>
          <span className="text-xs text-slate-400 hover:text-amber-400 cursor-pointer">⚙️</span>
        </div>
      </div>
    </aside>
  );
};
