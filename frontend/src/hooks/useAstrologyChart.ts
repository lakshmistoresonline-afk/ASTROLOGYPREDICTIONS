import { useState, useEffect } from 'react';
import { ChartPayload, BirthDetails } from '../types/astrology';

export interface UseAstrologyChartReturn {
  data: ChartPayload | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useAstrologyChart = (
  apiEndpoint: string,
  authToken: string | null,
  birthDetails: BirthDetails
): UseAstrologyChartReturn => {
  const [data, setData] = useState<ChartPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchChart = async () => {
    setLoading(true);
    setError(null);

    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
      }

      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          dob: birthDetails.dob,
          tob: birthDetails.tob,
          latitude: birthDetails.lat,
          longitude: birthDetails.lng,
          timezone: birthDetails.timezone || 'Asia/Kolkata',
        }),
      });

      if (!response.ok) {
        throw new Error(`Calculation Engine Error (${response.status}): ${response.statusText}`);
      }

      const payload: ChartPayload = await response.json();
      setData(payload);
    } catch (err: any) {
      setError(err?.message || 'Failed to calculate astrological chart.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchChart();
  }, [apiEndpoint, authToken, birthDetails.dob, birthDetails.tob, birthDetails.lat, birthDetails.lng, birthDetails.timezone]);

  return { data, loading, error, refetch: fetchChart };
};
