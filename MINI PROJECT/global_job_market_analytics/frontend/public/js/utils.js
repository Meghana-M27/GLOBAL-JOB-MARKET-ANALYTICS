/**
 * frontend/public/js/utils.js
 * Shared JS utilities — formatting, DOM helpers, data transforms.
 */

'use strict';

// ── NUMBER FORMATTERS ─────────────────────────────────────────────
function fmtUSD(value) {
  if (!value) return '$0';
  return '$' + (value >= 1000 ? (value / 1000).toFixed(0) + 'k' : Math.round(value));
}

function fmtUSDFull(value) {
  return '$' + Math.round(value || 0).toLocaleString();
}

function fmtPct(value, showPlus = true) {
  const rounded = +(value || 0).toFixed(1);
  return (showPlus && rounded >= 0 ? '+' : '') + rounded + '%';
}

function fmtNumber(value) {
  return (value || 0).toLocaleString();
}

// ── DOM HELPERS ───────────────────────────────────────────────────
function el(id) { return document.getElementById(id); }

function setHTML(id, html) {
  const elem = el(id);
  if (elem) elem.innerHTML = html;
}

function show(id) { const e = el(id); if (e) e.style.display = ''; }
function hide(id) { const e = el(id); if (e) e.style.display = 'none'; }

function showLoader(text = 'Loading...') {
  const loader = el('loader');
  const ltxt   = el('ltxt');
  if (loader) loader.style.display = 'flex';
  if (ltxt)   ltxt.textContent = text;
}

function hideLoader() {
  const loader = el('loader');
  if (loader) loader.style.display = 'none';
}

// ── TAB SWITCHER ──────────────────────────────────────────────────
function switchTab(n) {
  document.querySelectorAll('.tab-btn').forEach((b, i) => b.classList.toggle('active', i === n));
  document.querySelectorAll('.tab-pane').forEach((p, i) => p.classList.toggle('active', i === n));
}

// ── DATA TRANSFORMS ───────────────────────────────────────────────
function groupBy(arr, key) {
  return arr.reduce((acc, item) => {
    const k = item[key];
    if (!acc[k]) acc[k] = [];
    acc[k].push(item);
    return acc;
  }, {});
}

function sortByKey(arr, key, desc = true) {
  return [...arr].sort((a, b) => desc ? b[key] - a[key] : a[key] - b[key]);
}

function avgOf(arr, key) {
  if (!arr.length) return 0;
  return arr.reduce((s, r) => s + (r[key] || 0), 0) / arr.length;
}

function maxOf(arr, key) { return Math.max(...arr.map(r => r[key] || 0)); }
function minOf(arr, key) { return Math.min(...arr.map(r => r[key] || 0)); }

// ── DEMAND STATUS ─────────────────────────────────────────────────
function classifyDemand(growthPct) {
  if (growthPct > 5)  return { status: 'Growing',   color: '#10b981', icon: '↑', chip: 'up' };
  if (growthPct < -3) return { status: 'Declining',  color: '#ef4444', icon: '↓', chip: 'dn' };
  return               { status: 'Stable',    color: '#f59e0b', icon: '→', chip: 'nt' };
}

// ── RANK BADGE ────────────────────────────────────────────────────
function rankBadge(i) {
  const cls = i === 0 ? 'g' : i === 1 ? 's' : i === 2 ? 'b' : '';
  return `<span class="rank ${cls}">${i + 1}</span>`;
}

// ── WORK MODE BADGE ───────────────────────────────────────────────
function modeBadge(mode) {
  const cls = { Onsite: 'on', Hybrid: 'hy', Remote: 're' }[mode] || 'hy';
  return `<span class="wbadge ${cls}">${mode}</span>`;
}

// ── DEBOUNCE ──────────────────────────────────────────────────────
function debounce(fn, delay = 300) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), delay); };
}

if (typeof module !== 'undefined') {
  module.exports = { fmtUSD, fmtUSDFull, fmtPct, fmtNumber, groupBy, sortByKey, avgOf, classifyDemand, rankBadge, modeBadge, debounce };
}
