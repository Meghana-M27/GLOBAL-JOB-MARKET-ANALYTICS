/**
 * frontend/public/js/charts.js
 * Chart.js configuration, factory functions, and colour palette.
 * Reference file — mirrors the embedded chart logic in index.html.
 */

'use strict';

// ── COLOUR PALETTE ────────────────────────────────────────────────
const PALETTE = [
  '#00e5ff','#8b5cf6','#f97316','#10b981','#f59e0b',
  '#f472b6','#818cf8','#34d399','#fb923c','#60a5fa',
  '#a78bfa','#6ee7b7','#fcd34d','#f9a8d4','#93c5fd'
];

const CHART_BG    = '#0a1120';
const AXIS_STYLE  = { grid: { color: 'rgba(26,45,74,.5)' }, ticks: { color: '#5a7599' } };
const BASE_LAYOUT = {
  paper_bgcolor: '#0a1120', plot_bgcolor: '#0a1120',
  font: { color: '#5a7599', family: "'DM Sans', sans-serif" },
  margin: { l: 20, r: 20, t: 40, b: 20 },
  legend: { labels: { color: '#dde8f8', boxWidth: 12, padding: 14 } }
};

// Active chart registry
const ChartRegistry = {};

// ── DESTROY HELPER ────────────────────────────────────────────────
function destroyChart(id) {
  if (ChartRegistry[id]) {
    ChartRegistry[id].destroy();
    delete ChartRegistry[id];
  }
}

// ── BASE OPTIONS ──────────────────────────────────────────────────
function baseOptions(extraScales = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { labels: { color: '#dde8f8', boxWidth: 12, padding: 14 } }
    },
    scales: {
      x: { ...AXIS_STYLE },
      y: { ...AXIS_STYLE },
      ...extraScales
    }
  };
}

// ── USD TICK FORMATTER ────────────────────────────────────────────
function usdTick(value) {
  return value >= 1000 ? `$${(value / 1000).toFixed(0)}k` : `$${value}`;
}

// ── BAR CHART ─────────────────────────────────────────────────────
function createBarChart(canvasId, labels, values, label = 'Value', horizontal = false) {
  destroyChart(canvasId);
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx) return null;

  const opts = baseOptions();
  if (horizontal) {
    opts.indexAxis = 'y';
    opts.scales.x.ticks.callback = usdTick;
  } else {
    opts.scales.y.ticks.callback = usdTick;
  }

  ChartRegistry[canvasId] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label,
        data: values,
        backgroundColor: PALETTE.map(c => c + 'bb'),
        borderColor: PALETTE,
        borderWidth: 1.5,
        borderRadius: 6,
      }]
    },
    options: opts
  });
  return ChartRegistry[canvasId];
}

// ── LINE CHART ────────────────────────────────────────────────────
function createLineChart(canvasId, labels, datasets) {
  destroyChart(canvasId);
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx) return null;

  const opts = baseOptions();
  opts.scales.y.ticks.callback = usdTick;

  const chartDatasets = datasets.map((ds, i) => ({
    label: ds.label,
    data: ds.data,
    borderColor: PALETTE[i % PALETTE.length],
    backgroundColor: PALETTE[i % PALETTE.length] + '15',
    tension: 0.45,
    fill: ds.fill || false,
    pointRadius: 5,
    pointHoverRadius: 7,
    borderWidth: 2,
    ...ds.extra
  }));

  ChartRegistry[canvasId] = new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: chartDatasets },
    options: opts
  });
  return ChartRegistry[canvasId];
}

// ── DOUGHNUT CHART ────────────────────────────────────────────────
function createDoughnut(canvasId, labels, values, cutout = '65%') {
  destroyChart(canvasId);
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx) return null;

  ChartRegistry[canvasId] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: PALETTE.map(c => c + 'cc'),
        borderColor: '#0a1120',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout,
      plugins: {
        legend: { position: 'right', labels: { color: '#dde8f8', font: { size: 11 }, padding: 10 } }
      }
    }
  });
  return ChartRegistry[canvasId];
}

// ── GROUPED BAR CHART ─────────────────────────────────────────────
function createGroupedBar(canvasId, labels, datasets) {
  destroyChart(canvasId);
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx) return null;

  const opts = baseOptions();
  opts.scales.y.ticks.callback = usdTick;

  ChartRegistry[canvasId] = new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets },
    options: { ...opts, scales: { ...opts.scales } }
  });
  return ChartRegistry[canvasId];
}

// ── BUBBLE CHART (GDP scatter) ────────────────────────────────────
function createBubble(canvasId, datasets) {
  destroyChart(canvasId);
  const ctx = document.getElementById(canvasId)?.getContext('2d');
  if (!ctx) return null;

  const opts = baseOptions();
  opts.scales.x.ticks.callback = usdTick;
  opts.scales.y.ticks.callback = usdTick;

  ChartRegistry[canvasId] = new Chart(ctx, {
    type: 'bubble',
    data: { datasets },
    options: opts
  });
  return ChartRegistry[canvasId];
}

// ── EXPORT UTILITIES ──────────────────────────────────────────────
function downloadChart(canvasId, filename = 'chart.png') {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const link = document.createElement('a');
  link.download = filename;
  link.href = canvas.toDataURL('image/png');
  link.click();
}

function destroyAll() {
  Object.keys(ChartRegistry).forEach(id => destroyChart(id));
}

// Export for module usage
if (typeof module !== 'undefined') {
  module.exports = { createBarChart, createLineChart, createDoughnut, createGroupedBar, createBubble, downloadChart, destroyAll, PALETTE };
}
