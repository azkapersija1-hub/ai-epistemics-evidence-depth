"""Analisis keluaran (mock atau nyata) per provider dan ulangan, dengan header yang sesuai.

Keluaran dari mock diberi header SIMULASI/UJI PIPELINE. Keluaran dari provider lain diberi
header HASIL MODEL (belum diverifikasi). Kunci hanya dibaca di sini (evaluasi).

Contoh (split dev, setelah jalankan_provider_nyata.py):
  py -3.12 -I -X utf8 harness/analisis_keluaran.py --split dev --model qwen3.8-flash --ulangan 1 --out harness/log/laporan_dev.md
"""
import argparse
import os
import sys

HARNESS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HARNESS)

from epis import laporan, laporan_teks  # noqa: E402
from epis.jsonl_io import baca_jsonl  # noqa: E402
from epis.subset import pilih_split  # noqa: E402

FOLDER_FIXTURE = os.path.join(HARNESS, "fixture_tiruan")
FOLDER_LOG = os.path.join(HARNESS, "log")


def bangun_parser():
    p = argparse.ArgumentParser(description="Analisis keluaran per provider dan ulangan")
    p.add_argument("--split", required=True, choices=("pilot", "dev", "val", "holdout"))
    p.add_argument("--keluaran", nargs="+", help="berkas keluaran; default: nyata_<split>_*")
    p.add_argument("--items", default=os.path.join(FOLDER_FIXTURE, "items_model.jsonl"))
    p.add_argument("--kunci", default=os.path.join(FOLDER_FIXTURE, "kunci.jsonl"))
    p.add_argument("--tau", type=float, default=0.7)
    p.add_argument("--b", type=int, default=laporan.B_CI)
    p.add_argument("--out", required=True)
    return p


def _kelompokkan(rows):
    """{(provider_id, ulangan): [baris]} agar tiap provider dan ulangan dianalisis terpisah."""
    grup = {}
    for r in rows:
        grup.setdefault((r["provider_id"], r["ulangan"]), []).append(r)
    return grup


def analisis(rows, items, kunci, tau, b):
    """Kembalikan (bagian_markdown, ada_nyata). Satu bagian per (provider, ulangan)."""
    bagian, ada_nyata = [], False
    for (provider_id, ulangan), grup in sorted(_kelompokkan(rows).items()):
        if not provider_id.startswith("mock_"):
            ada_nyata = True
        final = laporan.muat_keluaran_final(grup)
        records = laporan.bangun_records(items, kunci, final)
        ringkas = laporan.ringkas(records, tau=tau, b=b)
        gagal1 = sum(1 for r in grup if r["percobaan"] == 1 and not r["parse_ok"])
        bagian.append(laporan_teks.format_provider(
            f"{provider_id} (ulangan {ulangan})", len(records), ringkas,
            grup[0]["prompt_hash"], gagal1))
    return bagian, ada_nyata


def main(argv=None):
    args = bangun_parser().parse_args(argv)
    items_semua = baca_jsonl(args.items)
    kunci = baca_jsonl(args.kunci)
    items = pilih_split(items_semua, kunci, args.split)
    if not args.keluaran:
        print("berikan --keluaran berkas keluaran (mis. harness/log/nyata_<split>_<model>_u1.jsonl)")
        return 2
    rows = []
    for path in args.keluaran:
        rows.extend(baca_jsonl(path))
    if not rows:
        print("keluaran kosong")
        return 2
    bagian, ada_nyata = analisis(rows, items, kunci, args.tau, args.b)
    teks = laporan_teks.format_laporan(bagian, nyata=ada_nyata)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(teks)
    print(f"ditulis: {args.out} (header {'HASIL MODEL' if ada_nyata else 'SIMULASI'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
