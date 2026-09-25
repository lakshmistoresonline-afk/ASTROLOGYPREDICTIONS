import { apiFetch } from './client';

export interface UserSession {
  uid: string;
  email: string;
  displayName: string;
  isAdmin: boolean;
  activeChartId?: string | null;
}

export const authApi = {
  async login(email: string, password?: string): Promise<UserSession> {
    const res = await apiFetch<{ success: boolean; user: UserSession }>('/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    return res.user || {
      uid: `uid_${email.split('@')[0]}`,
      email,
      displayName: email.split('@')[0].toUpperCase(),
      isAdmin: email.includes('admin'),
    };
  },

  async logout(): Promise<void> {
    await apiFetch('/logout', { method: 'GET' });
  },

  async getCurrentSession(): Promise<UserSession | null> {
    try {
      const res = await apiFetch<{ user: UserSession }>('/api/v1/user/settings', { method: 'GET' });
      return res.user;
    } catch {
      return null;
    }
  },
};
