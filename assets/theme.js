// Runs in <head> so a saved light/dark choice applies before the page paints.
try {
  const t = localStorage.getItem('zl-theme');
  if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t;
} catch {}
