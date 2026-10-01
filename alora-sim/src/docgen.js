'use strict';
/* =====================================================================================================
   Practice documents: made-up referral, order, face-to-face and insurance card pages (SVG).
   Every page says SAMPLE DOCUMENT FOR TRAINING. They contain no real person.
   ===================================================================================================== */
function svgEsc(s) { return String(s == null ? '' : s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])); }
function docSvg(kind, o) {
  o = o || {}; const name = o.name || 'DOE, JOHN', dob = o.dob || '01/01/1950', date = o.date ? (/^\d{4}-/.test(o.date) ? fmtD(o.date) : o.date) : '09/26/2026';
  const phys = o.phys || 'SAMPLE, ALEX MD', npi = o.npi || '1000000002';
  const T = (x, y, s, sz, w, fill, extra, ff) => `<text x="${x}" y="${y}" font-family="${ff || 'Arial, Helvetica, sans-serif'}" font-size="${sz || 20}" font-weight="${w || 400}" fill="${fill || '#222'}" ${extra || ''}>${svgEsc(s)}</text>`;
  const L = (x1, y1, x2, y2, c) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c || '#333'}" stroke-width="1.5"/>`;
  let body = '', title = '';
  const sign = (x, y, who, when, signed) => (signed === false ? T(x, y - 8, '(not signed)', 18, 400, '#b00', 'font-style="italic"') + L(x, y, x + 320, y) + T(x, y + 22, who, 15, 400, '#555') : T(x + 10, y - 8, o.sigName || who.replace(/,.*/, '').toLowerCase().replace(/^./, c => c.toUpperCase()), 30, 400, '#1a3a8a', 'font-style="italic"', 'Brush Script MT, Segoe Script, cursive') + L(x, y, x + 320, y) + T(x, y + 22, who + '   Date signed: ' + (when || date), 15, 400, '#555'));
  if (kind === 'referral' || kind === 'wrong') {
    title = 'REFERRAL FOR HOME HEALTH SERVICES';
    body = T(60, 200, 'Sample General Hospital (practice)', 24, 700, '#1d3a7a') + T(60, 228, 'Discharge Planning Office', 18, 400, '#555') + T(60, 300, 'Patient name:', 20, 700) + T(220, 300, name, 22) + T(60, 340, 'Date of birth:', 20, 700) + T(220, 340, dob, 22) + T(60, 380, 'Referral date:', 20, 700) + T(220, 380, date, 22) +
      T(60, 420, 'Phone:', 20, 700) + T(220, 420, '(954) 555-0000', 22) + T(60, 480, 'Diagnosis:', 20, 700) + T(220, 480, o.dx || 'Heart failure, unspecified (practice)', 22) + T(60, 540, 'Services requested:', 20, 700) + T(60, 575, 'Skilled nursing, physical therapy, home health aide', 21) +
      T(60, 640, 'Insurance:', 20, 700) + T(220, 640, o.payer || 'Medicare (practice)', 22) + T(60, 700, 'Referring physician:', 20, 700) + T(260, 700, phys + '   NPI ' + npi, 22) + sign(60, 860, phys, date, true);
  } else if (kind === 'order' || kind === 'order_unsigned') {
    title = 'PHYSICIAN ORDER';
    body = T(60, 200, 'Sample Family Clinic (practice)', 24, 700, '#1d3a7a') + T(60, 300, 'Patient:', 20, 700) + T(220, 300, name, 22) + T(60, 340, 'Date of birth:', 20, 700) + T(220, 340, dob, 22) + T(60, 380, 'Order date:', 20, 700) + T(220, 380, date, 22) +
      T(60, 460, 'Order:', 20, 700) + T(60, 500, 'Home health: skilled nursing, physical therapy and home health aide.', 21) + T(60, 535, 'Evaluate and treat. Start of care per agency assessment.', 21) + T(60, 570, 'Frequency per plan of care.', 21) +
      T(60, 700, 'Physician: ' + phys, 20, 400) + T(60, 732, 'NPI: ' + npi, 20, 400) + sign(60, 860, phys, date, kind === 'order');
  } else if (kind === 'f2f' || kind === 'f2f_old') {
    title = 'FACE-TO-FACE ENCOUNTER';
    const enc = o.enc ? (/^\d{4}-/.test(o.enc) ? fmtD(o.enc) : o.enc) : (kind === 'f2f_old' ? '05/01/2026' : '09/18/2026');
    body = T(60, 200, 'Sample General Hospital (practice)', 24, 700, '#1d3a7a') + T(60, 300, 'Patient:', 20, 700) + T(220, 300, name, 22) + T(60, 340, 'Date of birth:', 20, 700) + T(220, 340, dob, 22) +
      T(60, 400, 'Date of face-to-face encounter:', 20, 700) + T(400, 400, enc, 24, 700, '#1d3a7a') + T(60, 440, 'Seen by:', 20, 700) + T(220, 440, phys + ' (physician)', 22) +
      T(60, 500, 'Clinical findings:', 20, 700) + T(60, 535, 'Shortness of breath with exertion. Leg swelling. Needs help with', 20) + T(60, 565, 'medicines and walking. Practice text only.', 20) +
      T(60, 625, 'The encounter was related to the primary reason the patient needs home health.', 19) + T(60, 655, 'The patient is homebound (practice statement).', 19) + sign(60, 860, phys, enc, true);
  } else if (kind === 'insurance') {
    title = 'INSURANCE CARD COPY (front and back)';
    body = `<rect x="80" y="220" width="690" height="400" rx="26" fill="#e9f2fb" stroke="#1d3a7a" stroke-width="3"/>` + T(120, 290, 'PRACTICE HEALTH PLAN', 34, 700, '#1d3a7a') + T(120, 350, name, 28, 700) + T(120, 400, 'Member ID: ' + (o.member || 'PRACTICE-0001'), 24) + T(120, 440, 'Group: 000000', 22) + T(120, 480, 'Effective: ' + date, 22) + T(120, 580, 'SAMPLE ONLY. NOT A REAL CARD.', 22, 700, '#b00') +
      `<rect x="80" y="660" width="690" height="260" rx="26" fill="#f4f4f4" stroke="#1d3a7a" stroke-width="3"/>` + T(120, 720, 'Back of card (practice)', 24, 700, '#555') + T(120, 765, 'Member services: (800) 555-0100', 22);
  } else if (kind === 'facesheet') {
    title = 'FACE SHEET';
    body = T(60, 230, 'Name:', 20, 700) + T(260, 230, name, 22) + T(60, 270, 'Date of birth:', 20, 700) + T(260, 270, dob, 22) + T(60, 310, 'Address:', 20, 700) + T(260, 310, o.addr || '210 Sample Street, Tamarac FL 33321', 22) + T(60, 350, 'Phone:', 20, 700) + T(260, 350, '(954) 555-0201', 22) + T(60, 390, 'Insurance:', 20, 700) + T(260, 390, o.payer || 'Medicare (practice)', 22) + T(60, 430, 'Emergency contact:', 20, 700) + T(260, 430, 'Luis Sample (954) 555-0203', 22);
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="850" height="1100" viewBox="0 0 850 1100"><rect width="850" height="1100" fill="#fff"/><rect x="20" y="20" width="810" height="1060" fill="none" stroke="#999" stroke-width="2"/>` +
    T(425, 110, title, 30, 700, '#111', 'text-anchor="middle"') + L(60, 135, 790, 135, '#1d3a7a') + body +
    `<g transform="rotate(-28 425 560)"><text x="425" y="590" text-anchor="middle" font-family="Arial, sans-serif" font-size="58" font-weight="700" fill="#d33" opacity=".16">SAMPLE FOR TRAINING</text></g>` +
    T(425, 1050, 'SAMPLE DOCUMENT FOR TRAINING. NOT A REAL RECORD. NO REAL PERSON.', 15, 700, '#a00', 'text-anchor="middle"') + '</svg>';
}
function docUrl(kind, o) { return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(docSvg(kind, o)); }
