/**
 * North Indian Kundli chart renderer (Canvas 2D).
 * Draws the classic 4×4 grid with triangular houses.
 * Houses 1-12 are placed in the traditional North Indian layout.
 *
 * Layout map (cell positions in a 4×4 grid, 0-indexed row,col):
 *   [0,1]=H12  [0,2]=H1   [0,3]=H2
 *   [1,0]=H11  center     [1,3]=H3
 *   [2,0]=H10  center     [2,3]=H4
 *   [3,1]=H9   [3,2]=H8   [3,3] is outside -> use bottom row
 *
 * Actual North Indian layout (3×3 outer + center hollow):
 *   H12 | H1  | H2
 *   H11 |     | H3
 *   H10 | H9  | H8   <- bottom row mirrored
 * with H4–H7 on right/bottom continuation...
 *
 * Canonical North Indian diamond-square layout:
 * +----+----+----+
 * | 12 |  1 |  2 |
 * +----+    +----+
 * | 11 |    |  3 |
 * +----+    +----+
 * | 10 |  9 |  8 |  (7, 6, 5, 4 on right side going up)
 * +----+----+----+
 */

const RASHI_ABBR = [
  "Mes","Vri","Mit","Kar","Sim","Kan","Tul","Vri","Dha","Mak","Kum","Min"
];

const RASHI_GLYPHS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"];

/**
 * House positions in the North Indian chart.
 * Each entry: { row, col } in a 4×4 grid (0-indexed).
 * Center cells (rows 1-2, cols 1-2) are hollow (chart name area).
 *
 * Canonical North Indian 4×4 layout:
 * (0,0)=12  (0,1)=1  (0,2)=2  (0,3)=3
 * (1,0)=11  [CENTER] [CENTER] (1,3)=4
 * (2,0)=10  [CENTER] [CENTER] (2,3)=5
 * (3,0)=9   (3,1)=8  (3,2)=7  (3,3)=6
 */
const HOUSE_CELLS = {
  1:  { r:0, c:1 },
  2:  { r:0, c:2 },
  3:  { r:0, c:3 },
  4:  { r:1, c:3 },
  5:  { r:2, c:3 },
  6:  { r:3, c:3 },
  7:  { r:3, c:2 },
  8:  { r:3, c:1 },
  9:  { r:3, c:0 },
  10: { r:2, c:0 },
  11: { r:1, c:0 },
  12: { r:0, c:0 },
};

const PLANET_COLORS = {
  Sun:"#FF6B35", Moon:"#C8D8E8", Mars:"#FF4444", Mercury:"#00CC88",
  Jupiter:"#FFD700", Venus:"#FF69B4", Saturn:"#9CA3AF",
  Rahu:"#8B5CF6", Ketu:"#EC4899",
};

const PLANET_SYMBOLS = {
  Sun: "☉", Moon: "☽", Mars: "♂", Mercury: "☿",
  Jupiter: "♃", Venus: "♀", Saturn: "♄", Rahu: "☊", Ketu: "☋",
};

let currentChartStyle = localStorage.getItem("chartStyle") || "north";

function toggleChartStyle() {
  currentChartStyle = currentChartStyle === "north" ? "south" : "north";
  localStorage.setItem("chartStyle", currentChartStyle);
  window.dispatchEvent(new Event("resize"));
}

function renderChart(canvasId, houseOccupants, lagnaRashi, planets) {
  if (currentChartStyle === "north") {
    renderNorthIndianChart(canvasId, houseOccupants, lagnaRashi, planets);
  } else {
    renderSouthIndianChart(canvasId, houseOccupants, lagnaRashi, planets);
  }
}

/**
 * South Indian Kundli chart renderer (Canvas 2D).
 * 4x4 grid where signs are fixed.
 */
function renderSouthIndianChart(canvasId, houseOccupants, lagnaRashi, planets) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const dpr = window.devicePixelRatio || 1;
  const size = canvas.offsetWidth || 440;
  canvas.width = size * dpr;
  canvas.height = size * dpr;
  canvas.style.width = size + "px";
  canvas.style.height = size + "px";

  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);

  const S = size;
  const CW = S / 4;
  const CH = S / 4;

  // Background
  ctx.fillStyle = "#0d0820";
  ctx.fillRect(0, 0, S, S);

  // Outer border
  ctx.strokeStyle = "#FFD700";
  ctx.lineWidth = 2;
  ctx.strokeRect(2, 2, S - 4, S - 4);

  // Sign positions in 4x4 grid (row, col)
  const SIGN_CELLS = [
    { r: 0, c: 1 }, { r: 0, c: 2 }, { r: 0, c: 3 }, { r: 1, c: 3 },
    { r: 2, c: 3 }, { r: 3, c: 3 }, { r: 3, c: 2 }, { r: 3, c: 1 },
    { r: 3, c: 0 }, { r: 2, c: 0 }, { r: 1, c: 0 }, { r: 0, c: 0 }
  ];

  for (let s = 0; s < 12; s++) {
    const { r, c } = SIGN_CELLS[s];
    const x = c * CW;
    const y = r * CH;

    const isLagna = s === lagnaRashi;
    ctx.fillStyle = isLagna ? "rgba(255,215,0,0.07)" : "#130d2e";
    ctx.fillRect(x, y, CW, CH);
    ctx.strokeStyle = isLagna ? "#FFD700" : "#2e1f6e";
    ctx.lineWidth = 1;
    ctx.strokeRect(x, y, CW, CH);

    // Sign Name
    ctx.font = `${Math.floor(CW * 0.13)}px Inter, sans-serif`;
    ctx.fillStyle = "#7B6FA0";
    ctx.textAlign = "right";
    ctx.textBaseline = "top";
    ctx.fillText(RASHI_ABBR[s], x + CW * 0.95, y + CH * 0.06);

    if (isLagna) {
        ctx.font = `bold ${Math.floor(CW * 0.18)}px Inter, sans-serif`;
        ctx.fillStyle = "#FFD700";
        ctx.textAlign = "left";
        ctx.fillText("ASC", x + CW * 0.07, y + CH * 0.06);
    }

    // Planets in this sign
    const houseNum = (s - lagnaRashi + 12) % 12 + 1;
    const occupants = houseOccupants[houseNum] || houseOccupants[String(houseNum)] || [];

    const maxCols = 2;
    const pSize = Math.max(Math.floor(CW * 0.18), 10);
    const padX = CW * 0.1;
    const padY = CH * 0.35;
    const lineH = pSize + 2;

    occupants.forEach((pname, i) => {
      const col = i % maxCols;
      const row = Math.floor(i / maxCols);
      const px = x + padX + col * (CW - padX * 2) / maxCols;
      const py = y + padY + row * lineH;

      const color = (planets && planets[pname]) ? planets[pname].color : "#FFFFFF";
      const sym = PLANET_SYMBOLS[pname] || pname[0];

      ctx.font = `bold ${pSize}px Inter, sans-serif`;
      ctx.fillStyle = color;
      ctx.textAlign = "left";
      ctx.fillText(sym + pname.substring(0, 2), px, py);
    });
  }

  // Center logo
  ctx.font = `bold ${Math.floor(S * 0.09)}px serif`;
  ctx.fillStyle = "rgba(255,215,0,0.1)";
  ctx.textAlign = "center";
  ctx.fillText("ॐ", S / 2, S / 2);
}

// ─────────────────────────────────────────────────────
//  Main renderer
// ─────────────────────────────────────────────────────
function renderNorthIndianChart(canvasId, houseOccupants, lagnaRashi, planets) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const dpr  = window.devicePixelRatio || 1;
  const size = canvas.offsetWidth || 440;
  canvas.width  = size * dpr;
  canvas.height = size * dpr;
  canvas.style.width  = size + "px";
  canvas.style.height = size + "px";

  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);

  const S  = size;
  const CW = S / 4;
  const CH = S / 4;

  const isDark = document.documentElement.getAttribute("data-bs-theme") === "dark";
  const bgMain = isDark ? "#121217" : "#fdfbf7";
  const bgLagna = isDark ? "rgba(251, 191, 36, 0.04)" : "rgba(184, 134, 11, 0.04)";
  const borderColor = isDark ? "#27272a" : "#e5dfd3";
  const goldColor = "#b8860b";

  // Background
  ctx.fillStyle = bgMain;
  ctx.fillRect(0, 0, S, S);

  // Outer border
  ctx.strokeStyle = goldColor;
  ctx.lineWidth = 1;
  ctx.strokeRect(4, 4, S-8, S-8);

  // Draw all 12 house cells
  for (let h = 1; h <= 12; h++) {
    const { r, c } = HOUSE_CELLS[h];
    const x = c * CW, y = r * CH;
    const isLagna = h === 1;

    ctx.fillStyle = isLagna ? bgLagna : bgMain;
    ctx.fillRect(x, y, CW, CH);
    ctx.strokeStyle = isLagna ? goldColor : borderColor;
    ctx.lineWidth = isLagna ? 1.5 : 0.8;
    ctx.strokeRect(x, y, CW, CH);

    // Labels
    ctx.font = `bold ${Math.floor(CW * 0.16)}px 'Inter', sans-serif`;
    ctx.fillStyle = isLagna ? goldColor : (isDark ? "#52525b" : "#a1a1aa");
    ctx.textAlign = "left";
    ctx.textBaseline = "top";
    ctx.fillText(h, x + CW * 0.08, y + CH * 0.08);

    const rashiIdx = (lagnaRashi + h - 1) % 12;
    ctx.font = `${Math.floor(CW * 0.12)}px 'Inter', sans-serif`;
    ctx.fillStyle = isDark ? "#71717a" : "#7a6e5e";
    ctx.textAlign = "right";
    ctx.fillText(RASHI_ABBR[rashiIdx], x + CW * 0.92, y + CH * 0.08);

    // Planets
    const occupants = houseOccupants[h] || houseOccupants[String(h)] || [];
    if (occupants.length > 0) {
      const pSize = Math.max(Math.floor(CW * 0.15), 10);
      occupants.forEach((pname, i) => {
        const col = i % 3, row = Math.floor(i / 3);
        ctx.font = `bold ${pSize}px 'Inter', sans-serif`;
        ctx.fillStyle = (planets && planets[pname]) ? planets[pname].color : "#fff";
        ctx.textAlign = "left";
        ctx.fillText(pname.substring(0, 3), x + CW * 0.1 + col * (CW * 0.3), y + CH * 0.35 + row * (pSize + 4));
      });
    }
  }
}

// ─────────────────────────────────────────────────────
//  Draw a single house cell
// ─────────────────────────────────────────────────────
function drawHouseCell(ctx, x, y, w, h, houseNum, lagnaRashi, houseOccupants, planets) {
  // Cell background
  const isLagna = houseNum === 1;
  ctx.fillStyle = isLagna ? "rgba(255,215,0,0.07)" : "#130d2e";
  ctx.fillRect(x, y, w, h);

  // Cell border
  ctx.strokeStyle = isLagna ? "#FFD700" : "#2e1f6e";
  ctx.lineWidth = isLagna ? 1.5 : 1;
  ctx.strokeRect(x, y, w, h);

  // House number (top-left corner)
  ctx.font = `bold ${Math.floor(w * 0.18)}px Inter, sans-serif`;
  ctx.fillStyle = isLagna ? "#FFD700" : "#4a3f7a";
  ctx.textAlign = "left";
  ctx.textBaseline = "top";
  ctx.fillText(houseNum, x + w * 0.07, y + h * 0.06);

  // Rashi name (small, top-right)
  const rashiIdx = (lagnaRashi + houseNum - 1) % 12;
  ctx.font = `${Math.floor(w * 0.13)}px Inter, sans-serif`;
  ctx.fillStyle = "#7B6FA0";
  ctx.textAlign = "right";
  ctx.textBaseline = "top";
  ctx.fillText(RASHI_ABBR[rashiIdx], x + w * 0.95, y + h * 0.06);

  // Rashi glyph (center-background, very subtle)
  ctx.font = `${Math.floor(w * 0.28)}px serif`;
  ctx.fillStyle = "rgba(255,215,0,0.05)";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(RASHI_GLYPHS[rashiIdx], x + w / 2, y + h / 2);

  // Planets in this house
  const occupants = houseOccupants[houseNum] || houseOccupants[String(houseNum)] || [];
  if (occupants.length === 0) return;

  const maxCols = 3;
  const pSize   = Math.max(Math.floor(w * 0.16), 10);
  const padX    = w * 0.1;
  const padY    = h * 0.28;
  const lineH   = pSize + 2;

  occupants.forEach((pname, i) => {
    const col = i % maxCols;
    const row = Math.floor(i / maxCols);
    const px  = x + padX + col * (w - padX * 2) / maxCols;
    const py  = y + padY + row * lineH;

    const color = (planets && planets[pname]) ? planets[pname].color : "#FFFFFF";
    const sym   = PLANET_SYMBOLS[pname] || pname[0];
    const retro = planets && planets[pname] && planets[pname].retrograde;

    ctx.font = `bold ${pSize}px Inter, sans-serif`;
    ctx.fillStyle = color;
    ctx.textAlign = "left";
    ctx.textBaseline = "top";
    ctx.fillText((retro ? "℞" : "") + sym + pname.substring(0, 3), px, py);
  });
}

// ─────────────────────────────────────────────────────
//  Varga (D9, D10, etc.) chart — same grid, different rashis
// ─────────────────────────────────────────────────────
function renderVargaChart(canvasId, varga) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || !varga) return;

  // Build a pseudo house-occupants from varga data
  const lagnaRashi = varga["Lagna"] ? varga["Lagna"].rashi : varga["Lagna"];

  // Handle cases where Lagna might be just an int or a dict
  const lagnaIdx = typeof lagnaRashi === 'object' ? lagnaRashi.rashi : lagnaRashi;

  // Map each planet to its varga rashi, then to house (relative to varga lagna)
  const houseOccupants = {};
  for (let i = 1; i <= 12; i++) houseOccupants[i] = [];

  for (const [pname, data] of Object.entries(varga)) {
    if (pname === "Lagna") continue;
    const rashi = typeof data === 'object' ? data.rashi : data;
    const house = ((rashi - lagnaIdx + 12) % 12) + 1;
    houseOccupants[house].push(pname);
  }

  // Build minimal planets map (just colors)
  const planetsMap = {};
  for (const pname of Object.keys(varga)) {
    planetsMap[pname] = { color: PLANET_COLORS[pname] || "#fff", retrograde: false };
  }

  renderChart(canvasId, houseOccupants, lagnaIdx, planetsMap);
}

// Legacy alias
function renderNavamsaChart(canvasId, navamsa) {
  renderVargaChart(canvasId, navamsa);
}

// ─────────────────────────────────────────────────────
//  Bi-Wheel Chart (Natal + Transit)
// ─────────────────────────────────────────────────────
function renderBiWheelChart(canvasId, natalHouseOccupants, transitHouseOccupants, lagnaRashi, planets) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const dpr = window.devicePixelRatio || 1;
  const size = canvas.offsetWidth || 440;
  canvas.width = size * dpr;
  canvas.height = size * dpr;
  canvas.style.width = size + "px";
  canvas.style.height = size + "px";

  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);

  const S = size;
  const CW = S / 4;
  const CH = S / 4;

  // Background
  ctx.fillStyle = "#0d0820";
  ctx.fillRect(0, 0, S, S);

  // Outer border
  ctx.strokeStyle = "#FFD700";
  ctx.lineWidth = 2;
  ctx.strokeRect(2, 2, S - 4, S - 4);

  // Draw 12 houses
  for (let h = 1; h <= 12; h++) {
    const { r, c } = HOUSE_CELLS[h];
    const x = c * CW, y = r * CH;

    const isLagna = h === 1;
    ctx.fillStyle = isLagna ? "rgba(255,215,0,0.07)" : "#130d2e";
    ctx.fillRect(x, y, CW, CH);
    ctx.strokeStyle = isLagna ? "#FFD700" : "#2e1f6e";
    ctx.lineWidth = 1;
    ctx.strokeRect(x, y, CW, CH);

    // House & Rashi labels
    const rashiIdx = (lagnaRashi + h - 1) % 12;
    ctx.font = `bold ${Math.floor(CW * 0.15)}px Inter, sans-serif`;
    ctx.fillStyle = isLagna ? "#FFD700" : "#4a3f7a";
    ctx.textAlign = "left";
    ctx.textBaseline = "top";
    ctx.fillText(h, x + CW * 0.05, y + CH * 0.05);

    ctx.font = `${Math.floor(CW * 0.12)}px Inter, sans-serif`;
    ctx.fillStyle = "#7B6FA0";
    ctx.textAlign = "right";
    ctx.fillText(RASHI_ABBR[rashiIdx], x + CW * 0.95, y + CH * 0.05);

    // Divider line between Natal (bottom) and Transit (top)
    ctx.strokeStyle = "rgba(255,215,0,0.1)";
    ctx.beginPath();
    ctx.moveTo(x + 5, y + CH * 0.5);
    ctx.lineTo(x + CW - 5, y + CH * 0.5);
    ctx.stroke();

    const pSize = Math.max(Math.floor(CW * 0.14), 9);
    const lineH = pSize + 2;

    // 1. Transit (Top half)
    const tOccupants = transitHouseOccupants[h] || transitHouseOccupants[String(h)] || [];
    tOccupants.forEach((p, i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      ctx.fillStyle = (planets && planets[p]) ? planets[p].color : PLANET_COLORS[p] || "#fff";
      ctx.font = `bold ${pSize}px Inter, sans-serif`;
      ctx.fillText("T:" + p.substring(0, 2), x + 5 + col * (CW / 2), y + CH * 0.15 + row * lineH);
    });

    // 2. Natal (Bottom half)
    const nOccupants = natalHouseOccupants[h] || natalHouseOccupants[String(h)] || [];
    nOccupants.forEach((p, i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      ctx.fillStyle = (planets && planets[p]) ? planets[p].color : PLANET_COLORS[p] || "#fff";
      ctx.font = `bold ${pSize}px Inter, sans-serif`;
      ctx.fillText("N:" + p.substring(0, 2), x + 5 + col * (CW / 2), y + CH * 0.55 + row * lineH);
    });
  }
}

// ─────────────────────────────────────────────────────
//  Visual Aspect Lines (Drishti)
// ─────────────────────────────────────────────────────
function renderAspectLines(canvasId, lagnaRashi, planets) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const size = canvas.width / (window.devicePixelRatio || 1);
  const CW = size / 4, CH = size / 4;

  const houseToCenter = (h) => {
    const { r, c } = HOUSE_CELLS[h];
    return { x: c * CW + CW / 2, y: r * CH + CH / 2 };
  };

  const getDrishtis = (p, rashi) => {
    const aspects = [(rashi + 6) % 12]; // 7th aspect
    if (p === "Mars") aspects.push((rashi + 3) % 12, (rashi + 7) % 12);
    if (p === "Jupiter") aspects.push((rashi + 4) % 12, (rashi + 8) % 12);
    if (p === "Saturn") aspects.push((rashi + 2) % 12, (rashi + 9) % 12);
    if (p === "Rahu" || p === "Ketu") aspects.push((rashi + 4) % 12, (rashi + 8) % 12);
    return aspects;
  };

  ctx.save();
  ctx.globalAlpha = 0.4;
  ctx.setLineDash([5, 5]);

  Object.entries(planets).forEach(([name, data]) => {
    if (name === "Lagna" || !data.house) return;

    const startHouse = data.house;
    const startPos = houseToCenter(startHouse);
    const drishtis = getDrishtis(name, data.rashi);

    drishtis.forEach(targetRashi => {
      const targetHouse = (targetRashi - lagnaRashi + 12) % 12 + 1;
      const endPos = houseToCenter(targetHouse);

      ctx.beginPath();
      ctx.strokeStyle = data.color || PLANET_COLORS[name] || "#fff";
      ctx.lineWidth = 1.5;
      ctx.moveTo(startPos.x, startPos.y);
      ctx.lineTo(endPos.x, endPos.y);
      ctx.stroke();
    });
  });

  ctx.restore();
}

// ─────────────────────────────────────────────────────
//  Shadbala Radar Chart
// ─────────────────────────────────────────────────────
function renderShadbalaRadar(canvasId, planets) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  const labels = ["Sthana", "Dig", "Kala", "Naisargika"];
  const datasets = [];

  const displayPlanets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];

  displayPlanets.forEach(p => {
    const data = planets[p] && planets[p].shadbala_details;
    if (!data) return;

    datasets.push({
      label: p,
      data: [data.sthana_bala, data.dig_bala, data.kala_bala, data.naisargika_bala],
      fill: true,
      backgroundColor: PLANET_COLORS[p] + "33", // 20% opacity
      borderColor: PLANET_COLORS[p],
      pointBackgroundColor: PLANET_COLORS[p],
      pointBorderColor: "#fff",
      pointHoverBackgroundColor: "#fff",
      pointHoverBorderColor: PLANET_COLORS[p],
      hidden: p !== "Sun" // Only show Sun by default to avoid clutter
    });
  });

  new Chart(ctx, {
    type: 'radar',
    data: { labels, datasets },
    options: {
      elements: { line: { borderWidth: 2 } },
      scales: {
        r: {
          angleLines: { color: 'rgba(255,255,255,0.1)' },
          grid: { color: 'rgba(255,255,255,0.1)' },
          pointLabels: { color: '#7B6FA0', font: { size: 12 } },
          ticks: { backdropColor: 'transparent', color: '#4a3f7a', z: 10, stepSize: 20 },
          suggestedMin: 0,
          suggestedMax: 100
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: { color: '#fff', boxWidth: 12, padding: 15 }
        }
      }
    }
  });
}

function updateActivePlanetInfo(pname, planets) {
  const info = planets[pname] && planets[pname].shadbala_details;
  const panel = document.getElementById("active-planet-info");
  if (!info || !panel) return;

  panel.style.display = "block";
  document.getElementById("ap-name").textContent = pname;
  document.getElementById("ap-sthana").textContent = info.sthana_bala;
  document.getElementById("ap-dig").textContent = info.dig_bala;
  document.getElementById("ap-kala").textContent = info.kala_bala;
  document.getElementById("ap-nais").textContent = info.naisargika_bala;
  document.getElementById("ap-total").textContent = info.total_shadbala;

  const vScore = planets[pname].vimsopaka_score || 0;
  document.getElementById("ap-vims").textContent = vScore;
  document.getElementById("ap-vims-bar").style.width = (vScore / 20 * 100) + "%";
}

// ─────────────────────────────────────────────────────
//  Resize handler — redraw on window resize
// ─────────────────────────────────────────────────────
window.addEventListener("resize", () => {
  document.querySelectorAll(".kundli-canvas").forEach(canvas => {
    const chartData  = canvas.dataset.chart;
    const vargaData  = canvas.dataset.varga;
    const natalData  = canvas.dataset.natal;

    if (natalData && chartData) {
       // If both exist, it might be a bi-wheel.
       // However, we need to know the current active view.
       // For simplicity, we'll check if the bi-wheel button is active on the page
       const isBi = document.getElementById('btn-view-biwheel')?.classList.contains('active');
       if (isBi) {
         try {
           const t = JSON.parse(chartData);
           const n = JSON.parse(natalData);
           renderBiWheelChart(canvas.id, n.house_occupants, t.house_occupants, n.lagna.rashi, t.planets);
         } catch(e) {}
         return;
       }
    }

    if (chartData) {
      try {
        const d = JSON.parse(chartData);
        renderChart(canvas.id, d.house_occupants, d.lagna.rashi, d.planets);
      } catch(e) {}
    } else if (vargaData) {
      try {
        renderVargaChart(canvas.id, JSON.parse(vargaData));
      } catch(e) {}
    }
  });
});
