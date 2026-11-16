# -*- coding: utf-8 -*-
"""Bangun video ringkasan penelitian (EN / ID) dari hasil CSV yang sudah ada.

- Hanya membaca berkas sumber di C:\\EPIS_KERJA\\AI_EPISTEMICS_2026_PHASE_2_PREP.
- Tidak memanggil model/API dan tidak menghitung statistik baru.
- Bingkai digambar dengan Pillow lalu dialirkan ke ffmpeg (h264_nvenc) lewat pipe,
  sehingga tidak ada berkas bingkai sementara.

Pemakaian (dari folder ini):
  py -3.12 -I -X utf8 bangun_video.py --lang en --check
  py -3.12 -I -X utf8 bangun_video.py --lang en
  py -3.12 -I -X utf8 bangun_video.py --lang id
"""
import argparse
import csv
import json
import os
import re
import subprocess
import threading
import time

from PIL import Image, ImageDraw, ImageFont

SRC_ROOT = r"C:\EPIS_KERJA\AI_EPISTEMICS_2026_PHASE_2_PREP"
HASIL = os.path.join(SRC_ROOT, "HASIL_PENGUJIAN")
P_LAP36 = os.path.join(HASIL, "_lapis36", "tabel_lapis36_4model.csv")
P_PEM = os.path.join(HASIL, "_lapis36", "tabel_pembanding_lapis_40_36_26_19.csv")
P_ANALISIS = os.path.join(HASIL, "_lapis36", "analisis_lapis36.md")
P_KES = os.path.join(HASIL, "_retest_lapis19", "KESTABILAN.csv")
P_KES_MD = os.path.join(HASIL, "_retest_lapis19", "KESTABILAN.md")
P_PREREG = os.path.join(SRC_ROOT, "harness", "PREREG_DIBEKUKAN.md")

OUT = r"C:\EPIS_KERJA\RENDER\video"
CEK = os.path.join(OUT, "cek_bingkai")
FONT_DIR = r"C:\Windows\Fonts"
FONT_FILES = {"R": "segoeui.ttf", "L": "segoeuisl.ttf", "B": "segoeuib.ttf"}

W, H, FPS = 1920, 1080, 30
MAX_TEMP = 80
XFADE = 0.5
BRIER_MAX = 0.14

M_QWEN38 = "qwen3.8-flash"
M_QWEN4 = "qwen4-max-preview"
M_DEEP = "deepseek-v4.1-flash"
M_CODEX = "codex_gpt61_sol_tak_terverifikasi"
# (kunci di CSV, label tampil, warna buta-warna-aman Okabe-Ito, batang terang?)
MODELS = [
    (M_QWEN38, "qwen3.8-flash", "#0072B2", False),
    (M_QWEN4, "qwen4-max-preview", "#E69F00", False),
    (M_DEEP, "deepseek-v4.1-flash", "#009E73", False),
    (M_CODEX, "GPT-6.1 Sol (unverified)", "#CC79A7", True),
]
STAB_MODELS = [M_QWEN38, M_QWEN4, M_DEEP]
MET_BRIER = "Brier batas 1 own R3 (anchor SUPPORTED)"
MET_SESUAI = "Sesuai (label R1 = R3)"

WHITE = (255, 255, 255)
TXT = "#1F2933"
MUTED = "#52606D"
ACC = "#3E4C59"
CARD = "#F4F6F9"
BORDER = "#CBD2D9"
TRACK = "#E4E9F0"

TEXT = {
    "en": {
        "s1_title": "How Much Evidence Is Enough?",
        "s1_sub": "Calibration of LLM verdicts across evidence depth on academic claims",
        "s1_q": "Do model verdicts on academic claims stay calibrated as the model reads more of the paper?",
        "s1_tag": "Apart Research sprint, AI Epistemics",
        "s2_title": "Design: one claim, three evidence depths",
        "s2_cap": "Same claim, same question, same wording. Only the amount of evidence changes.",
        "s2_cards": [("R1", "Abstract"), ("R2", "Abstract + results"), ("R3", "Full text")],
        "s2_comp": "Comparator: evidence from other articles (sample animation)",
        "s2_comp_docs": "Evidence from other articles",
        "s2_foot": "Each model returns a verdict and a probability at every depth.",
        "s3_title": "From 294 candidate claims to 36 analysed claims",
        "s3_rows": [("294", "candidate claims, pre-registered"),
                    ("40", "claims assessed by the author team"),
                    ("36", "claims in the main analysis")],
        "s3_foot": "Main layer: 36 claims x 7 observations = {n_obs} per model.",
        "s4_title": "Results: Brier score and R1 vs R3 agreement",
        "s4_left": "Brier score at R3 on anchored claims (lower is better)",
        "s4_right": "R1 and R3 verdict labels agree",
        "s4_foot": "A pattern, not a ranking. Brier is measured against the mechanical key. GPT-6.1 Sol is unverified (lighter bar).",
        "s5_title": "Test-retest stability, three API models",
        "s5_sub": "Share of observations with the same verdict on re-run",
        "s5_foot": "{n_stab} observations per model across {n_claims} claims. Counting the 2 parse failures as changed verdicts gives {gagal_deep}% for deepseek-v4.1-flash.",
        "s6_title": "Limits",
        "s6_items": [
            "36 claims in the main layer: a small sample.",
            "Wide intervals: for qwen3.8-flash, the agreement interval runs from {ci_lo}% to {ci_hi}%.",
            "The key is mechanical, not an expert judgment.",
            "GPT-6.1 Sol is unverified, so its results are not confirmed.",
            "Confidence intervals overlap across the API models.",
        ],
        "s7_title": "Patterns, not model rankings",
        "s7_sub": "Four models, one method, one color per model.",
    },
    "id": {
        "s1_title": "Seberapa Banyak Bukti Itu Cukup?",
        "s1_sub": "Kalibrasi vonis LLM pada berbagai kedalaman bukti untuk klaim akademik",
        "s1_q": "Apakah vonis model terhadap klaim akademik tetap terkalibrasi saat model membaca lebih banyak isi artikel?",
        "s1_tag": "Sprint Apart Research, AI Epistemics",
        "s2_title": "Desain: satu klaim, tiga kedalaman bukti",
        "s2_cap": "Klaim, pertanyaan, dan kata-katanya sama. Hanya jumlah bukti yang berubah.",
        "s2_cards": [("R1", "Abstrak"), ("R2", "Abstrak + hasil"), ("R3", "Teks penuh")],
        "s2_comp": "Pembanding: bukti dari artikel lain (animasi contoh)",
        "s2_comp_docs": "Bukti dari artikel lain",
        "s2_foot": "Setiap model memberi vonis dan probabilitas pada setiap kedalaman bukti.",
        "s3_title": "Dari 294 klaim calon menjadi 36 klaim yang dianalisis",
        "s3_rows": [("294", "klaim calon, sudah praregistrasi"),
                    ("40", "klaim dinilai oleh tim penulis"),
                    ("36", "klaim dalam analisis utama")],
        "s3_foot": "Lapis utama: 36 klaim x 7 pengamatan = {n_obs} per model.",
        "s4_title": "Hasil: skor Brier dan kesesuaian R1 vs R3",
        "s4_left": "Skor Brier pada R3 untuk klaim berjangkar (makin kecil makin baik)",
        "s4_right": "Label vonis R1 dan R3 sama",
        "s4_foot": "Pola, bukan peringkat. Brier diukur terhadap kunci mekanis. GPT-6.1 Sol belum terverifikasi (batang terang).",
        "s5_title": "Kestabilan uji ulang, tiga model API",
        "s5_sub": "Proporsi pengamatan dengan vonis yang sama saat diulang",
        "s5_foot": "{n_stab} pengamatan per model dari {n_claims} klaim. Jika 2 kegagalan parse dihitung sebagai vonis berubah, deepseek-v4.1-flash menjadi {gagal_deep}%.",
        "s6_title": "Keterbatasan",
        "s6_items": [
            "36 klaim pada lapis utama: sampel kecil.",
            "Interval lebar: untuk qwen3.8-flash, kesesuaian berkisar {ci_lo}% sampai {ci_hi}%.",
            "Kunci bersifat mekanis, bukan penilaian ahli.",
            "GPT-6.1 Sol belum terverifikasi, sehingga hasilnya belum dapat dipastikan.",
            "Interval kepercayaan antarmodel API saling tumpang tindih.",
        ],
        "s7_title": "Pola, bukan peringkat model",
        "s7_sub": "Empat model, satu metode, satu warna per model.",
    },
}


# ---------------------------------------------------------------- data (baca saja)
def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def pick(rows, **want):
    hits = [r for r in rows if all(r.get(k) == v for k, v in want.items())]
    if len(hits) > 1:
        raise SystemExit("Pencocokan ganda: %s" % want)
    return hits[0] if hits else None


def load_data(log):
    lap = read_csv(P_LAP36)
    pem = read_csv(P_PEM)
    kes = read_csv(P_KES)
    D = {"brier": {}, "brier_n": {}, "sesuai": {}, "stab": {}, "stab_gagal": {}, "stab_n": {}}
    for key, label, _, _ in MODELS:
        r = pick(lap, model=key, lapis="36", metrik=MET_BRIER)
        s = pick(lap, model=key, lapis="36", metrik=MET_SESUAI)
        if r is None or s is None:
            raise SystemExit("Baris lapis36 tidak ditemukan untuk " + key)
        D["brier"][key] = float(r["nilai"])
        D["brier_n"][key] = int(r["n"])
        D["sesuai"][key] = float(s["nilai"])
        log.append(f"CSV lapis36 | {label} | Brier own R3 batas1 = {r['nilai']} (n={r['n']}) | Sesuai R1=R3 = {s['nilai']} (n={s['n']})")
        p = pick(pem, model=key, metrik=MET_BRIER)
        if p is None:
            log.append(f"  cek silang pembanding: baris tidak ada untuk {label}")
        else:
            ok = abs(float(p["nilai_lapis36"]) - D["brier"][key]) < 1e-6
            log.append(f"  cek silang pembanding nilai_lapis36 = {p['nilai_lapis36']} | cocok = {ok}")
            if not ok:
                raise SystemExit("Cek silang pembanding gagal untuk " + label)
    ci = pick(lap, model=M_QWEN38, lapis="36", metrik=MET_SESUAI)
    D["ci_lo"] = float(ci["ci_lo"])
    D["ci_hi"] = float(ci["ci_hi"])
    log.append(f"CSV lapis36 | qwen3.8-flash | Sesuai ci_lo = {ci['ci_lo']} ci_hi = {ci['ci_hi']}")
    ci_rng = {}
    for key, label, _, _ in MODELS:
        r = pick(lap, model=key, lapis="36", metrik=MET_SESUAI)
        ci_rng[key] = (float(r["ci_lo"]), float(r["ci_hi"]))
    api = [ci_rng[k] for k in STAB_MODELS]
    overlap_all = all(a[0] <= b[1] and b[0] <= a[1] for i, a in enumerate(api) for b in api[i + 1:])
    log.append(f"Interval Sesuai tiga model API saling tumpang tindih (semua pasangan) = {overlap_all}")
    if not overlap_all:
        raise SystemExit("Klaim 'interval saling tumpang tindih' tidak terpenuhi")
    for key in STAB_MODELS:
        r = pick(kes, model=key, tingkat_bukti="SEMUA")
        D["stab"][key] = float(r["persen_argmax_sama"])
        D["stab_gagal"][key] = float(r["persen_argmax_sama_gagal_dihitung_beda"])
        D["stab_n"][key] = int(r["n_observasi"])
        log.append(f"CSV KESTABILAN | {key} | SEMUA | persen_argmax_sama = {r['persen_argmax_sama']} | gagal dihitung beda = {r['persen_argmax_sama_gagal_dihitung_beda']} | n_observasi = {r['n_observasi']}")
    kes_md = open(P_KES_MD, encoding="utf-8", errors="replace").read()
    m = re.search(r"Cakupan: (\d+) klaim", kes_md)
    D["n_claims"] = int(m.group(1))
    log.append(f"KESTABILAN.md | Cakupan = {D['n_claims']} klaim")
    ana = open(P_ANALISIS, encoding="utf-8", errors="replace").read()
    obs = [int(x) for x in re.findall(r"Jumlah observasi: (\d+)", ana)]
    D["n_obs"] = obs[0]
    log.append(f"analisis_lapis36.md | 'Jumlah observasi' = {sorted(set(obs))} (jumlah kemunculan {len(obs)})")
    if not obs or set(obs) != {D["n_obs"]} or D["n_obs"] != 36 * 7:
        raise SystemExit("Jumlah observasi tidak sesuai 36 x 7")
    prereg = open(P_PREREG, encoding="utf-8", errors="replace").read()
    ok294 = "294 klaim" in prereg
    ok40 = "40 pernyataan" in prereg
    log.append(f"PREREG_DIBEKUKAN.md | '294 klaim' ditemukan = {ok294} | '40 pernyataan' ditemukan = {ok40}")
    if not (ok294 and ok40):
        raise SystemExit("Angka corong tidak ditemukan di praregistrasi")
    D["funnel"] = (294, 40, D["brier_n"][M_QWEN38])
    log.append(f"Corong: 294 (prereg) -> 40 (prereg) -> {D['funnel'][2]} (CSV n lapis36)")
    if D["funnel"][2] != 36:
        raise SystemExit("n lapis36 bukan 36")
    return D


# ---------------------------------------------------------------- drawing helpers
def F(kind, size, _cache={}):
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, FONT_FILES[kind]), size)
    return _cache[key]


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def ease(p):
    p = clamp(p)
    return 1 - (1 - p) ** 3


def P(t, start, dur=0.6):
    return ease((t - start) / dur)


def mix(col, op):
    """Campur warna dengan putih sesuai opasitas (latar selalu putih)."""
    op = clamp(op)
    base = col if isinstance(col, tuple) else tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))
    return tuple(round(255 + (b - 255) * op) for b in base)


def fmt(v, dec, lang):
    s = f"{v:.{dec}f}"
    return s.replace(".", ",") if lang == "id" else s


def overlap(a, b, pad=4):
    return not (a[3] + pad <= b[1] or b[3] + pad <= a[1] or a[4] + pad <= b[2] or b[4] + pad <= a[2])


class Canvas:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), WHITE)
        self.d = ImageDraw.Draw(self.img)
        self.boxes = []

    def text(self, x, y, s, f, col, op=1.0, anchor="la"):
        if op <= 0.01 or not s:
            return
        bb = self.d.textbbox((x, y), s, font=f, anchor=anchor)
        self.d.text((x, y), s, font=f, fill=mix(col, op), anchor=anchor)
        self.boxes.append((s[:24], bb[0], bb[1], bb[2], bb[3]))

    def width(self, s, f):
        return self.d.textlength(s, font=f)

    def wrap(self, s, f, maxw):
        lines, cur = [], ""
        for word in s.split():
            trial = (cur + " " + word).strip()
            if not cur or self.d.textlength(trial, font=f) <= maxw:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, f, col, maxw, lh, op=1.0):
        for i, ln in enumerate(self.wrap(s, f, maxw)):
            self.text(x, y + i * lh, ln, f, col, op)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=1, radius=0, op=1.0):
        if op <= 0.01:
            return
        kw = {}
        if fill is not None:
            kw["fill"] = mix(fill, op)
        if outline is not None:
            kw["outline"] = mix(outline, op)
        if radius > 0:
            self.d.rounded_rectangle((x0, y0, x1, y1), radius=radius, width=width, **kw)
        else:
            self.d.rectangle((x0, y0, x1, y1), width=width, **kw)

    def line(self, x0, y0, x1, y1, col, op, width=4):
        if op <= 0.01:
            return
        self.d.line((x0, y0, x1, y1), fill=mix(col, op), width=width)

    def poly(self, pts, col, op):
        if op <= 0.01:
            return
        self.d.polygon(pts, fill=mix(col, op))


def hbar(c, x, y, track_w, h, frac, col, light, op, grow):
    c.rect(x, y, x + track_w, y + h, fill=TRACK, radius=h // 2, op=op)
    w = max(h, round(track_w * clamp(frac) * clamp(grow)))
    if light:
        c.rect(x, y, x + w, y + h, fill=mix(col, 0.55), outline=col, width=3, radius=h // 2, op=op)
    else:
        c.rect(x, y, x + w, y + h, fill=col, radius=h // 2, op=op)


# ---------------------------------------------------------------- scenes
def scene1(c, t, L, D):
    c.text(120, 290, L["s1_title"], F("B", 96), TXT, P(t, 0.2, 0.8))
    bar_w = round(420 * P(t, 1.2, 1.0))
    if bar_w > 8:
        c.rect(120, 430, 120 + bar_w, 438, fill=ACC, radius=4)
    c.para(120, 470, L["s1_sub"], F("R", 44), MUTED, 1500, 60, P(t, 1.5))
    c.para(120, 680, L["s1_q"], F("R", 46), TXT, 1500, 62, P(t, 3.5))
    c.text(120, 975, L["s1_tag"], F("R", 30), MUTED, P(t, 5.0))


def scene2(c, t, L, D):
    c.text(120, 90, L["s2_title"], F("B", 60), TXT, P(t, 0.1))
    c.para(120, 180, L["s2_cap"], F("R", 36), MUTED, 1680, 50, P(t, 0.6))
    for i, (code, label) in enumerate(L["s2_cards"]):
        x, y = 120 + i * 540, 330
        op = P(t, 1.0 + i * 1.5, 0.7)
        c.rect(x, y, x + 480, y + 300, fill=CARD, outline=BORDER, width=2, radius=24, op=op)
        c.text(x + 40, y + 34, code, F("B", 84), ACC, op)
        c.text(x + 40, y + 140, label, F("R", 40), TXT, op)
        for j in range(3):
            c.rect(x + 40 + j * 140, y + 230, x + 150 + j * 140, y + 256,
                   fill=(ACC if j <= i else TRACK), radius=12, op=op)
        if i < 2:
            ap = P(t, 1.0 + (i + 1) * 1.5 - 0.6, 0.5)
            ax0, ax1, ay = x + 504, x + 516, y + 150
            c.line(ax0, ay, ax0 + (ax1 - ax0) * ap, ay, ACC, ap, 6)
            if ap > 0.9:
                c.poly([(x + 516, ay - 16), (x + 538, ay), (x + 516, ay + 16)], ACC, ap)
    c.text(120, 722, L["s2_comp"], F("R", 36), MUTED, P(t, 5.5))
    for i in range(5):
        p = P(t, 6.0 + i * 0.25, 0.8)
        x, ytop = 120 + i * 120, 790 + (1 - p) * 60
        c.rect(x, ytop, x + 80, ytop + 110, fill=CARD, outline=BORDER, width=2, radius=8, op=p)
        for j in range(3):
            c.rect(x + 14, ytop + 26 + j * 26, x + 66, ytop + 32 + j * 26, fill=BORDER, radius=3, op=p)
    c.text(760, 840, L["s2_comp_docs"], F("R", 40), TXT, P(t, 7.0))
    c.text(120, 960, L["s2_foot"], F("R", 36), TXT, P(t, 9.5))


def scene3(c, t, L, D):
    c.text(120, 90, L["s3_title"], F("B", 60), TXT, P(t, 0.1))
    fb, fd = F("B", 84), F("R", 36)
    scale = 820
    for i, (num, desc) in enumerate(L["s3_rows"]):
        n = D["funnel"][i]
        y = 260 + i * 220
        frac = n / D["funnel"][0]
        grow = ease((t - (1.0 + i * 2.0)) / 1.4)
        w = max(120, round(scale * frac * grow))
        c.rect(120, y, 120 + w, y + 120, fill=ACC, radius=20)
        lab_op = P(t, 1.0 + i * 2.0 + 1.2, 0.6)
        x_lab = 120 + round(scale * frac) + 40
        c.text(x_lab, y + 4, num, fb, ACC, lab_op)
        c.text(x_lab + c.width(num, fb) + 24, y + 30, desc, fd, TXT, lab_op)
    c.para(120, 930, L["s3_foot"].format(n_obs=D["n_obs"]), F("R", 36), TXT, 1680, 48, P(t, 9.0))


def scene4(c, t, L, D):
    c.text(120, 90, L["s4_title"], F("B", 56), TXT, P(t, 0.1))
    panels = [(120, L["s4_left"], "brier"), (1020, L["s4_right"], "sesuai")]
    for x, title, kind in panels:
        c.para(x, 215, title, F("R", 34), TXT, 780, 44, P(t, 0.5))
        for i, (key, label, col, light) in enumerate(MODELS):
            y = 370 + i * 130
            lab_op = P(t, 1.0 + i * 0.3, 0.6)
            c.text(x, y, label, F("R", 32), TXT, lab_op)
            if kind == "brier":
                frac, txt = D["brier"][key] / BRIER_MAX, fmt(D["brier"][key], 3, "en")
                txt = fmt(D["brier"][key], 3, L.get("lang", "en"))
            else:
                frac = D["sesuai"][key]
                txt = fmt(D["sesuai"][key] * 100, 1, L.get("lang", "en")) + "%"
            grow = ease((t - (1.5 + i * 0.3)) / 1.2)
            hbar(c, x, y + 50, 600, 44, frac, col, light, P(t, 1.0 + i * 0.3, 0.4), grow)
            c.text(x + 620, y + 52, txt, F("B", 36), TXT, P(t, 2.6 + i * 0.3, 0.6))
    c.para(120, 920, L["s4_foot"], F("R", 30), MUTED, 1680, 42, P(t, 8.0))


def scene5(c, t, L, D):
    c.text(120, 90, L["s5_title"], F("B", 60), TXT, P(t, 0.1))
    c.text(120, 178, L["s5_sub"], F("R", 38), MUTED, P(t, 0.5))
    for i, key in enumerate(STAB_MODELS):
        _, label, col, _ = [m for m in MODELS if m[0] == key][0]
        y = 300 + i * 150
        op = P(t, 1.2 + i * 0.6, 0.6)
        c.text(120, y, label, F("B", 40), TXT, op)
        grow = ease((t - (2.0 + i * 0.6)) / 1.6)
        hbar(c, 120, y + 64, 1400, 46, D["stab"][key], col, False, op, grow)
        c.text(1560, y + 56, fmt(D["stab"][key] * 100, 1, L.get("lang", "en")) + "%", F("B", 44), TXT,
               P(t, 2.8 + i * 0.6, 0.6))
    c.text(120, 722, "0%", F("R", 30), MUTED, P(t, 4.0))
    c.text(1520, 722, "100%", F("R", 30), MUTED, P(t, 4.0), anchor="ra")
    gagal = fmt(D["stab_gagal"][M_DEEP] * 100, 1, L.get("lang", "en"))
    c.para(120, 800, L["s5_foot"].format(n_stab=D["stab_n"][M_QWEN38], n_claims=D["n_claims"],
                                         gagal_deep=gagal), F("R", 34), TXT, 1680, 50, P(t, 5.5))


def scene6(c, t, L, D):
    c.text(120, 90, L["s6_title"], F("B", 64), TXT, P(t, 0.1))
    ci = {"ci_lo": fmt(D["ci_lo"] * 100, 1, L.get("lang", "en")), "ci_hi": fmt(D["ci_hi"] * 100, 1, L.get("lang", "en"))}
    for i, item in enumerate(L["s6_items"]):
        y = 260 + i * 140
        op = P(t, 0.8 + i * 1.2, 0.7)
        c.rect(122, y + 18, 142, y + 38, fill=ACC, radius=10, op=op)
        c.para(180, y, item.format(**ci), F("R", 44), TXT, 1640, 56, op)


def scene7(c, t, L, D):
    c.text(W // 2, 370, L["s7_title"], F("B", 92), TXT, P(t, 0.2, 0.9), anchor="ma")
    c.text(W // 2, 530, L["s7_sub"], F("L", 44), MUTED, P(t, 1.2), anchor="ma")
    for i, (key, label, col, _) in enumerate(MODELS):
        cx = 960 + round((i - 1.5) * 380)
        op = P(t, 2.2 + i * 0.3, 0.6)
        c.rect(cx - 14, 676, cx + 14, 704, fill=col, radius=14, op=op)
        c.text(cx, 730, label, F("R", 30), TXT, op, anchor="ma")


SCENES = [
    ("judul", scene1, 10.0),
    ("desain", scene2, 14.0),
    ("corong", scene3, 12.0),
    ("hasil", scene4, 18.0),
    ("kestabilan", scene5, 12.0),
    ("keterbatasan", scene6, 12.0),
    ("penutup", scene7, 6.0),
]


def timeline(durs):
    starts, s = [], 0.0
    for d in durs:
        starts.append(s)
        s = s + d - XFADE
    return starts, starts[-1] + durs[-1]


def scene_img(i, t, L, D):
    c = Canvas()
    SCENES[i][1](c, t, L, D)
    return c


def frame_img(T, L, D, starts):
    i = 0
    for j, s in enumerate(starts):
        if s <= T + 1e-9:
            i = j
    ti = T - starts[i]
    img = scene_img(i, ti, L, D).img
    if i > 0 and ti < XFADE:
        prev = scene_img(i - 1, T - starts[i - 1], L, D).img
        img = Image.blend(prev, img, clamp(ti / XFADE))
    return img


def layout_issues(L, D, durs):
    issues = []
    for i, (name, fn, _) in enumerate(SCENES):
        c = Canvas()
        fn(c, durs[i] - 1.0, L, D)
        bx = c.boxes
        for b in bx:
            if b[1] < 60 or b[3] > W - 60 or b[2] < 40 or b[4] > H - 40:
                issues.append(f"adegan {name}: teks keluar batas {b}")
        for a in range(len(bx)):
            for k in range(a + 1, len(bx)):
                if overlap(bx[a], bx[k]):
                    issues.append(f"adegan {name}: tumpang tindih {bx[a][0]!r} dan {bx[k][0]!r}")
    return issues


# ---------------------------------------------------------------- GPU, encode
class Overheat(Exception):
    pass


def gpu_status():
    r = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu",
                        "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError("nvidia-smi gagal: " + r.stderr.strip())
    temp, util = [int(x.strip()) for x in r.stdout.strip().splitlines()[0].split(",")]
    return temp, util


class TempWatch(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.peak = 0
        self.hot = threading.Event()
        self.stop_ev = threading.Event()

    def run(self):
        while not self.stop_ev.is_set():
            try:
                t, _ = gpu_status()
                self.peak = max(self.peak, t)
                if t > MAX_TEMP:
                    self.hot.set()
            except Exception:
                pass
            self.stop_ev.wait(5)


def wait_cool(log):
    while True:
        t, _ = gpu_status()
        log.append(f"  suhu GPU sebelum encode: {t} C")
        if t <= MAX_TEMP:
            return
        log.append("  suhu di atas 80 C, menunggu dingin (cek tiap 30 detik)")
        time.sleep(30)


def run_encode(out_path, L, D, starts, total, log):
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "h264_nvenc", "-preset", "p5", "-cq", "23", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    n = round(total * FPS)
    hot = False
    try:
        for k in range(n):
            if WATCH.hot.is_set():
                hot = True
                break
            proc.stdin.write(frame_img(k / FPS, L, D, starts).tobytes())
    except BrokenPipeError:
        pass
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
    if hot:
        proc.kill()
        proc.wait()
        log.append("  suhu GPU lebih dari 80 C saat encode, encode dihentikan dan diulang setelah dingin")
        return "hot"
    rc = proc.wait()
    err = proc.stderr.read().decode(errors="replace")
    if rc != 0:
        raise SystemExit(f"NVENC/ffmpeg gagal (rc={rc}): {err.strip()}")
    return "ok"


def encode_lang(lang, L, D, log):
    durs = [d for _, _, d in SCENES]
    starts, total = timeline(durs)
    out = os.path.join(OUT, f"ringkasan_{lang}.mp4")
    for attempt in range(1, 4):
        wait_cool(log)
        WATCH.hot.clear()
        log.append(f"encode {lang} percobaan {attempt}, h264_nvenc p5 cq23")
        if run_encode(out, L, D, starts, total, log) == "ok":
            break
    else:
        raise SystemExit("Suhu GPU terlalu tinggi 3 kali, berhenti")
    # cek-bingkai: tangkapan dari berkas MP4 jadi, satu per adegan (setelah isi tampil)
    for i, (name, _, dur) in enumerate(SCENES):
        ts = starts[i] + dur - 1.0
        dst = os.path.join(CEK, f"{lang}_{i + 1}_{name}.png")
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", out,
                        "-ss", f"{ts:.2f}", "-frames:v", "1", dst], check=True)
    pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                         "stream=codec_name,width,height,r_frame_rate,pix_fmt,nb_frames,codec_type:format=duration,size",
                         "-of", "json", out], capture_output=True, text=True, check=True)
    info = json.loads(pr.stdout)
    log.append(f"ffprobe {lang}: {json.dumps(info, ensure_ascii=True)}")
    return info


WATCH = TempWatch()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["en", "id"], required=True)
    ap.add_argument("--check", action="store_true", help="hanya cocokkan angka dan periksa tata letak")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CEK, exist_ok=True)
    log = [f"=== bahasa: {args.lang} ==="]
    D = load_data(log)
    L = dict(TEXT[args.lang])
    L["lang"] = args.lang
    durs = [d for _, _, d in SCENES]
    starts, total = timeline(durs)
    log.append(f"linimasa: total {total:.1f} s, {round(total * FPS)} bingkai, transisi {XFADE} s")
    issues = layout_issues(L, D, durs)
    log.append(f"periksa tata letak: {len(issues)} masalah")
    log.extend("  " + s for s in issues)
    with open(os.path.join(OUT, f"angka_pencocokan_{args.lang}.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    print("\n".join(log))
    if issues:
        raise SystemExit("Tata letak bermasalah, perbaiki sebelum encode")
    if args.check:
        return
    WATCH.start()
    try:
        info = encode_lang(args.lang, L, D, log)
    finally:
        WATCH.stop_ev.set()
    log.append(f"suhu GPU tertinggi selama sesi: {WATCH.peak} C")
    with open(os.path.join(OUT, f"angka_pencocokan_{args.lang}.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    print("\n".join(log[-3:]))
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    main()
