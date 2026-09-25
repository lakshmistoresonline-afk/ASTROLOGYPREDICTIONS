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
    return apiFetch<ChartPayload>('/api/v1/charts', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  },

  async getActiveChart(): Promise<ChartPayload> {
    const res = await apiFetch<{ status: string; chart: ChartPayload }>('/api/v1/dashboard', {
      method: 'GET',
    });
    return res.chart;
  },

  async listSavedCharts(): Promise<any[]> {
    const res = await apiFetch<{ status: string; charts: any[] }>('/api/v1/charts', {
      method: 'GET',
    });
    return res.charts || [];
  },

  async activateChart(cid: string): Promise<void> {
    await apiFetch(`/api/v1/charts/${encodeURIComponent(cid)}/activate`, {
      method: 'POST',
    });
  },

  async deleteChart(cid: string): Promise<void> {
    await apiFetch(`/api/v1/charts/${encodeURIComponent(cid)}`, {
      method: 'DELETE',
    });
  },
};
