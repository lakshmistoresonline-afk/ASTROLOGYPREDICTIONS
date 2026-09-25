import { apiFetch } from './client';

export const predictionsApi = {
  async getPredictions(): Promise<any> {
    return apiFetch<any>('/predictions', { method: 'GET' });
  },

  async getDomainExplanation(domain: string): Promise<any> {
    return apiFetch<any>(`/api/v1/predict/explain/${encodeURIComponent(domain)}`, { method: 'GET' });
  },

  async getTimelineRoadmap(): Promise<any> {
    return apiFetch<any>('/timeline', { method: 'GET' });
  },
};
