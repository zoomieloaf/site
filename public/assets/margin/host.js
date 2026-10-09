// A stand-in for VS Code: hands Margin's real webview a sample file and keeps the edits in memory.
// Nothing is saved or sent anywhere.
(() => {
  const SAMPLE = `# Launch plan

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
`;

  // Light or dark: from the parent page (#light / #dark, or a message), otherwise the system setting.
  const pick = () => (location.hash === '#dark' ? 'dark' : location.hash === '#light' ? 'light' : matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  // VS Code puts its colour variables on the root element, and Margin reads them from there.
  const setTheme = (t) => { const c = t === 'dark' ? 'vscode-dark' : 'vscode-light'; document.documentElement.className = c; document.body.className = c; };
  setTheme(pick());
  addEventListener('message', (e) => { if (e.data && e.data.type === 'zl-theme') setTheme(e.data.theme); });

  const host = { text: SAMPLE, version: 1 };
  const send = (m) => window.postMessage(m, '*');
  const apply = (text, edits) => {
    for (const e of [...edits].sort((a, b) => b.start - a.start)) text = text.slice(0, e.start) + e.text + text.slice(e.end);
    return text;
  };
  window.acquireVsCodeApi = () => ({
    setState() {}, getState() { return null; },
    postMessage(m) {
      if (m.type === 'ready') send({ type: 'init', text: host.text, version: host.version, mode: 'preview', settings: { outlineVisible: false, ai: 'off', aiEditor: false }, baseUri: location.href });
      if (m.type === 'edit') {
        if (m.version !== host.version) { send({ type: 'reset', text: host.text, version: host.version }); return; }
        host.text = apply(host.text, m.edits);
        host.version++;
        const ack = { type: 'ack', version: host.version, seq: m.seq };
        setTimeout(() => send(ack), 5);
      }
      if (m.type === 'resync') send({ type: 'reset', text: host.text, version: host.version });
    },
  });
})();
