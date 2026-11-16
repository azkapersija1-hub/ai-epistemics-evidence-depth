"""Tes pemilih split dan gerbang CLI provider nyata. TIDAK ada panggilan model dan tidak ada jaringan.

Nilai harapan jumlah per split dihitung tangan dari fixture: 14 artikel, 3 klaim per artikel,
7 observasi per klaim. pilot = 2 artikel, dev = 6, val = 3, holdout = 3.
"""
import os
import sys
import tempfile
import unittest

HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HARNESS)

import jalankan_provider_nyata as jpn  # noqa: E402
import analisis_keluaran as ana  # noqa: E402
from epis import runner  # noqa: E402
from epis.jsonl_io import baca_jsonl  # noqa: E402
from epis.provider import MockProvider  # noqa: E402
from epis.subset import pilih_split  # noqa: E402

ITEMS = baca_jsonl(os.path.join(HARNESS, "fixture_tiruan", "items_model.jsonl"))
KUNCI = baca_jsonl(os.path.join(HARNESS, "fixture_tiruan", "kunci.jsonl"))


class TestPilihSplit(unittest.TestCase):
    def test_jumlah_per_split_tangan(self):
        # pilot 2x3x7 = 42 ; dev 6x3x7 = 126 ; val 3x3x7 = 63 ; holdout 3x3x7 = 63
        self.assertEqual(len(pilih_split(ITEMS, KUNCI, "pilot")), 42)
        self.assertEqual(len(pilih_split(ITEMS, KUNCI, "dev")), 126)
        self.assertEqual(len(pilih_split(ITEMS, KUNCI, "val")), 63)
        self.assertEqual(len(pilih_split(ITEMS, KUNCI, "holdout")), 63)

    def test_split_saling_lepas_dan_menutup_semua(self):
        total = sum(len(pilih_split(ITEMS, KUNCI, s)) for s in ("pilot", "dev", "val", "holdout"))
        self.assertEqual(total, 294)

    def test_subset_tanpa_kolom_kunci(self):
        for it in pilih_split(ITEMS, KUNCI, "pilot"):
            self.assertNotIn("label", it)
            self.assertNotIn("split", it)

    def test_split_tidak_dikenal_ditolak(self):
        with self.assertRaises(ValueError):
            pilih_split(ITEMS, KUNCI, "rahasia")


class TestGerbangCli(unittest.TestCase):
    def test_tanpa_flag_dan_env_berhenti_kode_3_tanpa_menulis(self):
        with tempfile.TemporaryDirectory() as folder:
            lama = jpn.FOLDER_LOG
            jpn.FOLDER_LOG = folder
            try:
                kode = jpn.main(["--split", "pilot", "--model", "uji-model", "--limit", "2"])
            finally:
                jpn.FOLDER_LOG = lama
            self.assertEqual(kode, jpn.KODE_TERKUNCI)
            self.assertEqual(os.listdir(folder), [])

    def test_holdout_tanpa_konfirmasi_ditolak(self):
        self.assertEqual(jpn.main(["--split", "holdout", "--model", "uji-model"]), jpn.KODE_HOLDOUT)

    def test_holdout_yang_sudah_ada_tidak_diulang(self):
        with tempfile.TemporaryDirectory() as folder:
            lama = jpn.FOLDER_LOG
            jpn.FOLDER_LOG = folder
            try:
                open(os.path.join(folder, "nyata_holdout_uji-model_u1.jsonl"), "w").close()
                kode = jpn.main(["--split", "holdout", "--model", "uji-model",
                                 "--konfirmasi-holdout-sekali"])
            finally:
                jpn.FOLDER_LOG = lama
            self.assertEqual(kode, jpn.KODE_HOLDOUT)


class TestAnalisis(unittest.TestCase):
    def _rows_mock(self, folder):
        out = os.path.join(folder, "k.jsonl")
        runner.jalankan(os.path.join(HARNESS, "fixture_tiruan", "items_model.jsonl"), out,
                        MockProvider("konservatif"), timpa=True)
        return baca_jsonl(out)

    def test_header_simulasi_untuk_mock(self):
        with tempfile.TemporaryDirectory() as folder:
            rows = self._rows_mock(folder)
            items = pilih_split(ITEMS, KUNCI, "pilot")
            bagian, ada_nyata = ana.analisis(rows, items, KUNCI, tau=0.7, b=100)
            self.assertFalse(ada_nyata)
            self.assertEqual(len(bagian), 1)

    def test_header_hasil_model_untuk_provider_non_mock(self):
        with tempfile.TemporaryDirectory() as folder:
            rows = self._rows_mock(folder)
            for r in rows:
                r["provider_id"] = "profil_qwen_plan"
            items = pilih_split(ITEMS, KUNCI, "pilot")
            _, ada_nyata = ana.analisis(rows, items, KUNCI, tau=0.7, b=100)
            self.assertTrue(ada_nyata)


if __name__ == "__main__":
    unittest.main()
