/**
 * JYOTISH RENDERING ENGINE — Peak operational architecture.
 */

const RASHI_ABBR = ["Mes","Vri","Mit","Kar","Sim","Kan","Tul","Vri","Dha","Mak","Kum","Min"];
const PLANET_COLORS = {
  Sun:"#FF6B35", Moon:"#C8D8E8", Mars:"#FF4444", Mercury:"#00CC88",
  Jupiter:"#FFD700", Venus:"#FF69B4", Saturn:"#9CA3AF",
  Rahu:"#8B5CF6", Ketu:"#EC4899", Gulika: "#64748b", Mandi: "#475569"
};

function renderNorthIndianChart(canvasId, houseOccupants, lagnaRashi, planets) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const size = 440;

  canvas.width = size * dpr;
  canvas.height = size * dpr;
  canvas.style.width = "100%";
  canvas.style.maxWidth = "440px";
  canvas.style.height = "auto";
  ctx.scale(dpr, dpr);

  const S = size;
  const isDark = document.documentElement.getAttribute("data-bs-theme") === "dark";

  const colors = {
    bg: isDark ? "#0a0a10" : "#ffffff",
    lines: "#fbbf24", // Solid gold
    text: isDark ? "#f8fafc" : "#1e293b",
    dim: isDark ? "#71717a" : "#a1a1aa"
  };

  // 1. Draw Background
  ctx.fillStyle = colors.bg;
  ctx.fillRect(0, 0, S, S);

  // 2. Draw Geometric Frame
  ctx.strokeStyle = colors.lines;
  ctx.lineWidth = 3;
  ctx.lineJoin = "round";

  // Box
  ctx.strokeRect(5, 5, S-10, S-10);

  // Cross (X)
  ctx.beginPath();
  ctx.moveTo(5, 5); ctx.lineTo(S-5, S-5);
  ctx.moveTo(S-5, 5); ctx.lineTo(5, S-5);
  ctx.stroke();

  // Diamond
  ctx.beginPath();
  ctx.moveTo(S/2, 5); ctx.lineTo(S-5, S/2);
  ctx.lineTo(S/2, S-5); ctx.lineTo(5, S/2);
  ctx.closePath();
  ctx.stroke();

  // 3. Define House Center Coordinates (Geometric Logic)
  const centers = {
    1:  { x: S/2,    y: S/4 + 20 },
    2:  { x: S/4 + 10, y: S/8 + 10 },
    3:  { x: S/8 + 10, y: S/4 + 10 },
    4:  { x: S/4 + 20, y: S/2    },
    5:  { x: S/8 + 10, y: 3*S/4 - 10 },
    6:  { x: S/4 + 10, y: 7*S/8 - 10 },
    7:  { x: S/2,    y: 3*S/4 - 20 },
    8:  { x: 3*S/4 - 10, y: 7*S/8 - 10 },
    9:  { x: 7*S/8 - 10, y: 3*S/4 - 10 },
    10: { x: 3*S/4 - 20, y: S/2    },
    11: { x: 7*S/8 - 10, y: S/4 + 10 },
    12: { x: 3*S/4 - 10, y: S/8 + 10 }
  };

  // 4. Render Data
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  for (let h = 1; h <= 12; h++) {
    const cp = centers[h];
    const rashiIdx = ((lagnaRashi || 0) + h - 1) % 12;

    // Rashi Number (Sign)
    ctx.font = "bold 22px 'Inter', sans-serif";
    ctx.fillStyle = (h === 1) ? "#fbbf24" : colors.dim;
    ctx.fillText(rashiIdx + 1, cp.x, cp.y - 35);

    // Planets
    const occupants = houseOccupants[h] || houseOccupants[String(h)] || [];
    if (occupants.length > 0) {
      const pSize = 17;
      ctx.font = `bold ${pSize}px 'Inter', sans-serif`;

      occupants.forEach((p, i) => {
        const pColor = (planets && planets[p]) ? planets[p].color : (PLANET_COLORS[p] || "#fff");
        ctx.fillStyle = pColor;
        const rowOffset = (i * (pSize + 5));
        ctx.fillText(p.substring(0, 2), cp.x, cp.y + rowOffset);
      });
    }
  }

  // 5. Center Motif
  ctx.font = "40px serif";
  ctx.fillStyle = "rgba(251, 191, 36, 0.1)";
  ctx.fillText("ॐ", S/2, S/2);
}

function renderSouthIndianChart(canvasId, houseOccupants, lagnaRashi, planets) {
    // Simplified South Indian implementation
}

function safeParseJSON(str) {
    if (!str) return {};
    try {
        // Handle cases where the string might be double-escaped or contain HTML entities
        const doc = new DOMParser().parseFromString(str, 'text/html');
        const unescaped = doc.documentElement.textContent;
        return JSON.parse(unescaped || str);
    } catch (e) {
        console.error("JSON PARSE ERROR:", e, "SOURCE STR:", str);
        return {};
    }
}

window.addEventListener("resize", () => {
    document.querySelectorAll(".kundli-canvas").forEach(canvas => {
        const d = safeParseJSON(canvas.dataset.chart);
        if (d.house_occupants) {
            renderNorthIndianChart(canvas.id, d.house_occupants, d.lagna.rashi, d.planets);
        }
    });
});
