"""Hitung hasil penilaian kelayakan butir oleh tim penulis (Amandemen 5 dan 6, PREREG_DIBEKUKAN.md).

Pustaka standar saja. Hanya MEMBACA folder masukan; keluaran ditulis ke folder --keluar.
Galat yang merusak integritas (id tak dikenal, nilai tak sah, baris ganda, diskusi.csv tak valid,
folder keluar di dalam masukan) menghentikan penulisan keluaran (exit 2). Catatan yang hilang
TIDAK menghentikan: suara tetap dihitung dan butir ditandai CATATAN_HILANG.

Aturan keputusan per butir (kunci claim_id + jenis JANGKAR/UBAHAN):
  - 0 penilai                     -> BELUM_DINILAI (bukan suara)
  - 1 penilai                     -> SEMENTARA; keputusan = suara itu
  - 2 penilai, sama               -> SEMENTARA; keputusan = suara itu
  - 2 penilai, beda               -> PERLU_PENILAI_KETIGA; keputusan kosong
  - 3 penilai, >=2 sama           -> FINAL; LAYAK->DIPAKAI, PERLU_REVISI->DIREVISI, TIDAK_LAYAK->KELUAR
  - 3 penilai, 3 beda             -> PERLU_DISKUSI; keputusan kosong (tidak masuk ID_KELUAR)
  - diskusi.csv memuat butir      -> status DISKUSI; keputusan = keputusan_final dari diskusi.csv
Keluaran daftar KELUAR:
  - ID_KELUAR.txt           : FINAL KELUAR atau DISKUSI KELUAR (JANGKAR dan UBAHAN dipisah)
  - ID_KELUAR_SEMENTARA.txt : SEMENTARA KELUAR (hanya pratinjau)
  - ID_KELUAR_KETAT.txt     : semua butir dengan >=1 suara TIDAK_LAYAK (JANGKAR dan UBAHAN dipisah)
"""
import argparse
import csv
import glob
import hashlib
import os
import sys
from collections import Counter

KEP = ("LAYAK", "PERLU_REVISI", "TIDAK_LAYAK")
KEP_FINAL = ("DIPAKAI", "DIREVISI", "KELUAR")
STATUS_DARI = {"LAYAK": "DIPAKAI", "PERLU_REVISI": "DIREVISI", "TIDAK_LAYAK": "KELUAR"}
BAG2 = ("YA_MEMBAHAS", "TIDAK_MEMBAHAS", "RAGU")
ALASAN_REVISI = ("AMBIGU", "BUKAN_INTI", "BAHASA", "LAINNYA")
ALASAN_TIDAK = ("BUKTI_TERPOTONG", "BUKTI_DERAU", "BUKAN_TEMUAN", "LAINNYA")
JENIS = ("JANGKAR", "UBAHAN")
HDR_BUTIR = ["butir_no", "claim_id", "jenis", "keputusan", "alasan_kode", "catatan", "anotator", "detik", "status_akhir"]
HDR_PAS = ["pair_id", "jawaban_ahli", "catatan", "anotator", "detik"]
HDR_DISKUSI = ["claim_id", "jenis", "keputusan_final", "catatan"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # bahan/v2


# ---------------------------------------------------------------- pembacaan
def baca_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames or []), list(rd)


def muat_rujukan(folder):
    """Daftar sah dari berkas sumber (hanya dibaca)."""
    _, lem40 = baca_csv(os.path.join(folder, "lembar_ahli_40.csv"))
    _, lem30 = baca_csv(os.path.join(folder, "lembar_ahli_jangkar_30.csv"))
    return {
        "claims": [r["claim_id"].strip() for r in lem40],
        "altered": {r["claim_id"].strip() for r in lem40 if (r.get("claim_altered_draft") or "").strip()},
        "pairs": [r["pair_id"].strip() for r in lem30],
    }


def muat_penilaian(masukan, ref):
    """Kembalikan (suara_butir, suara_pas, penilai, galat, peringatan)."""
    galat, peringatan = [], []
    suara_butir, suara_pas, penilai = {}, {}, set()
    berkas = {}
    claims, altered, pairs = set(ref["claims"]), ref["altered"], set(ref["pairs"])

    for path in sorted(glob.glob(os.path.join(masukan, "kelayakan_butir_*.csv"))):
        nama = os.path.basename(path)
        hdr, rows = baca_csv(path)
        if not set(HDR_BUTIR).issubset(hdr):
            galat.append(f"{nama}: kolom tidak sesuai spesifikasi")
            continue
        for i, r in enumerate(rows, start=2):
            loc = f"{nama} baris {i}"
            pen = (r.get("anotator") or "").strip()
            if not pen:
                galat.append(f"{loc}: kolom anotator kosong")
                continue
            penilai.add(pen)
            berkas.setdefault((pen, "butir"), set()).add(nama)
            kep = (r.get("keputusan") or "").strip()
            if not kep:
                continue  # belum dinilai: bukan suara
            cid = (r.get("claim_id") or "").strip()
            jenis = (r.get("jenis") or "").strip()
            if kep not in KEP:
                galat.append(f"{loc}: keputusan '{kep}' tidak sah")
                continue
            if jenis not in JENIS:
                galat.append(f"{loc}: jenis '{jenis}' tidak sah")
                continue
            if cid not in claims:
                galat.append(f"{loc}: claim_id '{cid}' tidak dikenal")
                continue
            if jenis == "UBAHAN" and cid not in altered:
                galat.append(f"{loc}: UBAHAN untuk '{cid}' yang tidak punya draf ubahan")
                continue
            alasan = [a.strip() for a in (r.get("alasan_kode") or "").split(";") if a.strip()]
            sah_alasan = ALASAN_REVISI if kep == "PERLU_REVISI" else ALASAN_TIDAK if kep == "TIDAK_LAYAK" else ()
            salah = [a for a in alasan if a not in sah_alasan]
            if salah:
                galat.append(f"{loc}: alasan {salah} tidak sah untuk {kep}")
                continue
            catatan = (r.get("catatan") or "").strip()
            hilang = (kep == "PERLU_REVISI" and not catatan) or (kep == "TIDAK_LAYAK" and not alasan)
            if hilang:
                peringatan.append(f"{loc}: {cid} {jenis} dari '{pen}': "
                                  + ("PERLU_REVISI tanpa catatan" if kep == "PERLU_REVISI" else "TIDAK_LAYAK tanpa alasan")
                                  + " (suara tetap dihitung; ditandai CATATAN_HILANG)")
            st = (r.get("status_akhir") or "").strip()
            if st and st != STATUS_DARI[kep]:
                galat.append(f"{loc}: status_akhir '{st}' tidak sesuai keputusan {kep}")
                continue
            d = suara_butir.setdefault((cid, jenis), {})
            if pen in d:
                galat.append(f"{loc}: baris ganda dari penilai '{pen}' untuk {cid} {jenis}")
                continue
            d[pen] = {"keputusan": kep, "alasan": alasan, "catatan": catatan, "catatan_hilang": hilang, "file": nama}

    for path in sorted(glob.glob(os.path.join(masukan, "pasangan_*.csv"))):
        nama = os.path.basename(path)
        hdr, rows = baca_csv(path)
        if not set(HDR_PAS).issubset(hdr):
            galat.append(f"{nama}: kolom tidak sesuai spesifikasi")
            continue
        for i, r in enumerate(rows, start=2):
            loc = f"{nama} baris {i}"
            pen = (r.get("anotator") or "").strip()
            if not pen:
                galat.append(f"{loc}: kolom anotator kosong")
                continue
            penilai.add(pen)
            berkas.setdefault((pen, "pasangan"), set()).add(nama)
            jaw = (r.get("jawaban_ahli") or "").strip()
            if not jaw:
                continue  # belum dijawab: bukan suara
            pid = (r.get("pair_id") or "").strip()
            if jaw not in BAG2:
                galat.append(f"{loc}: jawaban '{jaw}' tidak sah")
                continue
            if pid not in pairs:
                galat.append(f"{loc}: pair_id '{pid}' tidak dikenal")
                continue
            d = suara_pas.setdefault(pid, {})
            if pen in d:
                galat.append(f"{loc}: baris ganda dari penilai '{pen}' untuk {pid}")
                continue
            d[pen] = {"jawab": jaw, "catatan": (r.get("catatan") or "").strip(), "file": nama}

    for (pen, jenis_berkas), files in sorted(berkas.items()):
        if len(files) > 1:
            peringatan.append(f"penilai '{pen}' punya lebih dari satu berkas {jenis_berkas}: {', '.join(sorted(files))}")
    return suara_butir, suara_pas, sorted(penilai), galat, peringatan


def muat_diskusi(masukan, ref):
    """Baca diskusi.csv bila ada. Kembalikan (dict kunci -> {keputusan_final, catatan}, galat)."""
    path = os.path.join(masukan, "diskusi.csv")
    if not os.path.exists(path):
        return {}, []
    galat, hasil = [], {}
    hdr, rows = baca_csv(path)
    if not set(HDR_DISKUSI).issubset(hdr):
        return {}, [f"diskusi.csv: kolom harus {','.join(HDR_DISKUSI)}"]
    claims, altered = set(ref["claims"]), ref["altered"]
    for i, r in enumerate(rows, start=2):
        loc = f"diskusi.csv baris {i}"
        cid = (r.get("claim_id") or "").strip()
        jenis = (r.get("jenis") or "").strip()
        kf = (r.get("keputusan_final") or "").strip()
        if cid not in claims:
            galat.append(f"{loc}: claim_id '{cid}' tidak dikenal")
            continue
        if jenis not in JENIS:
            galat.append(f"{loc}: jenis '{jenis}' tidak sah")
            continue
        if jenis == "UBAHAN" and cid not in altered:
            galat.append(f"{loc}: UBAHAN untuk '{cid}' yang tidak punya draf ubahan")
            continue
        if kf not in KEP_FINAL:
            galat.append(f"{loc}: keputusan_final '{kf}' tidak sah (DIPAKAI|DIREVISI|KELUAR)")
            continue
        if (cid, jenis) in hasil:
            galat.append(f"{loc}: butir {cid} {jenis} muncul dua kali di diskusi.csv")
            continue
        hasil[(cid, jenis)] = {"keputusan_final": kf, "catatan": (r.get("catatan") or "").strip()}
    return hasil, galat


# ---------------------------------------------------------------- keputusan
def putus(suara, diskusi=None):
    """suara: list of (penilai, keputusan). diskusi: dict atau None. Kembalikan (status, keputusan_akhir)."""
    if diskusi is not None:
        return "DISKUSI", diskusi["keputusan_final"]
    n = len(suara)
    if n == 0:
        return "BELUM_DINILAI", ""
    if n == 1:
        return "SEMENTARA", STATUS_DARI[suara[0][1]]
    c = Counter(k for _, k in suara)
    top_k, top_n = c.most_common(1)[0]
    ikat = [k for k, v in c.items() if v == top_n]
    if n == 2:
        if len(c) == 1:
            return "SEMENTARA", STATUS_DARI[top_k]
        return "PERLU_PENILAI_KETIGA", ""
    if top_n >= 2 and len(ikat) == 1:
        return "FINAL", STATUS_DARI[top_k]
    return "PERLU_DISKUSI", ""


def galat_status_diskusi(diskusi, suara_butir):
    """diskusi.csv HANYA boleh menimpa butir berstatus PERLU_DISKUSI (tiga suara berbeda).
    Butir lain ditolak: menimpanya akan membalik hasil suara terbanyak."""
    galat = []
    for cid, jenis in sorted(diskusi):
        d = suara_butir.get((cid, jenis), {})
        status, _ = putus([(p, d[p]["keputusan"]) for p in sorted(d)])
        if status != "PERLU_DISKUSI":
            galat.append(f"diskusi.csv: butir {cid} {jenis} berstatus {status}; diskusi hanya boleh untuk butir "
                         "PERLU_DISKUSI (tiga suara berbeda). Perhitungan dihentikan agar suara terbanyak tidak terbalik.")
    return galat


def gabung_catatan(d, diskusi=None):
    bagian = []
    for pen in sorted(d):
        r = d[pen]
        awal = f"[{pen}]"
        if r.get("alasan"):
            awal += " (" + ",".join(r["alasan"]) + ")"
        if r.get("catatan_hilang"):
            awal += " CATATAN_HILANG"
        if r.get("catatan"):
            awal += " " + r["catatan"]
        bagian.append(awal)
    if diskusi is not None:
        bagian.append("[diskusi] " + diskusi["catatan"] if diskusi["catatan"] else "[diskusi]")
    return " | ".join(bagian)


def baris_butir(ref, suara_butir, diskusi):
    baris = []
    kunci = [(c, "JANGKAR") for c in ref["claims"]] + [(c, "UBAHAN") for c in ref["claims"] if c in ref["altered"]]
    for cid, jenis in kunci:
        d = suara_butir.get((cid, jenis), {})
        dk = diskusi.get((cid, jenis))
        status, akhir = putus([(p, d[p]["keputusan"]) for p in sorted(d)], dk)
        baris.append({
            "claim_id": cid, "jenis": jenis, "n_penilai": len(d),
            "suara": "; ".join(f"{p}={d[p]['keputusan']}" for p in sorted(d)),
            "keputusan_akhir": akhir, "status": status, "catatan_gabungan": gabung_catatan(d, dk),
            "n_layak": sum(1 for p in d if d[p]["keputusan"] == "LAYAK"),
            "ada_tidak_layak": any(d[p]["keputusan"] == "TIDAK_LAYAK" for p in d),
            "catatan_hilang": any(d[p].get("catatan_hilang") for p in d),
        })
    return baris


# ---------------------------------------------------------------- kesepakatan
def cohen(xs, ys, cats):
    """Kembalikan (persen_sepakat, kappa). kappa None bila tidak terdefinisi."""
    n = len(xs)
    if n == 0:
        return None, None
    po = sum(1 for a, b in zip(xs, ys) if a == b) / n
    pe = sum((xs.count(c) / n) * (ys.count(c) / n) for c in cats)
    if abs(1 - pe) < 1e-12:
        return po, None
    return po, (po - pe) / (1 - pe)


def fleiss(tabel, n):
    """tabel: per item jumlah suara per kategori; setiap item punya n penilai. None bila tidak terdefinisi."""
    big_n = len(tabel)
    if big_n == 0 or n < 2:
        return None
    k = len(tabel[0])
    total = big_n * n
    p_i = [(sum(c * c for c in row) - n) / (n * (n - 1)) for row in tabel]
    p_bar = sum(p_i) / big_n
    p_j = [sum(row[j] for row in tabel) / total for j in range(k)]
    p_e = sum(p * p for p in p_j)
    if abs(1 - p_e) < 1e-12:
        return None
    return (p_bar - p_e) / (1 - p_e)


def analisis_sepakat(suara, cats, penilai_semua):
    """suara: dict kunci -> {penilai: nilai}. Kembalikan ringkasan kesepakatan."""
    hasil = {"pasangan": [], "keseluruhan": None, "n_banding": 0, "fleiss": None, "fleiss_n_item": 0}
    agr = tot = 0
    for d in suara.values():
        ps = sorted(d)
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                tot += 1
                agr += 1 if d[ps[i]] == d[ps[j]] else 0
    hasil["keseluruhan"] = (agr / tot) if tot else None
    hasil["n_banding"] = tot
    semua = list(penilai_semua)
    for i in range(len(semua)):
        for j in range(i + 1, len(semua)):
            a, b = semua[i], semua[j]
            both = [d for d in suara.values() if a in d and b in d]
            po, kap = cohen([d[a] for d in both], [d[b] for d in both], cats) if both else (None, None)
            hasil["pasangan"].append({"a": a, "b": b, "n": len(both), "persen": po, "kappa": kap})
    if len(semua) >= 3:
        penuh = [d for d in suara.values() if all(p in d for p in semua)]
        hasil["fleiss_n_item"] = len(penuh)
        if penuh:
            tabel = [[sum(1 for p in semua if d[p] == c) for c in cats] for d in penuh]
            hasil["fleiss"] = fleiss(tabel, len(semua))
    return hasil


def catatan_kesepakatan(persen, kap):
    if persen is None:
        return "tidak ada pasangan yang sama-sama menilai"
    if kap is None:
        return "kappa tidak terdefinisi: semua suara dalam satu kategori" if persen == 1 else "kappa tidak terdefinisi"
    if persen >= 0.8 and kap < 0.4:
        return "PERHATIAN: persen sepakat tinggi tetapi kappa rendah; kemungkinan distribusi sangat miring"
    return ""


def fmt(x, d=3):
    return "-" if x is None else f"{x:.{d}f}"


# ---------------------------------------------------------------- keluaran
def tulis_csv(path, header, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def tulis_daftar_id(path, judul, daftar):
    """daftar: dict jenis -> list claim_id. Satu id per baris; bagian JANGKAR dan UBAHAN dipisah."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# " + judul + "\n")
        f.write("# JANGKAR (pernyataan jangkar)\n")
        for c in daftar.get("JANGKAR", []):
            f.write(c + "\n")
        f.write("# UBAHAN (draf ubahan; dicatat terpisah, bukan jangkar)\n")
        for c in daftar.get("UBAHAN", []):
            f.write(c + "\n")


def kumpul(rows, pred):
    out = {"JANGKAR": [], "UBAHAN": []}
    for r in rows:
        if pred(r):
            out[r["jenis"]].append(r["claim_id"])
    return out


def hitung(masukan, keluar, rujukan_folder=ROOT):
    """Kembalikan (kode, pesan). 0 = berhasil, 1 = masalah pemakaian, 2 = galat integritas (tidak ada keluaran)."""
    if not os.path.isdir(masukan):
        return 1, [f"folder masukan tidak ada: {masukan}"]
    if os.path.abspath(keluar).startswith(os.path.abspath(masukan) + os.sep) or os.path.abspath(keluar) == os.path.abspath(masukan):
        return 1, ["folder keluar tidak boleh berada di dalam folder masukan"]
    if not glob.glob(os.path.join(masukan, "kelayakan_butir_*.csv")) and not glob.glob(os.path.join(masukan, "pasangan_*.csv")):
        return 1, ["tidak ada berkas penilaian (kelayakan_butir_*.csv / pasangan_*.csv) di folder masukan"]
    ref = muat_rujukan(rujukan_folder)
    suara_b, suara_p, penilai, galat, peringatan = muat_penilaian(masukan, ref)
    diskusi, galat_d = muat_diskusi(masukan, ref)
    galat += galat_d
    galat += galat_status_diskusi(diskusi, suara_b)
    if galat:
        return 2, ["GALAT INTEGRITAS (tidak ada keluaran yang ditulis):"] + ["  - " + g for g in galat]

    rows = baris_butir(ref, suara_b, diskusi)
    os.makedirs(keluar, exist_ok=True)
    tulis_csv(os.path.join(keluar, "status_butir.csv"),
              ["claim_id", "jenis", "n_penilai", "suara", "keputusan_akhir", "status", "catatan_gabungan"],
              [[r["claim_id"], r["jenis"], r["n_penilai"], r["suara"], r["keputusan_akhir"], r["status"], r["catatan_gabungan"]] for r in rows])
    tulis_csv(os.path.join(keluar, "proporsi_layak.csv"), ["claim_id", "jenis", "n_penilai", "n_layak", "proporsi_layak"],
              [[r["claim_id"], r["jenis"], r["n_penilai"], r["n_layak"],
                fmt(r["n_layak"] / r["n_penilai"]) if r["n_penilai"] else ""] for r in rows])
    tulis_csv(os.path.join(keluar, "daftar_revisi.csv"), ["claim_id", "jenis", "status", "catatan_gabungan"],
              [[r["claim_id"], r["jenis"], r["status"], r["catatan_gabungan"]] for r in rows if r["keputusan_akhir"] == "DIREVISI"])

    tulis_daftar_id(os.path.join(keluar, "ID_KELUAR.txt"),
                    "Butir KELUAR FINAL atau KELUAR lewat diskusi (analisis kepekaan utama). Status lengkap: status_butir.csv.",
                    kumpul(rows, lambda r: r["keputusan_akhir"] == "KELUAR" and r["status"] in ("FINAL", "DISKUSI")))
    tulis_daftar_id(os.path.join(keluar, "ID_KELUAR_SEMENTARA.txt"),
                    "PRATINJAU SAJA: butir KELUAR berstatus SEMENTARA (kurang dari 3 penilai). Bukan daftar keluar utama.",
                    kumpul(rows, lambda r: r["keputusan_akhir"] == "KELUAR" and r["status"] == "SEMENTARA"))
    tulis_daftar_id(os.path.join(keluar, "ID_KELUAR_KETAT.txt"),
                    "Analisis ketat: seluruh butir dengan setidaknya satu suara TIDAK_LAYAK (Amandemen 6 butir b).",
                    kumpul(rows, lambda r: r["ada_tidak_layak"]))

    kes = {}
    for label, jenis_f in [("JANGKAR", "JANGKAR"), ("UBAHAN", "UBAHAN"), ("GABUNGAN", None)]:
        sb = {(r["claim_id"], r["jenis"]): {p: suara_b[(r["claim_id"], r["jenis"])][p]["keputusan"]
                                           for p in suara_b.get((r["claim_id"], r["jenis"]), {})}
              for r in rows if jenis_f is None or r["jenis"] == jenis_f}
        kes[label] = analisis_sepakat(sb, KEP, penilai)
    kes["PASANGAN"] = analisis_sepakat({pid: {p: v["jawab"] for p, v in d.items()} for pid, d in suara_p.items()},
                                       BAG2, penilai)

    tulis_ringkasan(os.path.join(keluar, "RINGKASAN_KELAYAKAN.md"), penilai, rows, kes, ref,
                    n_pas=sum(1 for pid in ref["pairs"] if suara_p.get(pid)), n_pas_total=len(ref["pairs"]),
                    peringatan=peringatan, diskusi=diskusi)
    status_hitung = Counter((r["jenis"], r["status"]) for r in rows)
    pesan = [f"penilai: {len(penilai)} ({', '.join(penilai)})",
             f"butir: {len(rows)} baris; status {dict(status_hitung)}",
             f"pasangan dijawab: {sum(1 for pid in ref['pairs'] if suara_p.get(pid))} dari {len(ref['pairs'])}",
             f"diskusi.csv: {len(diskusi)} butir" if diskusi else "diskusi.csv: tidak ada"]
    pesan += ["peringatan: " + p for p in peringatan]
    return 0, pesan


def _blok_kes(L, judul, k):
    L.append(f"### {judul}")
    L.append("")
    L.append(f"- Persen sepakat keseluruhan: {fmt(k['keseluruhan'])} (dari {k['n_banding']} perbandingan pasangan penilai).")
    if not k["pasangan"]:
        L.append("- Kappa Cohen: belum dihitung (kurang dari dua penilai).")
    for p in k["pasangan"]:
        cat = catatan_kesepakatan(p["persen"], p["kappa"])
        L.append(f"  - Kappa Cohen {p['a']} vs {p['b']}: n={p['n']}, sepakat={fmt(p['persen'])}, kappa={fmt(p['kappa'])}" + (f". {cat}" if cat else ""))
    if k["fleiss"] is not None:
        L.append(f"- Kappa Fleiss (n={k['fleiss_n_item']} item dinilai semua penilai): {fmt(k['fleiss'])}")
    elif k["fleiss_n_item"] == 0 and k["pasangan"] and len(k["pasangan"]) >= 3:
        L.append("- Kappa Fleiss: belum dihitung (tidak ada item yang dinilai semua penilai).")
    else:
        L.append("- Kappa Fleiss: belum dihitung (membutuhkan tiga penilai atau lebih).")
    L.append("")


def tulis_ringkasan(path, penilai, rows, kes, ref, n_pas, n_pas_total, peringatan, diskusi):
    L = ["# Ringkasan penilaian kelayakan butir", "",
         "Penilaian ini dilakukan oleh tim penulis (bukan panel ahli eksternal, sehingga bukan CVI). "
         "Penilai adalah penulis yang mengetahui hipotesis. Keterbatasan ini ditulis di laporan.", "",
         f"**Jumlah penilai: {len(penilai)}** ({', '.join(penilai) if penilai else 'belum ada'}).", ""]
    if len(penilai) < 3:
        L += [f"**STATUS SEMENTARA**: penilai baru {len(penilai)} dari 3 yang direncanakan. "
              "Keputusan di bawah belum final dan dapat berubah saat penilai lain selesai.", ""]
    L += ["## Jumlah per status", "", "| Jenis | Status | Jumlah |", "|---|---|---|"]
    for (j, s), n in sorted(Counter((r["jenis"], r["status"]) for r in rows).items()):
        L.append(f"| {j} | {s} | {n} |")
    L += ["", "## Keputusan akhir", "", "| Jenis | Keputusan akhir | Jumlah |", "|---|---|---|"]
    for (j, k), n in sorted(Counter((r["jenis"], r["keputusan_akhir"]) for r in rows).items()):
        L.append(f"| {j} | {k or '(belum)'} | {n} |")
    L += ["", "Pasangan dengan jawaban kosong tidak dihitung sebagai suara. Butir tanpa suara ditandai BELUM_DINILAI. "
          "PERLU_DISKUSI tidak masuk ID_KELUAR sampai diskusi selesai.", ""]
    L += ["## Daftar keluar (tiga versi)", "",
          "- ID_KELUAR.txt: KELUAR FINAL atau KELUAR lewat diskusi (analisis utama).",
          "- ID_KELUAR_SEMENTARA.txt: KELUAR berstatus SEMENTARA (pratinjau saja).",
          "- ID_KELUAR_KETAT.txt: setiap butir dengan setidaknya satu suara TIDAK_LAYAK.", ""]
    L += ["## Kesepakatan penilai: butir", ""]
    _blok_kes(L, "Pernyataan JANGKAR", kes["JANGKAR"])
    _blok_kes(L, "Draf UBAHAN", kes["UBAHAN"])
    _blok_kes(L, "Gabungan (JANGKAR dan UBAHAN)", kes["GABUNGAN"])
    L += ["## Kesepakatan penilai: pasangan (nyambung / tidak nyambung / ragu)", "",
          f"- Pasangan dijawab: {n_pas} dari {n_pas_total}."]
    _blok_kes(L, "Pasangan", kes["PASANGAN"])
    L += ["## Butir perlu diskusi (PERLU_DISKUSI)", ""]
    L += [f"- {r['claim_id']} ({r['jenis']}): suara {r['suara']}" for r in rows if r["status"] == "PERLU_DISKUSI"] or ["Tidak ada."]
    L += ["", "## Hasil diskusi (diskusi.csv)", ""]
    L += [f"- {cid} ({jn}): keputusan_final {v['keputusan_final']}" + (f" | {v['catatan']}" if v["catatan"] else "")
          for (cid, jn), v in sorted(diskusi.items())] or ["Tidak ada berkas diskusi.csv."]
    L += ["", "## Butir menunggu penilai ketiga (PERLU_PENILAI_KETIGA)", ""]
    L += [f"- {r['claim_id']} ({r['jenis']}): suara {r['suara']}" for r in rows if r["status"] == "PERLU_PENILAI_KETIGA"] or ["Tidak ada."]
    L += ["", "## Catatan hilang (peringatan, suara tetap dihitung)", ""]
    L += [f"- {r['claim_id']} ({r['jenis']}): {r['catatan_gabungan']}" for r in rows if r["catatan_hilang"]] or ["Tidak ada."]
    if peringatan:
        L += ["", "## Peringatan berkas", ""]
        L += [f"- {p}" for p in peringatan]
    L += ["", "## Keterbatasan", "",
          "- Penilai adalah penulis laporan, bukan panel ahli. Angka ini bukan CVI dan tidak boleh disebut sebagai validitas isi oleh panel ahli.",
          "- Penilai mengetahui hipotesis penelitian; kebutaan tidak dapat dijamin sepenuhnya.",
          "- Kappa dan persen sepakat dengan jumlah penilai kecil sangat tidak stabil.",
          "- Proporsi LAYAK per butir disajikan sebagai angka deskriptif (lihat proporsi_layak.csv).",
          "- Keputusan SEMENTARA (1 atau 2 penilai) belum final.", ""]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blok in iter(lambda: f.read(65536), b""):
            h.update(blok)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hitung hasil penilaian kelayakan butir (Amandemen 5 dan 6).")
    ap.add_argument("--masukan", default=os.path.join(ROOT, "hasil_ahli"))
    ap.add_argument("--keluar", default=os.path.join(ROOT, "hasil_olahan"))
    ap.add_argument("--rujukan", default=ROOT, help="folder berisi lembar_ahli_40.csv dan lembar_ahli_jangkar_30.csv")
    a = ap.parse_args(argv)
    kode, pesan = hitung(a.masukan, a.keluar, a.rujukan)
    out = sys.stdout if kode == 0 else sys.stderr
    for p in pesan:
        print(p, file=out)
    return kode


if __name__ == "__main__":
    sys.exit(main())
