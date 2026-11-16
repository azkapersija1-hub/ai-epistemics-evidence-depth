"""Membuat fixture TIRUAN v2 (deterministik) dengan skema JANGKAR untuk uji pipeline.

PERINGATAN: semua klaim, bukti, dan artikel di sini FIKTIF. Tidak berasal dari artikel
nyata, tidak memiliki DOI. Label jangkar di kunci.jsonl dibuat skrip, BUKAN anotasi ahli.

Struktur: 14 artikel x 3 klaim = 42 klaim; tiap klaim 7 observasi:
  own  : R1, R2, R3  (bukti dari artikel klaim sendiri)
  near : R1, R3      (bukti dari artikel lain yang mirip topiknya)
  far  : R1, R3      (bukti dari artikel yang topiknya jauh)
Label jangkar: own R3 = SUPPORTED (kesimpulan penulis fiktif, risiko_jangkar=True);
near dan far = NEI; own R1 dan R2 = null (label_type none).

Keluaran: items_model.jsonl (tanpa kolom kunci) dan kunci.jsonl (rahasia), ditimpa
setiap dijalankan. Hasilnya sama byte per byte karena tidak ada acak.
"""
import os
import sys

HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HARNESS)

from epis.jsonl_io import tulis_jsonl  # noqa: E402

FOLDER = os.path.dirname(os.path.abspath(__file__))
JUMLAH_ARTIKEL = 14
KLAIM_PER_ARTIKEL = 3
BAHASA_SIKLUS = ("id", "en", "unk")
MANIPULASI = ["Metode Fiktif Alfa", "Intervensi Fiktif Beta", "Pelatihan Fiktif Gamma",
              "Program Fiktif Delta", "Alat Fiktif Epsilon", "Modul Fiktif Zeta",
              "Strategi Fiktif Eta", "Skema Fiktif Theta", "Kurikulum Fiktif Iota",
              "Pendekatan Fiktif Kappa", "Model Fiktif Lambda", "Teknik Fiktif Mu",
              "Sistem Fiktif Nu", "Kerangka Fiktif Xi"]
HASIL_UKUR = ["skor uji fiktif", "daya ingat fiktif", "kepuasan fiktif", "ketepatan fiktif"]
KELOMPOK = ["kelompok fiktif A", "kelompok fiktif B", "kelompok fiktif C"]
TOPIK_JAUH = ["pertanian fiktif", "logistik fiktif", "arsitektur fiktif"]
KALIMAT_ARAH = "Hasil fiktif menunjukkan peningkatan yang konsisten."
KALIMAT_KESIMPULAN = "Kesimpulan fiktif: intervensi tampak bermanfaat pada sampel fiktif."
PAIR_RUNG = (("own", "R1"), ("own", "R2"), ("own", "R3"),
             ("near", "R1"), ("near", "R3"), ("far", "R1"), ("far", "R3"))


def _klaim(j, bahasa):
    nama = MANIPULASI[j % len(MANIPULASI)]
    ukur = HASIL_UKUR[(j // 2) % len(HASIL_UKUR)]
    grup = KELOMPOK[(j // 3) % len(KELOMPOK)]
    if bahasa == "en":
        teks = f"The {nama.lower()} improves {ukur} in {grup}."
    else:
        teks = f"{nama} meningkatkan {ukur} pada {grup}."
    return teks, nama, ukur, grup


def _bukti(pair, rung, nama, ukur, grup, j):
    """Teks bukti untuk satu observasi. Hanya bukti 'own' yang mendukung klaim."""
    if pair == "own":
        teks = f"Abstract (FIKTIF): Studi tiruan membandingkan {nama} dengan kontrol pada {grup} untuk {ukur}."
        if rung in ("R2", "R3"):
            teks += f" Results (FIKTIF): {KALIMAT_ARAH}"
        if rung == "R3":
            teks += f" Conclusion (FIKTIF): {KALIMAT_KESIMPULAN}"
        return teks
    topik = TOPIK_JAUH[j % len(TOPIK_JAUH)]
    if pair == "near":
        teks = (f"Abstract (FIKTIF): Studi tiruan lain di bidang serupa membahas {KELOMPOK[(j + 1) % 3]} "
                f"tetapi tidak menguji {nama}.")
    else:
        teks = f"Abstract (FIKTIF): Studi tiruan tentang {topik} tanpa hubungan dengan {nama}."
    if rung == "R3":
        teks += f" Conclusion (FIKTIF): Studi itu tidak menyinggung klaim tentang {nama}."
    return teks


def _anotasi(pair, rung):
    """Label jangkar dan catatannya untuk satu (pair, rung)."""
    if pair == "own" and rung == "R3":
        return ("SUPPORTED", "anchor", "kesimpulan penulis fiktif", True)
    if pair == "own":
        return (None, "none", "tanpa label (hanya pergeseran)", False)
    return ("NEI", "anchor", "jangkar: bukti dari artikel lain tidak menjawab klaim", False)


def _artikel_bukti(indeks_artikel, pair):
    if pair == "own":
        return indeks_artikel
    langkah = 1 if pair == "near" else 5
    return (indeks_artikel + langkah) % JUMLAH_ARTIKEL


def _split(indeks_artikel):
    if indeks_artikel < 2:
        return "pilot"
    if indeks_artikel < 8:
        return "dev"
    if indeks_artikel < 11:
        return "val"
    return "holdout"


def _baris_klaim(j, indeks_artikel, bahasa):
    teks, nama, ukur, grup = _klaim(j, bahasa)
    artikel = f"A{indeks_artikel + 1:03d}"
    claim_id = f"C{j + 1:03d}"
    items, kunci = [], []
    for pair, rung in PAIR_RUNG:
        obs_id = f"{claim_id}_{pair}_{rung}"
        label, tipe, catatan, risiko = _anotasi(pair, rung)
        items.append({
            "obs_id": obs_id, "claim_id": claim_id, "rung": rung, "lang": bahasa,
            "claim_text": teks,
            "evidence_text": _bukti(pair, rung, nama, ukur, grup, j),
        })
        kunci.append({
            "obs_id": obs_id, "claim_id": claim_id, "article_id": artikel,
            "evidence_article_id": f"A{_artikel_bukti(indeks_artikel, pair) + 1:03d}",
            "split": _split(indeks_artikel), "pair_type": pair, "rung": rung,
            "label": label, "label_type": tipe, "anchor_note": catatan,
            "risiko_jangkar": risiko,
        })
    return items, kunci


def bangun_baris():
    """Kembalikan (items, kunci) sebagai daftar dict. Tanpa acak."""
    items, kunci = [], []
    for a in range(JUMLAH_ARTIKEL):
        for k in range(KLAIM_PER_ARTIKEL):
            j = a * KLAIM_PER_ARTIKEL + k
            bahasa = BAHASA_SIKLUS[(j // 3) % len(BAHASA_SIKLUS)]
            it, ku = _baris_klaim(j, a, bahasa)
            items.extend(it)
            kunci.extend(ku)
    return items, kunci


def main():
    items, kunci = bangun_baris()
    tulis_jsonl(os.path.join(FOLDER, "items_model.jsonl"), items, timpa=True)
    tulis_jsonl(os.path.join(FOLDER, "kunci.jsonl"), kunci, timpa=True)
    print(f"items_model: {len(items)} baris; kunci: {len(kunci)} baris (FIKTIF, skema jangkar v2)")


if __name__ == "__main__":
    main()
