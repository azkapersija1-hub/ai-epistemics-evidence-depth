"""Lapis 36 (40 klaim jangkar dikurangi C0056, C0295, C0057, C0225): hitung ulang empat model.

Memakai modul harness yang sama dengan Agen A (tabel_perbandingan_lapis) dan Agen C (tabel_codex_lapis):
ak.analisis(), laporan.muat_keluaran_final(), laporan.bangun_records(), laporan.ringkas(),
laporan_teks.format_laporan(). Tau 0,7; bootstrap B=2000 dengan seed default harness.

Tidak memanggil model apa pun. Berkas yang sudah ada tidak ditimpa: items dan kunci lapis 36 ditulis
dengan mode 'x'; bila sudah ada, isinya hanya dicocokkan. Kunci dibaca untuk evaluasi saja, isinya
tidak dicetak. Validasi replikasi dilakukan pada lapis 40, 26, dan 19 terhadap CSV Agen A dan Agen C.

Pemakaian (dari folder HASIL_PENGUJIAN/_lapis36, dengan -B agar tidak menulis __pycache__):
  py -3.12 -B -I -X utf8 skrip_analisis_lapis36.py
"""
import csv
import os
import sys

P = "C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP"
H = P + "/harness"
OUT = P + "/HASIL_PENGUJIAN/_lapis36"
CODEX = P + "/HASIL_PENGUJIAN/gpt61_codex"
ITEMS_SUMBER = P + "/bahan/v2/hasil_olahan_3penilai/lapis_data"
KUNCI_SUMBER = P + "/bahan/v2/RAHASIA/lapis_data"
ITEMS_36 = P + "/bahan/v2/hasil_olahan_final/lapis_data/items_lapis_36.jsonl"
KUNCI_36 = P + "/bahan/v2/RAHASIA/lapis_data/kunci_lapis_36.jsonl"
DAFTAR_36 = P + "/bahan/v2/hasil_olahan_final/lapis_36_claim_id.txt"
REF_AGEN_A = P + "/HASIL_PENGUJIAN/_perbandingan_lapis/tabel_perbandingan_lapis.csv"
REF_AGEN_C = CODEX + "/tabel_codex_lapis.csv"

TAU = 0.7
TOL = 1e-5
N_KLAIM_36 = 36
N_OBS_36 = 252
API = ("qwen3.8-flash", "qwen4-max-preview", "deepseek-v4.1-flash")
CODEX_ID = "codex_gpt61_sol_tak_terverifikasi"
MODELS = API + (CODEX_ID,)
NAMA = {
    "qwen3.8-flash": "qwen3.8-flash",
    "qwen4-max-preview": "qwen4-max-preview",
    "deepseek-v4.1-flash": "deepseek-v4.1-flash",
    CODEX_ID: "codex (gpt-6.1-sol, tak terverifikasi)",
}
PAIRS_SKOR = (("own", "R3"), ("near", "R1"), ("near", "R3"), ("far", "R1"), ("far", "R3"))
LAPIS_TABEL = (40, 36, 26, 19)

sys.path.insert(0, H)
from epis import laporan, laporan_teks  # noqa: E402
from epis.jsonl_io import baca_jsonl, tulis_jsonl  # noqa: E402
import analisis_keluaran as ak  # noqa: E402

B = laporan.B_CI


def tulis(nama, teks):
    with open(os.path.join(OUT, nama), "w", encoding="utf-8", newline="\n") as f:
        f.write(teks)


def bangun_items_kunci_36():
    """Saring items dan kunci lapis 40 ke 36 klaim. Kunci tidak dicetak."""
    with open(DAFTAR_36, encoding="utf-8-sig") as f:
        ids = [b.strip() for b in f if b.strip()]
    assert len(ids) == N_KLAIM_36 and len(set(ids)) == N_KLAIM_36, "daftar lapis 36 tidak tepat 36"
    daftar = set(ids)
    items40 = baca_jsonl(ITEMS_SUMBER + "/items_lapis_40.jsonl")
    kunci40 = baca_jsonl(KUNCI_SUMBER + "/kunci_lapis_40.jsonl")
    items = [it for it in items40 if it["claim_id"] in daftar]
    obs = {it["obs_id"] for it in items}
    kunci = [k for k in kunci40 if k["obs_id"] in obs]
    assert len(items) == N_OBS_36 and len(kunci) == N_OBS_36, "jumlah observasi lapis 36 tidak 252"
    assert {it["claim_id"] for it in items} == daftar, "klaim items tidak sama dengan daftar"
    assert {k["obs_id"] for k in kunci} == obs, "kunci tidak sama dengan items"
    assert {k["split"] for k in kunci} <= {"pilot", "dev", "val"}, "split tak terduga"
    return items, kunci


def tulis_atau_cocokkan(path, rows):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tulis_jsonl(path, rows)  # mode 'x': menolak menimpa
        return "ditulis baru"
    if baca_jsonl(path) != rows:
        raise RuntimeError(f"berkas sudah ada tetapi isinya berbeda: {path}")
    return "sudah ada, identik"


def muat_baris(model, ids, lap_codex):
    """Baris keluaran untuk observasi di ids. API: pilot+dev+val. Codex: impor sesi 40 pilot+dev."""
    rows = []
    if model == CODEX_ID:
        for sp in ("pilot", "dev"):
            rows += baca_jsonl(f"{CODEX}/impor_sesi40_lapis{lap_codex}_{sp}.jsonl")
    else:
        for sp in ("pilot", "dev", "val"):
            rows += baca_jsonl(f"{P}/HASIL_PENGUJIAN/{model}/nyata_{sp}_{model}_u1.jsonl")
    return [r for r in rows if r["obs_id"] in ids]


def hitung(model, items, kunci, lap_codex):
    ids = {it["obs_id"] for it in items}
    rows = muat_baris(model, ids, lap_codex)
    bagian, _nyata = ak.analisis(rows, items, kunci, TAU, B)
    final = laporan.muat_keluaran_final(rows)
    recs = laporan.bangun_records(items, kunci, final)
    ring = laporan.ringkas(recs, tau=TAU, b=B)
    info = {
        "n_klaim_items": len({it["claim_id"] for it in items}),
        "n_obs": len(items),
        "n_uji": ring["konsistensi"]["n_klaim"],
        "n_baris": len(rows),
        "gagal1": sum(1 for r in rows if r["percobaan"] == 1 and not r["parse_ok"]),
        "gagal_final": ring["n_gagal_total"],
    }
    return {"ring": ring, "info": info, "bagian": bagian}


def metrik(ring):
    """Daftar (nama, n, nilai, lo, hi), urutan dan nama sama dengan tabel Agen A dan Agen C."""
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
    for nama, kunci in (("Sesuai (label R1 = R3)", "sesuai"), ("Pergeseran dS", "dS"),
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


def f4(v, lo=None, hi=None):
    if v is None:
        return "-"
    if lo is None:
        return f"{v:.4f}"
    return f"{v:.4f} [{lo:.4f}; {hi:.4f}]"


def baca_referensi(path):
    """{(model, lapis, nama): (n, nilai, lo, hi)} dari CSV Agen A atau Agen C (6 desimal)."""
    hasil = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if not row or row[0] == "model":
                continue
            n, nilai, lo, hi, _sel = row[-5:]
            nama = ",".join(row[2:-5])
            hasil[(row[0], int(row[1]), nama)] = (
                int(n) if n != "" else None,  # CSV Agen A mengosongkan n pada baris "Selisih FS"
                float(nilai),
                float(lo) if lo != "" else None,
                float(hi) if hi != "" else None)
    return hasil


def validasi(hasil, ref, lap, model):
    mets = metrik(hasil[lap][model]["ring"])
    beda, tanpa, selisih_maks = [], [], 0.0
    for nama, n, v, lo, hi in mets:
        kunci = (model, lap, nama)
        if kunci not in ref:
            tanpa.append(nama)
            continue
        rn, rv, rlo, rhi = ref[kunci]
        if rn is not None and n != rn:
            beda.append(f"{nama}: n {n} vs {rn}")
        selisih_maks = max(selisih_maks, abs(v - rv))
        if (lo is None) != (rlo is None):
            beda.append(f"{nama}: ada atau tidak adanya CI berbeda")
        elif lo is not None:
            selisih_maks = max(selisih_maks, abs(lo - rlo), abs(hi - rhi))
    return {"n_metrik": len(mets), "tanpa_ref": tanpa, "beda": beda, "selisih_maks": selisih_maks}


def tabel_lapis36(hasil):
    m36 = {m: metrik(hasil[36][m]["ring"]) for m in MODELS}
    m40 = {m: metrik(hasil[40][m]["ring"]) for m in MODELS}
    L = [
        "# Lapis 36: skor empat model (HASIL MODEL, BELUM DIVERIFIKASI)", "",
        "Status: HASIL MODEL (BELUM DIVERIFIKASI). Lapis 36 = 40 klaim jangkar dikurangi C0056, C0295, "
        "C0057, C0225 (keputusan perundingan tim). Daftar: bahan/v2/hasil_olahan_final/lapis_36_claim_id.txt.",
        "Sumber: items_lapis_36.jsonl dan kunci_lapis_36.jsonl (turunan dari items dan kunci lapis 40). "
        "API: keluaran nyata pilot, dev, dan val. Codex: impor sesi 40 pilot dan dev.",
        "Codex: klaim C0230 dilewati (SKIP) di 7 observasi. Perlakuannya sama seperti Agen C: "
        "batas 1 mengeluarkannya, batas 2 memberinya 2,0, dan klaim itu tidak masuk uji konsistensi.",
        "Nilai: rerata atau proporsi [CI 95% bootstrap klaster per article_id, B=2000, seed default]. "
        "Brier batas 2 tanpa CI. Tau = 0,7.", "",
        "## Jumlah klaim dan observasi", "",
        "| Model | n klaim (items) | n observasi | n klaim uji konsistensi (R1 & R3 valid) "
        "| n baris keluaran | parse gagal percobaan 1 | parse gagal final |",
        "|---|---|---|---|---|---|---|",
    ]
    for m in MODELS:
        i = hasil[36][m]["info"]
        L.append(f"| {NAMA[m]} | {i['n_klaim_items']} | {i['n_obs']} | {i['n_uji']} | {i['n_baris']} | "
                 f"{i['gagal1']} | {i['gagal_final']} |")
    L += ["", "## Skor per metrik (nilai [CI 95%])", "",
          "| Metrik | " + " | ".join(NAMA[m] for m in MODELS) + " |",
          "|---|" + "---|" * len(MODELS)]
    for idx, (nama, *_r) in enumerate(m36[MODELS[0]]):
        cells = [f4(m36[m][idx][2], m36[m][idx][3], m36[m][idx][4]) for m in MODELS]
        L.append(f"| {nama} | " + " | ".join(cells) + " |")
    L.append("")
    tulis("tabel_lapis36_4model.md", "\n".join(L))

    C = ["model,lapis,metrik,n,nilai,ci_lo,ci_hi,selisih_vs_lapis40"]
    for m in MODELS:
        for idx, (nama, n, v, lo, hi) in enumerate(m36[m]):
            lo_s = "" if lo is None else f"{lo:.6f}"
            hi_s = "" if hi is None else f"{hi:.6f}"
            sel = f"{v - m40[m][idx][2]:.6f}"
            C.append(f"{m},36,\"{nama}\",{n},{v:.6f},{lo_s},{hi_s},{sel}")
    tulis("tabel_lapis36_4model.csv", "\n".join(C) + "\n")


def tabel_pembanding(hasil):
    L = [
        "# Pembanding lapis 40, 36, 26, 19 per model (nilai titik saja)", "",
        "Status: HASIL MODEL (BELUM DIVERIFIKASI). Nilai titik saja. Skrip tidak memberi CI untuk selisih "
        "antar lapis karena lapis bersarang (36 subset 40, 26 dan 19 subset 40).",
        "Lapis 40, 26, dan 19 dihitung dengan skrip yang sama dan sudah dicocokkan dengan tabel Agen A dan Agen C.", "",
        "| Model | Metrik | Lapis 40 | Lapis 36 | Lapis 26 | Lapis 19 |",
        "|---|---|---|---|---|---|",
    ]
    C = ["model,metrik,nilai_lapis40,nilai_lapis36,nilai_lapis26,nilai_lapis19"]
    for m in MODELS:
        mets = {lap: metrik(hasil[lap][m]["ring"]) for lap in LAPIS_TABEL}
        for idx, (nama, *_r) in enumerate(mets[40]):
            vals = [mets[lap][idx][2] for lap in LAPIS_TABEL]
            L.append(f"| {NAMA[m]} | {nama} | " + " | ".join(f"{v:.4f}" for v in vals) + " |")
            C.append(f"{m},\"{nama}\"," + ",".join(f"{v:.6f}" for v in vals))
    L.append("")
    tulis("tabel_pembanding_lapis_40_36_26_19.md", "\n".join(L))
    tulis("tabel_pembanding_lapis_40_36_26_19.csv", "\n".join(C) + "\n")


def tulis_analisis(hasil):
    bagian = []
    for m in MODELS:
        for teks in hasil[36][m]["bagian"]:
            garis = teks.split("\n")
            garis[0] = f"## Model: {NAMA[m]} (ulangan 1)"
            bagian.append("\n".join(garis))
    tulis("analisis_lapis36.md", laporan_teks.format_laporan(bagian, nyata=True))


def main():
    os.makedirs(OUT, exist_ok=True)
    items36, kunci36 = bangun_items_kunci_36()
    print("items_lapis_36:", tulis_atau_cocokkan(ITEMS_36, items36))
    print("kunci_lapis_36:", tulis_atau_cocokkan(KUNCI_36, kunci36))

    items = {36: baca_jsonl(ITEMS_36), 40: None, 26: None, 19: None}
    kunci = {36: baca_jsonl(KUNCI_36), 40: None, 26: None, 19: None}
    for lap in (40, 26, 19):
        items[lap] = baca_jsonl(f"{ITEMS_SUMBER}/items_lapis_{lap}.jsonl")
        kunci[lap] = baca_jsonl(f"{KUNCI_SUMBER}/kunci_lapis_{lap}.jsonl")

    hasil = {}
    for lap in LAPIS_TABEL:
        lap_codex = 40 if lap in (40, 36) else lap
        hasil[lap] = {m: hitung(m, items[lap], kunci[lap], lap_codex) for m in MODELS}
        for m in MODELS:
            i = hasil[lap][m]["info"]
            print(f"lapis {lap} | {NAMA[m]}: klaim={i['n_klaim_items']} obs={i['n_obs']} uji={i['n_uji']} "
                  f"baris={i['n_baris']} gagal1={i['gagal1']} gagal_final={i['gagal_final']}")

    ref = {}
    ref.update(baca_referensi(REF_AGEN_A))
    ref.update(baca_referensi(REF_AGEN_C))
    gagal_40 = []
    for lap in (40, 26, 19):
        for m in MODELS:
            v = validasi(hasil, ref, lap, m)
            cocok = (v["selisih_maks"] <= TOL and not v["beda"] and not v["tanpa_ref"])
            print(f"VALIDASI lapis {lap} | {NAMA[m]}: metrik={v['n_metrik']} "
                  f"tanpa_ref={len(v['tanpa_ref'])} beda={len(v['beda'])} "
                  f"selisih_maks={v['selisih_maks']:.3e} {'COCOK' if cocok else 'TIDAK COCOK'}")
            for b in v["beda"]:
                print("   beda:", b)
            if lap == 40 and not cocok:
                gagal_40.append(f"{lap}|{m}")
    if gagal_40:
        print("VALIDASI LAPIS 40 GAGAL:", gagal_40, "; tabel lapis 36 tidak ditulis.")
        sys.exit(1)

    tulis_analisis(hasil)
    tabel_lapis36(hasil)
    tabel_pembanding(hasil)
    print("selesai")


if __name__ == "__main__":
    main()
