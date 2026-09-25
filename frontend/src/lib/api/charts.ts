import { apiFetch } from './client';
import { ChartPayload } from '../../types/astrology';

export interface CreateProfileParams {
  name: string;
  dob: string;
  tob: string;
  place: string;
  latitude: number;
  longitude: number;
  timezone?: string;
}

export const chartsApi = {
  async calculateChart(params: CreateProfileParams): Promise<ChartPayload> {
    return apiFetch<ChartPayload>('/api/v3/predict/full', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  },

  async getActiveChart(): Promise<ChartPayload> {
    return apiFetch<ChartPayload>('/api/v1/debug/dashboard-data', {
      method: 'GET',
    });
  },

  async listSavedCharts(): Promise<any[]> {
    return apiFetch<any[]>('/my-charts', {
      method: 'GET',
    });
  },
};
