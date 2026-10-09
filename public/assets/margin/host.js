// A stand-in for VS Code around Margin's real webview: a few sample files, the Explorer and the
// editor tab. Edits are kept in memory per file while the page is open. Nothing is saved or sent.
(() => {
  const FILES = {
    'README.md': `# Docs

Notes for the launch. Start with the [launch plan](launch-plan.md), then the [release checklist](release-checklist.md).
`,
    'launch-plan.md': `# Launch plan

Everything before the store listings go live. Steps are in [Release checklist](release-checklist.md).

> [!TIP]
> Press **Ctrl+E**, or double-click any text, to edit right here. Your file stays plain Markdown.

## This week

- [x] Record the demo
- [ ] Write the Open VSX description
- [ ] Proofread the privacy policy

## Stores

| Store | Status |
| --- | --- |
| VS Code Marketplace | Submitted |
| Open VSX | Draft |
`,
    'release-checklist.md': `# Release checklist

Run these before tagging a version. Back to the [launch plan](launch-plan.md).

## Before the tag

- [x] Tests pass on Windows, macOS and Linux
- [x] \`CHANGELOG.md\` has a section for the version
- [ ] Screenshots in the README are current

## Publish

\`\`\`bash
npm run package
npx vsce publish
npx ovsx publish margin-0.1.0.vsix
\`\`\`
`,
  };

  // Light or dark: from the parent page (#light / #dark, or a message), otherwise the system setting.
  const pick = () => (location.hash === '#dark' ? 'dark' : location.hash === '#light' ? 'light' : matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  // VS Code puts its colour variables on the root element, and Margin reads them from there.
  const setTheme = (t) => { const c = t === 'dark' ? 'vscode-dark' : 'vscode-light'; document.documentElement.className = c; document.body.className = c; };
  setTheme(pick());
  addEventListener('message', (e) => { if (e.data && e.data.type === 'zl-theme') setTheme(e.data.theme); });

  let current = 'launch-plan.md';
  let version = 1;
  const back = [], forward = [];
  const send = (m) => window.postMessage(m, '*');
  const apply = (text, edits) => {
    for (const e of [...edits].sort((a, b) => b.start - a.start)) text = text.slice(0, e.start) + e.text + text.slice(e.end);
    return text;
  };
  // "./release-checklist.md#publish" -> ["release-checklist.md", "publish"]
  const resolve = (href) => {
    const [path, anchor] = String(href).split('#');
    const name = decodeURIComponent(path.split('/').pop() || '');
    return { name: path ? name : current, anchor };
  };

  function show(name, anchor) {
    current = name;
    version++;
    send({ type: 'reset', text: FILES[name], version });
    if (anchor) setTimeout(() => send({ type: 'scrollTo', anchor }), 30);
    renderChrome();
  }
  function open(name, anchor) {
    if (!(name in FILES)) return;
    if (name !== current) { back.push(current); forward.length = 0; show(name, anchor); }
    else if (anchor) send({ type: 'scrollTo', anchor });
  }

  function renderChrome() {
    const tab = document.getElementById('tabName');
    if (tab) tab.textContent = current;
    const list = document.getElementById('files');
    if (!list) return;
    list.innerHTML = '';
    for (const name of Object.keys(FILES)) {
      const li = document.createElement('li');
      const b = document.createElement('button');
      b.type = 'button';
      b.innerHTML = '<span class="md-icon" aria-hidden="true">M↓</span>';
      b.append(name);
      if (name === current) b.setAttribute('aria-current', 'true');
      b.addEventListener('click', () => open(name));
      li.append(b);
      list.append(li);
    }
  }
  document.addEventListener('DOMContentLoaded', renderChrome);

  window.acquireVsCodeApi = () => ({
    setState() {}, getState() { return null; },
    postMessage(m) {
      switch (m.type) {
        case 'ready':
          send({ type: 'init', text: FILES[current], version, mode: 'preview', settings: { outlineVisible: false, ai: 'off', aiEditor: false }, baseUri: location.href });
          send({ type: 'navButtons', visible: true });
          break;
        case 'edit': {
          if (m.version !== version) { send({ type: 'reset', text: FILES[current], version }); return; }
          FILES[current] = apply(FILES[current], m.edits);
          version++;
          const ack = { type: 'ack', version, seq: m.seq };
          setTimeout(() => send(ack), 5);
          break;
        }
        case 'resync': send({ type: 'reset', text: FILES[current], version }); break;
        case 'openLink': { const { name, anchor } = resolve(m.href); open(name, anchor); break; }
        case 'navigate':
          if (m.direction === 'back' && back.length) { forward.push(current); show(back.pop()); }
          else if (m.direction === 'forward' && forward.length) { back.push(current); show(forward.pop()); }
          break;
        case 'checkLinks': {
          const local = m.hrefs.filter((h) => !/^[a-z][a-z0-9+.-]*:/i.test(h) && !h.startsWith('#'));
          send({
            type: 'linkStatus',
            missing: local.filter((h) => !(resolve(h).name in FILES)),
            paths: local.map((h) => [h, 'docs/' + resolve(h).name]),
          });
          break;
        }
      }
    },
  });
})();
