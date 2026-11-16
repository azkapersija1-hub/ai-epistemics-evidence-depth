"""Tes epis/stats.py. Nilai harapan dihitung tangan atau dicocokkan dengan
tabel 14_STATISTICAL_ANALYSIS_PLAN.md dan agent_b_calc.py (verifikasi silang)."""
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import stats  # noqa: E402


class TestUkuranSampel(unittest.TestCase):
    def test_delta_010_sigma_035_menjadi_97(self):
        # (2,801585 * 0,35 / 0,10)^2 = 96,15 -> 97 (tabel dan agent_b_calc)
        self.assertEqual(stats.n_sampel(0.10, 0.35), 97)

    def test_delta_005_sigma_035_menjadi_385(self):
        # (2,801585 * 0,35 / 0,05)^2 = 384,6 -> 385
        self.assertEqual(stats.n_sampel(0.05, 0.35), 385)

    def test_delta_002_sigma_035_menjadi_2404(self):
        # (2,801585 * 0,35 / 0,02)^2 = 2403,7 -> 2404 (tabel 14)
        self.assertEqual(stats.n_sampel(0.02, 0.35), 2404)

    def test_deff_14_delta_010_menjadi_136(self):
        # n_dasar 97 x 1,4 = 135,8 -> 136 (tabel 14)
        self.assertEqual(stats.n_sampel(0.10, 0.35, deff_nilai=1.4), 136)

    def test_deff_14_delta_005_menjadi_539(self):
        # n_dasar 385 x 1,4 = 539,0 -> 539 (tabel 14)
        self.assertEqual(stats.n_sampel(0.05, 0.35, deff_nilai=1.4), 539)

    def test_sigma_nol_ditolak(self):
        with self.assertRaises(ValueError):
            stats.n_sampel(0.05, 0.0)


class TestDEFF(unittest.TestCase):
    def test_m3_icc02_menjadi_14(self):
        # 1 + (3 - 1) * 0,2 = 1,4
        self.assertAlmostEqual(stats.deff(3, 0.2), 1.4, places=12)

    def test_m1_selalu_satu(self):
        self.assertAlmostEqual(stats.deff(1, 0.9), 1.0, places=12)


class TestHolm(unittest.TestCase):
    def test_holm_contoh_tangan(self):
        # p = [0,01; 0,04; 0,03], m = 3, urut naik: 0,01 (rank1), 0,03 (rank2), 0,04 (rank3)
        # adj rank1 = 3 * 0,01 = 0,03
        # adj rank2 = 2 * 0,03 = 0,06 ; maks tetap 0,06
        # adj rank3 = 1 * 0,04 = 0,04 -> maks tetap 0,06
        # Dalam urutan input: p0 -> 0,03 ; p1 -> 0,06 ; p2 -> 0,06
        # Tolak pada alfa 0,05: hanya p0
        hasil = stats.holm([0.01, 0.04, 0.03], alfa=0.05)
        self.assertAlmostEqual(hasil["adj"][0], 0.03, places=12)
        self.assertAlmostEqual(hasil["adj"][1], 0.06, places=12)
        self.assertAlmostEqual(hasil["adj"][2], 0.06, places=12)
        self.assertEqual(hasil["tolak"], [True, False, False])

    def test_holm_dibatasi_satu(self):
        # p = [0,6; 0,001]: adj 0,001*2 = 0,002 ; adj 0,6*1 = 0,6 -> min 1
        hasil = stats.holm([0.6, 0.001])
        self.assertAlmostEqual(hasil["adj"][1], 0.002, places=12)
        self.assertAlmostEqual(hasil["adj"][0], 0.6, places=12)


class TestSelisihDanBootstrap(unittest.TestCase):
    def test_selisih_berpasangan_b_minus_a(self):
        self.assertEqual(stats.selisih_berpasangan([0.5, 1.0], [0.25, 1.5]), [-0.25, 0.5])

    def test_bootstrap_deterministik_dengan_seed(self):
        nilai = [0.1, 0.2, -0.1, 0.4, 0.0, 0.3]
        klaster = ["a", "a", "b", "b", "c", "c"]
        h1 = stats.bootstrap_klaster(nilai, klaster, b=300, seed=7)
        h2 = stats.bootstrap_klaster(nilai, klaster, b=300, seed=7)
        self.assertEqual(h1, h2)

    def test_bootstrap_mencakup_rerata(self):
        nilai = [0.1, 0.2, -0.1, 0.4, 0.0, 0.3]
        klaster = ["a", "a", "b", "b", "c", "c"]
        h = stats.bootstrap_klaster(nilai, klaster, b=500, seed=3)
        self.assertAlmostEqual(h["rerata"], 0.15, places=12)
        self.assertLessEqual(h["lo"], h["rerata"])
        self.assertGreaterEqual(h["hi"], h["rerata"])

    def test_bootstrap_nilai_konstan_ciutnya_nol(self):
        nilai = [0.5] * 4
        klaster = ["x", "x", "y", "y"]
        h = stats.bootstrap_klaster(nilai, klaster, b=100, seed=1)
        self.assertAlmostEqual(h["lo"], 0.5, places=12)
        self.assertAlmostEqual(h["hi"], 0.5, places=12)

    def test_bootstrap_efek_nol_mencakup_nol_pada_minimal_90_persen(self):
        """200 dataset sintetis dengan efek nol (klaster artikel + galat).

        Setiap dataset: 30 artikel x 3 klaim. Selisih = efek_artikel + galat,
        keduanya mean nol. Ukur proporsi CI 95% yang memuat nol.
        """
        rnd = random.Random(20261111)
        memuat_nol = 0
        ulangan = 200
        for r in range(ulangan):
            nilai, klaster = [], []
            for a in range(30):
                efek = rnd.gauss(0.0, 0.10)
                for _ in range(3):
                    nilai.append(efek + rnd.gauss(0.0, 0.30))
                    klaster.append(f"A{a:03d}")
            h = stats.bootstrap_klaster(nilai, klaster, b=2000, seed=r)
            if h["lo"] <= 0.0 <= h["hi"]:
                memuat_nol += 1
        proporsi = memuat_nol / ulangan
        print(f"\n[bootstrap nol] CI memuat 0 pada {memuat_nol}/{ulangan} = {proporsi:.3f}")
        self.assertGreaterEqual(proporsi, 0.90)


class TestDayaSimulasi(unittest.TestCase):
    def test_efek_nol_daya_sekitar_alfa(self):
        p = stats.daya_simulasi(n=200, delta=0.0, sigma=0.35, ulangan=800, seed=1)
        self.assertLess(p, 0.10)

    def test_daya_naik_seiring_n(self):
        p100 = stats.daya_simulasi(n=100, delta=0.05, sigma=0.35, ulangan=400, seed=1)
        p400 = stats.daya_simulasi(n=400, delta=0.05, sigma=0.35, ulangan=400, seed=1)
        self.assertLess(p100, p400)


if __name__ == "__main__":
    unittest.main()
