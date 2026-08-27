/**
 * JYOTISH RENDERING ENGINE — Definitive High-Contrast Version
 */

const RASHI_ABBR = ["Mes","Vri","Mit","Kar","Sim","Kan","Tul","Vri","Dha","Mak","Kum","Min"];
const PLANET_COLORS = {
  Sun:"#FF6B35", Moon:"#C8D8E8", Mars:"#FF4444", Mercury:"#00CC88",
  Jupiter:"#FFD700", Venus:"#FF69B4", Saturn:"#9CA3AF",
  Rahu:"#8B5CF6", Ketu:"#EC4899", Gulika: "#64748b", Mandi: "#475569"
};

function renderNorthIndianChart(canvasId, houseOccupants, lagnaRashi, planets) {
  console.log("ENGINE: Rendering", canvasId, {houseOccupants, lagnaRashi});
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const size = 440;

  canvas.width = size * dpr;
  canvas.height = size * dpr;
  canvas.style.width = "440px"; // Force visibility
  canvas.style.height = "440px";
  canvas.style.display = "block";
  canvas.style.margin = "0 auto";
  ctx.scale(dpr, dpr);

  const S = size;
  const isDark = document.documentElement.getAttribute("data-bs-theme") === "dark";

  const colors = {
    bg: isDark ? "#0a0a10" : "#ffffff",
    lines: "#fbbf24", // Solid gold geometric frame
    text: isDark ? "#f8fafc" : "#1e293b",
    dim: isDark ? "#71717a" : "#a1a1aa"
  };

  // 1. Background
  ctx.fillStyle = colors.bg;
  ctx.fillRect(0, 0, S, S);

  // 2. Geometric Frame (High Contrast)
  ctx.strokeStyle = colors.lines;
  ctx.lineWidth = 3;
  ctx.lineJoin = "round";

  // Outer Box
  ctx.strokeRect(4, 4, S-8, S-8);

  // X-Cross
  ctx.beginPath();
  ctx.moveTo(4, 4); ctx.lineTo(S-4, S-4);
  ctx.moveTo(S-4, 4); ctx.lineTo(4, S-4);
  ctx.stroke();

  // Inner Diamond
  ctx.beginPath();
  ctx.moveTo(S/2, 4); ctx.lineTo(S-4, S/2);
  ctx.lineTo(S/2, S-4); ctx.lineTo(4, S/2);
  ctx.closePath();
  ctx.stroke();

  // 3. House Center Coordinates
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

    // Planets (Occupants)
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
    console.log("South Indian Renderer not implemented in this version.");
}

// Global Resize logic
window.addEventListener("resize", () => {
    const canvases = document.querySelectorAll(".kundli-canvas");
    canvases.forEach(canvas => {
        const dataAttr = canvas.getAttribute('data-chart');
        if (dataAttr) {
            try {
                const d = JSON.parse(dataAttr);
                renderNorthIndianChart(canvas.id, d.house_occupants, d.lagna.rashi, d.planets);
            } catch(e) {}
        }
    });
});
