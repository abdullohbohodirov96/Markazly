"""Rough forced alignment: phrases ↔ speech time via pauses. Writes a timing module."""
import re, subprocess, sys
def silences(path, d=0.12):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise=-38dB:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
    return list(zip(st, en)), dur
def phrases(text):
    text = re.sub(r"\[[^\]]*\]", "", text).replace('"', "").strip()
    parts = re.findall(r"[^,.!?:—]+[,.!?:—]*", text)
    out = []
    for p in parts:
        p = p.strip()
        if not p: continue
        if out and (len(p) < 3 or p in ("—",)): out[-1] += " " + p; continue
        out.append(p)
    return out
def align(text, path):
    sil, dur = silences(path)
    sil = [(a, b) for a, b in sil if b - a < 2 and not (a < 0.05)]
    speech_start = 0.0
    pre = [(a, b) for a, b in silences(path)[0] if a < 0.05]
    if pre: speech_start = pre[0][1]
    end = dur
    if sil and sil[-1][1] >= dur - 0.05: end = sil[-1][0]; sil = sil[:-1]
    ph = phrases(text)
    L = [len(p) for p in ph]; tot = sum(L)
    # speech-time axis excluding pauses
    gaps = [(a, b) for a, b in sil if speech_start < a < end]
    speech = (end - speech_start) - sum(b - a for a, b in gaps)
    def time_at(frac):
        tgt = frac * speech; t = speech_start; acc = 0
        for a, b in gaps:
            seg = a - t
            if acc + seg >= tgt: return t + (tgt - acc)
            acc += seg; t = b
        return t + (tgt - acc)
    bounds = [speech_start]; c = 0
    used = set()
    for l in L[:-1]:
        c += l; t = time_at(c / tot)
        # snap to nearest unused pause within 0.9s
        best = None
        for i, (a, b) in enumerate(gaps):
            if i in used: continue
            m = (a + b) / 2
            if abs(m - t) < 0.9 and (best is None or abs(m - t) < abs((gaps[best][0] + gaps[best][1]) / 2 - t)): best = i
        if best is not None: used.add(best); bounds.append(gaps[best])
        else: bounds.append((t, t))
    segs = []
    starts = [speech_start] + [b for a, b in bounds[1:]]
    ends = [a for a, b in bounds[1:]] + [end]
    for p, s, e in zip(ph, starts, ends): segs.append((round(s, 2), round(e, 2), p))
    return segs, dur
if __name__ == "__main__":
    text = open(sys.argv[1]).read(); path = sys.argv[2]
    segs, dur = align(text, path)
    for s in segs: print(s)
