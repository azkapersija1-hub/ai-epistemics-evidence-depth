# -*- coding: utf-8 -*-
"""Bangun video ringkasan (EN / ID) memakai data UTAMA-274 (274 klaim non-pilot).

Salinan dari bangun_video294.py (yang berasal dari bangun_video.py), sumber data diganti
ke baris UTAMA-274 pada tabel_utama294_3model.csv yang sudah tersimpan di repo.
- Hanya membaca berkas yang sudah tersimpan. Tidak memanggil model/API, tidak menghitung
  statistik baru. Set 294 (termasuk pilot) hanya disebut sebagai analisis tambahan.
- Keluaran di folder video/ repo dengan nama *274*; berkas 294 tidak disentuh.
- Bingkai digambar dengan Pillow lalu dialirkan ke ffmpeg lewat pipe
  (h264_nvenc; bila NVENC gagal, otomatis libx264).

Pemakaian:
  py -3.12 -I -X utf8 bangun_video274.py --lang en --check
  py -3.12 -I -X utf8 bangun_video274.py --lang en
  py -3.12 -I -X utf8 bangun_video274.py --lang id
"""
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import threading
import time

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UTAMA_REPO = os.path.join(REPO, "results", "utama294")
P_MAIN = os.path.join(UTAMA_REPO, "tabel_utama294_3model.csv")
P_JUM = os.path.join(UTAMA_REPO, "jumlah_set.md")
P_G2 = os.path.join(REPO, "figures", "G2_near_far_en.svg")

SRC_ROOT = r"C:\EPIS_KERJA\AI_EPISTEMICS_2026_PHASE_2_PREP"
HASIL = os.path.join(SRC_ROOT, "HASIL_PENGUJIAN")
P_MAIN_SRC = os.path.join(HASIL, "_utama294", "tabel_utama294_3model.csv")
P_KES = os.path.join(HASIL, "_retest_lapis19", "KESTABILAN.csv")
P_KES_MD = os.path.join(HASIL, "_retest_lapis19", "KESTABILAN.md")
P_LAP36 = os.path.join(SRC_ROOT, "bahan", "v2", "hasil_olahan_final", "lapis_36_claim_id.txt")
P_PREREG = os.path.join(SRC_ROOT, "harness", "PREREG_DIBEKUKAN.md")

OUT = os.path.join(REPO, "video")
CEK = r"C:\Users\AZMI\AppData\Local\Temp\claude\ba4560581ec5e27d\b27b3f19-7d79-47d0-b1c8-4139d0074b6d\scratchpad\cek274"
FONT_DIR = r"C:\Windows\Fonts"
FONT_FILES = {"R": "segoeui.ttf", "L": "segoeuisl.ttf", "B": "segoeuib.ttf"}

W, H, FPS = 1920, 1080, 30
MAX_TEMP = 80
XFADE = 0.5
BRIER_MAX = 0.25

SET_MAIN = "UTAMA-274"   # 274 klaim non-pilot (dev+val+holdout), 1918 observasi per model
N_CLAIMS, N_OBS = 274, 1918
M_QWEN38 = "qwen3.8-flash"
M_QWEN4 = "qwen4-max-preview"
M_DEEP = "deepseek-v4.1-flash"
# (kunci di CSV, label tampil, warna Okabe-Ito)
MODELS = [
    (M_QWEN38, "qwen3.8-flash", "#0072B2"),
    (M_QWEN4, "qwen4-max-preview", "#E69F00"),
    (M_DEEP, "deepseek-v4.1-flash", "#009E73"),
]
MET_OWN = "Brier batas 1 own R3 (anchor SUPPORTED)"
MET_NEAR3 = "Brier batas 1 near R3 (anchor NEI)"
MET_FAR3 = "Brier batas 1 far R3 (anchor NEI)"
MET_FS_NEAR3 = "False-support near R3"
MET_FS_FAR3 = "False-support far R3"
MET_SESUAI = "Sesuai (label R1 = label R3)"
MET_DIFF_R1 = "Selisih FS near-far R1"
MET_DIFF_R3 = "Selisih FS near-far R3"

# Nilai kunci yang diminta (Table 1, set 274), urutan qwen3.8, qwen4, deepseek, 4 desimal.
EXPECTED = {
    "own": (0.0343, 0.0235, 0.0981),
    "near3": (0.1441, 0.2191, 0.0622),
    "sesuai": (0.5146, 0.5511, 0.5000),
    "diff_r3": (0.0483, 0.0631, 0.0086),
    "diff_r1": (0.0334, 0.0549, 0.0235),
}

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
        "s1_tag": "Apart Research sprint, AI Epistemics. Main analysis: 274 non-pilot claims.",
        "s2_title": "Design: one claim, three evidence depths",
        "s2_cap": "Same claim, same question, same wording. Only the amount of evidence changes.",
        "s2_cards": [("R1", "Abstract"), ("R2", "Abstract + results"), ("R3", "Full text")],
        "s2_comp": "Comparators: evidence from other articles, as near and far (sample animation)",
        "s2_near": "near",
        "s2_far": "far",
        "s2_comp_docs": "Evidence from other articles",
        "s2_foot": "Each model returns a verdict and a probability at every depth.",
        "s3_title": "Data: 274 non-pilot claims, three API models",
        "s3_cards": [("274", "non-pilot claims in the main analysis, pre-registered"),
                     ("{n_obs}", "observations per model: 274 claims x 7 readings"),
                     ("3", "API models, same prompt and same key")],
        "s3_val_title": "Validation by the author team: 40 claims assessed, 36 after deliberation",
        "s3_val_sub": "Anchor labels are mechanical and provisional. The key and claim text are not released.",
        "s3_supp": "The 294-claim set, which includes the pilot, is a supplementary analysis only.",
        "s4_title": "Results: Brier score by model and evidence source",
        "s4_sub": "Brier at R3 on anchored claims: own evidence, near evidence, far evidence",
        "s4_legend": ["own R3", "near R3", "far R3"],
        "s4_foot": "Lower is better. A pattern, not a ranking. Brier is measured against the mechanical key.",
        "s4_note": "Parse failures are excluded: own R3 for deepseek-v4.1-flash uses {n_deep_own} of 274 claims, far R3 for qwen3.8-flash uses {n_q38_far} of 274.",
        "s5_title": "False support and label consistency at R3",
        "s5_left": "False support at R3: near vs far evidence (share of observations)",
        "s5_right": "R1 and R3 verdict labels stay the same",
        "s5_right_note": "About half of the labels change between R1 and R3. For deepseek-v4.1-flash, {n_deep_ses} of 274 claims are compared.",
        "s5_near": "near",
        "s5_far": "far",
        "s5_foot": "False support: mass on SUPPORTED or REFUTED where the anchor label is NEI. Validity of near and far evidence is not yet independent.",
        "s6_title": "Near minus far false support, and test-retest stability",
        "s6_left": "Near minus far false support, 95% CI in brackets",
        "s6_cols": [("R1", "abstract"), ("R3", "full text")],
        "s6_zero": "For deepseek-v4.1-flash at R3, the interval includes zero. Descriptive pattern only, no causal claim.",
        "s6_right": "Same verdict on re-run, separate 19-claim retest",
        "s6_foot": "Stability uses {n_stab} observations per model and is not recomputed on the 274 set. Counting the 2 parse failures as changed gives {gagal_deep}% for deepseek-v4.1-flash.",
        "s7_title": "Limits",
        "s7_items": [
            "36 claims validated by the author team: a small sample.",
            "Wide intervals: for qwen3.8-flash, the agreement interval runs from {ci_lo}% to {ci_hi}%.",
            "Anchor labels are mechanical and provisional. They are not a judgment of factual accuracy.",
            "Near and far evidence is not yet validated independently. No causal claims.",
            "GPT-6.1 Sol is unverified and is not shown in this chart.",
            "The answer key and the claim text are not released.",
        ],
        "s8_title": "A pattern, not a ranking of models",
        "s8_sub": "Three API models, one method, one color per model.",
    },
    "id": {
        "s1_title": "Seberapa Banyak Bukti Itu Cukup?",
        "s1_sub": "Kalibrasi vonis LLM pada berbagai kedalaman bukti untuk klaim akademik",
        "s1_q": "Apakah vonis model terhadap klaim akademik tetap terkalibrasi saat model membaca lebih banyak isi artikel?",
        "s1_tag": "Sprint Apart Research, AI Epistemics. Analisis utama: 274 klaim non-pilot.",
        "s2_title": "Desain: satu klaim, tiga kedalaman bukti",
        "s2_cap": "Klaim, pertanyaan, dan kata-katanya sama. Hanya jumlah bukti yang berubah.",
        "s2_cards": [("R1", "Abstrak"), ("R2", "Abstrak + hasil"), ("R3", "Teks penuh")],
        "s2_comp": "Pembanding: bukti dari artikel lain, sebagai near dan far (animasi contoh)",
        "s2_near": "near",
        "s2_far": "far",
        "s2_comp_docs": "Bukti dari artikel lain",
        "s2_foot": "Setiap model memberi vonis dan probabilitas pada setiap kedalaman bukti.",
        "s3_title": "Data: 274 klaim non-pilot, tiga model API",
        "s3_cards": [("274", "klaim non-pilot dalam analisis utama, sudah praregistrasi"),
                     ("{n_obs}", "pengamatan per model: 274 klaim x 7 bacaan"),
                     ("3", "model API, prompt dan kunci yang sama")],
        "s3_val_title": "Validasi tim penulis: 40 klaim dinilai, 36 setelah perundingan",
        "s3_val_sub": "Label jangkar bersifat mekanis dan sementara. Kunci dan teks klaim tidak dirilis.",
        "s3_supp": "Set 294 klaim, yang memuat pilot, hanya analisis tambahan.",
        "s4_title": "Hasil: skor Brier menurut model dan sumber bukti",
        "s4_sub": "Brier pada R3 untuk klaim berjangkar: bukti sendiri, near, dan far",
        "s4_legend": ["sendiri R3", "near R3", "far R3"],
        "s4_foot": "Makin kecil makin baik. Pola, bukan peringkat. Brier diukur terhadap kunci mekanis.",
        "s4_note": "Kegagalan parse dikecualikan: sendiri R3 deepseek-v4.1-flash memakai {n_deep_own} dari 274 klaim, far R3 qwen3.8-flash memakai {n_q38_far} dari 274.",
        "s5_title": "Salah dukung dan konsistensi label pada R3",
        "s5_left": "Salah dukung pada R3: bukti near vs far (proporsi pengamatan)",
        "s5_right": "Label vonis R1 dan R3 tetap sama",
        "s5_right_note": "Sekitar separuh label berubah antara R1 dan R3. Untuk deepseek-v4.1-flash, {n_deep_ses} dari 274 klaim dibandingkan.",
        "s5_near": "near",
        "s5_far": "far",
        "s5_foot": "Salah dukung: massa pada DIDUKUNG atau DIBANTAH padahal label jangkarnya NEI. Validitas bukti near dan far belum independen.",
        "s6_title": "Selisih salah dukung near dikurangi far, dan kestabilan uji ulang",
        "s6_left": "Salah dukung near dikurangi far, CI 95% dalam kurung",
        "s6_cols": [("R1", "abstrak"), ("R3", "teks penuh")],
        "s6_zero": "Untuk deepseek-v4.1-flash pada R3, interval memuat nol. Hanya pola deskriptif, bukan klaim sebab-akibat.",
        "s6_right": "Vonis sama saat diulang, uji ulang terpisah 19 klaim",
        "s6_foot": "Kestabilan memakai {n_stab} pengamatan per model dan tidak dihitung ulang pada set 274. Jika 2 kegagalan parse dihitung berubah, deepseek-v4.1-flash menjadi {gagal_deep}%.",
        "s7_title": "Keterbatasan",
        "s7_items": [
            "36 klaim divalidasi tim penulis: sampel kecil.",
            "Interval lebar: untuk qwen3.8-flash, kesesuaian berkisar {ci_lo}% sampai {ci_hi}%.",
            "Label jangkar bersifat mekanis dan sementara. Bukan penilaian ketepatan faktual.",
            "Bukti near dan far belum divalidasi independen. Tanpa klaim kausal.",
            "GPT-6.1 Sol belum terverifikasi dan tidak ditampilkan di grafik ini.",
            "Kunci jawaban dan teks klaim tidak dirilis.",
        ],
        "s8_title": "Pola, bukan peringkat model",
        "s8_sub": "Tiga model API, satu metode, satu warna per model.",
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
    if not hits:
        raise SystemExit("Baris tidak ditemukan: %s" % want)
    return hits[0]


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_data(log):
    main = read_csv(P_MAIN)
    kes = read_csv(P_KES)
    h_repo, h_src = sha(P_MAIN), sha(P_MAIN_SRC)
    log.append(f"sumber angka: {os.path.relpath(P_MAIN, REPO)} (sha256 sama dengan CSV sumber C:\\EPIS_KERJA: {h_repo == h_src})")
    if h_repo != h_src:
        raise SystemExit("CSV repo berbeda dari CSV sumber")
    D = {k: {} for k in ["own", "own_n", "near3", "far3", "far3_n", "fs_near3", "fs_far3", "sesuai",
                         "sesuai_n", "diff_r1", "diff_r3", "stab", "stab_gagal", "stab_n"]}
    for key, label, _ in MODELS:
        def row(metrik, key=key):
            r = pick(main, model=key, set=SET_MAIN, metrik=metrik)
            if int(r["n_klaim"]) != N_CLAIMS or int(r["n_obs"]) != N_OBS:
                raise SystemExit(f"{key} {metrik}: n_klaim/n_obs bukan 274/1918")
            return r
        r_own = row(MET_OWN)
        r_near = row(MET_NEAR3)
        r_far = row(MET_FAR3)
        s = row(MET_SESUAI)
        r_fn, r_ff = row(MET_FS_NEAR3), row(MET_FS_FAR3)
        d1, d3 = row(MET_DIFF_R1), row(MET_DIFF_R3)
        D["own"][key], D["own_n"][key] = float(r_own["nilai"]), int(r_own["n"])
        D["near3"][key] = float(r_near["nilai"])
        D["far3"][key], D["far3_n"][key] = float(r_far["nilai"]), int(r_far["n"])
        D["sesuai"][key] = (float(s["nilai"]), float(s["ci_lo"]), float(s["ci_hi"]))
        D["sesuai_n"][key] = int(s["n"])
        D["fs_near3"][key], D["fs_far3"][key] = float(r_fn["nilai"]), float(r_ff["nilai"])
        D["diff_r1"][key] = (float(d1["nilai"]), float(d1["ci_lo"]), float(d1["ci_hi"]))
        D["diff_r3"][key] = (float(d3["nilai"]), float(d3["ci_lo"]), float(d3["ci_hi"]))
        log.append(f"CSV {SET_MAIN} | {label} | Brier own R3 = {r_own['nilai']} (n={r_own['n']}) | "
                   f"near R3 = {r_near['nilai']} | far R3 = {r_far['nilai']} (n={r_far['n']}) | "
                   f"Sesuai = {s['nilai']} [{s['ci_lo']}; {s['ci_hi']}] (n={s['n']}) | "
                   f"FS near R3 = {r_fn['nilai']} | FS far R3 = {r_ff['nilai']}")
        log.append(f"CSV {SET_MAIN} | {label} | selisih FS near-far R1 = {d1['nilai']} [{d1['ci_lo']}; {d1['ci_hi']}] | "
                   f"R3 = {d3['nilai']} [{d3['ci_lo']}; {d3['ci_hi']}]")
    log.append("--- pencocokan nilai kunci Table 1 (set 274): CSV dibulatkan 4 desimal vs nilai diminta ---")
    keys = [m[0] for m in MODELS]
    series = {"own": [D["own"][k] for k in keys], "near3": [D["near3"][k] for k in keys],
              "sesuai": [D["sesuai"][k][0] for k in keys],
              "diff_r3": [D["diff_r3"][k][0] for k in keys], "diff_r1": [D["diff_r1"][k][0] for k in keys]}
    names = {"own": "Brier own R3", "near3": "Brier near R3", "sesuai": "agreement R1-R3",
             "diff_r3": "selisih near-far R3", "diff_r1": "selisih near-far R1"}
    for name, exp in EXPECTED.items():
        got = [round(v, 4) for v in series[name]]
        ok = all(abs(g - e) < 1e-9 for g, e in zip(got, exp))
        log.append(f"  {names[name]} | tampil (qwen3.8, qwen4, deepseek) = {got} | diminta = {list(exp)} | cocok = {ok}")
        if not ok:
            raise SystemExit("Nilai kunci tidak cocok: " + name)
    d3_ds = D["diff_r3"][M_DEEP]
    inc0 = d3_ds[1] <= 0 <= d3_ds[2]
    log.append(f"  deepseek selisih R3 CI [{d3_ds[1]}; {d3_ds[2]}] memuat nol = {inc0}")
    if not inc0:
        raise SystemExit("CI deepseek R3 seharusnya memuat nol")
    for key, label, _ in MODELS:
        if key != M_DEEP:
            d = D["diff_r3"][key]
            if d[1] <= 0 <= d[2]:
                raise SystemExit("CI R3 memuat nol untuk " + key)
    svg = read_text(P_G2)
    nums = re.findall(r">(-?0\.\d{4})<", svg)
    exp_svg = {f"{D['diff_r1'][k][0]:.4f}" for k in keys} | {f"{D['diff_r3'][k][0]:.4f}" for k in keys}
    miss = sorted(exp_svg - set(nums))
    log.append(f"G2_near_far_en.svg memuat nilai selisih R1 dan R3 yang sama dengan CSV: nilai hilang = {miss}")
    if miss or "274 non-pilot claims" not in svg:
        raise SystemExit("Angka G2 tidak cocok dengan CSV")
    for key, label, _ in MODELS:
        r = pick(kes, model=key, tingkat_bukti="SEMUA")
        D["stab"][key] = float(r["persen_argmax_sama"])
        D["stab_gagal"][key] = float(r["persen_argmax_sama_gagal_dihitung_beda"])
        D["stab_n"][key] = int(r["n_observasi"])
        log.append(f"CSV KESTABILAN | {label} | SEMUA | persen_argmax_sama = {r['persen_argmax_sama']} | "
                   f"gagal dihitung beda = {r['persen_argmax_sama_gagal_dihitung_beda']} | n_observasi = {r['n_observasi']}")
    m = re.search(r"Cakupan: (\d+) klaim", read_text(P_KES_MD))
    D["n_claims_stab"] = int(m.group(1))
    log.append(f"KESTABILAN.md | Cakupan = {D['n_claims_stab']} klaim (sampel uji ulang terpisah)")
    if D["n_claims_stab"] != 19:
        raise SystemExit("Cakupan kestabilan bukan 19")
    jum = read_text(P_JUM)
    for key, label, _ in MODELS:
        pat = r"\| UTAMA-274 \| dev\+val\+holdout \| 274 \| 1918 \| " + re.escape(key) + r" \|"
        if not re.search(pat, jum):
            raise SystemExit("jumlah_set.md tidak cocok untuk " + key)
    D["n_obs"] = N_OBS
    log.append("jumlah_set.md | UTAMA-274: 274 klaim, 1918 observasi per model (3 model cocok)")
    D["n_deep_own"] = D["own_n"][M_DEEP]
    D["n_q38_far"] = D["far3_n"][M_QWEN38]
    D["n_deep_ses"] = D["sesuai_n"][M_DEEP]
    log.append(f"n tampil: deepseek own R3 = {D['n_deep_own']}/274 | qwen3.8 far R3 = {D['n_q38_far']}/274 | "
               f"deepseek Sesuai = {D['n_deep_ses']}/274 (gagal parse dikecualikan)")
    D["n_stab"] = D["stab_n"][M_QWEN38]
    n36 = len([x for x in read_text(P_LAP36).splitlines() if x.strip()])
    prereg = read_text(P_PREREG)
    if n36 != 36:
        raise SystemExit("Daftar lapis 36 bukan 36 baris: %d" % n36)
    if "294 klaim" not in prereg or "40 pernyataan" not in prereg:
        raise SystemExit("Angka 294/40 tidak ditemukan di praregistrasi")
    log.append(f"lapis_36_claim_id.txt = {n36} baris; PREREG memuat '294 klaim' dan '40 pernyataan' "
               "(294 hanya disebut sebagai analisis tambahan)")
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


def pct(v, lang):
    return fmt(v * 100, 1, lang) + "%"


def thou(n, lang):
    s = f"{n:,}"
    return s.replace(",", ".") if lang == "id" else s


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
    c.text(120, 700, L["s2_comp"], F("R", 36), MUTED, P(t, 5.5))
    for i in range(5):
        p = P(t, 6.0 + i * 0.25, 0.8)
        x, ytop = 120 + i * 120, 760 + (1 - p) * 60
        c.rect(x, ytop, x + 80, ytop + 110, fill=CARD, outline=BORDER, width=2, radius=8, op=p)
        for j in range(3):
            c.rect(x + 14, ytop + 26 + j * 26, x + 66, ytop + 32 + j * 26, fill=BORDER, radius=3, op=p)
    c.text(120, 886, L["s2_near"], F("R", 30), MUTED, P(t, 7.5))
    c.text(480, 886, L["s2_far"], F("R", 30), MUTED, P(t, 7.5))
    c.text(760, 790, L["s2_comp_docs"], F("R", 40), TXT, P(t, 7.0))
    c.text(120, 960, L["s2_foot"], F("R", 36), TXT, P(t, 9.5))


def scene3(c, t, L, D):
    c.text(120, 90, L["s3_title"], F("B", 60), TXT, P(t, 0.1))
    for i, (num, desc) in enumerate(L["s3_cards"]):
        x, y = 120 + i * 580, 230
        op = P(t, 0.8 + i * 1.0, 0.7)
        c.rect(x, y, x + 520, y + 360, fill=CARD, outline=BORDER, width=2, radius=24, op=op)
        num_txt = num.format(n_obs=thou(D["n_obs"], L["lang"]))
        c.text(x + 40, y + 30, num_txt, F("B", 110), ACC, op)
        c.para(x + 40, y + 180, desc, F("R", 36), TXT, 440, 48, op)
    c.rect(120, 640, 1800, 820, fill=CARD, outline=BORDER, width=2, radius=24, op=P(t, 4.5))
    c.text(160, 668, L["s3_val_title"], F("B", 40), TXT, P(t, 5.0))
    c.text(160, 748, L["s3_val_sub"], F("R", 34), MUTED, P(t, 6.2))
    c.text(120, 880, L["s3_supp"], F("R", 36), TXT, P(t, 7.4))


def scene4(c, t, L, D):
    lang = L["lang"]
    c.text(120, 90, L["s4_title"], F("B", 56), TXT, P(t, 0.1))
    c.text(120, 160, L["s4_sub"], F("R", 36), MUTED, P(t, 0.4))
    tones = [1.0, 0.55, 0.28]
    for k, name in enumerate(L["s4_legend"]):
        x = 120 + k * 380
        op = P(t, 0.8 + k * 0.2, 0.5)
        c.rect(x, 226, x + 44, 262, fill=ACC, outline=ACC, width=2, radius=8, op=op * tones[k])
        c.text(x + 60, 226, name, F("R", 32), TXT, op)
    base, scale = 850, 520
    centers = [470, 960, 1450]
    kinds = [("own", 1.0), ("near3", 0.55), ("far3", 0.28)]
    c.line(120, base, 1800, base, BORDER, 1.0, 2)
    for g, (key, label, col) in enumerate(MODELS):
        cx = centers[g]
        for b, (kind, tone) in enumerate(kinds):
            val = D[kind][key]
            x = cx - 211 + b * 146
            start = 1.2 + g * 0.3 + b * 0.15
            grow = ease((t - start) / 1.2)
            h = max(6, round(scale * clamp(val / BRIER_MAX) * grow))
            op = P(t, start, 0.4)
            if b == 2:
                c.rect(x, base - h, x + 130, base, fill=col, outline=col, width=2, radius=8, op=op * tone)
            else:
                c.rect(x, base - h, x + 130, base, fill=col, radius=8, op=op * tone)
            c.text(x + 65, base - h - 14, fmt(val, 4, lang), F("B", 28), TXT,
                   P(t, start + 1.0, 0.5), anchor="ms")
        c.text(cx, base + 18, label, F("R", 32), TXT, P(t, 1.0 + g * 0.3, 0.6), anchor="ma")
    c.para(120, 925, L["s4_note"].format(n_deep_own=D["n_deep_own"], n_q38_far=D["n_q38_far"]),
           F("R", 28), MUTED, 1680, 38, P(t, 6.0))
    c.para(120, 1000, L["s4_foot"], F("R", 28), MUTED, 1680, 38, P(t, 7.0))


def scene5(c, t, L, D):
    lang = L["lang"]
    c.text(120, 90, L["s5_title"], F("B", 56), TXT, P(t, 0.1))
    c.para(120, 200, L["s5_left"], F("R", 34), TXT, 780, 44, P(t, 0.4))
    for i, (key, label, col) in enumerate(MODELS):
        y = 320 + i * 170
        op = P(t, 0.8 + i * 0.3, 0.5)
        c.text(120, y, label, F("B", 34), TXT, op)
        for b, (kind, name, tone) in enumerate([("fs_near3", L["s5_near"], 1.0),
                                                 ("fs_far3", L["s5_far"], 0.55)]):
            val = D[kind][key]
            yy = y + 52 + b * 52
            grow = ease((t - (1.5 + i * 0.3 + b * 0.2)) / 1.1)
            hbar(c, 120, yy, 560, 36, val / BRIER_MAX, col, b == 1, op, grow)
            c.text(700, yy - 2, f"{name} {pct(val, lang)}", F("B", 30), TXT,
                   P(t, 2.4 + i * 0.3 + b * 0.2, 0.5))
    c.para(1020, 200, L["s5_right"], F("R", 34), TXT, 780, 44, P(t, 0.4))
    for i, (key, label, col) in enumerate(MODELS):
        y = 320 + i * 150
        op = P(t, 2.0 + i * 0.3, 0.5)
        c.text(1020, y, label, F("B", 34), TXT, op)
        val = D["sesuai"][key][0]
        grow = ease((t - (2.6 + i * 0.3)) / 1.2)
        hbar(c, 1020, y + 52, 640, 44, val, col, False, op, grow)
        c.text(1690, y + 50, pct(val, lang), F("B", 36), TXT, P(t, 3.4 + i * 0.3, 0.5))
    c.para(1020, 790, L["s5_right_note"].format(n_deep_ses=D["n_deep_ses"]), F("R", 30), MUTED, 780, 40,
           P(t, 4.6))
    c.para(120, 900, L["s5_foot"], F("R", 30), MUTED, 1680, 42, P(t, 6.0))


def scene6(c, t, L, D):
    lang = L["lang"]
    c.text(120, 90, L["s6_title"], F("B", 52), TXT, P(t, 0.1))
    c.para(120, 200, L["s6_left"], F("R", 34), TXT, 820, 44, P(t, 0.4))
    cols = [610, 830]
    for k, (h1, h2) in enumerate(L["s6_cols"]):
        op = P(t, 0.8 + k * 0.2, 0.5)
        c.text(cols[k], 270, h1, F("B", 32), TXT, op, anchor="ma")
        c.text(cols[k], 312, h2, F("R", 26), MUTED, op, anchor="ma")
    c.line(120, 358, 940, 358, BORDER, P(t, 1.0), 2)
    for i, (key, label, col) in enumerate(MODELS):
        y = 380 + i * 120
        op = P(t, 1.4 + i * 0.3, 0.5)
        c.rect(120, y + 14, 140, y + 34, fill=col, radius=10, op=op)
        c.text(152, y + 6, label, F("B", 26), TXT, op)
        for k, kind in enumerate(["diff_r1", "diff_r3"]):
            v, lo, hi = D[kind][key]
            c.text(cols[k], y, fmt(v, 4, lang), F("B", 36), TXT, op, anchor="ma")
            c.text(cols[k], y + 48, "[" + fmt(lo, 4, lang) + "; " + fmt(hi, 4, lang) + "]",
                   F("R", 22), MUTED, op, anchor="ma")
        c.line(120, y + 98, 940, y + 98, BORDER, op, 1)
    c.para(120, 760, L["s6_zero"], F("R", 30), MUTED, 820, 40, P(t, 4.6))
    c.para(1020, 200, L["s6_right"], F("R", 34), TXT, 780, 44, P(t, 0.4))
    for i, (key, label, col) in enumerate(MODELS):
        y = 320 + i * 150
        op = P(t, 2.0 + i * 0.3, 0.5)
        c.text(1020, y, label, F("B", 34), TXT, op)
        grow = ease((t - (2.6 + i * 0.3)) / 1.2)
        hbar(c, 1020, y + 52, 620, 44, D["stab"][key], col, False, op, grow)
        c.text(1660, y + 50, pct(D["stab"][key], lang), F("B", 36), TXT, P(t, 3.4 + i * 0.3, 0.5))
    c.text(1020, 790, "0%", F("R", 28), MUTED, P(t, 4.0))
    c.text(1640, 790, "100%", F("R", 28), MUTED, P(t, 4.0), anchor="ra")
    gagal = fmt(D["stab_gagal"][M_DEEP] * 100, 1, lang)
    c.para(120, 910, L["s6_foot"].format(n_stab=D["n_stab"], gagal_deep=gagal), F("R", 28),
           TXT, 1680, 38, P(t, 5.5))


def scene7(c, t, L, D):
    lang = L["lang"]
    ci = {"ci_lo": fmt(D["sesuai"][M_QWEN38][1] * 100, 1, lang),
          "ci_hi": fmt(D["sesuai"][M_QWEN38][2] * 100, 1, lang)}
    c.text(120, 90, L["s7_title"], F("B", 64), TXT, P(t, 0.1))
    for i, item in enumerate(L["s7_items"]):
        y = 230 + i * 130
        op = P(t, 0.8 + i * 1.0, 0.7)
        c.rect(122, y + 18, 142, y + 38, fill=ACC, radius=10, op=op)
        c.para(180, y, item.format(**ci), F("R", 40), TXT, 1640, 52, op)


def scene8(c, t, L, D):
    c.text(W // 2, 370, L["s8_title"], F("B", 88), TXT, P(t, 0.2, 0.9), anchor="ma")
    c.text(W // 2, 530, L["s8_sub"], F("L", 44), MUTED, P(t, 1.2), anchor="ma")
    for i, (key, label, col) in enumerate(MODELS):
        cx = 960 + (i - 1) * 480
        op = P(t, 2.2 + i * 0.3, 0.6)
        c.rect(cx - 14, 676, cx + 14, 704, fill=col, radius=14, op=op)
        c.text(cx, 730, label, F("R", 30), TXT, op, anchor="ma")


SCENES = [
    ("judul", scene1, 10.0),
    ("desain", scene2, 12.0),
    ("data", scene3, 10.0),
    ("hasil", scene4, 14.0),
    ("false_support", scene5, 11.0),
    ("near_far_kestabilan", scene6, 12.0),
    ("keterbatasan", scene7, 12.0),
    ("penutup", scene8, 6.0),
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


WATCH = TempWatch()


def wait_cool(log):
    while True:
        t, _ = gpu_status()
        log.append(f"  suhu GPU sebelum encode: {t} C")
        if t <= MAX_TEMP:
            return
        log.append("  suhu di atas 80 C, menunggu dingin (cek tiap 30 detik)")
        time.sleep(30)


ENC = [["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "23"], "nvenc"]


def run_encode(out_path, L, D, starts, total, log):
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           *ENC[0], "-pix_fmt", "yuv420p",
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
        if ENC[1] == "nvenc":
            log.append(f"  NVENC gagal (rc={rc}): {err.strip()[:200]}; beralih ke libx264 (CPU)")
            ENC[0] = ["-c:v", "libx264", "-preset", "medium", "-crf", "20"]
            ENC[1] = "x264"
            return "retry"
        raise SystemExit(f"ffmpeg gagal (rc={rc}): {err.strip()}")
    return "ok"


def encode_lang(lang, L, D, log):
    durs = [d for _, _, d in SCENES]
    starts, total = timeline(durs)
    out = os.path.join(OUT, f"ringkasan274_{lang}.mp4")
    for attempt in range(1, 4):
        wait_cool(log)
        WATCH.hot.clear()
        log.append(f"encode {lang} percobaan {attempt}, pengkode {ENC[1]}")
        if run_encode(out, L, D, starts, total, log) == "ok":
            break
    else:
        raise SystemExit("Suhu GPU terlalu tinggi 3 kali, berhenti")
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
    with open(os.path.join(OUT, f"angka_pencocokan274_{args.lang}.txt"), "w", encoding="utf-8") as fh:
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
    with open(os.path.join(OUT, f"angka_pencocokan274_{args.lang}.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    print("\n".join(log[-3:]))
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    main()
