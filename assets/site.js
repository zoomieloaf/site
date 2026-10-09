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
