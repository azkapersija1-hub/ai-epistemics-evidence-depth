"""Tes pipeline ujung-ke-ujung (skema JANGKAR v2) dengan MockProvider pada fixture tiruan.

Fixture: 42 klaim x 7 observasi = 294. Label jangkar: own R3 = SUPPORTED; near dan far = NEI;
own R1 dan R2 = null. Nilai harapan dihitung TANGAN dari pola mock dan label fixture.
Output mock tidak membedakan near dan far (mock hanya membaca penanda prompt), jadi selisih
near-far pada mock = 0 by construction; ini dicatat, bukan temuan.
"""
import os
import sys
import tempfile
import unittest

HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HARNESS)

import jalankan_uji_pipeline as pipa  # noqa: E402
from epis import laporan, skor  # noqa: E402
from epis.jsonl_io import baca_jsonl  # noqa: E402

_HASIL = {}


def _hasil_semua():
    """Jalankan semua mode sekali; tes lain memakai hasilnya."""
    if not _HASIL:
        folder = tempfile.mkdtemp(prefix="uji_pipeline_")
        teks, ringkas = pipa.jalankan_semua(folder_log=folder, b=200)
        _HASIL.update({"teks": teks, "ringkas": ringkas, "folder": folder})
    return _HASIL


def _skor(ringkas, pair, rung):
    return ringkas["skor"][(pair, rung)]["per_tipe"]["anchor"]


class TestFixtureDanKebocoran(unittest.TestCase):
    def test_fixture_294_observasi_dan_kebocoran_lulus(self):
        items = baca_jsonl(pipa.ITEMS)
        kunci = baca_jsonl(pipa.KUNCI)
        self.assertEqual(len(items), 294)
        self.assertEqual(len(kunci), 294)
        self.assertIn("lulus", pipa._uji_kebocoran())

    def test_komposisi_label_per_pasangan(self):
        kunci = baca_jsonl(pipa.KUNCI)
        own_r3 = [k for k in kunci if k["pair_type"] == "own" and k["rung"] == "R3"]
        self.assertEqual(len(own_r3), 42)
        self.assertTrue(all(k["label"] == "SUPPORTED" and k["label_type"] == "anchor" for k in own_r3))
        self.assertEqual(sum(1 for k in kunci if k["label"] is None), 84)  # own R1 dan R2


class TestKonservatif(unittest.TestCase):
    def test_brier_own_r3_dan_near_r1_tangan(self):
        # own R3 p=(0,2;0,2;0,6), label SUPPORTED: 0,64 + 0,04 + 0,36 = 1,04
        # near R1 p=(0,2;0,2;0,6), label NEI: 0,04 + 0,04 + 0,16 = 0,24
        r = _hasil_semua()["ringkas"]["konservatif"]
        self.assertAlmostEqual(_skor(r, "own", "R3")["brier"], 1.04, places=6)
        self.assertAlmostEqual(_skor(r, "near", "R1")["brier"], 0.24, places=6)

    def test_konsistensi_dan_false_support(self):
        # selalu sama di R1 dan R3 -> sesuai 1 ; overkomit 0 ; dS = dN = 0
        # false-support mass = p_S + p_R = 0,4 untuk near dan far
        k = _hasil_semua()["ringkas"]["konservatif"]["konsistensi"]
        self.assertAlmostEqual(k["sesuai"]["rerata"], 1.0, places=9)
        self.assertAlmostEqual(k["overkomit"]["rerata"], 0.0, places=9)
        self.assertAlmostEqual(k["dS"]["rerata"], 0.0, places=9)
        self.assertAlmostEqual(k["false_support"]["R1"]["near"]["rerata"], 0.4, places=9)
        self.assertAlmostEqual(k["false_support"]["R3"]["far"]["rerata"], 0.4, places=9)

    def test_recall_nei_near_satu(self):
        # selalu NEI -> recall NEI 1,0 pada observasi berkunci NEI
        s = _skor(_hasil_semua()["ringkas"]["konservatif"], "near", "R1")
        self.assertEqual(s["nei"]["recall_nei"], 1.0)


class TestTerluYakin(unittest.TestCase):
    def test_brier_tangan(self):
        # own R3 p=(0,9;0,05;0,05), label SUPPORTED: 0,01 + 0,0025 + 0,0025 = 0,015
        # near R1 p=(0,9;0,05;0,05), label NEI: 0,81 + 0,0025 + 0,9025 = 1,715
        r = _hasil_semua()["ringkas"]["terlalu_yakin"]
        self.assertAlmostEqual(_skor(r, "own", "R3")["brier"], 0.015, places=6)
        self.assertAlmostEqual(_skor(r, "near", "R1")["brier"], 1.715, places=6)

    def test_false_support_tinggi_dan_recall_nei_nol(self):
        # false-support mass = 0,9 + 0,05 = 0,95 ; tidak pernah memprediksi NEI -> recall 0
        r = _hasil_semua()["ringkas"]["terlalu_yakin"]
        self.assertAlmostEqual(r["konsistensi"]["false_support"]["R1"]["near"]["rerata"], 0.95, places=9)
        self.assertEqual(_skor(r, "near", "R3")["nei"]["recall_nei"], 0.0)

    def test_overkomit_nol_menurut_definisi(self):
        # terlalu_yakin tidak pernah berpindah label antara R1 dan R3 -> overkomit 0 (by definition)
        r = _hasil_semua()["ringkas"]["terlalu_yakin"]["konsistensi"]
        self.assertAlmostEqual(r["overkomit"]["rerata"], 0.0, places=9)


class TestOverkomitR1(unittest.TestCase):
    """Mode overkomit_r1: yakin SUPPORTED di R1/R2, NEI (0,2;0,1;0,7) bila ada kesimpulan (R3)."""

    def test_brier_tangan(self):
        # own R3 p=(0,2;0,1;0,7), label SUPPORTED: 0,64 + 0,01 + 0,49 = 1,14
        # near R1 p=(0,85;0,05;0,10), label NEI: 0,7225 + 0,0025 + 0,81 = 1,535
        # near R3 p=(0,2;0,1;0,7), label NEI: 0,04 + 0,01 + 0,09 = 0,14
        r = _hasil_semua()["ringkas"]["overkomit_r1"]
        self.assertAlmostEqual(_skor(r, "own", "R3")["brier"], 1.14, places=6)
        self.assertAlmostEqual(_skor(r, "near", "R1")["brier"], 1.535, places=6)
        self.assertAlmostEqual(_skor(r, "near", "R3")["brier"], 0.14, places=6)

    def test_konsistensi_overkomit_dan_pergeseran(self):
        # R1 label S (0,85 >= 0,7), R3 label NEI -> sesuai 0 ; overkomit 1
        # dS = 0,2 - 0,85 = -0,65 ; dN = 0,10 - 0,70 = -0,60
        k = _hasil_semua()["ringkas"]["overkomit_r1"]["konsistensi"]
        self.assertAlmostEqual(k["sesuai"]["rerata"], 0.0, places=9)
        self.assertAlmostEqual(k["overkomit"]["rerata"], 1.0, places=9)
        self.assertAlmostEqual(k["dS"]["rerata"], -0.65, places=6)
        self.assertAlmostEqual(k["dN"]["rerata"], -0.60, places=6)

    def test_false_support_r1_tinggi_r3_rendah(self):
        # R1: 0,85 + 0,05 = 0,90 ; R3: 0,2 + 0,1 = 0,30
        fs = _hasil_semua()["ringkas"]["overkomit_r1"]["konsistensi"]["false_support"]
        self.assertAlmostEqual(fs["R1"]["near"]["rerata"], 0.90, places=9)
        self.assertAlmostEqual(fs["R3"]["near"]["rerata"], 0.30, places=9)


class TestAcakDanRusak(unittest.TestCase):
    def test_acak_sesuai_di_antara_nol_dan_satu(self):
        k = _hasil_semua()["ringkas"]["acak"]["konsistensi"]
        self.assertGreater(k["sesuai"]["rerata"], 0.0)
        self.assertLess(k["sesuai"]["rerata"], 1.0)

    def test_rusak_gagal_percobaan_pertama_97(self):
        # Panggilan = 294 observasi + ulang. Kegagalan terjadi pada kelipatan 4.
        # Total panggilan 391 -> kelipatan 4 sampai 391 = 97. Ulang selalu sukses.
        r = _hasil_semua()["ringkas"]["rusak"]
        self.assertEqual(r["n_gagal_total"], 0)
        teks = _hasil_semua()["teks"]
        self.assertIn("Parse gagal percobaan pertama: 97", teks)


class TestLaporan(unittest.TestCase):
    def test_header_simulasi(self):
        self.assertTrue(_hasil_semua()["teks"].startswith("# SIMULASI/UJI PIPELINE, BUKAN HASIL MODEL"))

    def test_provider_non_mock_ditolak(self):
        with self.assertRaises(ValueError):
            laporan.periksa_hanya_mock([{"provider_id": "profil_qwen_plan"}])

    def test_skor_hanya_berlabel(self):
        # own R1 dan R2 tidak punya label -> tidak ada entri skor
        r = _hasil_semua()["ringkas"]["konservatif"]
        self.assertNotIn(("own", "R1"), r["skor"])
        self.assertNotIn(("own", "R2"), r["skor"])

    def test_skor_berjangkar_tidak_berubah_oleh_null(self):
        # n berlabel own R3 = 42 walaupun own R1/R2 (null) ada di data
        r = _hasil_semua()["ringkas"]["konservatif"]
        self.assertEqual(r["skor"][("own", "R3")]["n"], 42)


if __name__ == "__main__":
    unittest.main()
