# ── Arabic captions: words placed right-to-left, key words coloured
for a_, b_, ws in chunks():
    if a_ < S_B - .1 or a_ >= S_F - .05: continue
    words = [w[2] for w in ws if w[2] != "—"]
    size = 64
    widths = [AR.width(w, size) for w in words]; sp = size * .3
    tw = sum(widths) + sp * (len(words) - 1)
    if tw > 900:
        k = 900 / tw; size = int(size * k); widths = [AR.width(w, size) for w in words]; sp = size * .3; tw = sum(widths) + sp * (len(words) - 1)
    yb = 1530; x = CX + tw / 2
    cap = rr(CX - tw / 2 - 34, yb - size - 22, tw + 68, size + 60, 26, "#04140D").replace('fill="#04140D"', 'fill="#04140D" fill-opacity=".78"')
    for w, wd in zip(words, widths):
        col = BAD if w in BAD_KEY else (MINT if w in KEY else FG)
        cap += TA(w, x - wd, yb, size, AR, col, "start"); x -= wd + sp
    add(cap, a_, b_ + .02, dy=0, dur=.1, pop=True, fo=.04)

