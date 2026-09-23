/**
 * 365-Day Rolling Probability & Life Trend Chart Widget (Module 11 & Module 25 - Task 25.4).
 * Renders 5 core life pillar curves with interactive scrubbing and peak confluence tooltips.
 */

document.addEventListener("DOMContentLoaded", () => {
    const canvasElement = document.getElementById("lifeTrendsChart");
    if (!canvasElement) return;
});

function renderLifeTrendsChart(canvasId, timeSeriesData) {
    const canvasElement = document.getElementById(canvasId);
    if (!canvasElement || !timeSeriesData || timeSeriesData.length === 0) {
        return;
    }

    const labels = timeSeriesData.map(d => d.date);
    const career = timeSeriesData.map(d => d.career_momentum);
    const finance = timeSeriesData.map(d => d.financial_liquidity);
    const health = timeSeriesData.map(d => d.vitality_health);
    const relationships = timeSeriesData.map(d => d.relational_harmony);
    const mobility = timeSeriesData.map(d => d.relocation_mobility);

    const ctx = canvasElement.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                { label: 'Career Momentum', data: career, borderColor: '#FBBF24', backgroundColor: 'rgba(251, 191, 36, 0.1)', borderWidth: 2, tension: 0.3 },
                { label: 'Financial Liquidity', data: finance, borderColor: '#34D399', backgroundColor: 'rgba(52, 211, 153, 0.1)', borderWidth: 2, tension: 0.3 },
                { label: 'Physical Vitality', data: health, borderColor: '#F87171', backgroundColor: 'rgba(248, 113, 113, 0.1)', borderWidth: 2, tension: 0.3 },
                { label: 'Relationship Harmony', data: relationships, borderColor: '#EC4899', backgroundColor: 'rgba(236, 72, 153, 0.1)', borderWidth: 2, tension: 0.3 },
                { label: 'Relocation Mobility', data: mobility, borderColor: '#38BDF8', backgroundColor: 'rgba(56, 189, 248, 0.1)', borderWidth: 2, tension: 0.3 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                tooltip: {
                    callbacks: {
                        footer: function(tooltipItems) {
                            let maxScore = 0;
                            tooltipItems.forEach(item => { if (item.parsed.y > maxScore) maxScore = item.parsed.y; });
                            if (maxScore >= 0.80) {
                                return '🌟 PEAK CONFLUENCE WINDOW (>80%)';
                            }
                            return '';
                        }
                    }
                }
            },
            scales: {
                y: { min: 0.0, max: 1.0, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
            }
        }
    });
}
