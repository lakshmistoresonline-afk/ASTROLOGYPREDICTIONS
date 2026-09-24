import React, { useState } from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';

export interface ProfileNewProps {
  onProfileCreated?: (profile: any) => void;
}

export const ProfileNew: React.FC<ProfileNewProps> = ({ onProfileCreated }) => {
  const [name, setName] = useState<string>('Mahatma Gandhi');
  const [dob, setDob] = useState<string>('1869-10-02');
  const [tob, setTob] = useState<string>('08:36');
  const [place, setPlace] = useState<string>('Porbandar, Gujarat, India');
  const [latitude, setLatitude] = useState<number>(21.6417);
  const [longitude, setLongitude] = useState<number>(69.6293);
  const [timezone, setTimezone] = useState<string>('Asia/Kolkata');

  const quickCities = [
    { name: 'Palakkad', lat: 10.7867, lon: 76.6548, tz: 'Asia/Kolkata' },
    { name: 'Porbandar', lat: 21.6417, lon: 69.6293, tz: 'Asia/Kolkata' },
    { name: 'New Delhi', lat: 28.6139, lon: 77.2090, tz: 'Asia/Kolkata' },
    { name: 'London', lat: 51.5074, lon: -0.1278, tz: 'Europe/London' },
    { name: 'New York', lat: 40.7128, lon: -74.0060, tz: 'America/New_York' },
  ];

  const handleCitySelect = (c: any) => {
    setPlace(`${c.name}`);
    setLatitude(c.lat);
    setLongitude(c.lon);
    setTimezone(c.tz);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const profile = { name, dob, tob, place, latitude, longitude, timezone };
    if (onProfileCreated) {
      onProfileCreated(profile);
    }
  };

  return (
    <DashboardLayout activeRoute="vault" userProfileName={name}>
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="backdrop-blur-xl bg-slate-900/60 border border-white/10 rounded-2xl shadow-2xl p-8 space-y-6">
          <div className="border-b border-slate-800 pb-4">
            <h2 className="text-2xl font-bold font-serif text-white">Create Natal Chart Profile</h2>
            <p className="text-xs text-slate-400 font-mono">
              Precision Swiss Ephemeris Geocentric & Topocentric Calculation Baseline
            </p>
          </div>

          {/* Quick City Selector Pills */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300 font-mono block">Quick City Preset:</label>
            <div className="flex flex-wrap gap-2">
              {quickCities.map((c) => {
                const isSelected = place.includes(c.name);
                return (
                  <button
                    key={c.name}
                    type="button"
                    onClick={() => handleCitySelect(c)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-mono transition-all ${
                      isSelected
                        ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 font-bold'
                        : 'bg-slate-800/60 text-slate-400 border border-slate-700/60 hover:text-white hover:bg-slate-800'
                    }`}
                  >
                    📍 {c.name}
                  </button>
                );
              })}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4 text-xs font-sans">
            <div className="space-y-1.5">
              <label className="text-slate-300 font-semibold block">Full Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-sans"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-slate-300 font-semibold block">Date of Birth</label>
                <input
                  type="date"
                  value={dob}
                  onChange={(e) => setDob(e.target.value)}
                  required
                  className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-mono"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-slate-300 font-semibold block">Time of Birth (Local)</label>
                <input
                  type="time"
                  value={tob}
                  onChange={(e) => setTob(e.target.value)}
                  required
                  className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-mono"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-slate-300 font-semibold block">Latitude (° N)</label>
                <input
                  type="number"
                  step="0.0001"
                  value={latitude}
                  onChange={(e) => setLatitude(parseFloat(e.target.value))}
                  required
                  className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-mono"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-slate-300 font-semibold block">Longitude (° E)</label>
                <input
                  type="number"
                  step="0.0001"
                  value={longitude}
                  onChange={(e) => setLongitude(parseFloat(e.target.value))}
                  required
                  className="w-full px-4 py-3 bg-slate-800/80 border border-slate-700/80 rounded-xl text-slate-100 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all font-mono"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-3.5 px-4 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs shadow-lg shadow-sky-500/20 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2"
            >
              COMPUTE CANONICAL CHART →
            </button>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ProfileNew;
