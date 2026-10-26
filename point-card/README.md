# Digital business cards

Links (add `?src=nfc` on the NFC tag URL):
- /vignesh  /afroz  /jatin  /vayuvee  /desiree  (capitalised versions also work)

How it works
- `people.json` - name, title, phone, email, accent colour per person, plus `event` (adds "Met at ..." to every contact).
- `python3 build.py` - regenerates `<slug>/index.html`, `<slug>.vcf` and `vercel.json`. Run it after editing people.json.
- `assets/cards/<slug>-front.png|-back.png` - 4x Figma exports (336x192 frames). Re-export from Figma to change a design.
- `card.css`, `card.js`, `brand.css`, `fonts/` - shared look (Graphik, cream/ink + each person's accent).
- Hosted on Vercel project `pointacademy-contact` (root dir `point-card`). Pause the project after the event.
