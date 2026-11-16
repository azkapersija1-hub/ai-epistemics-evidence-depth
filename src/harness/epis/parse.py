"""Parser keluaran model (JSON ketat, toleransi pagar kode ```json).

Aturan (dari brief dan 14_STATISTICAL_ANALYSIS_PLAN.md):
  - Jumlah p dalam 1 +/- 0,01 diterima apa adanya.
  - Di luar itu p dinormalisasi dan diberi bendera normalized=True.
  - Label salah/hilang/tambahan, nilai negatif, bukan angka, NaN, Inf,
    atau teks yang bukan JSON = parse_failure.
Modul ini tidak memanggil model. Hanya memproses string keluaran.
"""
import json
import math

from epis.skor import LABELS, brier_multikelas

TOLERANSI_JUMLAH = 0.01
_EPS_FLOAT = 1e-9  # menutup galat representasi float di batas 1 +/- 0,01
GAGAL_BS = 2.0


class ParseGagal(ValueError):
    """Keluaran tidak valid menurut aturan parse."""


_DEKODER = json.JSONDecoder()  # default: NaN/Infinity terdekode lalu ditolak _cek_nilai


def _kandidat_objek(teks):
    """Semua objek JSON (dict) yang memuat minimal satu kunci label, urut posisi kemunculan.

    Model bernalar bisa menulis teks sebelum JSON, atau lebih dari satu objek.
    Objek yang tidak bisa didekode (mis. terpotong) dilewati.
    """
    hasil = []
    for i, ch in enumerate(teks):
        if ch != "{":
            continue
        try:
            obj, _ = _DEKODER.raw_decode(teks, i)
        except ValueError:
            continue
        if isinstance(obj, dict) and any(k in obj for k in LABELS):
            hasil.append(obj)
    return hasil


def _cek_nilai(objek):
    """Pastikan tepat tiga label dan setiap nilai adalah angka hingga non-negatif."""
    if not isinstance(objek, dict):
        raise ParseGagal("akar JSON bukan objek")
    kunci = set(objek.keys())
    if kunci != set(LABELS):
        hilang = sorted(set(LABELS) - kunci)
        asing = sorted(kunci - set(LABELS))
        raise ParseGagal(f"label tidak tepat; hilang={hilang} asing={asing}")
    bersih = {}
    for label in LABELS:
        nilai = objek[label]
        if isinstance(nilai, bool) or not isinstance(nilai, (int, float)):
            raise ParseGagal(f"nilai {label} bukan angka")
        if not math.isfinite(nilai):
            raise ParseGagal(f"nilai {label} tidak hingga")
        if nilai < 0:
            raise ParseGagal(f"nilai {label} negatif")
        bersih[label] = float(nilai)
    return bersih


def parse_keluaran(raw):
    """Parse satu string keluaran model.

    Kembalikan dict:
      ok (bool), p (dict|None), normalized (bool), jumlah_mentah (float|None),
      error (str|None).
    Tidak pernah melempar exception untuk input buruk; kegagalan dicatat.
    """
    gagal = {"ok": False, "p": None, "normalized": False,
             "jumlah_mentah": None, "error": None}
    try:
        kandidat = _kandidat_objek("" if raw is None else str(raw))
        if not kandidat:
            raise ParseGagal("tidak ada objek JSON dengan kunci label")
        bersih = _cek_nilai(kandidat[-1])  # objek JSON TERAKHIR yang memuat label
    except ParseGagal as e:
        return {**gagal, "error": str(e)}
    jumlah = sum(bersih.values())
    if jumlah <= 0:
        return {**gagal, "jumlah_mentah": jumlah, "error": "jumlah p nol"}
    if abs(jumlah - 1.0) <= TOLERANSI_JUMLAH + _EPS_FLOAT:
        return {"ok": True, "p": bersih, "normalized": False,
                "jumlah_mentah": jumlah, "error": None}
    normal = {k: v / jumlah for k, v in bersih.items()}
    return {"ok": True, "p": normal, "normalized": True,
            "jumlah_mentah": jumlah, "error": None}


def brier_dua_batas(hasil_list, kunci_list):
    """Brier dalam dua batas.

    hasil_list: daftar keluaran parse_keluaran (urutan sama dengan kunci_list).
    Batas 1: butir gagal DIKELUARKAN dari rata-rata.
    Batas 2: butir gagal diberi BS = 2,0 dan tetap ikut dirata-rata.
    Kembalikan dict dengan kedua nilai, jumlah gagal, dan jumlah normalized.
    """
    if len(hasil_list) != len(kunci_list):
        raise ValueError("jumlah hasil dan kunci tidak sama")
    if not hasil_list:
        raise ValueError("daftar kosong")
    bs_ok = [brier_multikelas(h["p"], k) for h, k in zip(hasil_list, kunci_list) if h["ok"]]
    bs_semua = [
        brier_multikelas(h["p"], k) if h["ok"] else GAGAL_BS
        for h, k in zip(hasil_list, kunci_list)
    ]
    n_gagal = sum(1 for h in hasil_list if not h["ok"])
    return {
        "batas1_tanpa_gagal": (sum(bs_ok) / len(bs_ok)) if bs_ok else None,
        "batas2_gagal_bs2": sum(bs_semua) / len(bs_semua),
        "n_total": len(hasil_list),
        "n_gagal": n_gagal,
        "n_normalized": sum(1 for h in hasil_list if h["normalized"]),
    }
