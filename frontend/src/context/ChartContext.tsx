import React, { createContext, useContext, useState, useEffect } from 'react';
import { chartsApi, CreateProfileParams } from '../lib/api/charts';
import { ChartPayload } from '../types/astrology';

export interface ChartContextType {
  activeChart: ChartPayload | null;
  savedCharts: any[];
  loading: boolean;
  error: string | null;
  refreshActiveChart: () => Promise<void>;
  createChart: (params: CreateProfileParams) => Promise<void>;
  activateChart: (cid: string) => Promise<void>;
  deleteChart: (cid: string) => Promise<void>;
}

const ChartContext = createContext<ChartContextType | undefined>(undefined);

export const ChartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeChart, setActiveChart] = useState<ChartPayload | null>(null);
  const [savedCharts, setSavedCharts] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const refreshActiveChart = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await chartsApi.getActiveChart();
      if (data && data.planets) {
        setActiveChart(data);
      }
      const list = await chartsApi.listSavedCharts();
      setSavedCharts(list || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load active chart from server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshActiveChart();
  }, []);

  const createChart = async (params: CreateProfileParams) => {
    setLoading(true);
    setError(null);
    try {
      await chartsApi.calculateChart(params);
      await refreshActiveChart();
    } catch (err: any) {
      setError(err.message || 'Failed to calculate and save birth profile.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const activateChart = async (cid: string) => {
    setLoading(true);
    try {
      await chartsApi.getActiveChart();
      await refreshActiveChart();
    } finally {
      setLoading(false);
    }
  };

  const deleteChart = async (cid: string) => {
    setLoading(true);
    try {
      await refreshActiveChart();
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChartContext.Provider
      value={{
        activeChart,
        savedCharts,
        loading,
        error,
        refreshActiveChart,
        createChart,
        activateChart,
        deleteChart,
      }}
    >
      {children}
    </ChartContext.Provider>
  );
};

export const useChart = (): ChartContextType => {
  const context = useContext(ChartContext);
  if (!context) {
    throw new Error('useChart must be used within a ChartProvider');
  }
  return context;
};
