"""Synthesised background music + sound effects for video 1 (no samples, all generated)."""
import numpy as np, scipy.signal as sg, wave, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing3 import *
SR = 44100
N = int((DUR + 0.5) * SR)
rng = np.random.default_rng(7)

def env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR))
def lp(x, fc, order=2): b, a = sg.butter(order, fc / (SR / 2)); return sg.lfilter(b, a, x)
def hp(x, fc, order=2): b, a = sg.butter(order, fc / (SR / 2), "high"); return sg.lfilter(b, a, x)
def bp(x, lo, hi): b, a = sg.butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return sg.lfilter(b, a, x)
def place(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += gain * sig[: j - i]
def note(m): return 440 * 2 ** ((m - 69) / 12)
def saw(f, n, det=0.0):
    t = np.arange(n) / SR; return 2 * ((t * f * (1 + det)) % 1) - 1

# ---------- instruments
def kick(): n = int(.45 * SR); t = np.arange(n) / SR; f = 45 + 95 * np.exp(-t / .035); ph = 2 * np.pi * np.cumsum(f) / SR; return np.sin(ph) * env_exp(n, .16)
def clap(): n = int(.25 * SR); x = bp(rng.standard_normal(n), 900, 4000) * env_exp(n, .06); return x * 0.9
def hat(o=False): n = int((.18 if o else .05) * SR); return hp(rng.standard_normal(n), 7000) * env_exp(n, .05 if o else .012) * 0.5
def tick(): n = int(.03 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * 2600 * t) * env_exp(n, .004)
def bass(m, dur): n = int(dur * SR); x = saw(note(m), n) + 0.5 * saw(note(m - 12), n); x = lp(x, 380); e = np.minimum(1, np.arange(n) / 300) * env_exp(n, dur * .9); return x * e * .6
def pluck(m, dur=.28): n = int(dur * SR); x = saw(note(m), n) + saw(note(m), n, .004); x = lp(x * env_exp(n, .09), 3200); return x * .35
def pad(ms, dur, cut=900):
    n = int(dur * SR); x = sum(saw(note(m), n, d) for m in ms for d in (-.003, .003)); x = lp(x, cut, 2)
    a = np.minimum(1, np.arange(n) / (0.4 * SR)); r = np.minimum(1, (n - np.arange(n)) / (0.3 * SR)); return x * a * r * .08
def boom(): n = int(1.6 * SR); t = np.arange(n) / SR; s = np.sin(2 * np.pi * (38 + 30 * np.exp(-t / .1)) * t) * env_exp(n, .5); nz = lp(rng.standard_normal(n), 1200) * env_exp(n, .12) * .5; return (s + nz) * .9
def riser(d):
    n = int(d * SR); t = np.arange(n) / SR; f = 200 + 1400 * (t / d) ** 2; s = np.sin(2 * np.pi * np.cumsum(f) / SR) * .25
    nz = rng.standard_normal(n); out = np.zeros(n); seg = n // 16
    for k in range(16): sl = slice(k * seg, (k + 1) * seg if k < 15 else n); out[sl] = hp(nz[sl], 300 + 500 * k)
    return (s + out * .35) * (t / d) ** 1.5
def whoosh(d=.45):
    n = int(d * SR); t = np.arange(n) / SR; nz = rng.standard_normal(n); out = np.zeros(n); seg = n // 12
    for k in range(12): sl = slice(k * seg, (k + 1) * seg if k < 11 else n); c = 400 + 3000 * np.sin(np.pi * k / 11); out[sl] = bp(nz[sl], c * .6, c * 1.4)
    return out * np.sin(np.pi * t / d) ** 2 * .7
def pop(f=900): n = int(.09 * SR); t = np.arange(n) / SR; ff = f * (1 + .6 * np.exp(-t / .01)); return np.sin(2 * np.pi * np.cumsum(ff) / SR) * env_exp(n, .025) * .6
def bell(f, d=.9): n = int(d * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * 2 * f * t) + .2 * np.sin(2 * np.pi * 3.01 * f * t)) * env_exp(n, .25) * .3
def chime(): out = np.zeros(int(1.3 * SR))
def chime_():
    out = np.zeros(int(1.4 * SR))
    for k, m in enumerate([84, 88, 91, 96]): place(out, bell(note(m)), k * .07)
    return out * .8
def glitch():
    n = int(.35 * SR); x = rng.standard_normal(n); x = np.round(x * 4) / 4; out = np.zeros(n); k = 0
    while k < n:
        L = int(rng.uniform(.01, .035) * SR); 
        if rng.random() > .35: out[k:k + L] = x[k:k + L] * rng.uniform(.3, 1)
        k += L + int(rng.uniform(.005, .02) * SR)
    sub = np.sin(2 * np.pi * 60 * np.arange(n) / SR) * env_exp(n, .12)
    return hp(out, 500) * .5 + sub * .8
def thud(): n = int(.4 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (70 + 60 * np.exp(-t / .02)) * t) * env_exp(n, .09) + lp(rng.standard_normal(n), 2500) * env_exp(n, .03) * .6) * .9
def ding(): return bell(note(88), .7) + np.concatenate([np.zeros(int(.09 * SR)), bell(note(93), .7)])[: int(.7 * SR)]

# ---------- music
mus = np.zeros(N)
BEAT = 0.5  # 120 bpm
t_drop = S_D
# tense part: A minor, ticking clock, low pulse, sparse kicks (half time)
prog_t = [(45, [57, 60, 64]), (41, [53, 57, 60]), (43, [55, 59, 62]), (40, [52, 56, 59])]  # Am F G E
t = 0.0; bar = 0
while t < t_drop - 1e-6:
    root, ch = prog_t[bar % 4]
    bl = min(4 * BEAT, t_drop - t)
    place(mus, pad([m - 12 for m in ch], bl + .3, 700), t, 1.0)
    for k in range(8):
        tt = t + k * BEAT / 2
        if tt >= t_drop: break
        place(mus, bass(root, BEAT / 2 * .9), tt, .55)
        place(mus, tick(), tt, .18 if k % 2 else .28)
    if bar >= 1:
        place(mus, kick(), t, .7); place(mus, kick(), t + 2.5 * BEAT, .5)
        if t + 2 * BEAT < t_drop - 1.6: place(mus, clap(), t + 2 * BEAT, .25)
    t += 4 * BEAT; bar += 1
# uplifting part: C major, four-on-the-floor, plucks
prog_u = [(48, [60, 64, 67]), (43, [55, 59, 62, 67]), (45, [57, 60, 64]), (41, [53, 57, 60, 65])]  # C G Am F
arp = [0, 1, 2, 1, 2, 0, 1, 2]
t = t_drop; bar = 0; t_end_music = DUR - 1.2
while t < t_end_music:
    root, ch = prog_u[bar % 4]
    place(mus, pad(ch, 4 * BEAT + .3, 1600), t, 1.1)
    for k in range(4):
        tt = t + k * BEAT
        if tt >= t_end_music: break
        place(mus, kick(), tt, .85)
        if k % 2: place(mus, clap(), tt, .45)
        place(mus, hat(True), tt + BEAT / 2, .35)
        place(mus, bass(root, BEAT / 2 * .85), tt + BEAT / 2, .6)
    for k in range(8):
        tt = t + k * BEAT / 2
        if tt >= t_end_music: break
        place(mus, pluck(ch[arp[k] % len(ch)] + 12), tt, .55)
    t += 4 * BEAT; bar += 1
place(mus, pad([60, 64, 67, 72], 2.2, 2000), t_end_music, 1.4)
place(mus, boom(), t_end_music, .6)
place(mus, riser(1.6), t_drop - 1.6, .7)
place(mus, boom(), t_drop, .9)
# gentle fade at the very end
fe = int((DUR - .6) * SR); mus[fe:] *= np.linspace(1, 0, len(mus) - fe)

# ---------- sound effects
fx = np.zeros(N)
place(fx, boom(), 0.0, .8)
for k in range(14): place(fx, tick(), 0.06 * k, .9)
place(fx, glitch(), 0.88, 1.0)
for st in (S_B, S_C, S_D, S_E, S_F): place(fx, whoosh(), st - .25, .9)
for k in range(10): place(fx, pop(700 + 40 * k), v(9.0) + k * .09, .7)
place(fx, thud(), v(13.02), .6); place(fx, thud(), v(15.56), .8)
place(fx, boom(), v(17.13), .9); place(fx, glitch(), v(17.13), .6)
place(fx, thud(), v(21.36), .8)
for i in range(5): place(fx, pop(1100), v(24.9) + i * .22, .5)
place(fx, pop(900), v(27.44), .6)
place(fx, chime_(), v(30.57), .9)
place(fx, chime_(), v(35.0), .9)

def save(name, x):
    x = np.clip(x, -1, 1); d = (x * 32767).astype(np.int16)
    with wave.open(name, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
mus /= np.max(np.abs(mus)) + 1e-9; fx /= np.max(np.abs(fx)) + 1e-9
save("audio/music3.wav", mus * .9); save("audio/sfx3.wav", fx * .9)
print("ok", len(mus) / SR)
