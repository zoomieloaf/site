"""Writes every page of the site from one shared header and footer.

Run from anywhere: python tools/build.py
Edit the text here, not in the generated HTML files.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent / 'public'
MARGIN_STORE = 'https://marketplace.visualstudio.com/items?itemName=zoomieloaf.margin'
MARGIN_OVSX = 'https://open-vsx.org/extension/zoomieloaf/margin'
CHROME_STORE = '#add-to-chrome'  # replace with the Chrome Web Store link once it's published
GITHUB = 'https://github.com/zoomieloaf'
CMD = 'code --install-extension zoomieloaf.margin'
EFFECTIVE = '9 October 2026'
SHOW_SUM = False  # AI Summarizer isn't published yet; True brings back its page, home row and policy sections

CAT = '''<button class="zl-catbtn" type="button" aria-label="Make the loaf zoom">
<svg class="zl-puff" viewBox="0 0 44 18" aria-hidden="true"><circle cx="11" cy="12" r="5"/><circle cx="22" cy="9" r="6.5"/><circle cx="33" cy="12" r="4.5"/></svg>
<svg class="zl-cat" viewBox="76 14 180 136" aria-hidden="true">
<mask id="zl-eyes"><rect x="76" y="14" width="180" height="136" fill="#fff"/><circle cx="198" cy="76" r="9.5" fill="#000"/><circle cx="227" cy="76" r="9.5" fill="#000"/></mask>
<g class="zl-plain"><rect x="80" y="52" width="152" height="96" rx="48"/><ellipse cx="212" cy="76" rx="40" ry="36"/><path d="M186 54 192 20 211 45ZM217 43 238 18 246 56Z"/></g>
<g class="zl-eyed" mask="url(#zl-eyes)"><rect x="80" y="52" width="152" height="96" rx="48"/><ellipse cx="212" cy="76" rx="40" ry="36"/><path d="M186 54 192 20 211 45ZM217 43 238 18 246 56Z"/></g>
</svg>
</button>'''

TOGGLE = '<button class="tgl" type="button" aria-label="Switch between light and dark theme"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10 3 A7 7 0 0 1 10 17 Z" fill="currentColor"/></svg></button>'

# Margin's own icon (vscode-md/media/icon.svg), in its own colours in both themes.
ICON_MARGIN = '<img class="app-icon" src="{p}assets/margin/icon.png" alt="" width="44" height="44">'
ICON_SUM = '<svg viewBox="0 0 40 40" aria-hidden="true"><rect class="icon-bg" width="40" height="40" rx="9"/><path class="icon-fg bold" d="M10 12 H30 M10 29 H22"/><rect class="icon-fill" x="8" y="17" width="24" height="7" rx="2"/></svg>'

CHECK = '<span class="box done"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 6.2 L5 8.6 L9.6 3.4"/></svg></span>'

# The real Margin editor (Margin's own webview build in assets/margin), running on a sample file.
MOCK_MARGIN = '''<div>
<div class="frame live"><iframe src="{p}embed/margin.html" title="Margin, running live in a small VS Code window with sample files"></iframe></div>
<p class="try">This is the real Margin editor. Switch to Edit or Markdown, tick a box, or open another file.</p>
</div>'''
MOCK_MARGIN_BARE = '''<div>
<div class="frame live"><iframe src="{p}embed/margin.html?bare" title="Margin, running live on a sample file"></iframe></div>
<p class="try">This is the real Margin editor. Switch to Edit or Markdown, tick a box, type something.</p>
</div>'''

MOCK_SUM = '''<div class="frame" role="img" aria-label="AI Summarizer: text selected on a web page, the action bar below it, and a summary answered on the device">
<div class="frame-bar"><span class="url">example.org/why-cats-sleep</span></div>
<div class="mock web">
<div class="serif web-title">Why cats sleep so much</div>
<p class="serif web-text">Cats sleep twelve to sixteen hours a day. <span class="selected">Most of it is light sleep: the ears keep turning toward sounds, and the cat can be up and running in under a second.</span> Deep sleep comes in short stretches.</p>
<div class="aibar"><span>Explain</span><span>Translate</span><span class="on">Summarize</span><span>Fix grammar</span><span>Ask</span><span class="mono key">Alt+Q</span></div>
<div class="answer"><b>Summary</b><span>Cats sleep 12 to 16 hours a day, mostly lightly, so they can wake almost instantly.</span><small>Answered on this device, offline.</small></div>
</div>
</div>'''


def page(path, title, description, body, current='', prefix=None):
    depth = len(pathlib.PurePosixPath(path).parts) - 1
    p = '../' * depth if prefix is None else prefix
    nav = lambda href, label, key: f'<a href="{p}{href}"{" aria-current=\"page\"" if current == key else ""}>{label}</a>'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}assets/site.css">
<script src="{p}assets/theme.js"></script>
<script src="{p}assets/site.js" defer></script>
</head>
<body>
<header class="wrap site-header">
<div class="brand">{CAT}<a href="{p}index.html">ZoomieLoaf</a></div>
<nav class="hnav" aria-label="Main">{nav('margin/index.html', 'Margin', 'margin')}{nav('ai-summarizer/index.html', 'AI Summarizer', 'sum') if SHOW_SUM else ''}{TOGGLE}</nav>
</header>
<main>
{body.replace('{p}', p)}
</main>
<footer class="wrap site-footer">
<div><span>© 2026 ZoomieLoaf</span><nav aria-label="Footer"><a href="mailto:hello@zoomieloaf.com">hello@zoomieloaf.com</a><a href="{GITHUB}">GitHub</a><a href="{p}privacy/index.html">Privacy</a><a href="{p}terms/index.html">Terms</a></nav></div>
</footer>
</body>
</html>
'''
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8', newline='\n')


# ---------- Home ----------
HOME = f'''<section class="wrap intro"><div>
<h1>Small tools for reading and writing.</h1>
<p class="tagline">Mostly loaf. Occasionally zoom.</p>
</div></section>
<div class="wrap products">
<article class="prod" aria-labelledby="p-margin">
<div class="prod-text">
<div class="prod-name">{ICON_MARGIN}<div><h2 id="p-margin"><a href="{{p}}margin/index.html">Margin</a></h2><div class="kind">Extension for VS Code</div></div></div>
<p>Notion-style editing for your Markdown files. Open a <code>.md</code> file as a clean page and edit it in place, with a slash menu, block handles and drag and drop. The file stays plain Markdown, so ticking a checkbox is a one-line diff.</p>
<dl class="facts">
<dt>Works in</dt><dd>VS Code, Cursor, Windsurf, VSCodium</dd>
<dt>Your files</dt><dd>Plain Markdown. Only edited blocks change.</dd>
<dt>Price</dt><dd>Free</dd>
</dl>
<div class="actions"><a class="btn" href="{MARGIN_STORE}">Install for VS Code</a><a class="btn ghost" href="{MARGIN_OVSX}">Install from Open VSX</a><a class="lnk" href="{{p}}margin/index.html">About Margin</a></div>
</div>
{MOCK_MARGIN_BARE}
</article>
{{HOME_SUM}}
</div>'''
HOME_SUM = f'''<article class="prod" aria-labelledby="p-sum">
<div class="prod-text">
<div class="prod-name">{ICON_SUM}<div><h2 id="p-sum"><a href="{{p}}ai-summarizer/index.html">AI Summarizer</a></h2><div class="kind">Extension for Chrome</div></div></div>
<p>Select text on any page to explain, translate, summarize, fix grammar or ask about it. Chat about the page with AI that runs on your device.</p>
<dl class="facts">
<dt>Works in</dt><dd>Chrome</dd>
<dt>Account</dt><dd>None. No sign-up, no API key.</dd>
<dt>AI</dt><dd>On-device, works offline after a one-time download. Or use your own ChatGPT or Claude login.</dd>
<dt>Price</dt><dd>Free</dd>
</dl>
<div class="actions"><a class="btn" href="{CHROME_STORE}">Add to Chrome</a><a class="lnk" href="{{p}}ai-summarizer/index.html">About AI Summarizer</a></div>
</div>
{MOCK_SUM}
</article>'''
HOME = HOME.replace('{HOME_SUM}', HOME_SUM if SHOW_SUM else '')
page('index.html', 'ZoomieLoaf: small tools for reading and writing',
     'ZoomieLoaf makes small tools for reading and writing, like Margin, a Markdown editor for VS Code. Mostly loaf. Occasionally zoom.', HOME)


# ---------- Margin ----------
def feature_list(items):
    return '<dl class="feature-list">' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in items) + '</dl>'

MARGIN = f'''<section class="wrap phero">
<div class="prod-name">{ICON_MARGIN}<div class="kind">Margin, an extension for VS Code</div></div>
<h1>Edit Markdown as a page. Commit plain text.</h1>
<p>Margin brings Notion-style editing to <code>.md</code> files in VS Code, Cursor, Windsurf and VSCodium: a clean page you edit in place, with a slash menu and blocks you drag around. When you save, only the lines you changed change.</p>
<div class="actions"><a class="btn" href="{MARGIN_STORE}">Install for VS Code</a><a class="btn ghost" href="{MARGIN_OVSX}">Install from Open VSX</a></div>
<span class="cmd"><code>{CMD}</code><button type="button" data-copy="{CMD}">Copy</button></span>
<p class="small">Open VSX is for Cursor, Windsurf, VSCodium and other editors without the VS Code Marketplace.</p>
</section>
<section class="wrap showcase">{MOCK_MARGIN}</section>
<section class="wrap section">
<div><h2>What it does</h2><p class="lede">Everything you'd expect from a writing app, inside the editor you already use.</p></div>
{feature_list([
    ('Edit in place', 'Press <kbd>Ctrl+E</kbd> or double-click any text. Select text for a menu with headings, lists, quotes, callouts and links.'),
    ('Slash menu', 'Type <kbd>/</kbd> on an empty line for headings, lists, to-dos, tables, code blocks, callouts or a Mermaid diagram.'),
    ('Block handles', 'Drag a block by its handle to move it, or duplicate and delete it from its menu.'),
    ('Wiki-style links', 'A link to another <code>.md</code> file opens it in Margin, scrolled to the heading. Back and Forward work like in VS Code.'),
    ('Tables', '<kbd>Tab</kbd> moves between cells and adds a row at the end. Add or delete rows and columns from the block menu.'),
    ('Export', 'PDF through the Edge or Chrome already on your computer, a single HTML file, or rich text for Slack and email.'),
    ('AI actions', 'Improve, shorten, fix or translate a selection with GitHub Copilot in VS Code, or hand the prompt to a chat.'),
])}
</section>
<section class="wrap section">
<div><h2>Your Markdown stays yours</h2><p class="lede">Blocks you didn't touch are written back byte for byte: spacing, list markers, emphasis style, line endings. A block you edit is written in the style the file already uses.</p></div>
<div class="frame">
<div class="frame-bar"><span class="mono file">git diff launch-plan.md</span></div>
<div class="diff mono diff-body"><span class="d hunk">@@ -5,3 +5,3 @@ ## This week</span><span class="d"> - [x] Record the demo</span><span class="d del">-- [ ] Write the Open VSX description</span><span class="d add">+- [x] Write the Open VSX description</span><span class="d"> - [ ] Proofread the privacy policy</span></div>
</div>
</section>
<section class="wrap section">
<div><h2>Getting started</h2></div>
<ol class="steps">
<li><span>Install Margin from the <a href="{MARGIN_STORE}">VS Code Marketplace</a> or <a href="{MARGIN_OVSX}">Open VSX</a>.</span></li>
<li><span>Open any <code>.md</code> file and click <b>Open in Margin</b> in the editor title bar. When Margin asks, you can make it the default for Markdown.</span></li>
<li><span>Press <kbd>Ctrl+E</kbd> (<kbd>Cmd+E</kbd> on macOS) to switch between reading and editing. <b>Reopen in Text Editor</b> brings the plain editor back.</span></li>
</ol>
</section>'''
page('margin/index.html', 'Margin: edit Markdown as a page in VS Code',
     'Notion-style editing for Markdown in VS Code, Cursor, Windsurf and VSCodium. Edit .md files as a clean page; the file stays plain Markdown.', MARGIN, 'margin')


# ---------- AI Summarizer ----------
SUM = f'''<section class="wrap phero">
<div class="prod-name">{ICON_SUM}<div class="kind">AI Summarizer, an extension for Chrome</div></div>
<h1>Help with what you're reading. No account, no API key.</h1>
<p>Select text on any page to explain, translate, summarize, fix grammar or ask about it. Summarize a whole page or PDF, and chat about it with AI that runs on your computer.</p>
<div class="actions"><a class="btn" href="{CHROME_STORE}">Add to Chrome</a><span class="mut">Free</span></div>
</section>
<section class="wrap showcase">{MOCK_SUM}</section>
<section class="wrap section">
<div><h2>What it does</h2><p class="lede">One bar for the text you select, and a side panel for the whole page.</p></div>
{feature_list([
    ('Selection bar', 'Select text, or press <kbd>Alt+Q</kbd>, and pick Explain, Translate, Summarize, Fix grammar or Ask.'),
    ('Whole page or PDF', 'Summarize the page you\'re on, or ask questions about it. PDFs are read on your computer.'),
    ('Chat', 'Talk about the page in Chrome\'s side panel, with the AI on your computer or with ChatGPT or Claude.'),
    ('Fix in place', 'Fix grammar in a text box you\'re writing in, then replace the text with one click. You can undo it.'),
    ('Your own actions', 'Change the instructions behind each action, or add your own.'),
])}
</section>
<section class="wrap section">
<div><h2>Where your text goes</h2><p class="lede">You choose for each action. ZoomieLoaf has no server, so nothing ever comes to us.</p></div>
<div class="where">
<div><b>This computer</b><p>Chrome's built-in AI, or the Gemma model downloaded once. Answers are made on your computer and work offline. Nothing leaves it.</p></div>
<div><b>ChatGPT or Claude</b><p>Only when you pick them. Your prompt goes to that site in the side panel, under your own login. You can review each prompt before it's sent.</p></div>
</div>
</section>
<section class="wrap section">
<div><h2>Getting started</h2></div>
<ol class="steps">
<li><span>Add AI Summarizer to Chrome.</span></li>
<li><span>Select text on any page, or press <kbd>Alt+Q</kbd>, and pick an action.</span></li>
<li><span>For offline answers, open Settings, then On-device AI, and download the model once, if your computer supports it.</span></li>
</ol>
</section>'''
if SHOW_SUM: page('ai-summarizer/index.html', 'AI Summarizer: private AI help for what you read in Chrome',
     'Summarize any page, PDF or selected text in Chrome. Explain and translate in one click. AI on your device that works offline. No sign-up, no API key.', SUM, 'sum')


# ---------- 404 ----------
NOT_FOUND = '''<section class="wrap intro"><div>
<h1>This page zoomed off.</h1>
<p class="mut">There's nothing at this address. <a href="/">Go to the home page</a>.</p>
</div></section>'''
page('404.html', 'Page not found: ZoomieLoaf', 'This page does not exist.', NOT_FOUND, prefix='/')


# ---------- Privacy and Terms ----------

WHO = ('ZoomieLoaf is the trading name of Individual Entrepreneur Valerii Pozdniakov, Georgia '
       '("ZoomieLoaf", "we", "us"). Contact: <a href="mailto:hello@zoomieloaf.com">hello@zoomieloaf.com</a>.')

PRIVACY = f'''<article class="wrap legal">
<h1>Privacy policy</h1>
<p class="effective">Effective {EFFECTIVE}</p>
<p class="lead">We don't collect your personal data. There are no accounts, no analytics, no ads and nothing to sell. Our products have no servers of their own: they work on your computer, and send text to another service only when you choose that service.</p>
<nav class="toc" aria-label="On this page"><a href="#website">Website</a><a href="#margin">Margin</a>{{TOC_SUM}}<a href="#rights">Your rights</a></nav>

<h2>Who we are</h2>
<p>{WHO}</p>
<p>This policy covers the website zoomieloaf.com and our products: {{COVERS}}.</p>

<h2 id="website">The website</h2>
<ul>
<li>The site is a set of static pages. It uses no analytics, no tracking cookies, and no third-party scripts or fonts.</li>
<li>If you switch between light and dark, your choice is saved in your own browser and never sent to us.</li>
<li>The site is hosted by Cloudflare. To deliver the pages and protect the site from abuse, Cloudflare processes technical data such as your IP address, browser type and the pages requested, and may keep it in short-lived logs. We don't use this data to identify you. See <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare's privacy policy</a>.</li>
<li>If you email us, we receive your address and your message. We use them only to reply, and delete them when the conversation is over, unless the law requires us to keep them.</li>
</ul>

<h2 id="margin">Margin</h2>
<ul>
<li><b>Your files stay on your computer.</b> Margin reads and writes the files you open in your editor and doesn't upload them anywhere.</li>
<li><b>No telemetry.</b> Margin collects no usage statistics or crash reports and never contacts us.</li>
<li><b>Settings stay in your editor.</b> Margin keeps a few preferences in the editor's local storage: the page width you chose for a file, whether it has asked about opening Markdown files by default, and which AI destinations you agreed to.</li>
<li><b>AI actions run only when you start one, and only after you agree.</b> The first time, Margin tells you where the text will go and asks for permission. If your editor provides a language model (for example GitHub Copilot in VS Code), the selected text and your instruction go to that model through the editor. Otherwise Margin opens ChatGPT or Claude in your browser with the prompt in the address, or copies it for you to paste. That provider's terms and privacy policy apply.</li>
<li><b>Export works on your computer.</b> PDF export uses a browser already installed on your computer. HTML and copy exports stay on your device.</li>
</ul>

{{PRIV_SUM_START}}<h2 id="ai-summarizer">AI Summarizer</h2>
<p>AI Summarizer helps with the text you read in Chrome. It can answer with AI that runs on your computer, or put your prompt into ChatGPT or Claude in the side panel, under your own account on those sites. It has no backend: nothing is sent to us.</p>

<h3>What it reads, and when</h3>
<ul>
<li><b>Selected text</b>, to show the selection bar. Its content is used only when you pick an action. With it, up to about 600 characters of nearby text give the AI context.</li>
<li><b>Page text, title and address</b>, only when you run a page action such as "Summarize page" or "Ask about this page". The main text is extracted on your computer and trimmed to the length you choose in Settings.</li>
<li><b>Text in a box you're editing</b>, only when you use an action with Replace, such as Fix grammar.</li>
<li><b>Files you attach</b> to the on-device chat (text files and PDFs). Their text is extracted on your computer.</li>
</ul>
<p>It doesn't read your browsing history, record the pages you visit, or track you across sites. It never reads the answers ChatGPT or Claude write.</p>

<h3>Where your text goes</h3>
<ul>
<li><b>This computer.</b> With Chrome's built-in AI or the Gemma model, the text and answers are not sent over the internet by the extension. Chrome's built-in AI is covered by Google's terms and Chrome's privacy notice.</li>
<li><b>ChatGPT or Claude</b>, only when an action, chat or the side panel is set to them. The prompt can include the selected text, nearby text, page text, the page title and address, and your instruction. It goes to OpenAI or Anthropic under your own account, and their terms and privacy policies apply (<a href="https://openai.com/policies/privacy-policy">OpenAI</a>, <a href="https://www.anthropic.com/legal/privacy">Anthropic</a>). The extension never sees your login details. You can turn on "Let me review before sending" for any action.</li>
<li><b>Showing those sites in the side panel.</b> To load chatgpt.com and claude.ai inside the extension's side panel, the extension removes two security headers (<code>X-Frame-Options</code> and <code>Content-Security-Policy</code>) for those sites' pages loaded in that panel only. Normal browser tabs are not affected.</li>
<li><b>Model download.</b> When you download Gemma, the file (about 2 to 3 GB) comes from huggingface.co, or from an address you enter. Like any download, this shows that server your IP address and normal browser information. No page content or prompts are sent.</li>
<li><b>Feedback.</b> "Send feedback", "Report this problem", and the page that opens when you remove the extension all open one feedback form in a new tab. The link adds only technical facts: where you opened it, the extension and Chrome version numbers, and which on-device model you use. Nothing is sent unless you fill in and submit the form.</li>
</ul>

<h3>What it stores</h3>
<p>Everything is kept in your Chrome profile, and we can't access it: your settings and actions (synced to your other computers if Chrome Sync is on), the model download status and file, and the current on-device chat, which is cleared when you close Chrome. Removing the extension deletes all of it. Chats you sent to ChatGPT or Claude are kept in those accounts; delete them there.</p>

<h3>Permissions</h3>
<ul>
<li><b>Read and change data on all websites</b>: to show the selection bar on any page, read the selection or page when you run an action, and replace text when you click Replace.</li>
<li><b>Side panel, context menus</b>: for the side panel chat and the right-click menu.</li>
<li><b>Storage, unlimited storage</b>: for settings, actions, the current chat and the model file.</li>
<li><b>Declarative net request</b>: to let chatgpt.com and claude.ai load in the side panel, as described above.</li>
<li><b>Offscreen</b>: to download and run the Gemma model in a hidden extension page.</li>
</ul>

<h3>Chrome Web Store Limited Use</h3>
<p>The use of information received from Google APIs will adhere to the Chrome Web Store User Data Policy, including the Limited Use requirements. Data is used only to provide AI help with the text and pages you choose, is transferred to ChatGPT or Claude only when you ask for it, is never sold, never used for advertising or credit decisions, and is not read by any person, including us.</p>
<p>AI Summarizer is not affiliated with or endorsed by OpenAI, Anthropic or Google.</p>{{PRIV_SUM_END}}

<h2>Stores and editors</h2>
<p>You get our products from {{STORES}}, and run them in software made by others. Those companies may collect data under their own policies, such as install counts or your editor's own telemetry. We don't control that data and don't receive personal data from it.</p>

<h2>Children</h2>
<p>Our products aren't aimed at children under 13, or the minimum age in your country, and we don't knowingly collect anyone's personal data.</p>

<h2 id="rights">Your rights</h2>
<p>Depending on where you live, you can ask what personal data we hold about you and have it corrected or deleted. We hold almost nothing, but write to <a href="mailto:hello@zoomieloaf.com">hello@zoomieloaf.com</a> and we'll reply within 30 days. You can also complain to your data protection authority; in Georgia, that's the Personal Data Protection Service.</p>

<h2>Changes</h2>
<p>If we change this policy, we'll update this page and the date at the top. If a change affects how a product handles your data, we'll say so in its release notes and store listing before it takes effect.</p>
</article>'''
if not SHOW_SUM:
    PRIVACY = re.sub(r'\{PRIV_SUM_START\}.*?\{PRIV_SUM_END\}\n*', '', PRIVACY, flags=re.S)
PRIVACY = (PRIVACY.replace('{PRIV_SUM_START}', '').replace('{PRIV_SUM_END}', '')
    .replace('{TOC_SUM}', '<a href="#ai-summarizer">AI Summarizer</a>' if SHOW_SUM else '')
    .replace('{COVERS}', '<b>Margin</b>, an extension for VS Code and compatible editors, and <b>AI Summarizer</b>, an extension for Chrome' if SHOW_SUM else '<b>Margin</b>, an extension for VS Code and compatible editors')
    .replace('{STORES}', 'the Visual Studio Marketplace, Open VSX and the Chrome Web Store' if SHOW_SUM else 'the Visual Studio Marketplace and Open VSX'))
page('privacy/index.html', 'Privacy policy: ZoomieLoaf', "How ZoomieLoaf's website and products handle your data.", PRIVACY)

TERMS = f'''<article class="wrap legal">
<h1>Terms of use</h1>
<p class="effective">Effective {EFFECTIVE}</p>
<p class="lead">Our products are free and provided as they are. Your content stays yours. Keep backups. Be nice.</p>

<h2>Who we are</h2>
<p>{WHO}</p>

<h2>What these terms cover</h2>
<p>These terms apply to the website zoomieloaf.com and to our products, {{PRODUCTS}} (the "products"). By using the website or a product, you agree to them. If you don't, please don't use them.</p>

<h2>Licenses</h2>
<p>Where a product comes with its own license, such as Margin's MIT License, that license governs your rights to use, copy, change and share its code, and wins over these terms if the two conflict. Otherwise we give you a personal, free, non-exclusive license to install and use the product.</p>
<p>The ZoomieLoaf name, logo and product names are ours. Please don't use them in a way that suggests we made or endorse something we didn't.</p>

<h2>Your content</h2>
<p>Everything you write, edit or read with our products belongs to you or its owner. We claim no rights to it, and our products don't send it to us. See the <a href="{{p}}privacy/index.html">privacy policy</a>.</p>

<h2>Third-party services</h2>
<p>Some features work with services we don't run: the stores that distribute our products, your editor and browser,{{CHROME_AI}} and AI services you choose, such as GitHub Copilot, ChatGPT and Claude. Their own terms apply to how you use them, and we aren't responsible for them. We aren't affiliated with OpenAI, Anthropic, Google or Microsoft.</p>

<h2>AI answers</h2>
<p>AI answers can be wrong, incomplete or out of date. Check anything important before you rely on it.</p>

<h2>Donations</h2>
<p>Our products are free. Donations are voluntary and very welcome. They don't buy features, support or priority, and are non-refundable, except where the law says otherwise.</p>

<h2>Fair use</h2>
<p>Please don't use the website or products to break the law, harm others, or disrupt the website, for example by attacking it or scraping it at a rate that slows it down.</p>

<h2>No warranty</h2>
<p>The website and products are provided "as is" and "as available", without warranties of any kind, express or implied, including fitness for a particular purpose and non-infringement. Software has bugs. Keep backups of anything important, for example in version control.</p>

<h2>Limitation of liability</h2>
<p>To the maximum extent the law allows, ZoomieLoaf isn't liable for indirect, incidental, special or consequential damages, or for loss of data, profits or business, arising from your use of the website or products. Where liability can't be excluded, it's limited to the amount you paid us for the product, which for free products is zero. Nothing here limits liability that can't be limited by law, or your rights as a consumer under mandatory law.</p>

<h2>Changes</h2>
<p>We may change or stop offering any product or part of the website. We may update these terms; the new version applies from the date at the top. If you keep using the products after a change, you accept the new terms.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of Georgia. Disputes go to the courts of Georgia, unless mandatory consumer law gives you the right to bring a claim where you live.</p>
</article>'''
TERMS = (TERMS.replace('{PRODUCTS}', 'Margin and AI Summarizer' if SHOW_SUM else 'such as Margin')
    .replace('{CHROME_AI}', " Chrome's built-in AI," if SHOW_SUM else ''))
page('terms/index.html', 'Terms of use: ZoomieLoaf', "The terms for using ZoomieLoaf's website and products.", TERMS)
print('Built the site in', ROOT)
