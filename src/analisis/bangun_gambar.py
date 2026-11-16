# -*- coding: utf-8 -*-
"""Bangun gambar G1-G7 (EN dan ID) untuk laporan dari hasil yang sudah ada.

Hanya membaca berkas di C:\\EPIS_KERJA. Tidak memanggil model, tidak menghitung
statistik baru, tidak mengubah berkas sumber. Keluaran hanya di
C:\\EPIS_KERJA\\RENDER\\gambar\\ dan cache font di C:\\EPIS_KERJA\\RENDER\\mplcache.

Jalankan: py -3.12 -I -X utf8 C:\\EPIS_KERJA\\RENDER\\gambar\\bangun_gambar.py
"""
import csv
import datetime
import json
import os
import re
from pathlib import Path

ROOT = Path(r"C:\EPIS_KERJA\RENDER")
OUT = ROOT / "gambar"
CACHE = ROOT / "mplcache"
OUT.mkdir(parents=True, exist_ok=True)
CACHE.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(CACHE)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.text import Text
from matplotlib.ticker import FuncFormatter

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 0.7,
    "savefig.dpi": 300,
    "svg.fonttype": "none",
})

# ---------------------------------------------------------------- sumber (baca saja)
SRC = Path(r"C:\EPIS_KERJA\AI_EPISTEMICS_2026_PHASE_2_PREP")
HP = SRC / "HASIL_PENGUJIAN"
BAHAN_V2 = SRC / "bahan" / "v2"
HASIL_FINAL = BAHAN_V2 / "hasil_olahan_final"
F = {
    "l36_csv": HP / "_lapis36" / "tabel_lapis36_4model.csv",
    "l36_md": HP / "_lapis36" / "tabel_lapis36_4model.md",
    "pem_csv": HP / "_lapis36" / "tabel_pembanding_lapis_40_36_26_19.csv",
    "pem_md": HP / "_lapis36" / "tabel_pembanding_lapis_40_36_26_19.md",
    "kest_csv": HP / "_retest_lapis19" / "KESTABILAN.csv",
    "kest_md": HP / "_retest_lapis19" / "KESTABILAN.md",
    "cod_csv": HP / "gpt61_codex" / "KESTABILAN_codex.csv",
    "cod_md": HP / "gpt61_codex" / "KESTABILAN_codex.md",
    "ring": HASIL_FINAL / "RINGKASAN_KELAYAKAN.md",
    "status": HASIL_FINAL / "status_butir.csv",
    "pool": BAHAN_V2 / "LAPORAN_AGEN_1_V2.md",
    "items36": HASIL_FINAL / "lapis_data" / "items_lapis_36.jsonl",
    "items40": BAHAN_V2 / "hasil_olahan_3penilai" / "lapis_data" / "items_lapis_40.jsonl",
    "items26": BAHAN_V2 / "hasil_olahan_3penilai" / "lapis_data" / "items_lapis_26.jsonl",
    "items19": BAHAN_V2 / "hasil_olahan_3penilai" / "lapis_data" / "items_lapis_19.jsonl",
}
for _k, _p in F.items():
    assert _p.exists(), f"berkas sumber tidak ada: {_p}"

MODELS = ["qwen3.8-flash", "qwen4-max-preview", "deepseek-v4.1-flash", "codex"]
API_MODELS = MODELS[:3]
DISP = {"qwen3.8-flash": "qwen3.8-flash", "qwen4-max-preview": "qwen4-max-preview",
        "deepseek-v4.1-flash": "deepseek-v4.1-flash", "codex": "GPT-6.1 Sol (unverified)"}
# Palet Okabe-Ito (aman buta warna); warna sama di semua gambar
COL = {"qwen3.8-flash": "#0072B2", "qwen4-max-preview": "#E69F00",
       "deepseek-v4.1-flash": "#009E73", "codex": "#CC79A7"}
MARK = {"qwen3.8-flash": "o", "qwen4-max-preview": "s", "deepseek-v4.1-flash": "^", "codex": "D"}
ORDER_LAP = [40, 36, 26, 19]
SESUAI = "Sesuai (label R1 = R3)"
BRIER = {"own R3": "Brier batas 1 own R3 (anchor SUPPORTED)",
         "near R1": "Brier batas 1 near R1 (anchor NEI)",
         "near R3": "Brier batas 1 near R3 (anchor NEI)",
         "far R1": "Brier batas 1 far R1 (anchor NEI)",
         "far R3": "Brier batas 1 far R3 (anchor NEI)"}
FS = {"near R1": "False-support near R1", "far R1": "False-support far R1",
      "near R3": "False-support near R3", "far R3": "False-support far R3"}
FOOT = ("Pilot+dev claims only; 36 claims, 252 observations per model; "
        "95% cluster bootstrap CI (B=2000); pattern not ranking")


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def read_text(path):
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def fnum(s):
    s = (s or "").strip()
    return float(s) if s else None


def mkey(model):
    return "codex" if model.startswith("codex") else model


# ---------------------------------------------------------------- muat CSV
L36 = {}
for r in read_rows(F["l36_csv"]):
    L36[(mkey(r["model"]), r["metrik"])] = {
        "n": int(r["n"]), "v": float(r["nilai"]), "lo": fnum(r["ci_lo"]), "hi": fnum(r["ci_hi"])}

PEM = {}
for r in read_rows(F["pem_csv"]):
    PEM[(mkey(r["model"]), r["metrik"])] = {
        40: float(r["nilai_lapis40"]), 36: float(r["nilai_lapis36"]),
        26: float(r["nilai_lapis26"]), 19: float(r["nilai_lapis19"])}

KEST = {}
for r in read_rows(F["kest_csv"]):
    if r["tingkat_bukti"] == "SEMUA":
        continue
    KEST[(mkey(r["model"]), r["tingkat_bukti"])] = {
        "n": int(r["n_observasi"]), "valid": int(r["n_pasangan_valid"]),
        "gagal": int(r["n_gagal_parse_salah_satu"]),
        "pct": float(r["persen_argmax_sama"]),
        "pct_beda": float(r["persen_argmax_sama_gagal_dihitung_beda"])}

COD = {}
for r in read_rows(F["cod_csv"]):
    if r["metrik"] == "argmax_sama_proporsi":
        COD[r["tingkat"]] = {"n": int(r["n"]), "v": float(r["nilai"]),
                             "lo": fnum(r["ci_lo"]), "hi": fnum(r["ci_hi"])}

# Pemeriksaan struktur: setiap metrik yang dipakai harus ada untuk keempat model
for m in MODELS:
    for k in list(BRIER.values()) + list(FS.values()) + [SESUAI]:
        assert (m, k) in L36, (m, k)
        assert (m, k) in PEM, (m, k)
for m in MODELS:
    for k in list(BRIER.values()) + list(FS.values()):
        rec = L36[(m, k)]
        if rec["lo"] is not None:
            assert rec["lo"] <= rec["v"] <= rec["hi"], (m, k, rec)
for m in API_MODELS:
    for lvl in ["R1", "R2", "R3"]:
        assert (m, lvl) in KEST
for lvl in ["R1", "R2", "R3"]:
    assert lvl in COD

# Silang: nilai lapis 36 di CSV utama harus sama dengan kolom lapis 36 di CSV pembanding
for key in set(L36) & set(PEM):
    assert abs(L36[key]["v"] - PEM[key][36]) <= 1e-6, key


# ---------------------------------------------------------------- muat sumber lain (hitungan & kutipan)
def load_status():
    rows = read_rows(F["status"])
    jk = [r for r in rows if r["jenis"] == "JANGKAR"]
    keluar = [r["claim_id"] for r in jk if r["keputusan_akhir"] == "KELUAR"]
    dipakai = sum(1 for r in jk if r["keputusan_akhir"] == "DIPAKAI")
    direvisi = sum(1 for r in jk if r["keputusan_akhir"] == "DIREVISI")
    assert len(jk) == 40 and dipakai == 35 and direvisi == 1 and len(keluar) == 4
    assert dipakai + direvisi == 36
    return {"n40": len(jk), "n36": dipakai + direvisi, "dipakai": dipakai,
            "direvisi": direvisi, "keluar": keluar}


STATUS = load_status()

_pool = read_text(F["pool"])
_m = re.search(r"Akibatnya: \*\*(\d+) klaim\*\*, bukan (\d+)", _pool)
assert _m, "kalimat jumlah kolam tidak ditemukan"
POOL, POOL_ORIG = int(_m.group(1)), int(_m.group(2))
assert (POOL, POOL_ORIG) == (294, 300)


def count_items(path):
    ids, n = set(), 0
    with open(path, encoding="utf-8-sig") as fh:
        for line in fh:
            if line.strip():
                ids.add(json.loads(line)["claim_id"])
                n += 1
    return len(ids), n


LAYER_N = {}
for lap in [40, 36, 26, 19]:
    claims, obs = count_items(F[f"items{lap}"])
    assert obs == 7 * claims, (lap, claims, obs)
    LAYER_N[lap] = claims
assert LAYER_N == {40: 40, 36: 36, 26: 26, 19: 19}, LAYER_N

_ring = read_text(F["ring"])
_jk = _ring.split("### Pernyataan JANGKAR", 1)[1].split("### Draf UBAHAN", 1)[0]
_pct = re.search(r"Persen sepakat keseluruhan: ([\d.]+) \(dari (\d+) perbandingan", _jk)
_fk = re.search(r"Kappa Fleiss \(n=(\d+)[^)]*\): (-?[\d.]+)", _jk)
_pairs = re.findall(r"Kappa Cohen (\S+) vs (\S+): n=(\d+), sepakat=([\d.]+), kappa=(-?[\d.]+)", _jk)
assert _pct and _fk and len(_pairs) == 3, "ringkasan kelayakan tidak terbaca"
AGREE = {"pct": float(_pct.group(1)) * 100, "n_pairs": int(_pct.group(2)),
         "fleiss": float(_fk.group(2)), "fleiss_n": int(_fk.group(1)),
         "cohen": [float(p[4]) for p in _pairs]}


# ---------------------------------------------------------------- pencocokan angka CSV vs MD
MATCH_LOG = {}
MISMATCH = []
NUM_CI = re.compile(r"^(-?\d+(?:\.\d+)?)(?:\s*\[(-?\d+(?:\.\d+)?);\s*(-?\d+(?:\.\d+)?)\])?$")


def md_rows(path):
    rows = []
    for line in read_text(path).splitlines():
        if line.startswith("|") and line.count("|") >= 3:
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def parse_cell(s):
    m = NUM_CI.match(s.strip().replace("%", ""))
    if not m:
        return None
    lo = float(m.group(2)) if m.group(2) else None
    hi = float(m.group(3)) if m.group(3) else None
    return float(m.group(1)), lo, hi


def log_cmp(name, ok, detail):
    MATCH_LOG.setdefault(name, [0, 0])
    MATCH_LOG[name][0 if ok else 1] += 1
    if not ok:
        MISMATCH.append(f"{name}: {detail}")


TOL4 = 0.00005 + 1e-9   # md memakai 4 desimal
TOL1P = 0.05 + 1e-9     # md persen memakai 1 desimal

# (a) tabel lapis 36 (md) vs CSV
for cells in md_rows(F["l36_md"]):
    key_metric = cells[0]
    if not any((m, key_metric) in L36 for m in MODELS):
        continue
    for j, m in enumerate(MODELS):
        p = parse_cell(cells[1 + j])
        rec = L36[(m, key_metric)]
        if p is None:
            log_cmp("tabel_lapis36_4model.md", False, f"sel tak terbaca {key_metric} {m}")
            continue
        ok = abs(rec["v"] - p[0]) <= TOL4
        if p[1] is not None and rec["lo"] is not None:
            ok = ok and abs(rec["lo"] - p[1]) <= TOL4 and abs(rec["hi"] - p[2]) <= TOL4
        log_cmp("tabel_lapis36_4model.md", ok, f"{key_metric} {m}: csv={rec['v']} md={p[0]}")

# (b) tabel pembanding lapis 40/36/26/19 (md) vs CSV
for cells in md_rows(F["pem_md"]):
    if len(cells) < 6:
        continue
    m = mkey(cells[0])
    key = (m, cells[1])
    if key not in PEM:
        continue
    for idx, lap in enumerate(ORDER_LAP):
        p = parse_cell(cells[2 + idx])
        ok = p is not None and abs(PEM[key][lap] - p[0]) <= TOL4
        log_cmp("tabel_pembanding_lapis_40_36_26_19.md", ok,
                f"{cells[1]} {m} lapis {lap}: csv={PEM[key][lap]} md={cells[2 + idx]}")

# (c) kestabilan API (md) vs CSV: kolom % sama dan % sama (gagal = beda)
for cells in md_rows(F["kest_md"]):
    if len(cells) < 7 or cells[0] not in API_MODELS or cells[1] not in ("R1", "R2", "R3"):
        continue
    rec = KEST[(cells[0], cells[1])]
    p1 = parse_cell(cells[5])
    p2 = parse_cell(cells[6])
    ok1 = p1 is not None and abs(rec["pct"] * 100 - p1[0]) <= TOL1P
    ok2 = p2 is not None and abs(rec["pct_beda"] * 100 - p2[0]) <= TOL1P
    log_cmp("KESTABILAN.md", ok1 and ok2, f"{cells[0]} {cells[1]}")

# (d) kestabilan codex (md) vs CSV
for cells in md_rows(F["cod_md"]):
    if len(cells) < 3 or cells[0] not in ("R1", "R2", "R3"):
        continue
    rec = COD[cells[0]]
    p = parse_cell(cells[2])
    ok = (p is not None and abs(rec["v"] * 100 - p[0]) <= TOL1P
          and p[1] is not None and abs(rec["lo"] * 100 - p[1]) <= TOL1P
          and abs(rec["hi"] * 100 - p[2]) <= TOL1P)
    log_cmp("KESTABILAN_codex.md", ok, f"codex {cells[0]}")

# (e) ringkasan kelayakan: dibaca langsung dari satu sumber (dicatat sebagai pembacaan)
log_cmp("RINGKASAN_KELAYAKAN.md (pembacaan regex)", AGREE["n_pairs"] == 120 and AGREE["fleiss_n"] == 40,
        "jumlah perbandingan atau n Fleiss tidak sesuai")

for name, (ok_n, bad_n) in MATCH_LOG.items():
    print(f"[cocok] {name}: {ok_n} cocok, {bad_n} beda")
if MISMATCH:
    raise SystemExit("ANGKA TIDAK COCOK, gambar dihentikan:\n" + "\n".join(MISMATCH[:30]))
assert sum(v[0] for v in MATCH_LOG.values()) >= 150, "pencocokan terlalu sedikit"


# ---------------------------------------------------------------- teks (EN dan ID)
def N(x, nd, lang):
    s = f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "id" else s


def retest_pct(model, lvl):
    if model == "codex":
        return COD[lvl]["v"] * 100
    return KEST[(model, lvl)]["pct_beda"] * 100


def n_note(lang):
    parts = []
    for m in MODELS:
        low = {c: L36[(m, BRIER[c])]["n"] for c in BRIER if L36[(m, BRIER[c])]["n"] < 36}
        if not low:
            continue
        if len(low) == len(BRIER) and len(set(low.values())) == 1:
            tail = (f"semua batang n={list(low.values())[0]}" if lang == "id"
                    else f"all bars n={list(low.values())[0]}")
        else:
            tail = ", ".join(f"{c} n={n}" for c, n in low.items())
        parts.append(f"{DISP[m]}: {tail}")
    if lang == "id":
        return "Batang dengan n < 36 (gagal parse atau klaim dilewati): " + "; ".join(parts) + "."
    return "Bars with n < 36 (parse failures or a skipped claim): " + "; ".join(parts) + "."


def ci_width_note(lang):
    widths = [(L36[(m, SESUAI)]["hi"] - L36[(m, SESUAI)]["lo"]) * 100 for m in MODELS]
    a, b = min(widths), max(widths)
    if lang == "id":
        return (f"Batang error: CI 95% hanya untuk lapis 36 (CSV tidak memuat CI untuk lapis 40, 26, 19). "
                f"Lebar CI {a:.0f} sampai {b:.0f} poin persen.")
    return (f"Error bars: 95% CI for layer 36 only (source CSV has no CI for layers 40, 26, 19). "
            f"CI width {a:.0f} to {b:.0f} percentage points.")


T = {
    "en": {
        "g1_title": "Figure 1. Study design: evidence forms, anchor labels and metrics",
        "g1_claim": "Claim\n(36 main-analysis claims)",
        "g1_forms": "Seven evidence forms per claim",
        "g1_scoring": "Four models scored\nR1 = abstract\nR2 = abstract + results\nR3 = full text",
        "g1_m1": "Brier score, boundary 1\n(own R3 vs near/far NEI;\nfailed parses excluded)",
        "g1_m2": "False-support mass\n(p SUPPORTED + p REFUTED,\nnear and far NEI items)",
        "g1_m3": "Consistency\n(share of claims with\nlabel R1 = label R3)",
        "g1_note": ["Schematic only, no data shown. own R3 SUPPORTED = author conclusion;",
                    "near and far NEI = evidence from other articles (by design). NEI = not enough information."],
        "g2_title": "Figure 2. Item funnel and assessor agreement",
        "g2_pool": ("Claim pool: 294 claims", f"(6 claims without embedding removed from {POOL_ORIG})"),
        "g2_a40": ("40 anchor claims assessed by the team", "3 assessors (author team)"),
        "g2_a36": ("36 main-analysis anchors", f"{STATUS['dipakai']} kept + {STATUS['direvisi']} revised (final status)"),
        "g2_out": ("4 excluded in team negotiation", ", ".join(STATUS["keluar"])),
        "g2_layers": "Sensitivity layers: subsets of the 40-claim pool (not of the 36 main set)",
        "g2_l40": ("Layer 40: 40 claims", "initial, before negotiation"),
        "g2_l26": ("Layer 26: 26 claims", "sensitivity layer"),
        "g2_l19": ("Layer 19: 19 claims", "sensitivity layer; also the retest set"),
        "g2_agree_hdr": "Assessor agreement, anchor statements (3 assessors)",
        "g2_agree_1": (f"Percent agreement {N(AGREE['pct'], 1, 'en')}% over {AGREE['n_pairs']} pairwise comparisons; "
                       f"Fleiss kappa = {N(AGREE['fleiss'], 3, 'en')} (n = {AGREE['fleiss_n']})"),
        "g2_agree_2": ("Pairwise Cohen kappa: " + "; ".join(N(k, 3, "en") for k in AGREE["cohen"])
                       + " (n = 40 per pair)"),
        "g2_agree_3": "Assessors are the author team, not an external expert panel. Kappa values near zero.",
        "g2_note": "Layers 26 and 19 are subsets of the 40-claim pool, drawn from the same items files.",
        "g3_title": "Figure 3. Brier score by evidence type, layer 36",
        "g3_y": "Brier score, boundary 1 (lower is better)",
        "g4_title": "Figure 4. R1 = R3 label consistency across item layers",
        "g4_y": "Claims with label R1 = R3 (%)",
        "g4_layers": ["layer 40\n(initial)", "layer 36\n(main)", "layer 26\n(sensitivity)", "layer 19\n(sensitivity)"],
        "g4_layers_s": ["40\n(initial)", "36\n(main)", "26\n(sens.)", "19\n(sens.)"],
        "g5_title": "Figure 5. False-support mass on NEI evidence, layer 36",
        "g5_y": "False-support mass: p(SUPPORTED) + p(REFUTED)\non NEI items (lower is better)",
        "g6_title": "Figure 6. Test-retest argmax agreement by evidence level (19-claim layer)",
        "g6_y": "Argmax agreement between two runs (%)",
        "g6_levels": ["R1\n(abstract)", "R2\n(abstract +\nresults)", "R3\n(full text)"],
        "g6_levels_s": ["R1", "R2", "R3"],
        "g6_note": [f"Retest: 19-claim layer, 133 observations per model (R1 {KEST[('qwen3.8-flash', 'R1')]['n']}, "
                    f"R2 {KEST[('qwen3.8-flash', 'R2')]['n']}, R3 {KEST[('qwen3.8-flash', 'R3')]['n']}). "
                    "Failed parses counted as disagreement (API models).",
                    "GPT-6.1 Sol (unverified): separate session, not verified (hatched). "
                    "Standard footnote not used: this layer is not the 36-claim main set."],
        "g7_title": "Figure 7. Summary panel: Brier, consistency, false-support, stability",
        "g7_panels": ["(a) Brier score, boundary 1", "(b) R1 = R3 label consistency",
                      "(c) False-support mass, NEI items", "(d) Test-retest agreement (19 claims)"],
        "g7_note_d": "Panel d: 19-claim retest layer, 133 observations per model; GPT-6.1 Sol (unverified) from a separate session.",
        "cat": {"own R3": "own R3\n(SUPPORTED)", "near R1": "near R1\n(NEI)", "near R3": "near R3\n(NEI)",
                "far R1": "far R1\n(NEI)", "far R3": "far R3\n(NEI)"},
        "ci_note": None,
    },
    "id": {
        "g1_title": "Gambar 1. Desain studi: bentuk bukti, label jangkar, dan metrik",
        "g1_claim": "Klaim\n(36 klaim analisis utama)",
        "g1_forms": "Tujuh bentuk bukti per klaim",
        "g1_scoring": "Empat model dinilai\nR1 = abstrak\nR2 = abstrak + hasil\nR3 = teks penuh",
        "g1_m1": "Skor Brier, batas 1\n(own R3 vs near/far NEI;\nobservasi gagal dikeluarkan)",
        "g1_m2": "Massa false-support\n(p SUPPORTED + p REFUTED,\nitem near dan far NEI)",
        "g1_m3": "Konsistensi\n(proporsi klaim dengan\nlabel R1 = label R3)",
        "g1_note": ["Skema saja, tanpa data. SUPPORTED pada own R3 = kesimpulan penulis; "
                    "NEI pada near dan far = bukti dari artikel lain (sesuai desain).",
                    "NEI = informasi tidak cukup."],
        "g2_title": "Gambar 2. Corong butir dan kesepakatan penilai",
        "g2_pool": ("Kolam klaim: 294 klaim", f"(6 klaim tanpa embedding dikeluarkan dari {POOL_ORIG})"),
        "g2_a40": ("40 klaim jangkar dinilai tim", "3 penilai (tim penulis)"),
        "g2_a36": ("36 jangkar analisis utama", f"{STATUS['dipakai']} dipakai + {STATUS['direvisi']} direvisi (status final)"),
        "g2_out": ("4 keluar setelah perundingan tim", ", ".join(STATUS["keluar"])),
        "g2_layers": "Lapis kepekaan: subset dari kolam 40 klaim (bukan dari 36 utama)",
        "g2_l40": ("Lapis 40: 40 klaim", "awal, sebelum perundingan"),
        "g2_l26": ("Lapis 26: 26 klaim", "lapis kepekaan"),
        "g2_l19": ("Lapis 19: 19 klaim", "lapis kepekaan; juga himpunan uji ulang"),
        "g2_agree_hdr": "Kesepakatan penilai, pernyataan jangkar (3 penilai)",
        "g2_agree_1": (f"Persen sepakat {N(AGREE['pct'], 1, 'id')}% dari {AGREE['n_pairs']} perbandingan pasangan; "
                       f"kappa Fleiss = {N(AGREE['fleiss'], 3, 'id')} (n = {AGREE['fleiss_n']})"),
        "g2_agree_2": ("Kappa Cohen per pasangan: " + "; ".join(N(k, 3, "id") for k in AGREE["cohen"])
                       + " (n = 40 tiap pasangan)"),
        "g2_agree_3": "Penilai adalah tim penulis, bukan panel ahli eksternal. Nilai kappa mendekati nol.",
        "g2_note": "Lapis 26 dan 19 adalah subset dari kolam 40 klaim, dari berkas items yang sama.",
        "g3_title": "Gambar 3. Skor Brier menurut jenis bukti, lapis 36",
        "g3_y": "Skor Brier, batas 1 (makin kecil makin baik)",
        "g4_title": "Gambar 4. Konsistensi label R1 = R3 antar lapis butir",
        "g4_y": "Klaim dengan label R1 = R3 (%)",
        "g4_layers": ["lapis 40\n(awal)", "lapis 36\n(utama)", "lapis 26\n(kepekaan)", "lapis 19\n(kepekaan)"],
        "g4_layers_s": ["40\n(awal)", "36\n(utama)", "26\n(kep.)", "19\n(kep.)"],
        "g5_title": "Gambar 5. Massa false-support pada bukti NEI, lapis 36",
        "g5_y": "Massa false-support: p(SUPPORTED) + p(REFUTED)\npada item NEI (makin kecil makin baik)",
        "g6_title": "Gambar 6. Kesepakatan argmax uji ulang per tingkat bukti (lapis 19 klaim)",
        "g6_y": "Kesepakatan argmax antar dua putaran (%)",
        "g6_levels": ["R1\n(abstrak)", "R2\n(abstrak +\nhasil)", "R3\n(teks penuh)"],
        "g6_levels_s": ["R1", "R2", "R3"],
        "g6_note": [f"Uji ulang: lapis 19 klaim, 133 observasi per model (R1 {KEST[('qwen3.8-flash', 'R1')]['n']}, "
                    f"R2 {KEST[('qwen3.8-flash', 'R2')]['n']}, R3 {KEST[('qwen3.8-flash', 'R3')]['n']}). "
                    "Gagal parse dihitung sebagai beda (model API).",
                    "GPT-6.1 Sol (unverified): sesi terpisah, tidak terverifikasi (diarsir). "
                    "Footnote standar tidak dipakai: lapis ini bukan himpunan utama 36 klaim."],
        "g7_title": "Gambar 7. Panel ringkas: Brier, konsistensi, false-support, kestabilan",
        "g7_panels": ["(a) Skor Brier, batas 1", "(b) Konsistensi label R1 = R3",
                      "(c) Massa false-support, item NEI", "(d) Kesepakatan uji ulang (19 klaim)"],
        "g7_note_d": "Panel d: lapis uji ulang 19 klaim, 133 observasi per model; GPT-6.1 Sol (unverified) dari sesi terpisah.",
        "cat": {"own R3": "own R3\n(SUPPORTED)", "near R1": "near R1\n(NEI)", "near R3": "near R3\n(NEI)",
                "far R1": "far R1\n(NEI)", "far R3": "far R3\n(NEI)"},
        "ci_note": None,
    },
}
for _lang in ("en", "id"):
    T[_lang]["ci_note"] = ci_width_note(_lang)
    T[_lang]["g3_note"] = n_note(_lang)

# Terjemahan bentuk bukti untuk diagram G1
FORMS = {
    "en": {"own R1": ("own R1 (abstract)", "no anchor label"),
           "own R2": ("own R2 (abstract + results)", "no anchor label"),
           "own R3": ("own R3 (full text)", "anchor: SUPPORTED (author conclusion)"),
           "near R1": ("near R1 (abstract)", "anchor: NEI, other article, near topic"),
           "near R3": ("near R3 (full text)", "anchor: NEI, other article, near topic"),
           "far R1": ("far R1 (abstract)", "anchor: NEI, other article, far topic"),
           "far R3": ("far R3 (full text)", "anchor: NEI, other article, far topic")},
    "id": {"own R1": ("own R1 (abstrak)", "tanpa label jangkar"),
           "own R2": ("own R2 (abstrak + hasil)", "tanpa label jangkar"),
           "own R3": ("own R3 (teks penuh)", "jangkar: SUPPORTED (kesimpulan penulis)"),
           "near R1": ("near R1 (abstrak)", "jangkar: NEI, artikel lain, topik dekat"),
           "near R3": ("near R3 (teks penuh)", "jangkar: NEI, artikel lain, topik dekat"),
           "far R1": ("far R1 (abstrak)", "jangkar: NEI, artikel lain, topik jauh"),
           "far R3": ("far R3 (teks penuh)", "jangkar: NEI, artikel lain, topik jauh")},
}
FORM_ORDER = ["own R1", "own R2", "own R3", "near R1", "near R3", "far R1", "far R3"]
FORM_FILL = {"own R1": "#EFEFEF", "own R2": "#EFEFEF", "own R3": "#CFE6F5",
             "near R1": "#FBE5CC", "near R3": "#FBE5CC", "far R1": "#FBE5CC", "far R3": "#FBE5CC"}

CONTAIN = []  # (teks, kotak) untuk pemeriksaan muat di dalam kotak


# ---------------------------------------------------------------- util gambar
def fig_title(fig, text, H):
    fig.text(0.015, 1 - 0.30 / H, text, ha="left", va="center", fontsize=10, fontweight="bold")


def footer(fig, lines, H):
    n = len(lines)
    for i, line in enumerate(lines):
        y_in = 0.10 + 0.16 * (n - 1 - i)
        fig.text(0.015, y_in / H, line, ha="left", va="bottom", fontsize=6.8, color="#333333")


def model_handles(hatch_codex=False):
    hs = []
    for m in MODELS:
        if m == "codex" and hatch_codex:
            hs.append(Patch(facecolor=COL[m], edgecolor="#222222", hatch="///", linewidth=0.4, label=DISP[m]))
        else:
            hs.append(Patch(facecolor=COL[m], edgecolor="#222222", linewidth=0.4, label=DISP[m]))
    return hs


def line_handles():
    return [Line2D([0], [0], color=COL[m], marker=MARK[m], markersize=4.5, lw=1.0,
                    markerfacecolor=COL[m], markeredgecolor="#222222", markeredgewidth=0.4, label=DISP[m])
            for m in MODELS]


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#555555", lw=0.7,
                                shrinkA=0, shrinkB=0, mutation_scale=7))


def box(ax, x, y, w, h, text, fc, fs=7.5, ha="center"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.0",
                       fc=fc, ec="#333333", lw=0.8)
    ax.add_patch(p)
    tx = x + w / 2 if ha == "center" else x + 1.2
    t = ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=fs, color="#111111", linespacing=1.3)
    CONTAIN.append((t, p))
    return p


def check_layout(fig, name):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    texts = [t for t in fig.findobj(Text) if t.get_visible() and t.get_text().strip()]
    boxes = [t.get_window_extent(r) for t in texts]
    overlaps = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = boxes[i], boxes[j]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0)
            oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > 1.0 and oy > 1.0:
                overlaps.append((texts[i].get_text()[:28].replace("\n", " "),
                                 texts[j].get_text()[:28].replace("\n", " ")))
    W, H = fig.bbox.width, fig.bbox.height
    outside = [t.get_text()[:28].replace("\n", " ") for t, b in zip(texts, boxes)
               if b.x0 < -1 or b.y0 < -1 or b.x1 > W + 1 or b.y1 > H + 1]
    contain_fail = []
    for t, p in CONTAIN:
        tb, pb = t.get_window_extent(r), p.get_window_extent(r)
        if not (tb.x0 >= pb.x0 - 1 and tb.x1 <= pb.x1 + 1 and tb.y0 >= pb.y0 - 1 and tb.y1 <= pb.y1 + 1):
            contain_fail.append(t.get_text()[:28].replace("\n", " "))
    return {"nama": name, "tumpang_tindih": overlaps, "keluar_figur": outside,
            "keluar_kotak": contain_fail}


CHECKS = []


def save(fig, name, lang):
    CHECKS.append(check_layout(fig, f"{name}_{lang}"))
    fig.savefig(OUT / f"{name}_{lang}.png", dpi=300)
    fig.savefig(OUT / f"{name}_{lang}.svg")
    plt.close(fig)


def style_axes(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.6)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- G3, G4, G5, G6 (gambar grafik)
CAT_SMALL = {"own R3": "own\nR3", "near R1": "near\nR1", "near R3": "near\nR3",
             "far R1": "far\nR1", "far R3": "far\nR3"}


def cat_label(lang, c, small):
    return CAT_SMALL[c] if small else T[lang]["cat"][c]


def draw_brier(ax, lang, small=False):
    cats = list(BRIER.keys())
    w = 0.19
    for j, m in enumerate(MODELS):
        xs, ys, lo, hi = [], [], [], []
        for i, c in enumerate(cats):
            rec = L36[(m, BRIER[c])]
            xs.append(i + (j - 1.5) * w)
            ys.append(rec["v"])
            lo.append(rec["v"] - rec["lo"])
            hi.append(rec["hi"] - rec["v"])
        ax.bar(xs, ys, width=w * 0.92, color=COL[m], edgecolor="#222222", linewidth=0.4,
               yerr=[lo, hi], capsize=1.5,
               error_kw={"elinewidth": 0.6, "ecolor": "#222222", "capthick": 0.6})
    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels([cat_label(lang, c, small) for c in cats])
    ax.set_xlim(-0.6, len(cats) - 0.4)
    ax.set_ylim(0, 0.5)
    ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: N(v, 2, lang)))
    ax.set_ylabel(T[lang]["g3_y"])
    style_axes(ax)


def draw_consistency(ax, lang, small=False):
    offs = [-0.12, -0.04, 0.04, 0.12]
    labels = T[lang]["g4_layers_s" if small else "g4_layers"]
    for j, m in enumerate(MODELS):
        xs = [i + offs[j] for i in range(4)]
        ys = [PEM[(m, SESUAI)][lap] * 100 for lap in ORDER_LAP]
        ax.plot(xs, ys, color=COL[m], lw=1.0, marker=MARK[m], ms=4.5, mfc=COL[m],
                mec="#222222", mew=0.4, zorder=3)
        rec = L36[(m, SESUAI)]
        assert abs(rec["v"] * 100 - ys[1]) <= 1e-6
        ax.errorbar([xs[1]], [ys[1]],
                    yerr=[[(rec["v"] - rec["lo"]) * 100], [(rec["hi"] - rec["v"]) * 100]],
                    fmt="none", ecolor=COL[m], elinewidth=0.8, capsize=2, zorder=2)
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels)
    ax.set_xlim(-0.45, 3.45)
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: N(v, 0, lang)))
    ax.set_ylabel(T[lang]["g4_y"])
    style_axes(ax)


def draw_fs(ax, lang, small=False):
    groups = ["near R1", "far R1", "near R3", "far R3"]
    w = 0.19
    for j, m in enumerate(MODELS):
        xs, ys, lo, hi = [], [], [], []
        for i, g in enumerate(groups):
            rec = L36[(m, FS[g])]
            assert rec["lo"] is not None
            xs.append(i + (j - 1.5) * w)
            ys.append(rec["v"])
            lo.append(rec["v"] - rec["lo"])
            hi.append(rec["hi"] - rec["v"])
        ax.bar(xs, ys, width=w * 0.92, color=COL[m], edgecolor="#222222", linewidth=0.4,
               yerr=[lo, hi], capsize=1.5,
               error_kw={"elinewidth": 0.6, "ecolor": "#222222", "capthick": 0.6})
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([cat_label(lang, g, small) for g in groups])
    ax.set_xlim(-0.6, len(groups) - 0.4)
    ax.set_ylim(0, 0.35)
    ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: N(v, 2, lang)))
    ax.set_ylabel(T[lang]["g5_y"])
    style_axes(ax)


def draw_stab(ax, lang, small=False):
    levels = ["R1", "R2", "R3"]
    labels = T[lang]["g6_levels_s" if small else "g6_levels"]
    w = 0.19
    for j, m in enumerate(MODELS):
        xs = [i + (j - 1.5) * w for i in range(3)]
        ys = [retest_pct(m, lvl) for lvl in levels]
        hatch = "///" if m == "codex" else None
        ax.bar(xs, ys, width=w * 0.92, color=COL[m], edgecolor="#222222", linewidth=0.4, hatch=hatch)
        if small:
            continue  # panel ringkas G7: nilai tidak dicetak, lihat G6 tunggal
        for x, y in zip(xs, ys):
            ax.text(x, y + 1.5, N(y, 1, lang), ha="center", va="bottom", fontsize=6.3, color="#111111")
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(0, 110)
    ax.set_yticks(range(0, 101, 20))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: N(v, 0, lang)))
    ax.set_ylabel(T[lang]["g6_y"])
    style_axes(ax)


def standalone(name, lang, draw, W, H, title_key, notes, handles=None, legend_ncol=4):
    fig = plt.figure(figsize=(W, H))
    left, right, top, bottom = 0.95, 0.25, 0.80, 1.35
    ax = fig.add_axes([left / W, bottom / H, (W - left - right) / W, (H - bottom - top) / H])
    draw(ax, lang, small=False)
    fig.legend(handles=handles, loc="center", bbox_to_anchor=(0.5, 0.56 / H), ncol=legend_ncol, frameon=False)
    fig_title(fig, T[lang][title_key], H)
    footer(fig, notes, H)
    return fig


def build_g3(lang):
    fig = standalone("G3", lang, draw_brier, 7.0, 4.4, "g3_title",
                     [FOOT, T[lang]["g3_note"]], model_handles())
    save(fig, "G3_brier_bukti_lapis36", lang)


def build_g4(lang):
    fig = standalone("G4", lang, draw_consistency, 6.6, 4.4, "g4_title",
                     [FOOT, T[lang]["ci_note"]], line_handles())
    save(fig, "G4_konsistensi_r1_r3", lang)


def build_g5(lang):
    fig = standalone("G5", lang, draw_fs, 7.0, 4.4, "g5_title", [FOOT], model_handles())
    save(fig, "G5_false_support", lang)


def build_g6(lang):
    fig = standalone("G6", lang, draw_stab, 6.6, 4.4, "g6_title", T[lang]["g6_note"],
                     model_handles(hatch_codex=True))
    save(fig, "G6_kestabilan_ulang", lang)


# ---------------------------------------------------------------- G1 (diagram)
def build_g1(lang):
    W, H = 9.0, 5.6
    CONTAIN.clear()
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0.01, 0.12, 0.98, 0.78])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    box(ax, 1, 42, 14, 16, T[lang]["g1_claim"], fc="#FFFFFF")
    ax.text(36, 92, T[lang]["g1_forms"], ha="center", va="center", fontsize=8, fontweight="bold")
    for i, key in enumerate(FORM_ORDER):
        yb = 88 - i * 10.5 - 8.5
        l1, l2 = FORMS[lang][key]
        box(ax, 20, yb, 32, 8.5, f"{l1}\n{l2}", fc=FORM_FILL[key], fs=7.2)
        cy = yb + 4.25
        arrow(ax, 15, 50, 20, cy)
        arrow(ax, 52, cy, 57, 50)
    box(ax, 57, 36, 18, 28, T[lang]["g1_scoring"], fc="#E8E8E8", fs=7.2)
    arrow(ax, 75, 50, 80, 77)
    arrow(ax, 75, 50, 80, 50)
    arrow(ax, 75, 50, 80, 23)
    box(ax, 80, 70, 19, 14, T[lang]["g1_m1"], fc="#E6F0FA", fs=7.0)
    box(ax, 80, 43, 19, 14, T[lang]["g1_m2"], fc="#E6F0FA", fs=7.0)
    box(ax, 80, 16, 19, 14, T[lang]["g1_m3"], fc="#E6F0FA", fs=7.0)
    fig_title(fig, T[lang]["g1_title"], H)
    footer(fig, T[lang]["g1_note"], H)
    save(fig, "G1_alur_desain", lang)


# ---------------------------------------------------------------- G2 (corong)
def build_g2(lang):
    W, H = 7.0, 6.6
    CONTAIN.clear()
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0.02, 0.13, 0.96, 0.78])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    t = T[lang]
    box(ax, 10, 86, 80, 10, "\n".join(t["g2_pool"]), fc="#EDEDED", fs=8)
    arrow(ax, 50, 86, 50, 78)
    box(ax, 16, 68, 56, 10, "\n".join(t["g2_a40"]), fc="#DCEBF7", fs=8)
    arrow(ax, 44, 68, 44, 56)
    arrow(ax, 64, 68, 86, 56)
    box(ax, 16, 46, 54, 10, "\n".join(t["g2_a36"]), fc="#B9D8EE", fs=8)
    box(ax, 74, 46, 25, 10, "\n".join(t["g2_out"]), fc="#FFFFFF", fs=7.2)
    ax.text(2, 40, t["g2_layers"], ha="left", va="center", fontsize=7.8, fontweight="bold")
    box(ax, 2, 20, 30, 14, "\n".join(t["g2_l40"]), fc="#F4F4F4", fs=7.5)
    box(ax, 35, 20, 30, 14, "\n".join(t["g2_l26"]), fc="#F4F4F4", fs=7.5)
    box(ax, 68, 20, 30, 14, "\n".join(t["g2_l19"]), fc="#F4F4F4", fs=7.5)
    box(ax, 2, 1, 96, 14, "\n".join([t["g2_agree_hdr"], t["g2_agree_1"], t["g2_agree_2"], t["g2_agree_3"]]),
        fc="#FFF8E7", fs=7.4, ha="left")
    fig_title(fig, t["g2_title"], H)
    footer(fig, [t["g2_note"]], H)
    save(fig, "G2_corong_butir", lang)


# ---------------------------------------------------------------- G7 (panel 2x2)
def build_g7(lang):
    W, H = 7.0, 7.0
    left, right, top, bottom, gx, gy = 0.85, 0.25, 0.80, 1.20, 0.60, 0.60
    cw = (W - left - right - gx) / 2
    ch = (H - top - bottom - gy) / 2
    fig = plt.figure(figsize=(W, H))
    draws = [draw_brier, draw_consistency, draw_fs, draw_stab]
    for k, (r, c) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
        x0 = left + c * (cw + gx)
        y_top = H - top - r * (ch + gy)
        y0 = y_top - ch
        ax = fig.add_axes([x0 / W, y0 / H, cw / W, ch / H])
        draws[k](ax, lang, small=True)
        ax.set_title(T[lang]["g7_panels"][k], fontsize=8, loc="left", pad=4)
    fig.legend(handles=model_handles(hatch_codex=True), loc="center", bbox_to_anchor=(0.5, 0.56 / H),
               ncol=4, frameon=False)
    fig_title(fig, T[lang]["g7_title"], H)
    footer(fig, [FOOT, T[lang]["g7_note_d"]], H)
    save(fig, "G7_panel_ringkas", lang)


# ---------------------------------------------------------------- bangun semua
def build_all():
    for lang in ("en", "id"):
        build_g1(lang)
        build_g2(lang)
        build_g3(lang)
        build_g4(lang)
        build_g5(lang)
        build_g6(lang)
        build_g7(lang)


# ---------------------------------------------------------------- INDEKS.md
def write_index():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append("# INDEKS gambar: Agen E (grafik statis)")
    lines.append("")
    lines.append(f"Dibangun: {now} oleh `C:\\EPIS_KERJA\\RENDER\\gambar\\bangun_gambar.py`. "
                 "Ulang dengan: `py -3.12 -I -X utf8 C:\\EPIS_KERJA\\RENDER\\gambar\\bangun_gambar.py`.")
    lines.append("")
    lines.append("Status angka: HASIL MODEL (BELUM DIVERIFIKASI), sesuai berkas sumber. "
                 "Tidak ada model dipanggil, tidak ada statistik baru, tidak ada berkas sumber diubah. "
                 "Semua keluaran hanya di `C:\\EPIS_KERJA\\RENDER\\`.")
    lines.append("")
    lines.append("## Daftar gambar")
    lines.append("")
    lines.append("Setiap gambar ada dalam dua bahasa (`_en`, `_id`) dengan format PNG 300 dpi dan SVG.")
    lines.append("")
    lines.append("| Gambar | Isi | Sumber data |")
    lines.append("|---|---|---|")
    lines.append("| G1 `G1_alur_desain` | Diagram desain: tujuh bentuk bukti, label jangkar, tiga metrik | Desain studi (skema, tanpa data); label dari aturan jangkar |")
    lines.append("| G2 `G2_corong_butir` | Corong 294 kolam, 40 jangkar, 36 utama, lapis 26 dan 19; kotak kesepakatan penilai | Angka 294 dari `bahan/v2/LAPORAN_AGEN_1_V2.md`; status dari `bahan/v2/hasil_olahan_final/status_butir.csv` (hanya hitungan dan ID keluar); kesepakatan dari `RINGKASAN_KELAYAKAN.md` |")
    lines.append("| G3 `G3_brier_bukti_lapis36` | Brier batas 1 per model dan jenis bukti, lapis 36, batang galat 95% CI | `_lapis36/tabel_lapis36_4model.csv` |")
    lines.append("| G4 `G4_konsistensi_r1_r3` | Proporsi R1 = R3 per model pada lapis 40, 36, 26, 19 | `_lapis36/tabel_pembanding_lapis_40_36_26_19.csv` (nilai titik); CI lapis 36 dari `tabel_lapis36_4model.csv` |")
    lines.append("| G5 `G5_false_support` | Massa false-support near dan far, R1 dan R3, lapis 36, CI 95% | `_lapis36/tabel_lapis36_4model.csv` |")
    lines.append("| G6 `G6_kestabilan_ulang` | Persen argmax sama per tingkat bukti, uji ulang 19 klaim | `_retest_lapis19/KESTABILAN.csv` (tiga model API, kolom gagal dihitung beda); `gpt61_codex/KESTABILAN_codex.csv` (GPT-6.1 Sol, sesi terpisah) |")
    lines.append("| G7 `G7_panel_ringkas` | Panel 2x2 dari G3, G4, G5, G6 | Sama dengan G3 sampai G6 |")
    lines.append("")
    lines.append("Nama berkas lengkap: `<nama>_en.png`, `<nama>_en.svg`, `<nama>_id.png`, `<nama>_id.svg`.")
    lines.append("")
    lines.append("## Pencocokan angka (CSV dibaca, MD dicocokkan)")
    lines.append("")
    lines.append("Setiap angka gambar dibaca dari CSV. Setelah itu, angka yang sama di MD dibandingkan "
                 "(toleransi 0,00005 untuk 4 desimal, 0,05 poin untuk persen 1 desimal). Skrip berhenti bila ada beda.")
    lines.append("")
    lines.append("| Berkas | Cocok | Beda |")
    lines.append("|---|---|---|")
    for name, (ok_n, bad_n) in MATCH_LOG.items():
        lines.append(f"| {name} | {ok_n} | {bad_n} |")
    lines.append("")
    lines.append("Contoh nilai yang dicocokkan (CSV = MD):")
    lines.append("")
    m_own = "qwen3.8-flash"
    lines.append(f"- G3 own R3, qwen3.8-flash: {N(L36[(m_own, BRIER['own R3'])]['v'], 4, 'en')} "
                 f"[{N(L36[(m_own, BRIER['own R3'])]['lo'], 4, 'en')}; {N(L36[(m_own, BRIER['own R3'])]['hi'], 4, 'en')}] "
                 "(md: 0.0765 [0.0004; 0.1985]).")
    lines.append(f"- G3 near R3, qwen4-max-preview: {N(L36[('qwen4-max-preview', BRIER['near R3'])]['v'], 4, 'en')} "
                 "(md: 0.1725 [0.0755; 0.2937]).")
    lines.append(f"- G5 far R3, qwen4-max-preview: {N(L36[('qwen4-max-preview', FS['far R3'])]['v'], 4, 'en')} "
                 f"[{N(L36[('qwen4-max-preview', FS['far R3'])]['lo'], 4, 'en')}; {N(L36[('qwen4-max-preview', FS['far R3'])]['hi'], 4, 'en')}] "
                 "(md: 0.2200 [0.1308; 0.3200]).")
    lines.append(f"- G4 lapis 36, sesuai R1 = R3, deepseek-v4.1-flash: {N(PEM[('deepseek-v4.1-flash', SESUAI)][36] * 100, 1, 'en')}% "
                 "(md: 0.4286).")
    lines.append(f"- G6 R3, deepseek-v4.1-flash (gagal dihitung beda): {N(retest_pct('deepseek-v4.1-flash', 'R3'), 1, 'en')}% "
                 f"(valid saja: {N(KEST[('deepseek-v4.1-flash', 'R3')]['pct'] * 100, 1, 'en')}%; md: 89.5% dan 92.7%).")
    lines.append(f"- G6 R1, GPT-6.1 Sol (unverified): {N(COD['R1']['v'] * 100, 1, 'en')}% "
                 f"[{N(COD['R1']['lo'] * 100, 1, 'en')}; {N(COD['R1']['hi'] * 100, 1, 'en')}] (md: 98.2% [94.7; 100.0]).")
    lines.append(f"- G2 persen sepakat {N(AGREE['pct'], 1, 'en')}% (120 pasangan), kappa Fleiss {N(AGREE['fleiss'], 3, 'en')} "
                 f"(n = {AGREE['fleiss_n']}), kappa Cohen {', '.join(N(k, 3, 'en') for k in AGREE['cohen'])}.")
    lines.append(f"- G2 jumlah: kolam {POOL}; jangkar {STATUS['n40']} (dipakai {STATUS['dipakai']}, direvisi {STATUS['direvisi']}, "
                 f"keluar {len(STATUS['keluar'])}); lapis 40/36/26/19 = {LAYER_N[40]}/{LAYER_N[36]}/{LAYER_N[26]}/{LAYER_N[19]} klaim unik "
                 "(dihitung dari items, 7 observasi per klaim).")
    lines.append("")
    lines.append("## Pemeriksaan tata letak")
    lines.append("")
    lines.append("Setiap teks diperiksa: tumpang tindih antar teks, teks keluar figur, dan teks keluar kotak diagram.")
    lines.append("")
    lines.append("| Gambar | Tumpang tindih | Keluar figur | Keluar kotak |")
    lines.append("|---|---|---|---|")
    for c in CHECKS:
        lines.append(f"| {c['nama']} | {len(c['tumpang_tindih'])} | {len(c['keluar_figur'])} | {len(c['keluar_kotak'])} |")
    lines.append("")
    lines.append("## Catatan dan masalah")
    lines.append("")
    lines.append("1. **Footnote lapis 36 belum cocok dengan sumber.** Footnote diminta berbunyi \"Pilot+dev claims only\", "
                 "tetapi `_lapis36/tabel_lapis36_4model.md` menulis keluaran API berasal dari pilot, dev, dan val. "
                 "`items_lapis_36.jsonl` tidak memuat field split, jadi tidak bisa diverifikasi dari berkas. "
                 "Footnote dipakai persis seperti diminta. Perlu dicek penulis.")
    lines.append("2. **CI hanya untuk lapis 36.** CSV pembanding (lapis 40, 26, 19) hanya memuat nilai titik. "
                 "G4 menampilkan CI hanya untuk lapis 36; tidak ada CI yang dikarang.")
    lines.append("3. **G6 memakai footnote khusus.** Kestabilan memakai lapis 19 klaim (133 observasi per model), "
                 "bukan 36 klaim dan 252 observasi, sehingga footnote standar tidak akurat. Footnote khusus dipakai dan dicatat.")
    lines.append("4. **G6 memakai angka konservatif untuk model API.** Kolom `persen_argmax_sama_gagal_dihitung_beda` dipakai, "
                 "sehingga gagal parse dihitung sebagai beda. Untuk deepseek-v4.1-flash R3: 89,5% (konservatif) "
                 "dan 92,7% (hanya pasangan valid). Kedua angka ada di KESTABILAN.csv.")
    lines.append("5. **Jumlah n tidak 36 di beberapa batang G3.** deepseek-v4.1-flash own R3 n = 35 (satu gagal parse final), "
                 "dan semua batang Brier batas 1 GPT-6.1 Sol (unverified) n = 35 (satu klaim SKIP, C0230). "
                 "Keterangan n tercetak di footnote G3.")
    lines.append("6. **Label codex.** Semua gambar memakai `GPT-6.1 Sol (unverified)`. Sumber menulis `codex (gpt-6.1-sol, tak terverifikasi)`. "
                 "Uji ulang codex berasal dari sesi terpisah dan belum terverifikasi (diarsir di G6).")
    lines.append("7. **Kesepakatan penilai.** Penilai adalah tiga anggota tim penulis, bukan panel ahli eksternal. "
                 "Kappa mendekati nol. Keterangan ini ada di G2 dan di ringkasan sumber.")
    lines.append("8. **Judul tanpa kesimpulan model.** Semua judul hanya menyebut isi grafik. Gambar menunjukkan pola, bukan peringkat.")
    lines.append("9. **Angka desimal.** Gambar ID memakai koma desimal. Footnote memakai teks Inggris persis seperti diminta di kedua bahasa.")
    lines.append("10. **Pembacaan lapis 26 dan 19.** Jumlah klaim dihitung dari `items_lapis_26.jsonl` dan `items_lapis_19.jsonl`, "
                 "yang sama dengan sumber skrip pembanding. Tidak ada angka yang diketik dari ingatan.")
    lines.append("")
    (OUT / "INDEKS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build_all()
    write_index()
    bad = [c for c in CHECKS if c["tumpang_tindih"] or c["keluar_figur"] or c["keluar_kotak"]]
    for c in CHECKS:
        print(f"[tata letak] {c['nama']}: tumpang={len(c['tumpang_tindih'])} "
              f"keluar_figur={len(c['keluar_figur'])} keluar_kotak={len(c['keluar_kotak'])}")
        for pair in c["tumpang_tindih"]:
            print("   overlap:", pair)
        for item in c["keluar_kotak"]:
            print("   keluar kotak:", item)
    print("selesai; berkas di", OUT)
    print("gambar dengan masalah:", len(bad))
