"""Laporan ujung-ke-ujung (skema JANGKAR v2): items, kunci, dan keluaran mentah.

Dipanggil SETELAH inferensi. Kunci hanya dibaca di sini (evaluasi), tidak pernah dikirim
ke provider. Skor (Brier, akurasi, ECE, AURC, NEI) hanya pada observasi berlabel
(label_type anchor atau expert). Observasi label null hanya dipakai di metrik pergeseran
(konsistensi.py). Keluaran dari mock diberi header SIMULASI.
"""
from epis import konsistensi, parse, skor, stats

HEADER_SIMULASI = "SIMULASI/UJI PIPELINE, BUKAN HASIL MODEL"
URUTAN_PAIR = ("own", "near", "far")
URUTAN_RUNG = ("R1", "R2", "R3")
B_CI = 2000


def periksa_hanya_mock(rows):
    """Tolak laporan bila ada keluaran dari provider yang bukan mock (sebelum adapter dibuka)."""
    for r in rows:
        if not str(r["provider_id"]).startswith("mock_"):
            raise ValueError(f"provider non-mock di keluaran: {r['provider_id']}")


def muat_keluaran_final(rows):
    """Untuk tiap obs_id, pakai percobaan terakhir (setelah ulang bila ada)."""
    final = {}
    for r in rows:
        lama = final.get(r["obs_id"])
        if lama is None or r["percobaan"] > lama["percobaan"]:
            final[r["obs_id"]] = r
    return final


def bangun_records(items, kunci, final):
    """Gabungkan items, kunci, dan keluaran akhir. Keluaran yang hilang melempar error."""
    kunci_map = {k["obs_id"]: k for k in kunci}
    records = []
    for it in items:
        k = kunci_map.get(it["obs_id"])
        f = final.get(it["obs_id"])
        if k is None or f is None:
            raise ValueError(f"data tidak lengkap untuk {it['obs_id']}")
        ok = bool(f["parse_ok"])
        records.append({
            "obs_id": it["obs_id"], "claim_id": it["claim_id"], "rung": it["rung"],
            "lang": it["lang"], "pair_type": k["pair_type"], "article_id": k["article_id"],
            "label": k["label"], "label_type": k["label_type"],
            "ok": ok, "p": f["p"] if ok else None,
            "normalized": bool(f["normalized"]),
        })
    return records


def _kelompok(records):
    """{(pair, rung): [records berlabel]} untuk observasi yang punya label (bukan null)."""
    grup = {}
    for r in records:
        if r["label"] is None:
            continue
        grup.setdefault((r["pair_type"], r["rung"]), []).append(r)
    return grup


def _skor_grup(recs, b):
    """Skor berlabel untuk satu (pair, rung): per label_type, dua batas, dan CI Brier."""
    valid = [r for r in recs if r["ok"]]
    per_tipe = skor.ringkas_berlabel(
        [r["p"] for r in valid], [r["label"] for r in valid], [r["label_type"] for r in valid])
    dua = parse.brier_dua_batas(
        [{"ok": r["ok"], "p": r["p"], "normalized": r["normalized"]} for r in recs],
        [r["label"] for r in recs])
    ci = None
    if valid:
        nilai = [skor.brier_multikelas(r["p"], r["label"]) for r in valid]
        ci = stats.bootstrap_klaster(nilai, [r["article_id"] for r in valid], b=b)
    return {
        "n": len(recs), "n_gagal": len(recs) - len(valid),
        "brier_batas1": dua["batas1_tanpa_gagal"], "brier_batas2": dua["batas2_gagal_bs2"],
        "ci_brier": ci, "per_tipe": per_tipe,
    }


def skor_berjangkar(records, b=B_CI):
    """{(pair, rung): ringkasan_grup} untuk setiap kelompok yang punya label."""
    grup = _kelompok(records)
    return {
        (pair, rung): _skor_grup(grup[(pair, rung)], b)
        for pair in URUTAN_PAIR for rung in URUTAN_RUNG
        if (pair, rung) in grup
    }


def ringkas(records, tau=konsistensi.DEFAULT_TAU, b=B_CI):
    """Semua metrik untuk satu provider: skor berjangkar, konsistensi, dan per bahasa."""
    return {
        "skor": skor_berjangkar(records, b=b),
        "konsistensi": konsistensi.ringkas(records, tau=tau, b=b),
        "per_bahasa": konsistensi.ringkas_per_bahasa(records, tau=tau, b=b),
        "n_gagal_total": sum(1 for r in records if not r["ok"]),
    }
