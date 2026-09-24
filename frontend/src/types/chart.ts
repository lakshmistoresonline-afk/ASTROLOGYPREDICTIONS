export interface PlanetPosition {
  id: string;
  name: string;
  glyph: string;
  degree: number; // 0 - 360 absolute longitude
  signDegree: number; // 0 - 30 degree in sign
  rashi: string;
  house: number; // 1 - 12
  nakshatra: string;
  pada: number; // 1 - 4
  isRetrograde: boolean;
  functionalPowerPct: number; // 0 - 100
}

export interface HouseCusp {
  house: number; // 1 - 12
  degree: number; // 0 - 360
  rashi: string;
}

export interface AspectLine {
  sourcePlanet: string;
  targetPlanet: string;
  aspectType: string; // Conjunction, Trine, Square, Opposition, Sextile
  orbDegree: number;
}

export interface BirthDetails {
  dob: string; // YYYY-MM-DD
  tob: string; // HH:MM
  lat: number;
  lng: number;
}

export interface ChartDataPayload {
  sha256Fingerprint: string;
  ascendantDegree: number;
  planets: PlanetPosition[];
  houseCusps: HouseCusp[];
  aspects: AspectLine[];
}
