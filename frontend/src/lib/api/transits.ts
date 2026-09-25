import { apiFetch } from './client';

export const transitsApi = {
  async getTransitRadar(): Promise<any> {
    return apiFetch<any>('/api/transit/heatmap', { method: 'GET' });
  },

  async getPanchang(): Promise<any> {
    return apiFetch<any>('/panchang', { method: 'GET' });
  },
};
