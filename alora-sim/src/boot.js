'use strict';
/* start-up */
document.addEventListener('DOMContentLoaded', () => {
  try { loadDB(); } catch (e) { console.error(e); DB = seedData(); FILES = Object.assign({}, SEED_FILES); }
  if (DB.session.userId && curUser()) { buildShell(); render(); phoneRefresh(); } else { showLogin(); if (location.hash && location.hash !== '#/login') { /* keep the address for after login */ } }
  window.addEventListener('beforeunload', () => { if (DB) save(); });
});
