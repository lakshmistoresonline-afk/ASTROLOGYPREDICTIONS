import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

export interface DashboardLayoutProps {
  children: React.ReactNode;
  activeRoute?: string;
  userProfileName?: string;
  onNavigate?: (route: string) => void;
  onSearch?: (query: string) => void;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  activeRoute = 'dashboard',
  userProfileName = 'Subramanian T S',
  onNavigate,
  onSearch
}) => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-amber-500 selection:text-slate-950 flex">
      {/* Background Ambient Celestial Halos */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute -top-40 -left-40 w-[600px] h-[600px] bg-indigo-950/20 rounded-full blur-[140px]" />
        <div className="absolute top-1/3 -right-40 w-[500px] h-[500px] bg-slate-900/30 rounded-full blur-[140px]" />
        <div className="absolute -bottom-40 left-1/3 w-[600px] h-[600px] bg-amber-950/15 rounded-full blur-[140px]" />
      </div>

      {/* 2-Column App Shell: Sidebar Left */}
      <Sidebar activeRoute={activeRoute} userProfileName={userProfileName} onNavigate={onNavigate} />

      {/* Main Workspace Right */}
      <div className="flex-1 flex flex-col min-w-0 z-10">
        <Header userProfileName={userProfileName} onSearch={onSearch} />
        <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
};
