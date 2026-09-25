import type { AppProps } from 'next/app';
import { AuthProvider } from '../context/AuthContext';
import { ChartProvider } from '../context/ChartContext';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <ChartProvider>
        <Component {...pageProps} />
      </ChartProvider>
    </AuthProvider>
  );
}
