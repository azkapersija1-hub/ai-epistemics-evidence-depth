"""Utama-294 (Agen U): hitung ulang analisis UTAMA praregistrasi dan dua analisis kepekaan.

Memakai modul harness yang sama dengan skrip lapis36 dan codex: epis.laporan (muat_keluaran_final,
bangun_records, ringkas), epis.laporan_teks (format_provider, format_laporan), epis.subset (pilih_split).
Tau 0,7; bootstrap B=2000, seed default harness.

hitung_set() meniru analisis() di analisis_keluaran.py untuk satu provider per model, tetapi
memanggil ringkas() sekali saja agar bootstrap tidak dihitung dua kali. Hasil teks untuk split
dev, val, dan holdout dibandingkan dengan analisis_<split>_<model>.md yang sudah ada.

Tidak memanggil model. Berkas input hanya dibaca. Keluaran hanya ditulis ke folder _utama294.
Kunci dibaca untuk evaluasi saja; isinya tidak dicetak.

Pemakaian (dari folder _utama294, dengan -B agar tidak menulis __pycache__):
  py -3.12 -B -I -X utf8 skrip_analisis_utama294.py
"""
import csv
import hashlib
import os
import sys
from collections import Counter

P = "C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP"
H = P + "/harness"
HASIL = P + "/HASIL_PENGUJIAN"
OUT = HASIL + "/_utama294"
BAHAN = P + "/bahan/v2"
ITEMS = BAHAN + "/items_model.jsonl"
KUNCI = BAHAN + "/RAHASIA/kunci.jsonl"
FIN = BAHAN + "/hasil_olahan_final"
KELUAR_A = FIN + "/ID_KELUAR.txt"
KELUAR_B = FIN + "/ID_KELUAR_KETAT.txt"
STATUS = FIN + "/status_butir.csv"
LAPIS36_CSV = HASIL + "/_lapis36/tabel_lapis36_4model.csv"
LAPIS36_N_KLAIM = 36
LAPIS36_N_OBS = 252

TAU = 0.7
MODELS = ("qwen3.8-flash", "qwen4-max-preview", "deepseek-v4.1-flash")
SPLITS = ("pilot", "dev", "val", "holdout")
SPLIT_KLAIM = {"pilot": 20, "dev": 78, "val": 98, "holdout": 98}
N_KLAIM_TOTAL = 294
N_OBS_TOTAL = 2058
N_KELUAR_A = 4
N_KELUAR_B = 14
PAIRS_SKOR = (("own", "R3"), ("near", "R1"), ("near", "R3"), ("far", "R1"), ("far", "R3"))

sys.path.insert(0, H)
from epis import laporan, laporan_teks  # noqa: E402
from epis.jsonl_io import baca_jsonl  # noqa: E402
from epis.subset import pilih_split  # noqa: E402

B = laporan.B_CI


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blok in iter(lambda: f.read(1 << 20), b""):
            h.update(blok)
    return h.hexdigest()


def daftar_hash():
    """Semua nyata_*.jsonl (tanpa ARSIP_) di HASIL_PENGUJIAN dan harness/log, plus items dan kunci."""
    berkas = [ITEMS, KUNCI]
    for akar in (HASIL, P + "/harness/log"):
        for dirpath, _dirs, files in os.walk(akar):
            for nama in files:
                if nama.startswith("nyata_") and nama.endswith(".jsonl"):
                    berkas.append(os.path.join(dirpath, nama).replace("\\", "/"))
    return sorted(set(berkas))


def muat_daftar(path):
    """[(claim_id, jenis)] dari berkas daftar; jenis mengikuti baris komentar '# JANGKAR' atau '# UBAHAN'."""
    hasil, bagian = [], None
    with open(path, encoding="utf-8-sig") as f:
        for baris in f:
            s = baris.strip()
            if not s:
                continue
            if s.startswith("#"):
                if s.startswith("# JANGKAR"):
                    bagian = "JANGKAR"
                elif s.startswith("# UBAHAN"):
                    bagian = "UBAHAN"
                continue
            if bagian is None:
                raise ValueError(f"ID sebelum bagian JANGKAR/UBAHAN di {path}")
            hasil.append((s, bagian))
    return hasil


def muat_status():
    with open(STATUS, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def cek_status(status, ex_a, ex_b):
    """Silang periksa berkas daftar dengan status_butir.csv (hanya JANGKAR)."""
    jangkar = [r for r in status if r["jenis"] == "JANGKAR"]
    keluar_status = {r["claim_id"] for r in jangkar if r["keputusan_akhir"] == "KELUAR"}
    tl_status = {r["claim_id"] for r in jangkar if "TIDAK_LAYAK" in r["suara"]}
    return {
        "a_sama_status": ex_a == keluar_status,
        "b_sama_status": ex_b == tl_status,
        "n_a_status": len(keluar_status),
        "n_b_status": len(tl_status),
        "status_keluar_tanpa_daftar_a": sorted(keluar_status - ex_a),
        "status_tl_tanpa_daftar_b": sorted(tl_status - ex_b),
    }


def metrik(ring):
    """Daftar (nama, n, nilai, lo, hi). Nama dan urutan sama dengan skrip lapis36."""
    out = []
    sk, k = ring["skor"], ring["konsistensi"]
    for pair, rung in PAIRS_SKOR:
        g = sk[(pair, rung)]
        tipe = "anchor SUPPORTED" if pair == "own" else "anchor NEI"
        ci = g["ci_brier"]
        out.append((f"Brier batas 1 {pair} {rung} ({tipe})", g["n"] - g["n_gagal"],
                    g["brier_batas1"], ci["lo"], ci["hi"]))
    for pair, rung in PAIRS_SKOR:
        g = sk[(pair, rung)]
        out.append((f"Brier batas 2 {pair} {rung} (gagal = 2,0)", g["n"], g["brier_batas2"], None, None))
    for nama, kunci in (("Sesuai (label R1 = label R3)", "sesuai"), ("Pergeseran dS", "dS"),
                        ("Pergeseran dN", "dN"), ("Overkomit (tau 0,7)", "overkomit")):
        c = k[kunci]
        out.append((nama, c["n"], c["rerata"], c["lo"], c["hi"]))
    fs = k["false_support"]
    for rung in ("R1", "R3"):
        near, far, sel = fs[rung]["near"], fs[rung]["far"], fs[rung]["selisih"]
        out.append((f"False-support near {rung}", near["n"], near["rerata"], near["lo"], near["hi"]))
        out.append((f"False-support far {rung}", far["n"], far["rerata"], far["lo"], far["hi"]))
        out.append((f"Selisih FS near-far {rung}", near["n"], sel["rerata"], sel["lo"], sel["hi"]))
    return out


def hitung_set(model, items_s, kunci_s, rows_semua):
    """Satu provider per model, meniru analisis() di analisis_keluaran.py dengan ringkas() sekali."""
    obs = {it["obs_id"] for it in items_s}
    rows = [r for r in rows_semua if r["obs_id"] in obs]
    grup = {}
    for r in rows:
        grup.setdefault((r["provider_id"], r["ulangan"]), []).append(r)
    assert len(grup) == 1, f"grup provider tidak tunggal: {list(grup)}"
    (provider_id, ulangan), baris = next(iter(grup.items()))
    final = laporan.muat_keluaran_final(baris)
    recs = laporan.bangun_records(items_s, kunci_s, final)
    ring = laporan.ringkas(recs, tau=TAU, b=B)
    gagal1 = sum(1 for r in baris if r["percobaan"] == 1 and not r["parse_ok"])
    teks = laporan_teks.format_provider(
        f"{provider_id} (ulangan {ulangan})", len(recs), ring, baris[0]["prompt_hash"], gagal1)
    info = {
        "n_klaim": len({it["claim_id"] for it in items_s}),
        "n_obs": len(items_s),
        "n_uji": ring["konsistensi"]["n_klaim"],
        "n_baris": len(rows),
        "gagal1": gagal1,
        "gagal_final": ring["n_gagal_total"],
        "provider_id": provider_id,
    }
    return {"ring": ring, "teks": teks, "info": info, "mets": metrik(ring)}


def f4(v, lo=None, hi=None):
    if v is None:
        return "-"
    if lo is None:
        return f"{v:.4f}"
    return f"{v:.4f} [{lo:.4f}; {hi:.4f}]"


def fcsv(x):
    return "" if x is None else f"{x:.6f}"


def tulis(nama, teks):
    with open(os.path.join(OUT, nama), "w", encoding="utf-8", newline="\n") as f:
        f.write(teks)


def tulis_csv(nama, header, baris):
    with open(os.path.join(OUT, nama), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(baris)


def tabel_kolom_model(hasil_m):
    """Baris metrik, kolom model. hasil_m: {model: hasil_set}."""
    lines = ["| Metrik | " + " | ".join(MODELS) + " |", "|---|" + "---|" * len(MODELS)]
    mets0 = hasil_m[MODELS[0]]["mets"]
    for idx, (nama, *_r) in enumerate(mets0):
        cells = []
        for m in MODELS:
            _n, v, lo, hi = hasil_m[m]["mets"][idx][1:]
            cells.append(f4(v, lo, hi))
        lines.append(f"| {nama} | " + " | ".join(cells) + " |")
    return lines


def baris_csv(m, nama_set, split_label, info, mets):
    out = []
    for nama, n, v, lo, hi in mets:
        out.append([m, nama_set, split_label, info["n_klaim"], info["n_obs"], nama, n,
                    f"{v:.6f}", fcsv(lo), fcsv(hi)])
    return out


HEADER_CSV = ["model", "set", "split", "n_klaim", "n_obs", "metrik", "n", "nilai", "ci_lo", "ci_hi"]


def muat_lapis36():
    hasil = {}
    with open(LAPIS36_CSV, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            lo = row["ci_lo"] or None
            hi = row["ci_hi"] or None
            nama = row["metrik"].replace("Sesuai (label R1 = R3)", "Sesuai (label R1 = label R3)")
            hasil[(row["model"], nama)] = (
                int(row["n"]), float(row["nilai"]),
                float(lo) if lo is not None else None,
                float(hi) if hi is not None else None)
    return hasil


def main():
    os.makedirs(OUT, exist_ok=True)
    pre = {p: sha256(p) for p in daftar_hash()}

    items = baca_jsonl(ITEMS)
    kunci = baca_jsonl(KUNCI)
    assert len(items) == N_OBS_TOTAL and len(kunci) == N_OBS_TOTAL, "jumlah observasi tidak 2058"
    claim_of = {it["obs_id"]: it["claim_id"] for it in items}
    assert len(claim_of) == len(items), "obs_id items tidak unik"
    split_obs = {k["obs_id"]: k["split"] for k in kunci}
    assert set(split_obs) == set(claim_of), "obs_id items dan kunci tidak sama"
    claims = sorted(set(claim_of.values()))
    assert len(claims) == N_KLAIM_TOTAL, f"jumlah klaim {len(claims)}"
    assert all(v == 7 for v in Counter(claim_of.values()).values()), "klaim tidak tepat 7 observasi"
    split_klaim = {}
    for obs, sp in split_obs.items():
        split_klaim.setdefault(claim_of[obs], set()).add(sp)
    assert all(len(v) == 1 for v in split_klaim.values()), "klaim lintas split"
    split_of = {c: next(iter(v)) for c, v in split_klaim.items()}
    hitung_split = Counter(split_of.values())
    assert dict(hitung_split) == SPLIT_KLAIM, f"split klaim {dict(hitung_split)}"
    print("validasi data: 294 klaim, 2058 obs, split", dict(hitung_split))

    daftar_a = muat_daftar(KELUAR_A)
    daftar_b = muat_daftar(KELUAR_B)
    ex_a = {c for c, j in daftar_a if j == "JANGKAR"}
    ex_b = {c for c, j in daftar_b if j == "JANGKAR"}
    assert ex_a <= set(claims) and ex_b <= set(claims), "ID daftar keluar tidak ada di pool"
    assert len(ex_a) == N_KELUAR_A and len(ex_b) == N_KELUAR_B, "jumlah daftar keluar tak sesuai"
    cek = cek_status(muat_status(), ex_a, ex_b)
    print("silang status: A sama =", cek["a_sama_status"], "| B sama =", cek["b_sama_status"])

    rows_semua = {m: [] for m in MODELS}
    for m in MODELS:
        for sp in SPLITS:
            rows_semua[m] += baca_jsonl(f"{HASIL}/{m}/nyata_{sp}_{m}_u1.jsonl")

    sets = [
        ("UTAMA-294", lambda c: True),
        ("UTAMA-274", lambda c: split_of[c] != "pilot"),
        ("KEPEKAAN-A", lambda c: c not in ex_a),
        ("KEPEKAAN-B", lambda c: c not in ex_b),
    ] + [(f"SPLIT-{sp}", (lambda s: lambda c: split_of[c] == s)(sp)) for sp in SPLITS]

    hasil = {}
    items_set = {}
    for nama, pred in sets:
        keep = {c for c in claims if pred(c)}
        items_s = [it for it in items if it["claim_id"] in keep]
        obs = {it["obs_id"] for it in items_s}
        kunci_s = [k for k in kunci if k["obs_id"] in obs]
        items_set[nama] = items_s
        for m in MODELS:
            hasil[(nama, m)] = hitung_set(m, items_s, kunci_s, rows_semua[m])
        print(f"selesai set {nama}: klaim={len(keep)} obs={len(items_s)}")

    for sp in SPLITS:
        pil = {it["obs_id"] for it in pilih_split(items, kunci, sp)}
        sub = {it["obs_id"] for it in items_set[f"SPLIT-{sp}"]}
        assert pil == sub, f"split {sp} tidak sama dengan pilih_split"

    # Replikasi: teks per split dibandingkan dengan analisis_<split>_<model>.md yang sudah ada.
    rep = []
    for m in MODELS:
        for sp in ("dev", "val", "holdout"):
            path = f"{HASIL}/{m}/analisis_{sp}_{m}.md"
            with open(path, encoding="utf-8", newline="") as f:
                ada = f.read().replace("\r\n", "\n")
            kini = laporan_teks.format_laporan([hasil[(f"SPLIT-{sp}", m)]["teks"]], nyata=True).replace("\r\n", "\n")
            identik = ada == kini
            beda = ""
            if not identik:
                a, b = ada.split("\n"), kini.split("\n")
                for i, (x, y) in enumerate(zip(a, b)):
                    if x != y:
                        beda = f"baris {i + 1}: ada='{x}' | kini='{y}'"
                        break
                else:
                    beda = f"panjang beda: ada={len(a)} kini={len(b)} baris"
            rep.append((m, sp, identik, beda))
            print(f"replikasi {m} {sp}: {'IDENTIK' if identik else 'BEDA'} {beda}")

    # Keluaran tabel utama
    def judul_set(nama):
        return {
            "UTAMA-294": "semua 294 klaim (pilot+dev+val+holdout)",
            "UTAMA-274": "274 klaim tanpa pilot (dev+val+holdout)",
            "KEPEKAAN-A": "294 dikurangi 4 JANGKAR KELUAR (Amandemen 6a)",
            "KEPEKAAN-B": "294 dikurangi 14 JANGKAR dengan suara TIDAK_LAYAK (Amandemen 6b)",
        }.get(nama, nama)

    catatan_pilot = ("Pilot adalah tahap teknis menurut praregistrasi dan tidak dilaporkan sebagai hasil. "
                     "Baris UTAMA-294 memasukkannya sesuai permintaan; UTAMA-274 adalah baris tanpa pilot.")
    konvensi = ("Nilai: rerata atau proporsi [CI 95% bootstrap klaster per article_id, B=2000, seed default]. "
                "Brier batas 2 tanpa CI. Tau = 0,7. HASIL MODEL, BELUM DIVERIFIKASI.")

    # tabel_utama294_3model
    L = ["# Utama-294: analisis utama praregistrasi (3 model API)", "",
         "Status: HASIL MODEL (BELUM DIVERIFIKASI). Hanya sah bila sesuai praregistrasi.", "",
         catatan_pilot, "", konvensi, ""]
    csv_u = []
    for nama, label in (("UTAMA-294", "semua (4 split)"), ("UTAMA-274", "dev+val+holdout")):
        h = {m: hasil[(nama, m)] for m in MODELS}
        info0 = h[MODELS[0]]["info"]
        L += [f"## {nama}: {judul_set(nama)}", "",
              f"n klaim = {info0['n_klaim']}, n observasi = {info0['n_obs']}", ""]
        L += tabel_kolom_model(h) + [""]
        for m in MODELS:
            csv_u += baris_csv(m, nama, label, h[m]["info"], h[m]["mets"])
    tulis("tabel_utama294_3model.md", "\n".join(L) + "\n")
    tulis_csv("tabel_utama294_3model.csv", HEADER_CSV, csv_u)

    # tabel_per_split
    L = ["# Per split: urutan eksploratif lalu konfirmatif (3 model API)", "",
         "Status: HASIL MODEL (BELUM DIVERIFIKASI). Pilot adalah tahap teknis menurut praregistrasi.",
         "Pilot tidak dilaporkan sebagai hasil; baris pilot hanya untuk kelengkapan.", "", konvensi, ""]
    csv_s = []
    for sp in SPLITS:
        nama = f"SPLIT-{sp}"
        h = {m: hasil[(nama, m)] for m in MODELS}
        info0 = h[MODELS[0]]["info"]
        L += [f"## Split {sp} ({info0['n_klaim']} klaim, {info0['n_obs']} observasi)", ""]
        L += tabel_kolom_model(h) + [""]
        for m in MODELS:
            csv_s += baris_csv(m, nama, sp, h[m]["info"], h[m]["mets"])
    tulis("tabel_per_split.md", "\n".join(L) + "\n")
    tulis_csv("tabel_per_split.csv", HEADER_CSV, csv_s)

    # tabel_kepekaan: 294 vs A vs B vs lapis36 (salinan)
    lap = muat_lapis36()
    L = ["# Kepekaan: 294 vs KEPEKAAN-A vs KEPEKAAN-B vs lapis36 (salinan)", "",
         "Status: HASIL MODEL (BELUM DIVERIFIKASI).",
         "Lapis36 disalin dari _lapis36/tabel_lapis36_4model.csv: 36 klaim jangkar (40 dikurangi 4 KELUAR), "
         "252 observasi, hanya split pilot+dev+val (tanpa holdout). Angka lapis36 tidak identik dengan "
         "KEPEKAAN-A karena cakupan klaim dan split berbeda.", "", konvensi, ""]
    csv_k = ["model", "metrik", "sumber", "n_klaim", "n_obs", "n", "nilai", "ci_lo", "ci_hi"]
    rows_k = []
    for m in MODELS:
        L += [f"## Model: {m}", "",
              "| Metrik | 294 (UTAMA-294) | KEPEKAAN-A | KEPEKAAN-B | lapis36 (salinan) |",
              "|---|---|---|---|---|"]
        base = hasil[("UTAMA-294", m)]["mets"]
        ka = hasil[("KEPEKAAN-A", m)]["mets"]
        kb = hasil[("KEPEKAAN-B", m)]["mets"]
        for idx, (nama, *_r) in enumerate(base):
            _n, v, lo, hi = base[idx][1:]
            _na, va, loa, hia = ka[idx][1:]
            _nb, vb, lob, hib = kb[idx][1:]
            if (m, nama) not in lap:
                raise KeyError(f"metrik lapis36 tidak ada: {m} | {nama}")
            nl, vl, lol, hil = lap[(m, nama)]
            L.append(f"| {nama} | {f4(v, lo, hi)} | {f4(va, loa, hia)} | {f4(vb, lob, hib)} | "
                     f"{f4(vl, lol, hil)} |")
            for sumber, nk, no, nn, vv, l1, h1 in (
                    ("294", 294, 2058, base[idx][1], v, lo, hi),
                    ("KEPEKAAN-A", hasil[("KEPEKAAN-A", m)]["info"]["n_klaim"],
                     hasil[("KEPEKAAN-A", m)]["info"]["n_obs"], ka[idx][1], va, loa, hia),
                    ("KEPEKAAN-B", hasil[("KEPEKAAN-B", m)]["info"]["n_klaim"],
                     hasil[("KEPEKAAN-B", m)]["info"]["n_obs"], kb[idx][1], vb, lob, hib),
                    ("lapis36", LAPIS36_N_KLAIM, LAPIS36_N_OBS, nl, vl, lol, hil)):
                rows_k.append([m, nama, sumber, nk, no, nn, f"{vv:.6f}", fcsv(l1), fcsv(h1)])
        L.append("")
    tulis("tabel_kepekaan.md", "\n".join(L) + "\n")
    tulis_csv("tabel_kepekaan.csv", csv_k, rows_k)

    # jumlah_set.md: n klaim, n obs, gagal parse, dan daftar keluar
    L = ["# Jumlah klaim, observasi, dan parse gagal per set", "",
         "| Set | Split | n klaim | n observasi | Model | n klaim uji konsistensi | n baris keluaran "
         "| parse gagal percobaan 1 | parse gagal final |",
         "|---|---|---|---|---|---|---|---|---|"]
    for nama, _p in sets:
        for m in MODELS:
            i = hasil[(nama, m)]["info"]
            label = {"UTAMA-294": "semua", "UTAMA-274": "dev+val+holdout", "KEPEKAAN-A": "semua",
                     "KEPEKAAN-B": "semua"}.get(nama, nama.replace("SPLIT-", ""))
            L.append(f"| {nama} | {label} | {i['n_klaim']} | {i['n_obs']} | {m} | {i['n_uji']} | "
                     f"{i['n_baris']} | {i['gagal1']} | {i['gagal_final']} |")
    L += ["", "## Daftar keluar yang dipakai", "",
          f"KEPEKAAN-A (ID_KELUAR.txt, JANGKAR): {len(ex_a)} klaim: " + ", ".join(sorted(ex_a)),
          "",
          f"KEPEKAAN-B (ID_KELUAR_KETAT.txt, JANGKAR dengan suara TIDAK_LAYAK): {len(ex_b)} klaim: "
          + ", ".join(sorted(ex_b)),
          "",
          "Baris UBAHAN di ID_KELUAR_KETAT.txt (C0085, C0233) tidak dikurangkan; keduanya tetap ada di "
          "pool JANGKAR dengan keputusan DIPAKAI.", "",
          f"Silang dengan status_butir.csv: A sama = {cek['a_sama_status']} "
          f"(status: {cek['n_a_status']} KELUAR); B sama = {cek['b_sama_status']} "
          f"(status: {cek['n_b_status']} JANGKAR dengan TIDAK_LAYAK).",
          f"Selisih status tanpa daftar A: {cek['status_keluar_tanpa_daftar_a']}; "
          f"tanpa daftar B: {cek['status_tl_tanpa_daftar_b']}.", ""]
    tulis("jumlah_set.md", "\n".join(L) + "\n")

    # analisis_<set>.md (teks harness per model), dan analisis_split_<split>.md
    def tulis_analisis(nama, ket, fname):
        bagian = []
        for m in MODELS:
            garis = hasil[(nama, m)]["teks"].split("\n")
            garis[0] = f"## Model: {m} | set {nama} (ulangan 1)"
            bagian.append("\n".join(garis))
        teks = laporan_teks.format_laporan(bagian, nyata=True)
        judul, sisa = teks.split("\n\n", 1)
        tulis(fname, judul + f"\n\nSet {nama}: {ket}\n\n" + sisa)

    tulis_analisis("UTAMA-294", judul_set("UTAMA-294") + ". " + catatan_pilot, "analisis_UTAMA294.md")
    tulis_analisis("UTAMA-274", judul_set("UTAMA-274"), "analisis_UTAMA274.md")
    tulis_analisis("KEPEKAAN-A", judul_set("KEPEKAAN-A"), "analisis_KEPEKAAN_A.md")
    tulis_analisis("KEPEKAAN-B", judul_set("KEPEKAAN-B"), "analisis_KEPEKAAN_B.md")
    for sp in SPLITS:
        tulis_analisis(f"SPLIT-{sp}", f"split {sp}" + (" (teknis menurut praregistrasi, bukan hasil)" if sp == "pilot" else ""),
                       f"analisis_split_{sp}.md")

    # replikasi_cek.md
    L = ["# Validasi replikasi: teks per split dibandingkan dengan analisis_<split>_<model>.md yang ada", "",
         "| Model | Split | Hasil | Keterangan |", "|---|---|---|---|"]
    for m, sp, identik, beda in rep:
        L.append(f"| {m} | {sp} | {'IDENTIK' if identik else 'BEDA'} | {beda or '-'} |")
    L += ["| (semua model) | pilot | tidak ada pembanding | berkas analisis_pilot tidak ada di HASIL_PENGUJIAN |",
          ""]
    tulis("replikasi_cek.md", "\n".join(L) + "\n")

    # hash_cek.md
    post = {p: sha256(p) for p in pre}
    L = ["# Cek hash berkas input (sebelum dan sesudah skrip)", "", "| Berkas | Sebelum | Sesudah | Sama |",
         "|---|---|---|---|"]
    semua_sama = True
    for p in sorted(pre):
        sama = pre[p] == post[p]
        semua_sama = semua_sama and sama
        L.append(f"| {p} | {pre[p]} | {post[p]} | {'ya' if sama else 'TIDAK'} |")
    L += ["", f"Jumlah berkas: {len(pre)}. Semua identik: {'ya' if semua_sama else 'TIDAK'}.", ""]
    tulis("hash_cek.md", "\n".join(L) + "\n")

    print("hash:", len(pre), "berkas; semua identik =", semua_sama)
    print("replikasi:", sum(1 for r in rep if r[2]), "dari", len(rep), "identik")
    print("selesai")


if __name__ == "__main__":
    main()
