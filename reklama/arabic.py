"""Arabic text → SVG path with proper shaping (HarfBuzz) and RTL order."""
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand")
class ArFace:
    def __init__(self, weight="700"):
        p = os.path.join(_D, f"Cairo-Arabic-{weight}.ttf")
        blob = hb.Blob.from_file_path(p); self.hbface = hb.Face(blob); self.font = hb.Font(self.hbface)
        self.upm = self.hbface.upem; self.tt = TTFont(p); self.gs = self.tt.getGlyphSet(); self.order = self.tt.getGlyphOrder()
    def _shape(self, text):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.font, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions
    def _adv(self, i, p, text):
        if i.codepoint == 0:
            ch = text[i.cluster] if i.cluster < len(text) else " "
            return self.upm * (0.26 if ch == " " else 0.5)
        return p.x_advance
    def width(self, text, size):
        inf, pos = self._shape(text); return sum(self._adv(i, p, text) for i, p in zip(inf, pos)) * size / self.upm
    def path(self, text, size, x, base):
        inf, pos = self._shape(text); s = size / self.upm; cx = x; parts = []
        for i, p in zip(inf, pos):
            if i.codepoint == 0:
                ch = text[i.cluster] if i.cluster < len(text) else " "
                if ch in "—-":
                    parts.append(f"M{cx + .08 * size} {base - .3 * size} h{.34 * size} v{.07 * size} h{-.34 * size} Z")
                cx += self._adv(i, p, text) * s; continue
            g = self.gs[self.order[i.codepoint]]
            pen = SVGPathPen(self.gs); g.draw(TransformPen(pen, (s, 0, 0, -s, cx + p.x_offset * s, base - p.y_offset * s)))
            parts.append(pen.getCommands()); cx += p.x_advance * s
        return " ".join(parts)
AR = ArFace("700"); AR6 = ArFace("600")
def TA(text, x, base, size, face=None, fill="#F4F8F6", anchor="middle"):
    face = face or AR; w = face.width(text, size)
    if anchor == "middle": x -= w / 2
    elif anchor == "end": x -= w        # for RTL, "end" = left edge given as x
    elif anchor == "right": x -= w      # right-aligned at x
    return f'<path d="{face.path(text, size, x, base)}" fill="{fill}"/>'
