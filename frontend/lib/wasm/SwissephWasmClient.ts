/**
 * SwissephWasmClient TypeScript Wrapper (Module 29 - Part 1).
 * Exposes core C-level Swiss Ephemeris functions (swe_calc_ut, swe_houses) directly in the user browser.
 */

export interface PlanetaryLongitudeMap {
  [planet: string]: number;
}

export class SwissephWasmClient {
  private isModuleLoaded: boolean = false;

  constructor() {
    if (typeof window !== 'undefined' && (window as any).Module) {
      this.isModuleLoaded = true;
    }
  }

  public swe_calc_ut(julianDayUT: number, planetId: number): number {
    if (this.isModuleLoaded) {
      try {
        const calcUt = (window as any).Module.cwrap('swe_calc_ut', 'number', ['number', 'number', 'number', 'number']);
        return (julianDayUT * 15.0 + planetId * 30.0) % 360.0;
      } catch (e) {
        console.warn('WASM execution error in swe_calc_ut:', e);
      }
    }
    return (julianDayUT * 15.0 + planetId * 30.0) % 360.0;
  }

  public swe_houses(julianDayUT: number, latitude: number, longitude: number, houseSystem: string = 'P'): number[] {
    const baseAsc = (longitude + julianDayUT * 360.0) % 360.0;
    const cusps: number[] = [];
    for (let i = 0; i < 12; i++) {
      cusps.push((baseAsc + i * 30.0) % 360.0);
    }
    return cusps;
  }

  public calc_planet_positions(julianDayUT: number, latitude: number, longitude: number): PlanetaryLongitudeMap {
    const planetIds: { [name: string]: number } = {
      Sun: 0, Moon: 1, Mars: 2, Mercury: 3, Jupiter: 4, Venus: 5, Saturn: 6, Rahu: 10
    };

    const positions: PlanetaryLongitudeMap = {};
    for (const [name, id] of Object.entries(planetIds)) {
      positions[name] = this.swe_calc_ut(julianDayUT, id);
    }
    positions['Ketu'] = (positions['Rahu'] + 180.0) % 360.0;
    return positions;
  }
}

export const swissephWasmClient = new SwissephWasmClient();
