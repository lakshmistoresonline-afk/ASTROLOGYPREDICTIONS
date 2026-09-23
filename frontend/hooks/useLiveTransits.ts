import { useState, useEffect, useRef } from 'react';

export interface TransitPositions {
  [planet: string]: number;
}

export interface LiveTransitPayload {
  stream_event: string;
  timestamp_utc: string;
  julian_day_ut: number;
  transits: TransitPositions;
}

export interface UseLiveTransitsReturn {
  transits: TransitPositions | null;
  timestamp: string | null;
  isConnected: boolean;
  error: string | null;
  reconnectAttempts: number;
}

export const useLiveTransits = (websocketUrl: string = 'ws://localhost:5000/ws/transits/live'): UseLiveTransitsReturn => {
  const [transits, setTransits] = useState<TransitPositions | null>(null);
  const [timestamp, setTimestamp] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [reconnectAttempts, setReconnectAttempts] = useState<number>(0);

  const wsRef = useRef<WebSocket | null>(null);
  const attemptsRef = useRef<number>(0);

  useEffect(() => {
    let isMounted = true;

    const connect = () => {
      try {
        const ws = new WebSocket(websocketUrl);
        wsRef.current = ws;

        ws.onopen = () => {
          if (!isMounted) return;
          setIsConnected(true);
          setError(null);
          attemptsRef.current = 0;
          setReconnectAttempts(0);
        };

        ws.onmessage = (event) => {
          if (!isMounted) return;
          try {
            const data: LiveTransitPayload = JSON.parse(event.data);
            if (data.transits) {
              setTransits(data.transits);
              setTimestamp(data.timestamp_utc);
            }
          } catch (e) {
            console.error('Failed to parse WebSocket transit payload:', e);
          }
        };

        ws.onerror = (err) => {
          if (!isMounted) return;
          setError('WebSocket connection error.');
        };

        ws.onclose = () => {
          if (!isMounted) return;
          setIsConnected(false);

          // Exponential backoff reconnect up to 5 attempts
          if (attemptsRef.current < 5) {
            attemptsRef.current += 1;
            setReconnectAttempts(attemptsRef.current);
            const timeout = Math.min(1000 * Math.pow(2, attemptsRef.current), 16000);
            setTimeout(() => {
              if (isMounted) connect();
            }, timeout);
          } else {
            setError('Max reconnection attempts (5) reached.');
          }
        };
      } catch (e) {
        setError(String(e));
      }
    };

    connect();

    return () => {
      isMounted = false;
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [websocketUrl]);

  return { transits, timestamp, isConnected, error, reconnectAttempts };
};
