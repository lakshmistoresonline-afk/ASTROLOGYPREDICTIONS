#!/bin/bash
# Swiss Ephemeris C-to-WASM Emscripten Compilation Pipeline (Module 29)
echo "Building Swiss Ephemeris swisseph.wasm with maximum performance optimization (-O3)..."

emcc swisseph/src/*.c \
  -O3 \
  -s WASM=1 \
  -s ALLOW_MEMORY_GROWTH=1 \
  -s EXPORTED_FUNCTIONS='["_swe_calc_ut", "_swe_houses", "_swe_houses_ex", "_swe_set_topocentric", "_swe_set_sid_mode"]' \
  -s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap"]' \
  -o ../frontend/lib/wasm/swisseph.js

echo "Swiss Ephemeris WASM compilation completed successfully."
