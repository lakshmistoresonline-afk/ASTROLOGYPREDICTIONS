export interface Planet {
  id: string;
  name: string;
  glyph: string;
  degree: number; // 0° - 360° total longitude
  signDegree: number; // 0° - 30° within sign
  rashi: string;
  house: number; // 1 - 12
  nakshatra: string;
  pada: number; // 1 - 4
  isRetrograde: boolean;
  functionalPowerPct: number; // 0 - 100
}

export interface HouseCusp {
  house: number; // 1 - 12
  degree: number; // 0° - 360°
  rashi: string;
}

export interface Aspect {
  sourcePlanet: string;
  targetPlanet: string;
  aspectType: 'conjunction' | 'opposition' | 'trine' | 'square' | 'sextile';
  orbDegree: number;
}

export interface BirthDetails {
  dob: string; // YYYY-MM-DD
  tob: string; // HH:MM
  lat: number;
  lng: number;
  timezone?: string;
}

export interface ChartPayload {
  sha256Fingerprint: string;
  ascendantDegree: number;
  planets: Planet[];
  houseCusps: HouseCusp[];
  aspects: Aspect[];
}
