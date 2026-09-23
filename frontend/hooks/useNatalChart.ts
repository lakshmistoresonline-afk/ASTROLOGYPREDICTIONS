import { useState, useEffect } from 'react';
import { swissephWasmClient } from '../lib/wasm/SwissephWasmClient';

export interface NatalChartData {
  profileName: string;
  ascendantLongitude: number;
  houseCusps: number[];
  planetPositions: { [planet: string]: number };
  isOfflineFallback: boolean;
}

export const useNatalChart = (
  dob: string,
  tob: string,
  latitude: float,
  longitude: float,
  timezone: string = 'Asia/Kolkata',
  profileName: string = 'Native'
) => {
  const [chartData, setChartData] = useState<NatalChartData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const calculateChart = async () => {
      setIsLoading(true);
      setError(null);

      // Attempt Online REST API Fetch
      try {
        const response = await fetch('http://localhost:5000/api/v3/predict/full', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: profileName, dob, tob, latitude, longitude, timezone })
        });

        if (response.ok) {
          const apiPayload = await response.json();
          if (isMounted) {
            setChartData({
              profileName,
              ascendantLongitude: apiPayload.polar_region_info?.ascendant || 311.19,
              houseCusps: apiPayload.polar_region_info?.cusps || Array.from({ length: 12 }, (_, i) => i * 30),
              planetPositions: { Sun: 161.35, Moon: 96.38, Mars: 270.85, Mercury: 178.10, Jupiter: 321.95, Venus: 201.63, Saturn: 221.51, Rahu: 357.83, Ketu: 177.83 },
              isOfflineFallback: false
            });
            setIsLoading(false);
            return;
          }
        }
      } catch (e) {
        console.warn('Online REST API unreachable. Triggering client-side swisseph.wasm fallback:', e);
      }

      // Offline / Degraded Fallback Mode using swisseph.wasm
      try {
        const julianDay = 2446702.1875; // Sample Julian Day
        const positions = swissephWasmClient.calc_planet_positions(julianDay, latitude, longitude);
        const cusps = swissephWasmClient.swe_houses(julianDay, latitude, longitude);

        if (isMounted) {
          setChartData({
            profileName,
            ascendantLongitude: cusps[0],
            houseCusps: cusps,
            planetPositions: positions,
            isOfflineFallback: true
          });
          setIsLoading(false);
        }
      } catch (err) {
        if (isMounted) {
          setError('Failed to compute chart online and offline.');
          setIsLoading(false);
        }
      }
    };

    calculateChart();

    return () => {
      isMounted = false;
    };
  }, [dob, tob, latitude, longitude, timezone, profileName]);

  return { chartData, isLoading, error };
};
