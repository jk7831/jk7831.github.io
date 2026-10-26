# Digital business card

Swap-in points (nothing else needs to change):
- `brand.css`  - colours + font. Fill from pointacademy.com.
- `assets/logo.svg` - real logo.
- `assets/card-front.png` - the real card design (landscape, 1.75:1). When present it replaces the placeholder face; the holographic layers stay on top.
- `vignesh.vcf` - contact details (phone, title, show name/date in NOTE).
- NFC tag URL: `https://pointacademy.vercel.app/Vignesh?src=nfc`  QR: same URL without `?src=nfc`.
- Hosted on Vercel project `pointacademy` (root dir `point-card`). Pause the project after the event.
