#!/usr/bin/env python3
"""Render master-accomplishments-record.md into the designed HTML artifact."""
import re, html, sys

SRC = '/home/user/Chores/cv/master-accomplishments-record.md'
OUT = '/home/user/Chores/cv/master-record.html'

md = open(SRC, encoding='utf-8').read()
lines = md.split('\n')

# ---------- inline ----------
def inline(s, esc=True):
    if esc:
        s = html.escape(s, quote=False)
    # code first, protect contents
    codes = []
    def stash(m):
        codes.append(m.group(1))
        return f'\x00{len(codes)-1}\x00'
    s = re.sub(r'`([^`]+)`', stash, s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*([^*\n]+?)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    # semantic markers
    s = s.replace('◆ ON RECORD', '<span class="mk mk-rec">◆ on record</span>')
    s = s.replace('▢ FILL', '<span class="mk mk-fill">▢ fill</span>')
    s = re.sub(r'⟡\s*\*\*(M#[\d.,\s M#]*?)\*\*', r'<span class="mk mk-men">⟡ \1</span>', s)
    s = re.sub(r'⟡\s*(M#[\d.]+(?:,\s*M#[\d.]+)*)', r'<span class="mk mk-men">⟡ \1</span>', s)
    s = s.replace('⟡', '<span class="glyph-men">⟡</span>')
    s = s.replace('▢', '<span class="glyph-fill">▢</span>')
    s = s.replace('✅', '<span class="glyph-done">✔</span>')
    s = s.replace('✓', '<span class="glyph-yes">✓</span>')
    s = re.sub(r'\x00(\d+)\x00', lambda m: '<code>' + html.escape(codes[int(m.group(1))]) + '</code>', s)
    return s

def slug(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'[^\w\s.§-]', '', t).strip().lower()
    return re.sub(r'[\s.]+', '-', t)[:60]

# ---------- block parse ----------
out, toc = [], []
i = 0
n = len(lines)
sec_open = False

def close_sec():
    global sec_open
    if sec_open:
        out.append('</section>')
        sec_open = False

# split a heading like "§4.1 — NewsFlick Ltd" into (marker, rest)
def split_num(t):
    m = re.match(r'^(§?[\d.]+[A-E]?)\s*(?:—|·|-)?\s*(.*)$', t)
    if m and re.search(r'\d', m.group(1)):
        return m.group(1), m.group(2) or t
    return None, t

while i < n:
    ln = lines[i]
    st = ln.strip()

    if not st:
        i += 1; continue

    # horizontal rule
    if re.fullmatch(r'-{3,}', st):
        out.append('<hr/>'); i += 1; continue

    # headings
    m = re.match(r'^(#{1,5})\s+(.*)$', st)
    if m:
        lvl, txt = len(m.group(1)), m.group(2).strip()
        num, rest = split_num(txt)
        sid = slug(txt)
        if lvl <= 2:
            close_sec()
            out.append(f'<section id="{sid}">')
            sec_open = True
        if lvl == 1:
            out.append(f'<h1>{inline(txt)}</h1>')
        else:
            tag = f'h{lvl}'
            label = f'<span class="secno">{html.escape(num)}</span>' if num else ''
            out.append(f'<{tag} id="{sid}">{label}<span class="htxt">{inline(rest)}</span></{tag}>')
            if lvl in (2, 3):
                toc.append((lvl, num, rest, sid))
        i += 1; continue

    # blockquote (mentor callouts)
    if st.startswith('>'):
        buf = []
        while i < n and lines[i].strip().startswith('>'):
            buf.append(lines[i].strip()[1:].strip())
            i += 1
        body = ' '.join(x for x in buf if x)
        cls = 'callout men' if '⟡' in body else 'callout'
        out.append(f'<blockquote class="{cls}">{inline(body)}</blockquote>')
        continue

    # table
    if st.startswith('|'):
        rows = []
        while i < n and lines[i].strip().startswith('|'):
            rows.append(lines[i].strip())
            i += 1
        cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
        head = cells[0]
        body = [r for r in cells[1:] if not re.fullmatch(r'[:\- ]+', r[0])]
        t = ['<div class="tw"><table><thead><tr>']
        t += [f'<th>{inline(c)}</th>' for c in head]
        t.append('</tr></thead><tbody>')
        BLANK = '<span class="blank">&mdash;</span>'
        for r in body:
            t.append('<tr>' + ''.join('<td>' + (inline(c) if c else BLANK) + '</td>' for c in r) + '</tr>')
        t.append('</tbody></table></div>')
        out.append(''.join(t))
        continue

    # lists
    if re.match(r'^[-*]\s', st):
        items = []
        while i < n:
            s2 = lines[i].strip()
            if not s2:
                # allow single blank inside list only if next is a list item
                if i + 1 < n and re.match(r'^\s*[-*]\s', lines[i+1]):
                    i += 1; continue
                break
            if not re.match(r'^[-*]\s', s2):
                break
            items.append(s2[2:].strip())
            i += 1
        li = []
        checks = 0
        for it in items:
            if it.startswith('[ ]'):
                checks += 1
                li.append(f'<li class="todo">{inline(it[3:].strip())}</li>')
            elif it.startswith('[x]'):
                li.append(f'<li class="todo done">{inline(it[3:].strip())}</li>')
            else:
                li.append(f'<li>{inline(it)}</li>')
        cls = 'checklist' if checks else 'bullets'
        out.append(f'<ul class="{cls}">' + ''.join(li) + '</ul>')
        continue

    # paragraph
    buf = []
    while i < n and lines[i].strip() and not re.match(r'^(#{1,5}\s|[-*]\s|\||>|-{3,}$)', lines[i].strip()):
        buf.append(lines[i].strip())
        i += 1
    p = ' '.join(buf)
    cls = ''
    if p.startswith('<span class') or '◆ ON RECORD' in p or '▢ FILL' in p:
        pass
    out.append(f'<p{cls}>{inline(p)}</p>')

close_sec()
body_html = '\n'.join(out)

# ---------- TOC ----------
toc_html = []
for lvl, num, txt, sid in toc:
    c = 'l2' if lvl == 2 else 'l3'
    nm = f'<span class="tn">{html.escape(num)}</span>' if num else ''
    plain = re.sub(r'<[^>]+>', '', inline(txt))
    toc_html.append(f'<a class="{c}" href="#{sid}">{nm}<span>{plain}</span></a>')
toc_html = '\n'.join(toc_html)

CSS = r"""
*{box-sizing:border-box}
:root{
  --ground:#F4F6F5; --surface:#FFFFFF; --surface-2:#EBEFED;
  --ink:#191D1C; --ink-2:#414A47; --muted:#69736F;
  --line:#D6DDDA; --line-2:#E6EAE8;
  --accent:#1F5F5B; --accent-soft:#E0EBE8;
  --rec:#2A6A5F; --rec-bg:#E4EFEB; --rec-line:#8FBDB2;
  --fill:#8A590F; --fill-bg:#F5EDDD; --fill-bg-soft:#FAF5EC; --fill-line:#CFAE72;
  --men:#873C50; --men-bg:#F5E5E9; --men-line:#C79AA6;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,"Times New Roman",serif;
  --sans:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#101514; --surface:#171D1B; --surface-2:#1E2523;
    --ink:#E2E8E5; --ink-2:#B3BDB9; --muted:#889490;
    --line:#2C3532; --line-2:#232B29;
    --accent:#68B9AB; --accent-soft:#1A2C29;
    --rec:#6FBDAC; --rec-bg:#152623; --rec-line:#2F5B53;
    --fill:#D5A257; --fill-bg:#2A2318; --fill-bg-soft:#1E2019; --fill-line:#5C4B2C;
    --men:#D98AA0; --men-bg:#2A1B20; --men-line:#633B45;
  }
}
:root[data-theme="dark"]{
  --ground:#101514; --surface:#171D1B; --surface-2:#1E2523;
  --ink:#E2E8E5; --ink-2:#B3BDB9; --muted:#889490;
  --line:#2C3532; --line-2:#232B29;
  --accent:#68B9AB; --accent-soft:#1A2C29;
  --rec:#6FBDAC; --rec-bg:#152623; --rec-line:#2F5B53;
  --fill:#D5A257; --fill-bg:#2A2318; --fill-bg-soft:#1E2019; --fill-line:#5C4B2C;
  --men:#D98AA0; --men-bg:#2A1B20; --men-line:#633B45;
}

body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--sans); font-size:16px; line-height:1.62;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px 96px;display:grid;grid-template-columns:1fr;gap:0}
/* grid items default to min-width:auto, so an unbreakable token widens the whole track */
.wrap>*{min-width:0}

/* ---- masthead ---- */
.mast{grid-column:1/-1;padding:56px 0 28px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:0 0 14px}
.mast h1{font-family:var(--serif);font-weight:600;font-size:clamp(30px,4.4vw,46px);line-height:1.1;margin:0 0 12px;letter-spacing:-.015em;text-wrap:balance}
.mast .sub{color:var(--ink-2);max-width:64ch;margin:0 0 26px;font-size:16.5px}
.mast .sub em{color:var(--ink);font-style:normal;font-weight:600}

.stats{display:flex;flex-wrap:wrap;gap:0;border:1px solid var(--line);border-radius:3px;background:var(--surface);overflow:hidden}
.stat{flex:1 1 150px;padding:14px 18px;border-right:1px solid var(--line-2)}
.stat:last-child{border-right:0}
.stat b{display:block;font-family:var(--mono);font-size:23px;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.2}
.stat span{display:block;font-size:11.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-top:3px}
.stat.s-rec b{color:var(--rec)} .stat.s-fill b{color:var(--fill)} .stat.s-men b{color:var(--men)}

/* ---- toc ---- */
.toc{grid-column:1/-1;margin:26px 0 0;padding:18px 0 4px;border-bottom:1px solid var(--line)}
.toc .th{font-family:var(--mono);font-size:10.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.toc a{display:flex;gap:9px;text-decoration:none;color:var(--ink-2);font-size:13.5px;padding:3px 0;line-height:1.4}
.toc a:hover{color:var(--accent)}
.toc a.l3{display:none}
.toc .tn{font-family:var(--mono);font-size:11.5px;color:var(--muted);flex:0 0 auto;min-width:34px;padding-top:1px}
.toc::-webkit-scrollbar{width:6px}
.toc::-webkit-scrollbar-thumb{background:var(--line);border-radius:3px}

/* ---- document ---- */
.doc{grid-column:1/-1;padding-top:24px;min-width:0}
.doc section{scroll-margin-top:16px}
.doc h1{display:none}
.doc h2,.doc h3,.doc h4,.doc h5{font-family:var(--serif);font-weight:600;letter-spacing:-.01em;position:relative;scroll-margin-top:16px}
.doc h2{font-size:27px;line-height:1.2;margin:56px 0 18px;padding-bottom:12px;border-bottom:2px solid var(--accent)}
.doc h3{font-size:21px;line-height:1.25;margin:44px 0 14px}
.doc h4{font-size:17px;line-height:1.3;margin:32px 0 10px;color:var(--ink)}
.doc h5{font-family:var(--sans);font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin:26px 0 8px}
.htxt{text-wrap:balance}
.secno{
  font-family:var(--mono);font-size:.66em;font-weight:500;color:var(--accent);
  letter-spacing:.02em;display:inline-block;margin-right:.6em;vertical-align:.08em;
}
@media(min-width:1240px){
  .doc h3 .secno,.doc h4 .secno{position:absolute;right:calc(100% + 14px);margin:0;color:var(--muted);white-space:nowrap}
}
.doc p{margin:0 0 15px;max-width:70ch;color:var(--ink-2)}
.doc p strong{color:var(--ink);font-weight:650}
.doc hr{border:0;border-top:1px solid var(--line-2);margin:40px 0}
.doc a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}
code{font-family:var(--mono);font-size:.86em;background:var(--surface-2);padding:.1em .38em;border-radius:2px;color:var(--ink)}

/* ---- lists ---- */
ul{margin:0 0 16px;padding:0;list-style:none;max-width:74ch}
ul.bullets li{position:relative;padding-left:19px;margin-bottom:7px;color:var(--ink-2)}
ul.bullets li::before{content:"";position:absolute;left:3px;top:.66em;width:5px;height:5px;border-radius:50%;background:var(--line);}
ul.checklist{border-left:2px solid var(--fill-line);padding-left:0;margin-left:0;background:var(--fill-bg-soft);border-radius:0 3px 3px 0;padding:12px 16px 12px 14px}
ul.checklist li.todo{position:relative;padding-left:26px;margin-bottom:9px;color:var(--ink-2);font-size:15px}
ul.checklist li.todo:last-child{margin-bottom:0}
ul.checklist li.todo::before{
  content:"";position:absolute;left:0;top:.42em;width:13px;height:13px;
  border:1.5px solid var(--fill-line);border-radius:2px;background:transparent;
}
ul.checklist li.todo.done::after{content:"✓";position:absolute;left:2px;top:-.02em;color:var(--fill);font-size:13px}
ul.checklist li strong{color:var(--ink)}

/* ---- markers ---- */
.mk{
  display:inline-block;font-family:var(--mono);font-size:10.5px;font-weight:600;
  letter-spacing:.09em;text-transform:uppercase;padding:.2em .5em;border-radius:2px;
  vertical-align:.12em;white-space:nowrap;
}
.mk-rec{background:var(--rec-bg);color:var(--rec);border:1px solid var(--rec-line)}
.mk-fill{background:var(--fill-bg);color:var(--fill);border:1px solid var(--fill-line)}
.mk-men{background:var(--men-bg);color:var(--men);border:1px solid var(--men-line)}
.glyph-men{color:var(--men)}
.glyph-fill{color:var(--fill)}
.glyph-done{color:var(--rec);font-weight:700}
.glyph-yes{color:var(--rec)}

/* on-record paragraphs get a settled stripe */
.doc p:has(.mk-rec){
  background:var(--rec-bg);border-left:2px solid var(--rec-line);
  padding:9px 14px;margin:0 0 8px;border-radius:0 3px 3px 0;color:var(--ink);
}
.doc p:has(.mk-fill){
  border-left:2px solid var(--fill-line);padding:2px 0 2px 14px;margin:20px 0 8px;
  color:var(--ink);font-size:15px;
}

/* ---- callouts ---- */
blockquote.callout{
  margin:18px 0 20px;padding:14px 18px;background:var(--surface);
  border:1px solid var(--line);border-left:3px solid var(--muted);border-radius:0 3px 3px 0;
  color:var(--ink-2);font-size:15px;max-width:74ch;
}
blockquote.callout.men{background:var(--men-bg);border-color:var(--men-line);border-left-color:var(--men)}
blockquote.callout.men em{color:var(--ink);font-style:italic}
blockquote.callout strong{color:var(--ink)}

/* ---- tables ---- */
.tw{overflow-x:auto;margin:18px 0 24px;border:1px solid var(--line);border-radius:3px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:520px}
thead th{
  text-align:left;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);font-weight:600;padding:11px 14px;border-bottom:1px solid var(--line);
  background:var(--surface-2);white-space:nowrap;
}
td{padding:10px 14px;border-bottom:1px solid var(--line-2);vertical-align:top;color:var(--ink-2)}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--surface-2)}
td:first-child{font-variant-numeric:tabular-nums;color:var(--ink)}
.blank{color:var(--line)}
td code{font-size:.85em}

/* ---- legend ---- */
.legend{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));margin:26px 0 0}
.lg{border:1px solid var(--line);border-left-width:3px;border-radius:0 3px 3px 0;padding:11px 14px;background:var(--surface);font-size:13.5px;color:var(--ink-2)}
.lg b{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px}
.lg.l-rec{border-left-color:var(--rec)} .lg.l-rec b{color:var(--rec)}
.lg.l-fill{border-left-color:var(--fill)} .lg.l-fill b{color:var(--fill)}
.lg.l-men{border-left-color:var(--men)} .lg.l-men b{color:var(--men)}

a:focus-visible,.toc a:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:2px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
@media(max-width:640px){
  body{font-size:15.5px}
  code{overflow-wrap:anywhere}
  .mast .sub{max-width:none}
  .wrap{padding:0 16px 64px}
  .stat{flex:1 1 50%;border-bottom:1px solid var(--line-2)}
  .doc h2{font-size:23px}
}

/* ---- two-column placement. Declared last so nothing above re-flattens it. ---- */
@media(min-width:1040px){
  .wrap{grid-template-columns:224px minmax(0,1fr);column-gap:56px;padding-right:32px}
  .mast{grid-column:1/-1;grid-row:1}
  .toc{
    grid-column:1;grid-row:2;margin:0;padding:36px 0 40px;border-bottom:0;
    position:sticky;top:0;align-self:start;max-height:100vh;overflow-y:auto;
  }
  .toc a.l3{display:flex;padding-left:14px;font-size:12.5px;color:var(--muted)}
  .toc a.l3 .tn{min-width:40px}
  .doc{grid-column:2;grid-row:2;padding-top:36px}
}
"""

PAGE = f"""<title>Master Record of Work</title>
<style>{CSS}</style>
<div class="wrap">
  <header class="mast">
    <p class="eyebrow">Working document &middot; source of truth</p>
    <h1>Master Record of Work</h1>
    <p class="sub">A complete inventory of systems built, decisions taken, methods used and results obtained &mdash; the file a CV, an SOP, or an interview answer gets cut down <em>from</em>. Built from <code>Lingbo_Zeng_CV_EN_drone.docx</code> and the seven unresolved mentor comments inside it.</p>
    <div class="stats">
      <div class="stat s-rec"><b>49</b><span>facts on record</span></div>
      <div class="stat s-fill"><b>365</b><span>open fill-in slots</span></div>
      <div class="stat s-men"><b>7</b><span>mentor comments</span></div>
      <div class="stat"><b>12</b><span>tier-1 blockers</span></div>
    </div>
    <div class="legend">
      <div class="lg l-rec"><b>&#9670; on record</b>Stated in the current CV. Verified against the source document.</div>
      <div class="lg l-fill"><b>&#9634; fill</b>A slot for a fact only you hold. Nothing here was invented &mdash; blanks are blanks.</div>
      <div class="lg l-men"><b>&#10209; M#n</b>Requested by mentor comment #n. These are the load-bearing gaps.</div>
    </div>
  </header>
  <nav class="toc">
    <div class="th">Contents</div>
    {toc_html}
  </nav>
  <main class="doc">
{body_html}
  </main>
</div>
"""

open(OUT, 'w', encoding='utf-8').write(PAGE)
print(f'wrote {OUT}  ({len(PAGE):,} bytes)')
