"""Uji pipeline ujung-ke-ujung dengan MockProvider (SIMULASI/UJI PIPELINE, BUKAN HASIL MODEL).

Urutan: uji kebocoran pada fixture -> runner tiap mode mock -> laporan skema JANGKAR v2.
Jalankan dari folder PHASE_2_PREP:
  py -3.12 -I -X utf8 harness/jalankan_uji_pipeline.py
"""
import os
import sys

HARNESS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HARNESS)

from epis import bocor, laporan, laporan_teks, runner  # noqa: E402
from epis.jsonl_io import baca_jsonl  # noqa: E402
from epis.prompt import muat_templat  # noqa: E402
from epis.provider import MODES, MockProvider  # noqa: E402

FOLDER_FIXTURE = os.path.join(HARNESS, "fixture_tiruan")
FOLDER_LOG = os.path.join(HARNESS, "log")
ITEMS = os.path.join(FOLDER_FIXTURE, "items_model.jsonl")
KUNCI = os.path.join(FOLDER_FIXTURE, "kunci.jsonl")


def _uji_kebocoran():
    pelanggaran = bocor.jalankan_semua(ITEMS, KUNCI, metadata={"fixture": "fiktif"})
    if pelanggaran:
        raise SystemExit("uji kebocoran GAGAL: " + "; ".join(pelanggaran))
    return "uji kebocoran: lulus (0 pelanggaran)"


def jalankan_satu_mode(mode, folder_log=FOLDER_LOG, b=laporan.B_CI):
    """Kembalikan (ringkasan, jumlah_observasi, prompt_hash, gagal_percobaan_1)."""
    path_keluaran = os.path.join(folder_log, f"keluaran_mentah_{mode}.jsonl")
    runner.jalankan(ITEMS, path_keluaran, MockProvider(mode), order="claim_first",
                    ulangan=1, timpa=True)
    rows = baca_jsonl(path_keluaran)
    laporan.periksa_hanya_mock(rows)
    final = laporan.muat_keluaran_final(rows)
    records = laporan.bangun_records(baca_jsonl(ITEMS), baca_jsonl(KUNCI), final)
    ringkasan = laporan.ringkas(records, b=b)
    gagal1 = sum(1 for r in rows if r["percobaan"] == 1 and not r["parse_ok"])
    return ringkasan, len(records), muat_templat()[1], gagal1


def jalankan_semua(folder_log=FOLDER_LOG, b=laporan.B_CI):
    """Jalankan semua mode mock. Kembalikan (teks_laporan, {mode: ringkasan})."""
    os.makedirs(folder_log, exist_ok=True)
    semua, bagian = {}, []
    for mode in MODES:
        ringkasan, n, h, gagal1 = jalankan_satu_mode(mode, folder_log, b=b)
        semua[mode] = ringkasan
        bagian.append(laporan_teks.format_provider(f"mock_{mode}", n, ringkasan, h, gagal1))
    return laporan_teks.format_laporan(bagian), semua


def main():
    print(_uji_kebocoran())
    teks, _ = jalankan_semua()
    path_laporan = os.path.join(FOLDER_LOG, "laporan_uji_pipeline.md")
    with open(path_laporan, "w", encoding="utf-8", newline="\n") as f:
        f.write(teks)
    print(teks)
    print(f"\n[ditulis] {path_laporan}")


if __name__ == "__main__":
    main()
