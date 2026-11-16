# -*- coding: utf-8 -*-
"""Bangun gambar H1-H5 (EN dan ID) untuk analisis utama 294 (tiga model API).

Sumber hanya dibaca dari C:\\EPIS_KERJA\\AI_EPISTEMICS_2026_PHASE_2_PREP\\HASIL_PENGUJIAN\\_utama294.
Tidak memanggil model, tidak menghitung statistik baru, tidak mengubah berkas sumber.
Keluaran hanya di C:\\EPIS_KERJA\\RENDER\\gambar294\\ (cache font di C:\\EPIS_KERJA\\RENDER\\mplcache).

Jalankan: py -3.12 -I -X utf8 C:\\EPIS_KERJA\\RENDER\\gambar294\\bangun_gambar294.py
"""
import csv
import datetime
import math
import os
import re
import textwrap
from pathlib import Path

ROOT = Path(r"C:\EPIS_KERJA\RENDER")
OUT = ROOT / "figures_294"
CACHE = ROOT / "mplcache"
OUT.mkdir(parents=True, exist_ok=True)
CACHE.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(CACHE)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from matplotlib.text import Text

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 8,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 6.8,
    "ytick.labelsize": 7,
    "legend.fontsize": 7.5,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 0.7,
    "savefig.dpi": 300,
    "svg.fonttype": "none",
})

# ---------------------------------------------------------------- sumber (baca saja)
SRC = Path(r"C:\EPIS_KERJA\AI_EPISTEMICS_2026_PHASE_2_PREP\HASIL_PENGUJIAN\_utama294")
F = {
    "main_csv": SRC / "tabel_utama294_3model.csv",
    "main_md": SRC / "tabel_utama294_3model.md",
    "kep_csv": SRC / "tabel_kepekaan.csv",
    "kep_md": SRC / "tabel_kepekaan.md",
    "jumlah": SRC / "jumlah_set.md",
    "catatan": SRC / "CATATAN_UTAMA294.md",
}
for _k, _p in F.items():
    assert _p.exists(), f"berkas sumber tidak ada: {_p}"

MODELS = ["qwen3.8-flash", "qwen4-max-preview", "deepseek-v4.1-flash"]
# Palet Okabe-Ito, warna sama dengan gambar G1-G7
COL = {"qwen3.8-flash": "#0072B2", "qwen4-max-preview": "#E69F00", "deepseek-v4.1-flash": "#009E73"}
MARK = {"qwen3.8-flash": "o", "qwen4-max-preview": "s", "deepseek-v4.1-flash": "^"}
SHORT = {"qwen3.8-flash": "qwen3.8-\nflash", "qwen4-max-preview": "qwen4-max-\npreview",
         "deepseek-v4.1-flash": "deepseek-\nv4.1-flash"}
SETS = ["294", "KEPEKAAN-A", "KEPEKAAN-B"]
N_MAIN = 294
NKEY = {"294": "UTAMA-294", "KEPEKAAN-A": "KEPEKAAN-A", "KEPEKAAN-B": "KEPEKAAN-B"}

M_OWN = "Brier batas 1 own R3 (anchor SUPPORTED)"
M_NEAR = "Brier batas 1 near R3 (anchor NEI)"
M_FAR = "Brier batas 1 far R3 (anchor NEI)"
M_SES = "Sesuai (label R1 = label R3)"
M_DS = "Pergeseran dS"
M_DN = "Pergeseran dN"
M_OVER = "Overkomit (tau 0,7)"
M_FSN = "False-support near R3"
M_FSF = "False-support far R3"
SHORT_NAME = {M_OWN: "own R3", M_NEAR: "near R3", M_FAR: "far R3", M_SES: "label consistency",
              M_DS: "shift dS", M_DN: "shift dN", M_OVER: "overcommitment",
              M_FSN: "false-support near R3", M_FSF: "false-support far R3"}
FOOT = ("294 claims, 2058 observations per model (pilot included; pilot is technical per preregistration); "
        "95% cluster bootstrap CI (B=2000); pattern not ranking")

TOP_IN = 0.85        # ruang judul di atas area gambar (inci)
BOTTOM_EXTRA = 0.92  # jarak dari atas blok footnote ke tepi bawah area gambar (inci)
PAD, GAP, RIGHT = 0.55, 0.30, 0.15


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def read_text(path):
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def fnum(s):
    s = (s or "").strip()
    return float(s) if s else None


def rec_of(r):
    return {"nk": int(r["n_klaim"]), "nobs": int(r["n_obs"]), "n": int(r["n"]),
            "v": float(r["nilai"]), "lo": fnum(r["ci_lo"]), "hi": fnum(r["ci_hi"])}


# ---------------------------------------------------------------- muat CSV
MAIN = {}
for r in read_rows(F["main_csv"]):
    if r["set"] == "UTAMA-294":
        MAIN[(r["model"], r["metrik"])] = rec_of(r)

KEP = {}
for r in read_rows(F["kep_csv"]):
    KEP[(r["model"], r["metrik"], r["sumber"])] = rec_of(r)

for m in MODELS:
    for c in [M_OWN, M_NEAR, M_FAR, M_SES, M_DS, M_DN, M_OVER, M_FSN, M_FSF]:
        assert (m, c) in MAIN, (m, c)
        for s in SETS:
            assert (m, c, s) in KEP, (m, c, s)
for key, rec in list(MAIN.items()) + [((k[0], k[1]), v) for k, v in KEP.items() if k[2] == "294"]:
    if rec["lo"] is not None:
        assert rec["lo"] <= rec["v"] <= rec["hi"], (key, rec)
assert MAIN[(MODELS[0], M_SES)]["nk"] == 294 and MAIN[(MODELS[0], M_SES)]["nobs"] == 2058

# ---------------------------------------------------------------- pencocokan angka
MATCH_LOG = {}
MISMATCH = []
NUM_CI = re.compile(r"^(-?\d+(?:\.\d+)?)(?:\s*\[(-?\d+(?:\.\d+)?);\s*(-?\d+(?:\.\d+)?)\])?$")
TOL4 = 0.00005 + 1e-9


def log_cmp(name, ok, detail):
    MATCH_LOG.setdefault(name, [0, 0])
    MATCH_LOG[name][0 if ok else 1] += 1
    if not ok:
        MISMATCH.append(f"{name}: {detail}")


def parse_cell(s):
    m = NUM_CI.match(s.strip().replace("%", ""))
    if not m:
        return None
    lo = float(m.group(2)) if m.group(2) else None
    hi = float(m.group(3)) if m.group(3) else None
    return float(m.group(1)), lo, hi


def md_rows(text):
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and line.count("|") >= 3:
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def same_val(rec, p):
    if p is None or abs(rec["v"] - p[0]) > TOL4:
        return False
    if p[1] is None:
        return rec["lo"] is None
    return rec["lo"] is not None and abs(rec["lo"] - p[1]) <= TOL4 and abs(rec["hi"] - p[2]) <= TOL4


# (a) tabel utama 294 (md, bagian sebelum UTAMA-274) vs CSV
MAIN_METRICS = {k[1] for k in MAIN}
main_part = read_text(F["main_md"]).split("## UTAMA-274", 1)[0]
for cells in md_rows(main_part):
    if cells[0] not in MAIN_METRICS:
        continue
    for j, m in enumerate(MODELS):
        log_cmp("tabel_utama294_3model.md", same_val(MAIN[(m, cells[0])], parse_cell(cells[1 + j])),
                f"{cells[0]} {m}")

# (b) tabel kepekaan (md) vs CSV, per model, kolom 294 / KEPEKAAN-A / KEPEKAAN-B
cur = None
for line in read_text(F["kep_md"]).splitlines():
    if line.startswith("## Model: "):
        cur = line.split(": ", 1)[1].strip()
        continue
    if not (line.startswith("|") and line.count("|") >= 3) or cur not in MODELS:
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if cells[0] not in MAIN_METRICS:
        continue
    for idx, s in enumerate(SETS):
        log_cmp("tabel_kepekaan.md", same_val(KEP[(cur, cells[0], s)], parse_cell(cells[1 + idx])),
                f"{cur} {cells[0]} {s}")

# (c) CSV kepekaan kolom 294 harus sama dengan CSV utama 294 (silang dua berkas)
for (m, metrik) in MAIN:
    a, b = KEP[(m, metrik, "294")], MAIN[(m, metrik)]
    ok = (abs(a["v"] - b["v"]) <= 1e-9 and a["n"] == b["n"]
          and (a["lo"] is None) == (b["lo"] is None)
          and (a["lo"] is None or (abs(a["lo"] - b["lo"]) <= 1e-9 and abs(a["hi"] - b["hi"]) <= 1e-9)))
    log_cmp("tabel_kepekaan.csv (294) vs tabel_utama294_3model.csv", ok, f"{m} {metrik}")

# (d) jumlah_set.md: klaim, observasi, dan n uji konsistensi per set
for cells in md_rows(read_text(F["jumlah"])):
    if len(cells) < 9 or cells[1] != "semua" or cells[0] not in NKEY.values():
        continue
    src = [k for k, v in NKEY.items() if v == cells[0]][0]
    m = cells[4]
    if m not in MODELS:
        continue
    rec = KEP[(m, M_SES, src)]
    ok = (int(cells[2]) == rec["nk"] and int(cells[3]) == rec["nobs"]
          and int(cells[5]) == rec["n"])
    log_cmp("jumlah_set.md (klaim, observasi, uji konsistensi)", ok,
            f"{cells[0]} {m}: md={cells[2:6]} csv={rec['nk']},{rec['nobs']},{rec['n']}")

for name, (ok_n, bad_n) in MATCH_LOG.items():
    print(f"[cocok] {name}: {ok_n} cocok, {bad_n} beda")
if MISMATCH:
    raise SystemExit("ANGKA TIDAK COCOK, gambar dihentikan:\n" + "\n".join(MISMATCH[:30]))
assert sum(v[0] for v in MATCH_LOG.values()) >= 150, "pencocokan terlalu sedikit"


# ---------------------------------------------------------------- util teks dan sumbu
def N(x, nd, lang):
    s = f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "id" else s


def nice_top(vmax, step):
    return math.ceil(vmax / step) * step


def ticks(top, step):
    k = int(round(top / step))
    return [round(i * step, 4) for i in range(k + 1)]


def n_note(metrics):
    items = []
    for m in MODELS:
        for c in metrics:
            n = MAIN[(m, c)]["n"]
            item = f"{m} {SHORT_NAME[c]} n = {n}"
            if n != N_MAIN and item not in items:
                items.append(item)
    if not items:
        return "All bars and points use n = 294."
    return "Exceptions to n = 294: " + "; ".join(items) + "."


def set_note():
    parts = []
    for m in MODELS:
        ns = [KEP[(m, M_SES, s)]["n"] for s in SETS]
        parts.append(f"{m} {ns[0]}/{ns[1]}/{ns[2]}")
    return ("Label-consistency n for UTAMA-294 / KEPEKAAN-A / KEPEKAAN-B: " + "; ".join(parts) + ". "
            "KEPEKAAN-A (290 claims) drops 4 anchor claims from UTAMA-294; KEPEKAAN-B (280) drops 14, "
            "including those 4, so the three sets are nested and not independent.")


def wrap_lines(texts):
    out = []
    for t in texts:
        out.extend(textwrap.wrap(t, width=140) or [""])
    return out


def top_footer(lines):
    return 0.10 + 0.155 * len(lines)


def draw_footer(fig, lines, H):
    n = len(lines)
    for i, line in enumerate(lines):
        y_in = 0.10 + 0.155 * (n - 1 - i)
        fig.text(0.015, y_in / H, line, ha="left", va="bottom", fontsize=6.6, color="#333333")


def fig_title(fig, text, H):
    fig.text(0.015, 1 - 0.30 / H, text, ha="left", va="center", fontsize=10, fontweight="bold")


def legend_at(fig, handles, H, y_in, ncol):
    fig.legend(handles=handles, loc="center", bbox_to_anchor=(0.5, y_in / H), ncol=ncol, frameon=False)


def model_handles():
    return [Patch(facecolor=COL[m], edgecolor="#222222", linewidth=0.4, label=m) for m in MODELS]


def line_handles():
    return [Line2D([0], [0], color=COL[m], marker=MARK[m], markersize=4.5, lw=1.0,
                   markerfacecolor=COL[m], markeredgecolor="#222222", markeredgewidth=0.4, label=m)
            for m in MODELS]


def style_axes(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.6)
    ax.set_axisbelow(True)


def axes_in(fig, W, H, x0, y0, w, h):
    return fig.add_axes([x0 / W, y0 / H, w / W, h / H])


def fmt_axis(ax, lang, nd, axis="y"):
    f = FuncFormatter(lambda v, _: N(v, nd, lang))
    if axis == "y":
        ax.yaxis.set_major_formatter(f)


def bars(ax, lang, cats, getter, ylim, yticks, cat_labels, ylab, axnd, small=False, nd=3):
    w = 0.2
    for j, m in enumerate(MODELS):
        xs, vs, los, his = [], [], [], []
        for i, c in enumerate(cats):
            rec = getter(m, c)
            xs.append(i + (j - 1) * w)
            vs.append(rec["v"])
            los.append(rec["v"] - rec["lo"])
            his.append(rec["hi"] - rec["v"])
        ax.bar(xs, vs, width=w * 0.92, color=COL[m], edgecolor="#222222", linewidth=0.4,
               yerr=[los, his], capsize=1.8,
               error_kw={"elinewidth": 0.6, "ecolor": "#222222", "capthick": 0.6})
        if not small:
            for x, v, h in zip(xs, vs, his):
                ax.text(x, v + h + ylim[1] * 0.012, N(v, nd, lang), ha="center", va="bottom", fontsize=6.0)
    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels(cat_labels)
    ax.set_xlim(-0.6, len(cats) - 0.4)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    fmt_axis(ax, lang, axnd)
    ax.set_ylabel(ylab)
    style_axes(ax)


def dot_models(ax, lang, metric, small, ylim, yticks, ylab, axnd, nd=3):
    for j, m in enumerate(MODELS):
        rec = MAIN[(m, metric)]
        ax.errorbar([j], [rec["v"]], yerr=[[rec["v"] - rec["lo"]], [rec["hi"] - rec["v"]]],
                    fmt=MARK[m], color=COL[m], markersize=4.8, markeredgecolor="#222222",
                    markeredgewidth=0.4, ecolor=COL[m], elinewidth=0.9, capsize=2.2, zorder=3)
        if not small:
            ax.text(j + 0.12, rec["v"], N(rec["v"], nd, lang), ha="left", va="center", fontsize=6.2)
    labels = []
    for m in MODELS:
        n = MAIN[(m, metric)]["n"]
        labels.append(SHORT[m] + (f"\n(n = {n})" if n != N_MAIN else ""))
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels, fontsize=6.6)
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    fmt_axis(ax, lang, axnd)
    ax.set_ylabel(ylab)
    style_axes(ax)


def dot_sets(ax, lang, metric, ylim, yticks, ylab, axnd, set_labels, small=False):
    for j, m in enumerate(MODELS):
        off = (j - 1) * 0.22
        xs = [i + off for i in range(3)]
        vs = [KEP[(m, metric, s)]["v"] for s in SETS]
        los = [KEP[(m, metric, s)]["v"] - KEP[(m, metric, s)]["lo"] for s in SETS]
        his = [KEP[(m, metric, s)]["hi"] - KEP[(m, metric, s)]["v"] for s in SETS]
        ax.plot(xs, vs, color=COL[m], lw=0.8, zorder=2)
        ax.errorbar(xs, vs, yerr=[los, his], fmt=MARK[m], color=COL[m], markersize=4.8,
                    markeredgecolor="#222222", markeredgewidth=0.4, ecolor=COL[m],
                    elinewidth=0.9, capsize=2.2, zorder=3)
    ax.set_xticks(range(3))
    ax.set_xticklabels(set_labels, fontsize=6.0)
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    fmt_axis(ax, lang, axnd)
    ax.set_ylabel(ylab)
    style_axes(ax)


def sens_top(metric):
    hi = max(KEP[(m, metric, s)]["hi"] for m in MODELS for s in SETS)
    return nice_top(hi + 0.01, 0.05)


def panel_title(ax, text):
    ax.set_title(text, fontsize=7.6, loc="left", pad=3)


CONTAIN = []
CHECKS = []


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
    return {"nama": name, "tumpang_tindih": overlaps, "keluar_figur": outside}


def save(fig, name, lang):
    CHECKS.append(check_layout(fig, f"{name}_{lang}"))
    fig.savefig(OUT / f"{name}_{lang}.png", dpi=300)
    fig.savefig(OUT / f"{name}_{lang}.svg")
    plt.close(fig)


# ---------------------------------------------------------------- teks EN dan ID
T = {
    "en": {
        "h1_title": "Figure H1. Brier score by evidence type, UTAMA-294",
        "h1_y": "Brier score, boundary 1 (lower is better)",
        "h1_cats": ["own R3\n(SUPPORTED)", "near R3\n(NEI)", "far R3\n(NEI)"],
        "h2_title": "Figure H2. Label consistency R1 = R3 and shifts dS and dN, UTAMA-294",
        "h2_p": ["(a) Label R1 = R3", "(b) Shift dS", "(c) Shift dN"],
        "h2_y": "Value (0 to 1 scale)",
        "h3_title": "Figure H3. False-support on NEI evidence at R3, and overcommitment, UTAMA-294",
        "h3_p": ["(a) False-support, R3", "(b) Overcommitment, tau 0.7"],
        "h3_y": "False-support mass (lower is better)",
        "h3_cats": ["near R3\n(NEI)", "far R3\n(NEI)"],
        "h3_over_y": "Overcommitment value (as in CSV)",
        "h3_tau": "tau 0.7",
        "h4_title": "Figure H4. Sensitivity across nested sets: Brier own R3, Brier near R3, label consistency",
        "h4_p": ["(a) Brier, own R3", "(b) Brier, near R3", "(c) Label R1 = R3"],
        "h4_y_brier": "Brier score, boundary 1",
        "h4_y_ses": "Proportion (0 to 1 scale)",
        "h5_title": "Figure H5. Summary panel, UTAMA-294",
        "h5_p": ["(a) Brier by evidence type (H1)", "(b) Label R1 = R3 (H2)",
                 "(c) False-support, R3 (H3)", "(d) Brier, own R3, across sets (H4)"],
        "h5_y_brier": "Brier score",
        "h5_y_fs": "False-support mass",
        "h5_y_ses": "Proportion",
        "sets": ["UTAMA\n294", "KEPEKAAN\nA (290)", "KEPEKAAN\nB (280)"],
    },
    "id": {
        "h1_title": "Gambar H1. Skor Brier menurut jenis bukti, UTAMA-294",
        "h1_y": "Skor Brier, batas 1 (makin kecil makin baik)",
        "h1_cats": ["own R3\n(SUPPORTED)", "near R3\n(NEI)", "far R3\n(NEI)"],
        "h2_title": "Gambar H2. Kesesuaian label R1 = R3 dan pergeseran dS serta dN, UTAMA-294",
        "h2_p": ["(a) Label R1 = R3", "(b) Pergeseran dS", "(c) Pergeseran dN"],
        "h2_y": "Nilai (skala 0 sampai 1)",
        "h3_title": "Gambar H3. False-support pada bukti NEI di R3, dan overkomit, UTAMA-294",
        "h3_p": ["(a) False-support, R3", "(b) Overkomit, tau 0,7"],
        "h3_y": "Massa false-support (makin kecil makin baik)",
        "h3_cats": ["near R3\n(NEI)", "far R3\n(NEI)"],
        "h3_over_y": "Nilai overkomit (sesuai CSV)",
        "h3_tau": "tau 0,7",
        "h4_title": "Gambar H4. Kepekaan antar set bersarang: Brier own R3, Brier near R3, kesesuaian label",
        "h4_p": ["(a) Brier, own R3", "(b) Brier, near R3", "(c) Label R1 = R3"],
        "h4_y_brier": "Skor Brier, batas 1",
        "h4_y_ses": "Proporsi (skala 0 sampai 1)",
        "h5_title": "Gambar H5. Panel ringkas, UTAMA-294",
        "h5_p": ["(a) Brier menurut jenis bukti (H1)", "(b) Label R1 = R3 (H2)",
                 "(c) False-support R3 (H3)", "(d) Brier own R3 antar set (H4)"],
        "h5_y_brier": "Skor Brier",
        "h5_y_fs": "Massa false-support",
        "h5_y_ses": "Proporsi",
        "sets": ["UTAMA\n294", "KEPEKAAN\nA (290)", "KEPEKAAN\nB (280)"],
    },
}


def getter_main(m, c):
    return MAIN[(m, c)]


# ---------------------------------------------------------------- H1
def fig_h1(lang):
    t = T[lang]
    lines = wrap_lines([FOOT, "Brier score, boundary 1: lower is better; failed parses are excluded. "
                              + n_note([M_OWN, M_NEAR, M_FAR])])

    W, ax_h = 7.0, 2.7
    base = top_footer(lines) + BOTTOM_EXTRA
    H = base + ax_h + TOP_IN
    fig = plt.figure(figsize=(W, H))
    ax = axes_in(fig, W, H, 0.95, base, W - 0.95 - 0.25, ax_h)
    top = nice_top(max(MAIN[(m, c)]["hi"] for m in MODELS for c in [M_OWN, M_NEAR, M_FAR]) + 0.03, 0.05)
    bars(ax, lang, [M_OWN, M_NEAR, M_FAR], getter_main, (0, top), ticks(top, 0.05),
         t["h1_cats"], t["h1_y"], axnd=2, nd=3)
    legend_at(fig, model_handles(), H, top_footer(lines) + 0.22, 3)
    fig_title(fig, t["h1_title"], H)
    draw_footer(fig, lines, H)
    save(fig, "H1_brier_bukti_utama294", lang)


# ---------------------------------------------------------------- H2
def fig_h2(lang):
    t = T[lang]
    lines = wrap_lines([FOOT,
                        "Shift dS and shift dN are shown under the names used in the source CSV, on that file's "
                        "0 to 1 scale. " + n_note([M_SES, M_DS, M_DN])])
    W, ax_h = 7.0, 2.6
    base = top_footer(lines) + BOTTOM_EXTRA
    H = base + ax_h + TOP_IN
    fig = plt.figure(figsize=(W, H))
    pw = (W - 3 * PAD - 2 * GAP - RIGHT) / 3
    specs = [(M_SES, t["h2_p"][0]), (M_DS, t["h2_p"][1]), (M_DN, t["h2_p"][2])]
    for k, (metric, ptitle) in enumerate(specs):
        x0 = PAD + k * (pw + GAP + PAD)
        ax = axes_in(fig, W, H, x0, base, pw, ax_h)
        dot_models(ax, lang, metric, False, (0, 1), ticks(1, 0.2), t["h2_y"], axnd=1, nd=3)
        panel_title(ax, ptitle)
    legend_at(fig, line_handles(), H, top_footer(lines) + 0.22, 3)
    fig_title(fig, t["h2_title"], H)
    draw_footer(fig, lines, H)
    save(fig, "H2_kesesuaian_pergeseran_utama294", lang)


# ---------------------------------------------------------------- H3
def fig_h3(lang):
    t = T[lang]
    lines = wrap_lines([FOOT,
                        "False-support = p(SUPPORTED) + p(REFUTED) on NEI items; lower is better. "
                        "Overcommitment at tau 0.7 as reported in the source CSV. "
                        + n_note([M_FSN, M_FSF, M_OVER])])
    W, ax_h = 7.0, 2.7
    base = top_footer(lines) + BOTTOM_EXTRA
    H = base + ax_h + TOP_IN
    fig = plt.figure(figsize=(W, H))
    ax1 = axes_in(fig, W, H, 0.95, base, 3.6, ax_h)
    top1 = nice_top(max(MAIN[(m, c)]["hi"] for m in MODELS for c in [M_FSN, M_FSF]) + 0.03, 0.05)
    bars(ax1, lang, [M_FSN, M_FSF], getter_main, (0, top1), ticks(top1, 0.05),
         t["h3_cats"], t["h3_y"], axnd=2, nd=3)
    panel_title(ax1, t["h3_p"][0])
    ax2 = axes_in(fig, W, H, 5.3, base, 1.45, ax_h)
    top2 = nice_top(max(MAIN[(m, M_OVER)]["hi"] for m in MODELS) + 0.03, 0.01)
    bars(ax2, lang, [M_OVER], getter_main, (0, top2), ticks(top2, 0.01),
         [t["h3_tau"]], t["h3_over_y"], axnd=2, nd=3)
    panel_title(ax2, t["h3_p"][1])
    legend_at(fig, model_handles(), H, top_footer(lines) + 0.22, 3)
    fig_title(fig, t["h3_title"], H)
    draw_footer(fig, lines, H)
    save(fig, "H3_false_support_overkomit_utama294", lang)


# ---------------------------------------------------------------- H4
def fig_h4(lang):
    t = T[lang]
    lines = wrap_lines([FOOT, set_note()])
    W, ax_h = 7.0, 2.7
    base = top_footer(lines) + BOTTOM_EXTRA
    H = base + ax_h + TOP_IN
    fig = plt.figure(figsize=(W, H))
    pw = (W - 3 * PAD - 2 * GAP - RIGHT) / 3
    top_own = sens_top(M_OWN)
    top_near = sens_top(M_NEAR)
    specs = [
        (M_OWN, (0, top_own), ticks(top_own, 0.05), t["h4_y_brier"], 2, t["h4_p"][0]),
        (M_NEAR, (0, top_near), ticks(top_near, 0.05), t["h4_y_brier"], 2, t["h4_p"][1]),
        (M_SES, (0, 1), ticks(1, 0.2), t["h4_y_ses"], 1, t["h4_p"][2]),
    ]
    for k, (metric, ylim, yt, ylab, nd, ptitle) in enumerate(specs):
        x0 = PAD + k * (pw + GAP + PAD)
        ax = axes_in(fig, W, H, x0, base, pw, ax_h)
        dot_sets(ax, lang, metric, ylim, yt, ylab, nd, t["sets"])
        panel_title(ax, ptitle)
    legend_at(fig, line_handles(), H, top_footer(lines) + 0.22, 3)
    fig_title(fig, t["h4_title"], H)
    draw_footer(fig, lines, H)
    save(fig, "H4_kepekaan_set_bersarang_utama294", lang)


# ---------------------------------------------------------------- H5 (panel ringkas 2x2)
def fig_h5(lang):
    t = T[lang]
    lines = wrap_lines([FOOT,
                        n_note([M_OWN, M_NEAR, M_FAR, M_SES, M_FSN, M_FSF])
                        + " Panel (b) shows label consistency only; shifts dS and dN are in H2. "
                          "Panel (d) shows own R3 Brier across the nested sets of H4."])
    W, ax_h, gy = 7.0, 2.25, 0.8
    base = top_footer(lines) + BOTTOM_EXTRA
    H = base + 2 * ax_h + gy + TOP_IN
    fig = plt.figure(figsize=(W, H))
    pw = (W - 0.85 - 0.25 - 0.6) / 2
    xa, xb = 0.85, 0.85 + pw + 0.6
    yb, yt = base, base + ax_h + gy
    top_h1 = nice_top(max(MAIN[(m, c)]["hi"] for m in MODELS for c in [M_OWN, M_NEAR, M_FAR]) + 0.03, 0.05)
    top_fs = nice_top(max(MAIN[(m, c)]["hi"] for m in MODELS for c in [M_FSN, M_FSF]) + 0.03, 0.05)
    top_own = sens_top(M_OWN)

    ax_a = axes_in(fig, W, H, xa, yt, pw, ax_h)
    bars(ax_a, lang, [M_OWN, M_NEAR, M_FAR], getter_main, (0, top_h1), ticks(top_h1, 0.05),
         t["h1_cats"], t["h5_y_brier"], axnd=2, small=True)
    panel_title(ax_a, t["h5_p"][0])

    ax_b = axes_in(fig, W, H, xb, yt, pw, ax_h)
    dot_models(ax_b, lang, M_SES, True, (0, 1), ticks(1, 0.2), t["h5_y_ses"], axnd=1)
    panel_title(ax_b, t["h5_p"][1])

    ax_c = axes_in(fig, W, H, xa, yb, pw, ax_h)
    bars(ax_c, lang, [M_FSN, M_FSF], getter_main, (0, top_fs), ticks(top_fs, 0.05),
         t["h3_cats"], t["h5_y_fs"], axnd=2, small=True)
    panel_title(ax_c, t["h5_p"][2])

    ax_d = axes_in(fig, W, H, xb, yb, pw, ax_h)
    dot_sets(ax_d, lang, M_OWN, (0, top_own), ticks(top_own, 0.05), t["h5_y_brier"], 2, t["sets"], small=True)
    panel_title(ax_d, t["h5_p"][3])

    legend_at(fig, model_handles(), H, top_footer(lines) + 0.22, 3)
    fig_title(fig, t["h5_title"], H)
    draw_footer(fig, lines, H)
    save(fig, "H5_panel_ringkas_utama294", lang)


def build_all():
    for lang in ("en", "id"):
        fig_h1(lang)
        fig_h2(lang)
        fig_h3(lang)
        fig_h4(lang)
        fig_h5(lang)


# ---------------------------------------------------------------- INDEKS294.md
def write_index():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    L = []
    L.append("# INDEKS294: gambar analisis utama 294 (tiga model API)")
    L.append("")
    L.append(f"Dibangun: {now} oleh `C:\\EPIS_KERJA\\RENDER\\gambar294\\bangun_gambar294.py`. "
             "Ulang dengan: `py -3.12 -I -X utf8 C:\\EPIS_KERJA\\RENDER\\gambar294\\bangun_gambar294.py`.")
    L.append("")
    L.append("Status angka: HASIL MODEL (BELUM DIVERIFIKASI), sesuai berkas sumber. Tidak ada model dipanggil, "
             "tidak ada statistik baru, tidak ada berkas sumber diubah. Keluaran hanya di "
             "`C:\\EPIS_KERJA\\RENDER\\gambar294\\`. Gambar lama di `C:\\EPIS_KERJA\\RENDER\\gambar\\` tidak disentuh.")
    L.append("")
    L.append("## Daftar gambar")
    L.append("")
    L.append("Setiap gambar ada dalam dua bahasa (`_en`, `_id`) dengan PNG 300 dpi dan SVG. "
             "Keterangan kaki selalu dalam bahasa Inggris, sesuai permintaan.")
    L.append("")
    L.append("| Gambar | Isi | Sumber data (CSV) |")
    L.append("|---|---|---|")
    L.append("| H1 `H1_brier_bukti_utama294` | Brier batas 1 per model: own R3, near R3, far R3, batang galat 95% CI | `tabel_utama294_3model.csv`, set UTAMA-294 |")
    L.append("| H2 `H2_kesesuaian_pergeseran_utama294` | Kesesuaian label R1 = R3, pergeseran dS, pergeseran dN, dengan CI (tiga panel) | `tabel_utama294_3model.csv`, set UTAMA-294 |")
    L.append("| H3 `H3_false_support_overkomit_utama294` | False-support near R3 dan far R3 dengan CI; panel kecil overkomit tau 0,7 | `tabel_utama294_3model.csv`, set UTAMA-294 |")
    L.append("| H4 `H4_kepekaan_set_bersarang_utama294` | Nilai titik dan CI: Brier own R3, Brier near R3, kesesuaian R1 = R3 untuk UTAMA-294, KEPEKAAN-A, KEPEKAAN-B | `tabel_kepekaan.csv` (kolom sumber 294, KEPEKAAN-A, KEPEKAAN-B) |")
    L.append("| H5 `H5_panel_ringkas_utama294` | Panel 2x2 ringkas: (a) H1, (b) H2 kesesuaian, (c) H3 false-support, (d) H4 Brier own R3 antar set | Sama dengan H1 sampai H4 |")
    L.append("")
    L.append("Nama berkas lengkap: `<nama>_en.png`, `<nama>_en.svg`, `<nama>_id.png`, `<nama>_id.svg`.")
    L.append("")
    L.append("## Pencocokan angka")
    L.append("")
    L.append("Setiap angka gambar dibaca dari CSV. Angka yang sama di MD dibandingkan (toleransi 0,00005 untuk "
             "4 desimal). Skrip berhenti bila ada beda. Pencocokan lintas berkas juga dilakukan untuk kolom 294 "
             "dan jumlah klaim.")
    L.append("")
    L.append("| Berkas yang dicocokkan | Cocok | Beda |")
    L.append("|---|---|---|")
    for name, (ok_n, bad_n) in MATCH_LOG.items():
        L.append(f"| {name} | {ok_n} | {bad_n} |")
    L.append("")
    L.append("Contoh angka yang dicocokkan (CSV = MD):")
    L.append("")
    m0 = MODELS[0]
    r = MAIN[(m0, M_OWN)]
    L.append(f"- H1 own R3, {m0}: {r['v']:.4f} [{r['lo']:.4f}; {r['hi']:.4f}] (md: 0.0322 [0.0112; 0.0579]).")
    r = MAIN[(MODELS[1], M_NEAR)]
    L.append(f"- H1 near R3, {MODELS[1]}: {r['v']:.4f} [{r['lo']:.4f}; {r['hi']:.4f}] (md: 0.2312 [0.1753; 0.2932]).")
    r = MAIN[(MODELS[2], M_OWN)]
    L.append(f"- H1 own R3, {MODELS[2]} (n = {r['n']}): {r['v']:.4f} [{r['lo']:.4f}; {r['hi']:.4f}] (md: 0.0919 [0.0547; 0.1340]).")
    r = MAIN[(MODELS[0], M_FSF)]
    L.append(f"- H3 false-support far R3, {MODELS[0]} (n = {r['n']}): {r['v']:.4f} [{r['lo']:.4f}; {r['hi']:.4f}] (md: 0.0707 [0.0503; 0.0952]).")
    r = MAIN[(MODELS[2], M_SES)]
    L.append(f"- H2 kesesuaian R1 = R3, {MODELS[2]} (n = {r['n']}): {r['v']:.4f} [{r['lo']:.4f}; {r['hi']:.4f}] (md: 0.4896 [0.4340; 0.5486]).")
    r = KEP[(MODELS[1], M_OWN, "KEPEKAAN-B")]
    L.append(f"- H4 own R3, {MODELS[1]}, KEPEKAAN-B: {r['v']:.4f} [{r['lo']:.4f}; {r['hi']:.4f}] (md: 0.0228 [0.0093; 0.0399]).")
    L.append(f"- Jumlah: UTAMA-294 294 klaim, 2058 observasi; KEPEKAAN-A 290 klaim, 2030 observasi; "
             f"KEPEKAAN-B 280 klaim, 1960 observasi; uji konsistensi DeepSeek 288 / 284 / 274 klaim.")
    L.append("")
    L.append("## Pemeriksaan tata letak")
    L.append("")
    L.append("Setiap teks diperiksa untuk tumpang tindih antar teks dan keluar dari figur. Pemeriksaan visual "
             "dengan membaca PNG dilakukan terpisah (lihat catatan).")
    L.append("")
    L.append("| Gambar | Tumpang tindih | Keluar figur |")
    L.append("|---|---|---|")
    for c in CHECKS:
        L.append(f"| {c['nama']} | {len(c['tumpang_tindih'])} | {len(c['keluar_figur'])} |")
    L.append("")
    L.append("## Catatan dan masalah")
    L.append("")
    L.append("1. **Tidak ada GPT-6.1 Sol (codex) di set ini.** Set UTAMA-294 hanya memuat tiga model API. "
             "Codex tidak digambar karena datanya tidak ada di sumber ini.")
    L.append("2. **n di bawah 294.** deepseek-v4.1-flash punya n = 288 pada uji konsistensi, pergeseran, dan overkomit, "
             "serta pada own R3 Brier. qwen3.8-flash punya n = 293 pada far R3. Pengecualian ini ditulis di "
             "keterangan kaki H1 sampai H5, dan keterangan kaki juga memuat n uji konsistensi DeepSeek 288.")
    L.append("3. **Definisi pergeseran dS dan dN tidak tertulis di CSV atau MD.** Skrip sumber hanya memakai nama "
             "metrik. Gambar memakai nama seperti di CSV dengan skala 0 sampai 1 sesuai berkas. Definisi perlu "
             "dicek penulis sebelum dikutip di laporan.")
    L.append("4. **Definisi overkomit tau 0,7 tidak diulang di gambar.** Gambar hanya menulis 'as in CSV'. Pemakaian "
             "tau 0,7 sama dengan judul kolom sumber.")
    L.append("5. **Set bersarang.** KEPEKAAN-B (280) adalah subset dari KEPEKAAN-A (290), yang adalah subset dari "
             "UTAMA-294 (294). Keterangan kaki H4 dan H5 menyatakan hal ini. Titik antar set tidak independen, "
             "dan garis di H4 hanya menunjukkan urutan set.")
    L.append("6. **Lapis 36 tidak dipakai.** `tabel_kepekaan.csv` juga memuat kolom lapis36 dengan cakupan berbeda "
             "(36 klaim, 252 observasi). Kolom itu sengaja dikeluarkan dari H4 karena permintaan hanya tiga set.")
    L.append("7. **Kepekaan hanya nilai titik dan CI.** Brier batas 2 tidak dipakai karena tidak ada CI di sumber.")
    L.append("8. **Versi ringkas H5 lebih sedikit dari H2, H3, H4.** Panel (b) H5 hanya kesesuaian R1 = R3. "
             "Panel (c) H5 hanya near dan far R3 tanpa overkomit. Panel (d) H5 hanya Brier own R3 antar set.")
    L.append("9. **Pilot ikut dalam UTAMA-294** sesuai permintaan. Keterangan kaki menyatakan bahwa pilot adalah tahap "
             "teknis menurut praregistrasi.")
    L.append("10. **Judul tanpa kesimpulan model.** Judul hanya menyebut isi grafik. Keterangan kaki memuat "
             "'pattern not ranking'.")
    L.append("11. **Angka ID memakai koma desimal.** Keterangan kaki tetap berbahasa Inggris di kedua versi.")
    L.append("")
    (OUT / "INDEKS294.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build_all()
    write_index()
    bad = [c for c in CHECKS if c["tumpang_tindih"] or c["keluar_figur"]]
    for c in CHECKS:
        print(f"[tata letak] {c['nama']}: tumpang={len(c['tumpang_tindih'])} keluar_figur={len(c['keluar_figur'])}")
        for pair in c["tumpang_tindih"]:
            print("   overlap:", pair)
        for item in c["keluar_figur"]:
            print("   keluar figur:", item)
    print("selesai; berkas di", OUT)
    print("gambar dengan masalah:", len(bad))
