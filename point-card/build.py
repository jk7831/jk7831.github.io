#!/usr/bin/env python3
"""Generate one page + vCard per person from people.json.
Usage: python3 build.py   (run from point-card/)
Set "event" in people.json (e.g. "AI Show 2026") to add a 'Met at ...' note to every contact."""
import json, html, os, shutil
BASE = "https://pointacademy-contact.vercel.app"
data = json.load(open("people.json"))
event = data.get("event", "").strip()
esc = html.escape

PAGE = """<!doctype html>
<html lang="en" style="--accent:{accent}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{name} · Point Academy</title>
<meta name="description" content="{name}, {title} at Point Academy.">
<meta name="theme-color" content="#f2ebdc">
<meta property="og:type" content="website">
<meta property="og:title" content="{name} · Point Academy">
<meta property="og:description" content="{title}. Tap to save my contact.">
<meta property="og:image" content="{base}/assets/cards/{slug}-front.png">
<meta property="og:url" content="{base}/{slug}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/cards/{slug}-front.png" as="image">
<link rel="stylesheet" href="/brand.css">
<link rel="stylesheet" href="/card.css">
</head>
<body>
  <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
  <div class="who">
    <div class="greet" id="greet"></div>
    <p class="eyebrow"><img src="/assets/logo-dark.svg" alt="">Point Academy</p>
    <h1>Hi, I'm <em>{first}.</em></h1>
    <p>Tap below to save my contact.</p>
  </div>

  <div class="stage" id="stage">
    <div class="card idle" id="card">
      <div class="flip" id="flip">
        <img class="side front" id="front" src="/assets/cards/{slug}-front.png" alt="{name}, {title}, Point Academy" width="1344" height="768" decoding="async" fetchpriority="high">
        <img class="side back" id="back" src="/assets/cards/{slug}-back.png" alt="Point Academy" width="1344" height="768" decoding="async" hidden>
      </div>
      <div class="holo"></div>
      <div class="glare"></div>
    </div>
  </div>
  <div class="tilt-hint" id="hint">Tilt, drag or tap to flip</div>

  <div class="actions">
    <a class="btn primary" id="save" href="/{slug}.vcf" download="{name} - Point Academy.vcf"><span>Add to Contacts</span><i></i><span aria-hidden="true">→</span></a>
    <a class="btn ghost" href="https://pointacademy.com">Visit pointacademy.com</a>
  </div>
<script src="/card.js"></script>
</body>
</html>
"""

def vcard(p):
    first, last = (p["name"].split(" ", 1) + [""])[:2]
    lines = ["BEGIN:VCARD", "VERSION:3.0", f"N:{last};{first};;;", f"FN:{p['name']}",
             "ORG:Point Academy", f"TITLE:{p['title']}"]
    if p["phone"]: lines.append(f"TEL;TYPE=CELL,VOICE:{p['phone']}")
    if p["email"]: lines.append(f"EMAIL;TYPE=INTERNET,WORK:{p['email']}")
    lines.append("URL:https://pointacademy.com")
    if event: lines.append("NOTE:Met at " + event.replace(",", "\\,"))
    lines.append("END:VCARD")
    return "\n".join(lines) + "\n"

rewrites = []
for p in data["people"]:
    s = p["slug"]
    os.makedirs(s, exist_ok=True)
    open(f"{s}/index.html", "w").write(PAGE.format(base=BASE, name=esc(p["name"]), title=esc(p["title"]),
                                                  first=esc(p["first"]), slug=s, accent=p["accent"]))
    open(f"{s}.vcf", "w").write(vcard(p))
    for v in {s, s.capitalize()}:
        rewrites.append({"source": f"/{v}", "destination": f"/{s}/index.html"})
        rewrites.append({"source": f"/{v}/", "destination": f"/{s}/index.html"})
    print("built", s)

vercel = {"rewrites": rewrites, "headers": [{"source": "/(.*)\\.vcf", "headers": [
    {"key": "Content-Type", "value": "text/vcard; charset=utf-8"}]}]}
json.dump(vercel, open("vercel.json", "w"), indent=2)
