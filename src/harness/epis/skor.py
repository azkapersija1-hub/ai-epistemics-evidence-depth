"""Metrik skor murni untuk harness AI x Epistemics.

Semua fungsi tanpa efek samping, hanya stdlib. Distribusi p berbentuk dict
{"SUPPORTED": float, "REFUTED": float, "NEI": float}. Kunci berupa salah satu
dari tiga label. Tidak ada angka hasil eksperimen di modul ini.

Aturan seri argmax (dipraregistrasi, lihat 11_OPERATIONAL_DEFINITIONS.md):
  - Jika NEI termasuk kandidat seri tertinggi, NEI dipilih.
  - Seri lain (SUPPORTED vs REFUTED, tanpa NEI) diselesaikan dengan urutan
    tetap LABELS (SUPPORTED lebih dulu). Aturan ini belum disetujui peneliti.
"""
import math

LABELS = ("SUPPORTED", "REFUTED", "NEI")
NEI = "NEI"
N_BINS = 10
_TOL = 1e-12


def _cek_label(kunci):
    if kunci not in LABELS:
        raise ValueError(f"label tidak dikenal: {kunci!r}")


def one_hot(kunci):
    """Vektor target satu-panas untuk label kunci."""
    _cek_label(kunci)
    return {k: (1.0 if k == kunci else 0.0) for k in LABELS}


def brier_multikelas(p, kunci):
    """Brier multikelas satu observasi: jumlah_k (p_k - y_k)^2, rentang 0..2."""
    y = one_hot(kunci)
    return sum((float(p[k]) - y[k]) ** 2 for k in LABELS)


def _cek_pasangan(p_list, kunci_list):
    if len(p_list) != len(kunci_list):
        raise ValueError("jumlah p dan kunci tidak sama")
    if not p_list:
        raise ValueError("daftar observasi kosong")


def brier_per_observasi(p_list, kunci_list):
    """Daftar Brier multikelas per observasi (urutan sama dengan input)."""
    _cek_pasangan(p_list, kunci_list)
    return [brier_multikelas(p, k) for p, k in zip(p_list, kunci_list)]


def brier_rata(p_list, kunci_list):
    """Rata-rata Brier multikelas. Baseline seragam = 2/3 = 0,666667."""
    nilai = brier_per_observasi(p_list, kunci_list)
    return sum(nilai) / len(nilai)


def label_terpilih(p):
    """Label argmax dengan aturan seri yang didokumentasikan di modul ini."""
    tertinggi = max(float(p[k]) for k in LABELS)
    kandidat = [k for k in LABELS if abs(float(p[k]) - tertinggi) <= _TOL]
    if NEI in kandidat:
        return NEI
    return kandidat[0]


def confidence_terpilih(p):
    """Nilai p pada label terpilih."""
    return float(p[label_terpilih(p)])


def akurasi(p_list, kunci_list):
    """Proporsi observasi dengan label terpilih = kunci."""
    _cek_pasangan(p_list, kunci_list)
    benar = sum(1 for p, k in zip(p_list, kunci_list) if label_terpilih(p) == k)
    return benar / len(p_list)


def _bin_index(conf):
    return min(int(conf * N_BINS), N_BINS - 1)


def _statistik_bin(conf_list, benar_list):
    """Ringkasan satu bin: n, rata-rata confidence, dan akurasi."""
    n = len(conf_list)
    if n == 0:
        return {"n": 0, "conf_rata": None, "akurasi": None}
    return {
        "n": n,
        "conf_rata": sum(conf_list) / n,
        "akurasi": sum(benar_list) / n,
    }


def ece(p_list, kunci_list):
    """Expected Calibration Error, 10 bin, pada confidence label terpilih.

    Kembalikan dict {"ece": float, "bins": [ {n, conf_rata, akurasi} x10 ]}.
    """
    _cek_pasangan(p_list, kunci_list)
    konf = [[] for _ in range(N_BINS)]
    benar = [[] for _ in range(N_BINS)]
    for p, k in zip(p_list, kunci_list):
        c = confidence_terpilih(p)
        i = _bin_index(c)
        konf[i].append(c)
        benar[i].append(1.0 if label_terpilih(p) == k else 0.0)
    total = len(p_list)
    bins = [_statistik_bin(konf[i], benar[i]) for i in range(N_BINS)]
    nilai = 0.0
    for b in bins:
        if b["n"]:
            nilai += (b["n"] / total) * abs(b["akurasi"] - b["conf_rata"])
    return {"ece": nilai, "bins": bins}


def aurc(p_list, kunci_list):
    """Area di bawah kurva risiko-cakupan (discrete).

    Urutkan observasi menurun menurut confidence terpilih (sort stabil: seri
    mempertahankan urutan input). Untuk k = 1..N, cakupan = k/N dan risiko =
    rata-rata kesalahan pada k teratas. AURC = (1/N) * jumlah_k risiko_k.
    Kembalikan {"aurc": float, "kurva": [(cakupan, risiko), ...]}.
    """
    _cek_pasangan(p_list, kunci_list)
    urut = sorted(
        zip(p_list, kunci_list),
        key=lambda pk: -confidence_terpilih(pk[0]),
    )
    total = len(urut)
    kurva = []
    salah_kumulatif = 0
    for k, (p, kunci) in enumerate(urut, start=1):
        if label_terpilih(p) != kunci:
            salah_kumulatif += 1
        kurva.append((k / total, salah_kumulatif / k))
    nilai = sum(risiko for _, risiko in kurva) / total
    return {"aurc": nilai, "kurva": kurva}


def _rasio(pembilang, penyebut):
    return None if penyebut == 0 else pembilang / penyebut


def metrik_nei(p_list, kunci_list):
    """Recall NEI pada observasi berkunci NEI; presisi NEI pada prediksi NEI."""
    _cek_pasangan(p_list, kunci_list)
    pred = [label_terpilih(p) for p in p_list]
    idx_kunci_nei = [i for i, k in enumerate(kunci_list) if k == NEI]
    idx_pred_nei = [i for i, pr in enumerate(pred) if pr == NEI]
    recall_tp = sum(1 for i in idx_kunci_nei if pred[i] == NEI)
    presisi_tp = sum(1 for i in idx_pred_nei if kunci_list[i] == NEI)
    return {
        "n_kunci_nei": len(idx_kunci_nei),
        "recall_nei": _rasio(recall_tp, len(idx_kunci_nei)),
        "n_pred_nei": len(idx_pred_nei),
        "presisi_nei": _rasio(presisi_tp, len(idx_pred_nei)),
    }


def _kelompokkan_per_klaim(records):
    """records: daftar dict {claim_id, rung, p, kunci}. Kembalikan {claim: {rung: brier}}."""
    per_klaim = {}
    for r in records:
        isi = per_klaim.setdefault(r["claim_id"], {})
        if r["rung"] in isi:
            raise ValueError(f"duplikat klaim/rung: {r['claim_id']} {r['rung']}")
        isi[r["rung"]] = brier_multikelas(r["p"], r["kunci"])
    return per_klaim


def abstract_overconfidence_gap(records):
    """Rata-rata per klaim dari Brier(R1) - Brier(R3); hanya klaim yang punya keduanya.

    Kembalikan {"gap": float|None, "n_klaim": int}.
    """
    selisih = [
        isi["R1"] - isi["R3"]
        for isi in _kelompokkan_per_klaim(records).values()
        if "R1" in isi and "R3" in isi
    ]
    if not selisih:
        return {"gap": None, "n_klaim": 0}
    return {"gap": sum(selisih) / len(selisih), "n_klaim": len(selisih)}


LABEL_TYPE_BERLABEL = ("anchor", "expert")


def _skor_kelompok(p_list, kunci_list):
    """Skor untuk satu kelompok berlabel (sudah tanpa label null)."""
    n = len(p_list)
    if n == 0:
        return {"n": 0, "brier": None, "akurasi": None, "ece": None,
                "aurc": None, "nei": None}
    return {
        "n": n,
        "brier": brier_rata(p_list, kunci_list),
        "akurasi": akurasi(p_list, kunci_list),
        "ece": ece(p_list, kunci_list)["ece"],
        "aurc": aurc(p_list, kunci_list)["aurc"],
        "nei": metrik_nei(p_list, kunci_list),
    }


def ringkas_berlabel(p_list, kunci_list, tipe_list):
    """Skor HANYA pada observasi berlabel, dipisah per label_type.

    kunci None (label null, label_type 'none') dikecualikan dari skor.
    Kembalikan {tipe: skor} untuk tipe 'anchor' dan 'expert'.
    """
    if not (len(p_list) == len(kunci_list) == len(tipe_list)):
        raise ValueError("panjang p, kunci, dan label_type tidak sama")
    hasil = {}
    for tipe in LABEL_TYPE_BERLABEL:
        idx = [i for i, (k, t) in enumerate(zip(kunci_list, tipe_list))
               if k is not None and t == tipe]
        hasil[tipe] = _skor_kelompok([p_list[i] for i in idx], [kunci_list[i] for i in idx])
    return hasil


def sama_dekat(a, b, toleransi=1e-6):
    """Pembanding float untuk tes dan verifikasi silang."""
    return math.isclose(a, b, abs_tol=toleransi)
