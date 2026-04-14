/**
 * frontend/public/js/filters.js
 * Sidebar filter state management and auto-trigger logic.
 */

'use strict';

const FilterState = {
  country: '',
  role: '',
  mode: 'Hybrid',

  get() {
    return { country: this.country, role: this.role, mode: this.mode };
  },

  set(key, value) {
    if (key in this) {
      this[key] = value;
      this.onChange();
    }
  },

  onChange() {
    // Debounce — wait 150ms before triggering analyse
    clearTimeout(FilterState._timer);
    FilterState._timer = setTimeout(() => {
      if (typeof analyse === 'function') analyse();
    }, 150);
  },

  _timer: null
};

// Bind selects to FilterState on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const selCountry = document.getElementById('sel-c');
  const selRole    = document.getElementById('sel-r');
  const selMode    = document.getElementById('sel-m');

  if (selCountry) selCountry.addEventListener('change', e => FilterState.set('country', e.target.value));
  if (selRole)    selRole.addEventListener('change',    e => FilterState.set('role', e.target.value));
  if (selMode)    selMode.addEventListener('change',    e => FilterState.set('mode', e.target.value));
});

// Utility — read current filter values from DOM
function getFilters() {
  return {
    country: document.getElementById('sel-c')?.value || '',
    role:    document.getElementById('sel-r')?.value || '',
    mode:    document.getElementById('sel-m')?.value || 'Hybrid',
  };
}

// Utility — reset all filters to defaults
function resetFilters() {
  const defaults = { 'sel-c': '', 'sel-r': '', 'sel-m': 'Hybrid' };
  Object.entries(defaults).forEach(([id, val]) => {
    const el = document.getElementById(id);
    if (el) el.value = val;
  });
  if (typeof analyse === 'function') analyse();
}

if (typeof module !== 'undefined') {
  module.exports = { FilterState, getFilters, resetFilters };
}
