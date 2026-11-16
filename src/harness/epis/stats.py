"""Fungsi statistik untuk rencana analisis (14_STATISTICAL_ANALYSIS_PLAN.md).

Stdlib saja. Angka di sini adalah alat hitung, bukan hasil eksperimen.
Ukuran sampel memakai asumsi sigma dan ICC yang WAJIB diestimasi dari pilot.
"""
import math
import random
from statistics import NormalDist

B_BOOTSTRAP = 2000
SEED_DEFAULT = 20261111


def selisih_berpasangan(nilai_a, nilai_b):
    """Selisih per butir antara dua kondisi: b - a (urutan sama, panjang sama)."""
    if len(nilai_a) != len(nilai_b):
        raise ValueError("panjang dua kondisi tidak sama")
    return [float(b) - float(a) for a, b in zip(nilai_a, nilai_b)]


def _kelompok_jumlah(nilai, klaster):
    """Jumlah dan banyak butir per klaster, dengan urutan klaster yang stabil."""
    jumlah, banyak = {}, {}
    for x, c in zip(nilai, klaster):
        jumlah[c] = jumlah.get(c, 0.0) + x
        banyak[c] = banyak.get(c, 0) + 1
    kunci = sorted(jumlah, key=str)
    return [jumlah[c] for c in kunci], [banyak[c] for c in kunci]


def bootstrap_klaster(nilai, klaster, b=B_BOOTSTRAP, seed=SEED_DEFAULT, alfa=0.05):
    """Bootstrap persentil berkluster (resampel klaster, mis. article_id).

    Setiap ulangan memilih jumlah klaster yang sama dengan jumlah klaster asli,
    dengan pengembalian. Estimator: rata-rata seluruh butir di klaster terpilih.
    Kembalikan {"rerata": float, "lo": float, "hi": float, "b": int}.
    """
    if len(nilai) != len(klaster):
        raise ValueError("panjang nilai dan klaster tidak sama")
    if not nilai:
        raise ValueError("data kosong")
    jumlah, banyak = _kelompok_jumlah(nilai, klaster)
    k = len(jumlah)
    rnd = random.Random(seed)
    hasil = []
    for _ in range(b):
        pilih = [rnd.randrange(k) for _ in range(k)]
        tot = sum(jumlah[i] for i in pilih)
        n = sum(banyak[i] for i in pilih)
        hasil.append(tot / n)
    hasil.sort()
    lo = hasil[int(math.floor((alfa / 2) * (b - 1)))]
    hi = hasil[int(math.ceil((1 - alfa / 2) * (b - 1)))]
    return {"rerata": sum(nilai) / len(nilai), "lo": lo, "hi": hi, "b": b}


def _jumlah_per_klaster(nilai, klaster):
    jumlah, banyak = {}, {}
    for x, c in zip(nilai, klaster):
        jumlah[c] = jumlah.get(c, 0.0) + float(x)
        banyak[c] = banyak.get(c, 0) + 1
    return jumlah, banyak


def bootstrap_selisih_klaster(nilai_a, klaster_a, nilai_b, klaster_b,
                              b=B_BOOTSTRAP, seed=SEED_DEFAULT, alfa=0.05):
    """Bootstrap selisih rerata (A - B) dengan resampel klaster BERSAMA (mis. article_id).

    Himpunan klaster dari A dan B disatukan; setiap ulangan mengambil klaster dengan
    pengembalian. Ulangan yang salah satu grupnya kosong dilewati.
    Kembalikan {"rerata", "lo", "hi", "b", "n_valid"}.
    """
    if len(nilai_a) != len(klaster_a) or len(nilai_b) != len(klaster_b):
        raise ValueError("panjang nilai dan klaster tidak sama")
    if not nilai_a or not nilai_b:
        raise ValueError("kedua grup harus punya data")
    ja, ca = _jumlah_per_klaster(nilai_a, klaster_a)
    jb, cb = _jumlah_per_klaster(nilai_b, klaster_b)
    kunci = sorted(set(ja) | set(jb), key=str)
    sa = [ja.get(k, 0.0) for k in kunci]
    na = [ca.get(k, 0) for k in kunci]
    sb = [jb.get(k, 0.0) for k in kunci]
    nb = [cb.get(k, 0) for k in kunci]
    rnd = random.Random(seed)
    k = len(kunci)
    hasil = []
    for _ in range(b):
        pilih = [rnd.randrange(k) for _ in range(k)]
        n_a = sum(na[i] for i in pilih)
        n_b = sum(nb[i] for i in pilih)
        if n_a == 0 or n_b == 0:
            continue
        hasil.append(sum(sa[i] for i in pilih) / n_a - sum(sb[i] for i in pilih) / n_b)
    if not hasil:
        raise ValueError("tidak ada ulangan valid")
    hasil.sort()
    lo = hasil[int(math.floor((alfa / 2) * (len(hasil) - 1)))]
    hi = hasil[int(math.ceil((1 - alfa / 2) * (len(hasil) - 1)))]
    titik = sum(nilai_a) / len(nilai_a) - sum(nilai_b) / len(nilai_b)
    return {"rerata": titik, "lo": lo, "hi": hi, "b": b, "n_valid": len(hasil)}


def holm(p_values, alfa=0.05):
    """Koreksi Holm. Kembalikan {"adj": [...], "tolak": [...]} dalam urutan input.

    adj_(i) = maks_{j<=i} min(1, (m - j + 1) * p_(j)) pada p terurut naik.
    """
    m = len(p_values)
    if m == 0:
        raise ValueError("daftar p kosong")
    urut = sorted(range(m), key=lambda i: p_values[i])
    adj = [0.0] * m
    maks = 0.0
    for rank, i in enumerate(urut):
        cand = min(1.0, (m - rank) * float(p_values[i]))
        maks = max(maks, cand)
        adj[i] = maks
    tolak = [a <= alfa for a in adj]
    return {"adj": adj, "tolak": tolak}


def deff(m, icc):
    """Design effect untuk m butir per klaster: 1 + (m - 1) * ICC."""
    return 1.0 + (m - 1) * icc


def n_sampel(delta, sigma, alfa=0.05, daya=0.80, deff_nilai=1.0):
    """Ukuran sampel paired.

    n_dasar = ceil(((z_{a/2} + z_b) * sigma / delta)^2), lalu
    n = ceil(DEFF * n_dasar). Urutan ini sama dengan tabel 14_STATISTICAL_ANALYSIS_PLAN.md
    (97 x 1,4 = 135,8 -> 136).
    """
    if delta <= 0 or sigma <= 0:
        raise ValueError("delta dan sigma harus positif")
    z_a = NormalDist().inv_cdf(1 - alfa / 2)
    z_b = NormalDist().inv_cdf(daya)
    n_dasar = math.ceil(((z_a + z_b) * sigma / delta) ** 2)
    return math.ceil(deff_nilai * n_dasar)


def daya_simulasi(n, delta, sigma, ulangan=800, seed=1, alfa=0.05):
    """Daya simulasi uji-z pada selisih normal (SIMULASI TEORETIS).

    Untuk setiap ulangan: n selisih ~ N(delta, sigma), hitung t, tolak bila |t| > z.
    Kembalikan proporsi penolakan.
    """
    if n < 2:
        raise ValueError("n minimal 2")
    z = NormalDist().inv_cdf(1 - alfa / 2)
    rnd = random.Random(seed)
    tolak = 0
    for _ in range(ulangan):
        d = [rnd.gauss(delta, sigma) for _ in range(n)]
        mean = sum(d) / n
        var = sum((x - mean) ** 2 for x in d) / (n - 1)
        se = math.sqrt(var / n)
        if se > 0 and abs(mean / se) > z:
            tolak += 1
    return tolak / ulangan
