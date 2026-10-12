// A stand-in for VS Code around Margin's real webview: a few sample files, the Explorer and the
// editor tab. Edits are kept in memory per file while the page is open. Nothing is saved or sent.
(() => {
  const FILES = {
    'handbook.md': `# Crew handbook: Station Margin

Welcome aboard. The station runs on plain Markdown files, so this handbook will outlive the hardware. Everything here is live: the real editor, running in your browser.

> [!TIP]
> You're in Edit mode, so just start typing. **Ctrl+E** switches to Preview, the page as readers see it.

## Your first shift

- [ ] **Select a few words.** A menu floats up over them: bold, highlight, link, turn into a heading, and ✨ AI.
- [ ] **Hover a block** and look left: **+** adds a block below, **⋮⋮** drags it or opens its options.
- [ ] **Type \`/\`** on an empty line for to-dos, callouts, tables and code.
- [ ] Follow a link: the [airlock procedure](airlock.md) opens as a page, and Back brings you here.

## Try AI on this

The coffee machine on deck three is broken again and nobody really knows who is supposed to fix it, so please do not touch it until somebody from engineering has had a look at it, which might be tomorrow.

Select the paragraph above, click **✨ AI** and pick **Shorten**, or **Translate** it for the night shift.
`,
    'airlock.md': `# Airlock procedure

Back to the [crew handbook](handbook.md). What went wrong last time is in the [captain's log](log.md).

> [!WARNING]
> Both doors open at once only in the movies.

1. Check your suit. Then check it again.
2. Close the inner door.
3. Wait for the **green** light. Not the orange one.

| Light | Means |
| --- | --- |
| Green | Go |
| Orange | Someone is in the shower |
| Red | Go back to step 1 |
`,
    'log.md': `# Captain's log

Back to the [airlock procedure](airlock.md).

- [x] Day 1: coffee machine installed on deck three
- [x] Day 2: coffee machine broken on deck three
- [ ] Day 3: find out who renamed the reactor to \`reactor-final-v2\`
- [ ] Day 4: teach the plants to water themselves

\`\`\`bash
station status --deck 3   # coffee: offline, morale: offline
\`\`\`
`,
  };

  // Margin's AI, simulated: canned answers for the coffee paragraph, streamed like a real model.
  const COFFEE = {
    improve: 'The coffee machine on deck three is broken again. Please leave it alone until engineering has checked it, which may be tomorrow.',
    shorten: 'Coffee machine, deck three: broken. Hands off until engineering checks it.',
    longer: 'The coffee machine on deck three is broken again and nobody really knows who is supposed to fix it, so please do not touch it until somebody from engineering has had a look at it, which might be tomorrow. Until then, the galley on deck two has a working kettle, and the emergency instant coffee is in the locker marked "Do not open". Open it.',
    grammar: 'The coffee machine on deck three is broken again, and nobody really knows who is supposed to fix it. Please don\'t touch it until someone from engineering has had a look, which might be tomorrow.',
    summarize: 'Deck three coffee machine is broken; wait for engineering.',
    continue: 'Until then, the emergency instant coffee is in the locker marked "Do not open". Open it.',
    ask: 'Coffee machine on deck three: out of order. Engineering will look at it soon, possibly tomorrow. Please don\'t touch it.',
  };
  const TRANSLATED = {
    Russian: 'Кофемашина на третьей палубе снова сломалась, и никто толком не знает, кто должен её чинить, поэтому, пожалуйста, не трогайте её, пока кто-нибудь из инженеров на неё не посмотрит. Возможно, завтра.',
    German: 'Die Kaffeemaschine auf Deck drei ist schon wieder kaputt, und niemand weiß so genau, wer sie reparieren soll. Bitte nicht anfassen, bis jemand von der Technik sie sich angesehen hat, vielleicht morgen.',
    French: 'La machine à café du pont trois est encore en panne, et personne ne sait vraiment qui doit la réparer. Merci de ne pas y toucher avant qu\'un ingénieur l\'ait examinée, peut-être demain.',
    Spanish: 'La cafetera de la cubierta tres se ha vuelto a romper y nadie sabe muy bien quién tiene que arreglarla, así que no la toquéis hasta que alguien de ingeniería le eche un vistazo, quizá mañana.',
    Chinese: '三号甲板的咖啡机又坏了，也没人知道该由谁来修。在工程部的人来看之前请不要碰它，可能要等到明天。',
    Japanese: '第3デッキのコーヒーマシンがまた壊れました。誰が直すのかよく分かっていないので、エンジニアが見るまで触らないでください。たぶん明日です。',
    English: 'The coffee machine on deck three is broken again. Please don\'t touch it until engineering has looked at it, maybe tomorrow.',
  };
  const answer = (m) => {
    if (!/coffee machine/i.test(m.markdown)) return 'This demo only knows the coffee paragraph. In your editor, Margin runs AI on any text with GitHub Copilot or your editor\'s chat.';
    if (m.action === 'translate') return TRANSLATED[m.lang] || TRANSLATED.German;
    return COFFEE[m.action] || COFFEE.improve;
  };
  const streams = new Map();
  function stream(m) {
    const words = answer(m).match(/\S+\s*/g) || [];
    let i = 0;
    const timer = setInterval(() => {
      if (i < words.length) return send({ type: 'aiChunk', id: m.id, text: words.slice(i, (i += 2)).join('') });
      clearInterval(timer);
      streams.delete(m.id);
      send({ type: 'aiDone', id: m.id });
    }, 45);
    streams.set(m.id, timer);
  }

  // ?bare shows only Margin's editor, without the VS Code window around it (the home page uses this).
  if (new URLSearchParams(location.search).has('bare')) document.documentElement.dataset.bare = '';

  // The demo opens in Edit mode, and Margin then focuses the page. Inside a website that would take
  // the keyboard away from the page around it, so focus waits until the visitor clicks or taps in.
  if (window !== top) {
    let touched = false;
    addEventListener('pointerdown', () => { touched = true; }, { capture: true, once: true });
    addEventListener('focusin', (e) => {
      if (touched) return;
      e.target.blur?.();
      try { parent.focus(); } catch {}
    }, true);
  }

  // Light or dark: from the parent page (#light / #dark, or a message), otherwise the system setting.
  const pick = () => (location.hash === '#dark' ? 'dark' : location.hash === '#light' ? 'light' : matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  // VS Code puts its colour variables on the root element, and Margin reads them from there.
  const setTheme = (t) => { const c = t === 'dark' ? 'vscode-dark' : 'vscode-light'; document.documentElement.className = c; document.body.className = c; };
  setTheme(pick());
  addEventListener('message', (e) => { if (e.data && e.data.type === 'zl-theme') setTheme(e.data.theme); });

  let current = 'handbook.md';
  let version = 1;
  const back = [], forward = [];
  const send = (m) => window.postMessage(m, '*');
  const apply = (text, edits) => {
    for (const e of [...edits].sort((a, b) => b.start - a.start)) text = text.slice(0, e.start) + e.text + text.slice(e.end);
    return text;
  };
  // "./airlock.md#lights" -> ["airlock.md", "lights"]
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
          send({ type: 'init', text: FILES[current], version, mode: 'edit', settings: { outlineVisible: false, ai: 'editor', aiEditor: true }, baseUri: location.href });
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
        case 'ai': stream(m); break;
        case 'aiCancel': clearInterval(streams.get(m.id)); streams.delete(m.id); break;
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
