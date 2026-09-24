import React, { useState } from 'react';

export interface HeaderProps {
  userProfileName?: string;
  onSearch?: (query: string) => void;
}

export const Header: React.FC<HeaderProps> = ({
  userProfileName = 'Subramanian T S',
  onSearch
}) => {
  const [searchQuery, setSearchQuery] = useState<string>('');

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setSearchQuery(val);
    if (onSearch) {
      onSearch(val);
    }
  };

  return (
    <header className="sticky top-0 z-30 backdrop-blur-xl bg-slate-950/80 border-b border-slate-800/80 px-6 py-3.5 flex flex-wrap items-center justify-between gap-4 shadow-xl">
      {/* Search Input Bar */}
      <div className="relative flex-1 max-w-md hidden sm:block">
        <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500 text-xs">
          🔍
        </span>
        <input
          type="text"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search domains, transits, charts, aspects..."
          className="w-full pl-9 pr-4 py-2 bg-slate-900/60 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-sans"
        />
      </div>

      {/* Top-Right Live Transit Pills & Profile Badge */}
      <div className="flex items-center gap-3 ml-auto">
        <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/80 border border-amber-500/30 text-[11px] font-mono shadow-sm">
          <span className="text-amber-400 font-bold">🌕 TRANSIT FOCUS:</span>
          <span className="text-slate-200">VENUS IN LIBRA (9TH HOUSE)</span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs font-mono">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
          <span className="text-slate-300 font-semibold">{userProfileName}</span>
        </div>
      </div>
    </header>
  );
};
