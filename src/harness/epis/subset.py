"""Pemilih split: membentuk daftar items per split dari kunci (evaluasi, bukan inferensi).

Hasil berupa items tanpa kolom kunci, sehingga aman dikirim ke runner. Kunci tidak ikut.
"""
SPLITS = ("pilot", "dev", "val", "holdout")


def pilih_split(items, kunci, split):
    """Items yang obs_id-nya berada di split tertentu. Split tidak dikenal melempar ValueError."""
    if split not in SPLITS:
        raise ValueError(f"split tidak dikenal: {split!r}")
    ids = {k["obs_id"] for k in kunci if k["split"] == split}
    return [it for it in items if it["obs_id"] in ids]
