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
    <div
      className="min-h-screen text-slate-100 font-sans selection:bg-sky-500 selection:text-slate-950 flex"
      style={{
        backgroundColor: '#0B0F19',
        backgroundImage: 'radial-gradient(circle at top right, rgba(30, 27, 75, 0.4), rgba(15, 23, 42, 0.8))'
      }}
    >
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
