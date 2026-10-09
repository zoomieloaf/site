// The loaf in the header zooms on click, 5 s after load, then every 18 to 42 s.
const cat = document.querySelector('.zl-catbtn');
const calm = matchMedia('(prefers-reduced-motion: reduce)');
let zooming = false;

function zoom() {
  if (!cat || zooming || calm.matches) return;
  zooming = true;
  cat.classList.add('zl-zoom');
  setTimeout(() => { cat.classList.remove('zl-zoom'); zooming = false; }, 2650);
}
function later(ms) { setTimeout(() => { zoom(); later(18000 + Math.random() * 24000); }, ms); }
if (cat) { cat.addEventListener('click', zoom); later(5000); }

// Light / dark toggle. The choice is kept in this browser only.
const toggle = document.querySelector('.tgl');
if (toggle) toggle.addEventListener('click', () => {
  const root = document.documentElement;
  const dark = root.dataset.theme === 'dark' || (!root.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
  root.dataset.theme = dark ? 'light' : 'dark';
  try { localStorage.setItem('zl-theme', root.dataset.theme); } catch {}
});

// Copy buttons next to install commands.
document.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = 'Copied'; }
  catch { b.textContent = 'Select and copy'; }
  setTimeout(() => (b.textContent = 'Copy'), 1500);
}));

// Margin window: Preview / Markdown, and ticked boxes rewrite exactly their own line.
document.querySelectorAll('.mdmock').forEach((m) => {
  const show = (view) => {
    m.querySelectorAll('[data-view]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.view === view)));
    m.querySelectorAll('[data-pane]').forEach((p) => (p.hidden = p.dataset.pane !== view));
  };
  m.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => show(b.dataset.view)));
  m.querySelectorAll('input[data-line]').forEach((box) => {
    const line = m.querySelector(`[data-src="${box.dataset.line}"]`);
    const was = box.checked;
    box.addEventListener('change', () => {
      line.textContent = line.textContent.replace(/\[.\]/, box.checked ? '[x]' : '[ ]');
      line.classList.toggle('changed', box.checked !== was);
    });
  });
});
