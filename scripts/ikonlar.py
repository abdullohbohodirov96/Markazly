#!/usr/bin/env python3
"""Markaz logotipidan barcha ikonlarni yasaydi (favicon, PWA, Apple).

Ishlatish:
  python3 scripts/ikonlar.py                 # markaz.json dagi nom va rangdan oddiy logo chizadi
  python3 scripts/ikonlar.py yangi-logo.png  # tayyor logodan (kvadrat, kamida 512px tavsiya)

Natija: assets/logo.png, assets/icon-*.png, assets/icon-maskable-*.png, favicon.ico
Talab: Pillow (pip install pillow)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf = json.load(open(os.path.join(ROOT, 'markaz.json'), encoding='utf-8'))
color = (conf.get('rang') or {}).get('asosiy') or '#16705f'
rgb = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
deep = tuple(int(v * 0.65) for v in rgb)

def font(size):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
              'C:/Windows/Fonts/arialbd.ttf']:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def drawn_logo(n=1024):
    """Logo yo'q bo'lsa: rangli doira ichida markaz nomining bosh harfi(lari)"""
    text = (conf.get('logoMatn') or '').strip()
    if not text:
        words = [w for w in (conf.get('qisqaNom') or conf.get('nom') or 'M').replace('‘', '').split() if w]
        text = ''.join(w[0] for w in words[:2]).upper() or 'M'
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, n - 1, n - 1], fill=deep + (255,))
    d.ellipse([n * .06, n * .06, n * .94, n * .94], fill=rgb + (255,))
    f = font(int(n * (0.46 if len(text) <= 2 else 0.30)))
    box = d.textbbox((0, 0), text, font=f)
    d.text(((n - (box[2] - box[0])) / 2 - box[0], (n - (box[3] - box[1])) / 2 - box[1]), text, font=f, fill=(255, 255, 255, 255))
    return im

src = sys.argv[1] if len(sys.argv) > 1 else None
logo = Image.open(src).convert('RGBA') if src else drawn_logo()
if logo.width != logo.height:          # kvadratga keltiramiz (shaffof chet)
    s = max(logo.size); sq = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    sq.paste(logo, ((s - logo.width) // 2, (s - logo.height) // 2)); logo = sq

A = os.path.join(ROOT, 'assets')
os.makedirs(A, exist_ok=True)
def save(size, name):
    logo.resize((size, size), Image.LANCZOS).save(os.path.join(A, name), optimize=True)
save(192, 'logo.png')
for s in (16, 32, 48, 180, 192, 512):
    save(s, 'icon-%d.png' % s)
for s in (192, 512):                    # maskable: rangli fon + 80% xavfsiz hudud
    bg = Image.new('RGBA', (s, s), rgb + (255,))
    inner = logo.resize((int(s * .72), int(s * .72)), Image.LANCZOS)
    bg.paste(inner, ((s - inner.width) // 2, (s - inner.height) // 2), inner)
    bg.save(os.path.join(A, 'icon-maskable-%d.png' % s), optimize=True)
logo.resize((48, 48), Image.LANCZOS).save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
print('Ikonlar tayyor:', A)
