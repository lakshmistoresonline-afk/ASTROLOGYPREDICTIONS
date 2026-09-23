#!/bin/bash
# Emscripten Compilation Script for Swiss Ephemeris C Source to swisseph.wasm
echo "Building Swiss Ephemeris C-to-WASM binary..."

emcc swisseph/src/*.c \
  -O3 \
  -s WASM=1 \
  -s EXPORTED_FUNCTIONS='["_swe_calc_ut", "_swe_houses_ex", "_swe_set_topocentric", "_swe_set_sid_mode"]' \
  -s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap"]' \
  -o ../frontend/lib/ephemeris/swisseph.js

echo "Swiss Ephemeris WASM build completed successfully."
