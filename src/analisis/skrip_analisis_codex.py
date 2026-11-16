"""Analisis Codex (gpt-6.1-sol, tak terverifikasi) memakai modul harness yang sama.

Dijalankan SETELAH impor_luar.py (berkas impor_*.jsonl sudah ada). Tidak memanggil model.
Tidak mencetak isi kunci; hanya agregat. Tau = 0,7; bootstrap B = 2000 dengan seed tetap
(default epis.stats).

Pemakaian (dari folder harness, dengan -B agar tidak menulis __pycache__):
  py -3.12 -B -I -X utf8 ..\\HASIL_PENGUJIAN\\gpt61_codex\\skrip_analisis_codex.py
"""
import hashlib
import os
import sys

H = "C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP/harness"
P = "C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP"
OUT = P + "/HASIL_PENGUJIAN/gpt61_codex"
AGEN_A = P + "/HASIL_PENGUJIAN/_perbandingan_lapis/tabel_perbandingan_lapis.md"
LAP = P + "/bahan/v2/hasil_olahan_3penilai/lapis_data"
KUN = P + "/bahan/v2/RAHASIA/lapis_data"
TAU = 0.7
MODEL_KOL = "codex (gpt-6.1-sol, tak terverifikasi)"
PAIRS_SKOR = [("own", "R3"), ("near", "R1"), ("near", "R3"), ("far", "R1"), ("far", "R3")]

sys.path.insert(0, H)
from epis import laporan, laporan_teks, skor, stats  # noqa: E402
from epis.jsonl_io import baca_jsonl  # noqa: E402
from epis.subset import pilih_split  # noqa: E402
import analisis_keluaran as ak  # noqa: E402

B = laporan.B_CI


def rd(p):
    return baca_jsonl(p)


def tulis(nama, teks):
    with open(os.path.join(OUT, nama), "w", encoding="utf-8", newline="\n") as f:
        f.write(teks)


def muat_impor(prefix, lap):
    rows = []
    for sp in ("pilot", "dev"):
        rows += rd(f"{OUT}/{prefix}_lapis{lap}_{sp}.jsonl")
    return rows


def items_gabungan(lap):
    items = rd(f"{LAP}/items_lapis_{lap}.jsonl")
    kunci = rd(f"{KUN}/kunci_lapis_{lap}.jsonl")
    gab = pilih_split(items, kunci, "pilot") + pilih_split(items, kunci, "dev")
    assert len(gab) == len(items), "items tidak semua di pilot/dev"
    return items, kunci, gab


def f4(v, lo=None, hi=None):
    if v is None:
        return "-"
    if lo is None:
        return f"{v:.4f}"
    return f"{v:.4f} [{lo:.4f}; {hi:.4f}]"


def metrik(ring):
    """Daftar (nama, n, nilai, lo, hi) dengan urutan dan nama SAMA seperti tabel Agen A."""
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
    for nama, kunci in [("Sesuai (label R1 = R3)", "sesuai"), ("Pergeseran dS", "dS"),
                        ("Pergeseran dN", "dN"), ("Overkomit (tau 0,7)", "overkomit")]:
        c = k[kunci]
        out.append((nama, c["n"], c["rerata"], c["lo"], c["hi"]))
    fs = k["false_support"]
    for rung in ("R1", "R3"):
        near, far, sel = fs[rung]["near"], fs[rung]["far"], fs[rung]["selisih"]
        out.append((f"False-support near {rung}", near["n"], near["rerata"], near["lo"], near["hi"]))
        out.append((f"False-support far {rung}", far["n"], far["rerata"], far["lo"], far["hi"]))
        out.append((f"Selisih FS near-far {rung}", near["n"], sel["rerata"], sel["lo"], sel["hi"]))
    return out


def analisis_lapis(lap):
    items, kunci, gab = items_gabungan(lap)
    rows = muat_impor("impor_sesi40", lap)
    bagian, nyata = ak.analisis(rows, gab, kunci, TAU, B)
    tulis(f"analisis_lapis_{lap}.md", laporan_teks.format_laporan(bagian, nyata=nyata))
    final = laporan.muat_keluaran_final(rows)
    recs = laporan.bangun_records(gab, kunci, final)
    ring = laporan.ringkas(recs, tau=TAU, b=B)
    info = {
        "n_klaim_items": len({i["claim_id"] for i in gab}),
        "n_obs": len(gab),
        "n_uji": ring["konsistensi"]["n_klaim"],
        "n_baris": len(rows),
        "gagal1": sum(1 for r in rows if r["percobaan"] == 1 and not r["parse_ok"]),
        "gagal_final": ring["n_gagal_total"],
        "skip_ids": sorted({r["obs_id"] for r in rows if not r["parse_ok"]}),
        "claim_kecuali": sorted({i["claim_id"] for i in gab if i["obs_id"] in set(
            r["obs_id"] for r in rows if not r["parse_ok"])}),
    }
    return ring, info


def tabel_codex(hasil):
    lapis = (40, 26, 19)
    ms = {lap: metrik(hasil[lap][0]) for lap in lapis}
    L = ["# Codex (gpt-6.1-sol, tak terverifikasi): skor per lapis", "",
         "Status: HASIL MODEL (BELUM DIVERIFIKASI). Versi model tidak terverifikasi.",
         "Sumber: sesi 40 klaim (hasil_40.jsonl), pilot + dev. Lapis 19 dan 26 = irisan klaim dari sesi 40, "
         "BUKAN sesi 19 (sesi 19 hanya untuk kestabilan, lihat KESTABILAN_codex.md).",
         "Nilai: rerata atau proporsi [CI 95% bootstrap klaster per article_id, B=2000, seed tetap]. "
         "Brier batas 2 tidak punya CI. Selisih terhadap lapis 40 hanya angka titik.",
         "Observasi SKIP (C0230, 7 baris) diimpor sebagai gagal parse (tanpa nilai pengganti): "
         "batas 1 mengeluarkannya, batas 2 memberinya 2,0, dan klaim C0230 tidak masuk uji konsistensi "
         "(n klaim uji = 39 pada lapis 40).", "",
         "## Jumlah klaim dan observasi", "",
         "| Lapis | n klaim (items) | n observasi | n klaim uji konsistensi (R1 & R3 valid) | n baris keluaran (pilot+dev) | parse gagal percobaan 1 | parse gagal final |",
         "|---|---|---|---|---|---|---|"]
    for lap in lapis:
        i = hasil[lap][1]
        L.append(f"| {lap} | {i['n_klaim_items']} | {i['n_obs']} | {i['n_uji']} | {i['n_baris']} | "
                 f"{i['gagal1']} | {i['gagal_final']} |")
    L += ["", "## Skor per metrik (nilai [CI 95%])", "",
          "| Metrik | codex L40 | codex L26 | codex L19 |", "|---|---|---|---|"]
    for idx, (nama, *_rest) in enumerate(ms[40]):
        sel = []
        for lap in lapis:
            _, n, v, lo, hi = ms[lap][idx]
            sel.append(f4(v, lo, hi))
        L.append(f"| {nama} | " + " | ".join(sel) + " |")
    L += ["", "## Selisih titik terhadap lapis 40 (lapis minus 40)", "",
          "| Metrik | codex L26-40 | codex L19-40 |", "|---|---|---|"]
    for idx, (nama, *_rest) in enumerate(ms[40]):
        v40 = ms[40][idx][2]
        d26 = ms[26][idx][2] - v40
        d19 = ms[19][idx][2] - v40
        L.append(f"| {nama} | {d26:+.4f} | {d19:+.4f} |")
    L.append("")
    tulis("tabel_codex_lapis.md", "\n".join(L))

    C = ["model,lapis,metrik,n,nilai,ci_lo,ci_hi,selisih_vs_lapis40"]
    for lap in lapis:
        for idx, (nama, n, v, lo, hi) in enumerate(ms[lap]):
            if lap == 40:
                sel = "0 (acuan)"
            else:
                sel = f"{v - ms[40][idx][2]:.6f}"
            lo_s = "" if lo is None else f"{lo:.6f}"
            hi_s = "" if hi is None else f"{hi:.6f}"
            C.append(f"codex_gpt61_sol_tak_terverifikasi,{lap},\"{nama}\",{n},{v:.6f},{lo_s},{hi_s},{sel}")
    tulis("tabel_codex_lapis.csv", "\n".join(C) + "\n")
    return ms


def ambil_tabel(teks, judul):
    baris = []
    mulai = False
    for ln in teks.splitlines():
        if not mulai:
            if ln.startswith(judul):
                mulai = True
            continue
        if ln.startswith("|"):
            baris.append([c.strip() for c in ln.strip().strip("|").split("|")])
        elif baris:
            break
    return baris


def tabel_gabungan(ms, hasil):
    teks = open(AGEN_A, encoding="utf-8").read()
    jumlah = ambil_tabel(teks, "## Jumlah klaim dan observasi")
    skor_t = ambil_tabel(teks, "## Skor per metrik")
    hdr_skor = skor_t[0]
    agen_model = ["qwen3.8-flash", "qwen4-max-preview", "deepseek-v4.1-flash"]
    kolom = {c: i for i, c in enumerate(hdr_skor)}
    G = ["# Tabel gabungan empat model per lapis", "",
         "Status: HASIL MODEL (BELUM DIVERIFIKASI). Tiga model pertama disalin dari "
         "HASIL_PENGUJIAN/_perbandingan_lapis/tabel_perbandingan_lapis.md tanpa perubahan angka. "
         "Kolom codex dari tabel_codex_lapis.md (gpt-6.1-sol, versi tidak terverifikasi).",
         "Nilai: [CI 95% bootstrap klaster per article_id]; Brier batas 2 tanpa CI.", ""]
    for lap in (40, 19):
        G += [f"## Lapis {lap}", "",
              "| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash | codex (gpt-6.1-sol, tak terverifikasi) |",
              "|---|---|---|---|---|"]
        # jumlah: kolom 2..7 pada tabel Agen A
        nama_j = ["n klaim (items)", "n observasi", "n klaim uji konsistensi (R1 & R3 valid)",
                  "n baris keluaran (pilot+dev+val)", "parse gagal percobaan 1", "parse gagal final"]
        info = hasil[lap][1]
        kodex_j = [info["n_klaim_items"], info["n_obs"], info["n_uji"], info["n_baris"],
                   info["gagal1"], info["gagal_final"]]
        for k_i, nama in enumerate(nama_j):
            cells = []
            for m in agen_model:
                row = next(r for r in jumlah[2:] if r[0] == m and r[1] == str(lap))
                cells.append(row[2 + k_i])
            G.append(f"| {nama} | " + " | ".join(cells) + f" | {kodex_j[k_i]} |")
        # skor: nama dari tabel Agen A (indeks kolom 'MODEL LAP')
        for nama, n, v, lo, hi in ms[lap]:
            cells = []
            for m in agen_model:
                cells.append(skor_t[next(i for i, r in enumerate(skor_t) if r and r[0] == nama)][kolom[f"{m} L{lap}"]])
            G.append(f"| {nama} | " + " | ".join(cells) + f" | {f4(v, lo, hi)} |")
        G.append("")
    tulis("tabel_gabungan_4model.md", "\n".join(G))


def stabilitas():
    items, kunci, gab = items_gabungan(19)
    obs = {i["obs_id"]: i for i in gab}
    kmap = {k["obs_id"]: k for k in kunci}
    s40 = {r["obs_id"]: r for r in muat_impor("impor_sesi40", 19)}
    s19 = {r["obs_id"]: r for r in muat_impor("impor_sesi19", 19)}
    assert set(s40) == set(obs) and set(s19) == set(obs), "obs_id sesi tidak sama dengan lapis 19"
    valid, gagal = [], []
    for oid in sorted(obs):
        a, b = s40[oid], s19[oid]
        if not (a["parse_ok"] and b["parse_ok"]):
            gagal.append((oid, bool(a["parse_ok"]), bool(b["parse_ok"])))
            continue
        k = kmap[oid]
        lab = k["label"]
        valid.append({
            "oid": oid, "rung": obs[oid]["rung"], "claim": obs[oid]["claim_id"], "art": k["article_id"],
            "sama": 1.0 if skor.label_terpilih(a["p"]) == skor.label_terpilih(b["p"]) else 0.0,
            "dps": abs(b["p"]["SUPPORTED"] - a["p"]["SUPPORTED"]),
            "db": (skor.brier_multikelas(b["p"], lab) - skor.brier_multikelas(a["p"], lab))
            if lab is not None else None,
        })
    ringkas = []
    for tingkat in ("R1", "R2", "R3", "semua"):
        rs = valid if tingkat == "semua" else [r for r in valid if r["rung"] == tingkat]
        ringkas.append(ringkas_tingkat(tingkat, rs))
    tulis_stabilitas(ringkas, gagal, len(obs))


def ringkas_tingkat(tingkat, rs):
    n = len(rs)
    ci_sama = stats.bootstrap_klaster([r["sama"] for r in rs], [r["art"] for r in rs], b=B)
    ci_dps = stats.bootstrap_klaster([r["dps"] for r in rs], [r["art"] for r in rs], b=B)
    lab = [r for r in rs if r["db"] is not None]
    out = {"tingkat": tingkat, "n": n, "sama": ci_sama, "dps": ci_dps, "n_lab": len(lab),
           "db": None, "klaim": None}
    if lab:
        out["db"] = stats.bootstrap_klaster([r["db"] for r in lab], [r["art"] for r in lab], b=B)
        per = {}
        for r in lab:
            per.setdefault(r["claim"], []).append(r["db"])
        rata = {c: sum(v) / len(v) for c, v in per.items()}
        nilai = list(rata.values())
        out["klaim"] = {
            "n": len(nilai), "rerata": sum(nilai) / len(nilai), "min": min(nilai), "max": max(nilai),
            "pos": sum(1 for x in nilai if x > 0), "neg": sum(1 for x in nilai if x < 0),
        }
    return out


def tulis_stabilitas(ringkas, gagal, n_obs):
    M = ["# Kestabilan Codex: sesi 40 vs sesi 19 (19 klaim lapis 19)", "",
         "Status: HASIL MODEL (BELUM DIVERIFIKASI). Sesi 19 adalah putaran uji ulang kestabilan, "
         "BUKAN penambah data hasil utama. Keduanya memakai provider dan model_id yang sama; "
         "perbandingan per observasi lewat obs_id.",
         f"Observasi lapis 19: {n_obs}. Pasangan yang valid di kedua sesi dipakai; "
         f"pasangan yang gagal (SKIP/gagal parse) dicatat di bawah dan TIDAK dibuang diam-diam.",
         f"Observasi dengan SKIP/gagal parse di salah satu sesi: {len(gagal)}"
         + (" (" + ", ".join(f"{o}: sesi40={a}, sesi19={b}" for o, a, b in gagal) + ")" if gagal else "")
         + ".",
         "Argmax = label terpilih (aturan seri NEI menang). Selisih Brier = BS(sesi 19) - BS(sesi 40), "
         "hanya observasi berlabel; per klaim = rerata selisih di atas observasi berlabel klaim itu "
         "pada tingkat tersebut (tingkat semua = seluruh tingkat). R2 tidak berlabel, jadi Brier tidak dihitung.",
         "CI: bootstrap klaster per article_id, B=2000, seed tetap.", "",
         "| Tingkat bukti | n obs (kedua sesi valid) | Argmax sama (%) [CI] | Rerata abs selisih p(SUPPORTED) [CI] "
         "| n obs berlabel | Selisih Brier per obs [CI] | n klaim berlabel | Rerata selisih Brier per klaim "
         "| Min | Max | Klaim selisih > 0 | Klaim selisih < 0 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    C = ["tingkat,metrik,n,nilai,ci_lo,ci_hi"]
    for r in ringkas:
        s = r["sama"]
        d = r["dps"]
        pct = f"{100 * s['rerata']:.1f}% [{100 * s['lo']:.1f}; {100 * s['hi']:.1f}]"
        dps = f4(d["rerata"], d["lo"], d["hi"])
        if r["db"]:
            db = f4(r["db"]["rerata"], r["db"]["lo"], r["db"]["hi"])
            k = r["klaim"]
            kl = (str(k["n"]), f"{k['rerata']:+.4f}", f"{k['min']:+.4f}", f"{k['max']:+.4f}",
                  str(k["pos"]), str(k["neg"]))
        else:
            db, kl = "-", ("-", "-", "-", "-", "-", "-")
        M.append(f"| {r['tingkat']} | {r['n']} | {pct} | {dps} | {r['n_lab']} | {db} | " + " | ".join(kl) + " |")
        C.append(f"{r['tingkat']},n_obs_valid,{r['n']},{r['n']},,")
        C.append(f"{r['tingkat']},argmax_sama_proporsi,{r['n']},{s['rerata']:.6f},{s['lo']:.6f},{s['hi']:.6f}")
        C.append(f"{r['tingkat']},abs_selisih_pSUPPORTED_rerata,{r['n']},{d['rerata']:.6f},{d['lo']:.6f},{d['hi']:.6f}")
        if r["db"]:
            C.append(f"{r['tingkat']},selisih_brier_per_obs_berlabel,{r['n_lab']},{r['db']['rerata']:.6f},{r['db']['lo']:.6f},{r['db']['hi']:.6f}")
            C.append(f"{r['tingkat']},selisih_brier_per_klaim_rerata,{r['klaim']['n']},{r['klaim']['rerata']:.6f},,")
    M.append("")
    tulis("KESTABILAN_codex.md", "\n".join(M))
    tulis("KESTABILAN_codex.csv", "\n".join(C) + "\n")


def main():
    hasil = {}
    for lap in (40, 26, 19):
        hasil[lap] = analisis_lapis(lap)
    ms = tabel_codex(hasil)
    tabel_gabungan(ms, hasil)
    stabilitas()
    for lap in (40, 26, 19):
        info = hasil[lap][1]
        print(f"lapis {lap}: {info}")
    print("selesai")


if __name__ == "__main__":
    main()
