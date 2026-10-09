import base64, os, shutil
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import cairosvg

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "markazly")
os.makedirs(OUT, exist_ok=True)

WHITE = "#F4F8F6"
MUTED = "#A9C2B6"


class Face:
    def __init__(self, path):
        f = TTFont(path)
        self.gs = f.getGlyphSet()
        self.cmap = f.getBestCmap()
        self.upm = f["head"].unitsPerEm

    def run(self, text, size, x, base, track=0.0):
        """SVG path for text, plus its advance width. track = extra spacing in em."""
        s = size / self.upm
        parts, cx = [], x
        for ch in text:
            g = self.gs[self.cmap[ord(ch)]]
            pen = SVGPathPen(self.gs)
            g.draw(TransformPen(pen, (s, 0, 0, -s, cx, base)))
            parts.append(pen.getCommands())
            cx += g.width * s + track * size
        return " ".join(parts), cx - x - track * size


semi = Face(os.path.join(D, "Poppins-SemiBold.ttf"))
reg = Face(os.path.join(D, "Poppins-Regular.ttf"))

with open(os.path.join(D, "mark_transparent.png"), "rb") as fh:
    MARK = "data:image/png;base64," + base64.b64encode(fh.read()).decode()
MW, MH = 342, 377  # mark image size


def defs():
    return ('<defs>'
            '<radialGradient id="bg" cx="50%" cy="42%" r="75%">'
            '<stop offset="0%" stop-color="#0C2C21"/><stop offset="55%" stop-color="#06180F"/>'
            '<stop offset="100%" stop-color="#020A07"/></radialGradient>'
            '<linearGradient id="ly" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0%" stop-color="#2EE59D"/><stop offset="100%" stop-color="#1FB5C8"/></linearGradient>'
            '</defs>')


def wordmark(size, x, base):
    """'Markaz' in white + 'ly' in the mint→teal gradient. Returns svg, width."""
    d1, w1 = semi.run("Markaz", size, x, base, track=-0.01)
    d2, w2 = semi.run("ly", size, x + w1 + size * -0.01, base, track=-0.01)
    svg = (f'<path d="{d1}" fill="{WHITE}"/>'
           f'<path d="{d2}" fill="url(#ly)"/>')
    return svg, w1 + w2


def mark(x, y, h):
    w = h * MW / MH
    return f'<image href="{MARK}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/>', w


def svg(w, h, body, bg=True):
    back = f'<rect width="{w}" height="{h}" fill="url(#bg)"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">{defs()}{back}{body}</svg>')


def save(name, s):
    with open(os.path.join(OUT, name + ".svg"), "w") as fh:
        fh.write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, name + ".png"))


# 1) Square post / presentation logo: mark, wordmark, tagline (like the original layout)
S = 1080
_, ww = wordmark(150, 0, 0)
m_svg, mw = mark((S - 300 * MW / MH) / 2, 190, 300)
wm_svg, _ = wordmark(150, (S - ww) / 2, 690)
tag = "O‘quv markazlari uchun web tizim"
td, tw = reg.run(tag, 40, 0, 0, track=0.02)
td, _ = reg.run(tag, 40, (S - tw) / 2, 790, track=0.02)
save("markazly_post_1080", svg(S, S, m_svg + wm_svg + f'<path d="{td}" fill="{MUTED}"/>'))

# 2) Horizontal logo (mark + wordmark), dark and transparent
H = 400
_, ww = wordmark(170, 0, 0)
W = int(80 + 250 * MW / MH + 50 + ww + 90)
m_svg, mw = mark(80, 70, 250)
wm_svg, _ = wordmark(170, 80 + mw + 50, 262)
save("markazly_gorizontal_qora", svg(W, H, m_svg + wm_svg))
save("markazly_gorizontal_shaffof", svg(W, H, m_svg + wm_svg, bg=False))

# 3) Wordmark only, transparent (for site header, documents on dark)
_, ww = wordmark(200, 0, 0)
wm_svg, _ = wordmark(200, 20, 200)
save("markazly_yozuv_shaffof", svg(int(ww + 40), 260, wm_svg, bg=False))

# 4) Instagram profile: the mark alone (no name, so it is reused as is)
shutil.copy(os.path.join(D, "ig_profil_ilmora.png"), os.path.join(OUT, "markazly_ig_profil.png"))
print("ok", W)
