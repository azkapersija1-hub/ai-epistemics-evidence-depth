"""Tes skor berlabel (label null dikecualikan) dan bootstrap selisih klaster."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import skor, stats  # noqa: E402


def d(s, r, n):
    return {"SUPPORTED": s, "REFUTED": r, "NEI": n}


class TestRingkasBerlabel(unittest.TestCase):
    def test_label_null_dikecualikan_dari_skor(self):
        # anchor SUPPORTED p=(0,9;0,05;0,05): BS = 0,01+0,0025+0,0025 = 0,015
        # anchor NEI p=(0,2;0,2;0,6): BS = 0,04+0,04+0,16 = 0,24 ; rata-rata anchor = 0,1275
        # observasi null (kunci None, label_type none) diabaikan total
        # tidak ada expert -> n=0 dan brier None
        p = [d(0.9, 0.05, 0.05), d(0.2, 0.2, 0.6), d(0.1, 0.1, 0.8)]
        kunci = ["SUPPORTED", "NEI", None]
        tipe = ["anchor", "anchor", "none"]
        hasil = skor.ringkas_berlabel(p, kunci, tipe)
        self.assertEqual(hasil["anchor"]["n"], 2)
        self.assertAlmostEqual(hasil["anchor"]["brier"], 0.1275, places=9)
        self.assertEqual(hasil["expert"]["n"], 0)
        self.assertIsNone(hasil["expert"]["brier"])

    def test_pisah_per_label_type(self):
        # expert: REFUTED p=(0,05;0,9;0,05): BS = 0,0025+0,01+0,0025 = 0,015
        p = [d(0.9, 0.05, 0.05), d(0.05, 0.9, 0.05)]
        kunci = ["SUPPORTED", "REFUTED"]
        tipe = ["anchor", "expert"]
        hasil = skor.ringkas_berlabel(p, kunci, tipe)
        self.assertAlmostEqual(hasil["anchor"]["brier"], 0.015, places=9)
        self.assertAlmostEqual(hasil["expert"]["brier"], 0.015, places=9)
        self.assertEqual(hasil["anchor"]["n"], 1)

    def test_brier_null_ditolak_langsung(self):
        with self.assertRaises(ValueError):
            skor.brier_multikelas(d(0.2, 0.2, 0.6), None)

    def test_panjang_tidak_sama_ditolak(self):
        with self.assertRaises(ValueError):
            skor.ringkas_berlabel([d(1, 0, 0)], [], ["anchor"])


class TestBootstrapSelisih(unittest.TestCase):
    def test_selisih_konstan_tangan(self):
        # A = [1, 1] (klaster a1, a2); B = [0, 0] (klaster a1, a2)
        # Setiap ulangan: rerata A - rerata B = 1 - 0 = 1 -> CI [1, 1], rerata 1
        h = stats.bootstrap_selisih_klaster([1.0, 1.0], ["a1", "a2"],
                                            [0.0, 0.0], ["a1", "a2"], b=300, seed=2)
        self.assertAlmostEqual(h["rerata"], 1.0, places=12)
        self.assertAlmostEqual(h["lo"], 1.0, places=12)
        self.assertAlmostEqual(h["hi"], 1.0, places=12)

    def test_selisih_titik_tangan_klaster_berbeda(self):
        # A = [0,6 (a1), 0,2 (a2)] -> rerata 0,4 ; B = [0,1 (a1)] -> rerata 0,1
        # titik estimasi = 0,4 - 0,1 = 0,3
        h = stats.bootstrap_selisih_klaster([0.6, 0.2], ["a1", "a2"], [0.1], ["a1"], b=200)
        self.assertAlmostEqual(h["rerata"], 0.3, places=12)

    def test_grup_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            stats.bootstrap_selisih_klaster([], [], [1.0], ["a"])


if __name__ == "__main__":
    unittest.main()
