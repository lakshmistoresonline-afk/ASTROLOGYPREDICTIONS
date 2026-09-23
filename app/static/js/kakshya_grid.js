/**
 * Kakshya Heatmap & Transit Radar Grid Widget (Module 11 - Task 11.2).
 * Visual 12-sign x 8-Kakshya grid displaying active planetary transits.
 * Green: Kakshya lord BAV bindu = 1.
 * Amber/Red: Kakshya lord BAV bindu = 0 or active SBC Vedha.
 */

function renderKakshyaHeatmap(containerId, kakshyaData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const rashiNames = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
    const kakshyaLords = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Lagna"];

    let html = `<div class="table-responsive"><table class="table table-dark table-bordered text-center xxsmall font-mono">`;
    html += `<thead><tr class="text-gold"><th>Rashi / Kakshya</th>`;
    kakshyaLords.forEach(lord => { html += `<th>${lord}</th>`; });
    html += `</tr></thead><tbody>`;

    for (let r = 0; r < 12; r++) {
        html += `<tr><td class="fw-bold text-white">${rashiNames[r]}</td>`;
        for (let k = 0; k < 8; k++) {
            // Check active transit status
            const activeTransit = (kakshyaData && kakshyaData.rashi === r && kakshyaData.kakshya_index === k);
            const isHigh = activeTransit && kakshyaData.has_bav_bindu;

            let bgClass = "bg-dark bg-opacity-40";
            if (activeTransit) {
                bgClass = isHigh ? "bg-success text-white fw-bold shadow" : "bg-warning text-dark fw-bold";
            }

            html += `<td class="${bgClass}">${activeTransit ? (isHigh ? '⚡ 1' : '0') : '•'}</td>`;
        }
        html += `</tr>`;
    }

    html += `</tbody></table></div>`;
    container.innerHTML = html;
}
