"""Tes known-answer untuk epis/skor.py.

Nilai harapan dihitung TANGAN di komentar, bukan dengan memanggil fungsi.
Notasi: p = (SUPPORTED, REFUTED, NEI), kunci = label benar.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import skor  # noqa: E402


def dist(s, r, n):
    return {"SUPPORTED": s, "REFUTED": r, "NEI": n}


class TestBrier(unittest.TestCase):
    def test_seragam_vs_satu_kelas_benar(self):
        # p=(1/3,1/3,1/3), y=(1,0,0):
        # (1/3-1)^2 + (1/3)^2 + (1/3)^2 = 4/9 + 1/9 + 1/9 = 6/9 = 0,666667
        p = dist(1 / 3, 1 / 3, 1 / 3)
        self.assertAlmostEqual(skor.brier_multikelas(p, "SUPPORTED"), 0.666667, places=6)

    def test_kelas_kedua_benar_yakin_kecil(self):
        # p=(0,05;0,9;0,05), y=(0,1,0):
        # 0,05^2 + (0,9-1)^2 + 0,05^2 = 0,0025 + 0,01 + 0,0025 = 0,015
        p = dist(0.05, 0.9, 0.05)
        self.assertAlmostEqual(skor.brier_multikelas(p, "REFUTED"), 0.015, places=9)

    def test_yakin_salah_total_pada_kelas_kedua(self):
        # p=(0,9;0,05;0,05), y=(0,1,0):
        # 0,9^2 + (0,05-1)^2 + 0,05^2 = 0,81 + 0,9025 + 0,0025 = 1,715
        p = dist(0.9, 0.05, 0.05)
        self.assertAlmostEqual(skor.brier_multikelas(p, "REFUTED"), 1.715, places=9)

    def test_prediksi_sempurna_nol(self):
        # p=(1,0,0), y=(1,0,0): 0 + 0 + 0 = 0
        self.assertEqual(skor.brier_multikelas(dist(1.0, 0.0, 0.0), "SUPPORTED"), 0.0)

    def test_salah_total_yakin_dua(self):
        # p=(0,1,0), y=(1,0,0): 1 + 1 + 0 = 2,0
        self.assertAlmostEqual(skor.brier_multikelas(dist(0.0, 1.0, 0.0), "SUPPORTED"), 2.0, places=12)

    def test_rata_rata_dua_observasi(self):
        # observasi 1: 0,0 (sempurna); observasi 2: 2,0 (salah total)
        # rata-rata = (0 + 2) / 2 = 1,0
        p_list = [dist(1.0, 0.0, 0.0), dist(0.0, 1.0, 0.0)]
        kunci = ["SUPPORTED", "SUPPORTED"]
        self.assertAlmostEqual(skor.brier_rata(p_list, kunci), 1.0, places=12)

    def test_label_tidak_dikenal_ditolak(self):
        with self.assertRaises(ValueError):
            skor.brier_multikelas(dist(1 / 3, 1 / 3, 1 / 3), "MUNGKIN")


class TestArgmaxDanAkurasi(unittest.TestCase):
    def test_seri_dengan_nei_menang(self):
        # p=(0,4;0,2;0,4): seri SUPPORTED dan NEI -> NEI menang
        self.assertEqual(skor.label_terpilih(dist(0.4, 0.2, 0.4)), "NEI")

    def test_seri_tanpa_nei_urutan_tetap(self):
        # p=(0,45;0,45;0,1): seri SUPPORTED vs REFUTED -> SUPPORTED (urutan LABELS)
        self.assertEqual(skor.label_terpilih(dist(0.45, 0.45, 0.1)), "SUPPORTED")

    def test_akurasi_dua_dari_tiga(self):
        # benar, benar, salah -> 2/3 = 0,666667
        p_list = [dist(0.7, 0.2, 0.1), dist(0.1, 0.8, 0.1), dist(0.1, 0.1, 0.8)]
        kunci = ["SUPPORTED", "REFUTED", "REFUTED"]
        self.assertAlmostEqual(skor.akurasi(p_list, kunci), 0.666667, places=6)


# Himpunan 4 observasi untuk ECE dan AURC (dihitung tangan):
#   o1: p=(0,75;0,15;0,10) pilih SUPPORTED conf 0,75; kunci SUPPORTED -> benar, bin 7
#   o2: p=(0,65;0,20;0,15) pilih SUPPORTED conf 0,65; kunci REFUTED   -> salah, bin 6
#   o3: p=(0,05;0,10;0,85) pilih NEI conf 0,85; kunci NEI             -> benar, bin 8
#   o4: p=(0,90;0,05;0,05) pilih SUPPORTED conf 0,90; kunci SUPPORTED -> benar, bin 9
ECE_SET = (
    [dist(0.75, 0.15, 0.10), dist(0.65, 0.20, 0.15), dist(0.05, 0.10, 0.85), dist(0.90, 0.05, 0.05)],
    ["SUPPORTED", "REFUTED", "NEI", "SUPPORTED"],
)


class TestECE(unittest.TestCase):
    def test_ece_empat_observasi_tangan(self):
        # Bin 6: n=1, conf 0,65, akurasi 0 -> |0-0,65| = 0,65
        # Bin 7: n=1, conf 0,75, akurasi 1 -> |1-0,75| = 0,25
        # Bin 8: n=1, conf 0,85, akurasi 1 -> |1-0,85| = 0,15
        # Bin 9: n=1, conf 0,90, akurasi 1 -> |1-0,90| = 0,10
        # ECE = (1/4)(0,65+0,25+0,15+0,10) = 1,15/4 = 0,2875
        hasil = skor.ece(*ECE_SET)
        self.assertAlmostEqual(hasil["ece"], 0.2875, places=9)

    def test_ece_mengembalikan_n_per_bin(self):
        bins = skor.ece(*ECE_SET)["bins"]
        self.assertEqual(len(bins), 10)
        self.assertEqual([b["n"] for b in bins], [0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
        self.assertIsNone(bins[0]["akurasi"])
        self.assertAlmostEqual(bins[6]["akurasi"], 0.0, places=9)

    def test_ece_sempurna_nol(self):
        # satu observasi conf 1,0 benar -> bin 9 (min dengan 9), |1-1| = 0 -> ECE 0
        hasil = skor.ece([dist(1.0, 0.0, 0.0)], ["SUPPORTED"])
        self.assertAlmostEqual(hasil["ece"], 0.0, places=12)


class TestAURC(unittest.TestCase):
    def test_aurc_salah_terakhir_empat_titik(self):
        # Urut confidence menurun (lihat ECE_SET):
        # 0,90 benar (o4); 0,85 benar (o3); 0,75 benar (o1); 0,65 salah (o2).
        # Risiko k: 0/1, 0/2, 0/3, 1/4 = 0; 0; 0; 0,25
        # AURC = (0+0+0+0,25)/4 = 0,0625
        hasil = skor.aurc(*ECE_SET)
        self.assertAlmostEqual(hasil["aurc"], 0.0625, places=9)
        self.assertEqual(hasil["kurva"][-1], (1.0, 0.25))

    def test_aurc_salah_di_atas_empat_titik(self):
        # o_A conf 0,9 SALAH; o_B conf 0,8 benar; o_C conf 0,7 SALAH; o_D conf 0,6 benar
        # Risiko k: 1/1 = 1; 1/2 = 0,5; 2/3; 2/4 = 0,5
        # Jumlah = 1 + 0,5 + 0,666667 + 0,5 = 2,666667; AURC = 2,666667/4 = 0,666667
        p_list = [
            dist(0.9, 0.05, 0.05),  # A, kunci REFUTED -> salah
            dist(0.8, 0.10, 0.10),  # B, kunci SUPPORTED -> benar
            dist(0.7, 0.20, 0.10),  # C, kunci NEI -> salah
            dist(0.6, 0.20, 0.20),  # D, kunci SUPPORTED -> benar
        ]
        kunci = ["REFUTED", "SUPPORTED", "NEI", "SUPPORTED"]
        hasil = skor.aurc(p_list, kunci)
        self.assertAlmostEqual(hasil["aurc"], 0.666667, places=6)
        self.assertAlmostEqual(hasil["kurva"][1][1], 0.5, places=9)
        self.assertAlmostEqual(hasil["kurva"][2][1], 2 / 3, places=9)


class TestNEI(unittest.TestCase):
    def test_recall_dan_presisi_nei(self):
        # o1 kunci NEI, pred NEI  (recall benar)
        # o2 kunci NEI, pred SUPPORTED (recall salah)
        # o3 kunci SUPPORTED, pred NEI (presisi salah)
        # o4 kunci NEI, pred NEI  (recall dan presisi benar)
        # Recall NEI = 2/3 ; kunci NEI = 3 (o1,o2,o4)
        # Presisi NEI = 2/3 ; pred NEI = 3 (o1,o3,o4)
        p_list = [
            dist(0.1, 0.1, 0.8),
            dist(0.8, 0.1, 0.1),
            dist(0.1, 0.1, 0.8),
            dist(0.1, 0.1, 0.8),
        ]
        kunci = ["NEI", "NEI", "SUPPORTED", "NEI"]
        hasil = skor.metrik_nei(p_list, kunci)
        self.assertEqual(hasil["n_kunci_nei"], 3)
        self.assertAlmostEqual(hasil["recall_nei"], 2 / 3, places=9)
        self.assertEqual(hasil["n_pred_nei"], 3)
        self.assertAlmostEqual(hasil["presisi_nei"], 2 / 3, places=9)

    def test_tanpa_kunci_nei_recall_none(self):
        hasil = skor.metrik_nei([dist(0.8, 0.1, 0.1)], ["SUPPORTED"])
        self.assertIsNone(hasil["recall_nei"])
        self.assertIsNone(hasil["presisi_nei"])


class TestOverconfidenceGap(unittest.TestCase):
    def test_gap_dua_klaim_tangan(self):
        # Klaim c1: R1 seragam vs kunci SUPPORTED = 0,666667;
        #           R3 (0,9;0,05;0,05) = 0,01 + 0,0025 + 0,0025 = 0,015
        #           selisih = 0,651667
        # Klaim c2: R1 (0,2;0,4;0,4) kunci REFUTED = 0,04 + 0,36 + 0,16 = 0,56;
        #           R3 (0,1;0,8;0,1) kunci REFUTED = 0,01 + 0,04 + 0,01 = 0,06;
        #           selisih = 0,50
        # Gap = (0,651667 + 0,50) / 2 = 0,575833
        records = [
            {"claim_id": "c1", "rung": "R1", "p": dist(1 / 3, 1 / 3, 1 / 3), "kunci": "SUPPORTED"},
            {"claim_id": "c1", "rung": "R3", "p": dist(0.9, 0.05, 0.05), "kunci": "SUPPORTED"},
            {"claim_id": "c2", "rung": "R1", "p": dist(0.2, 0.4, 0.4), "kunci": "REFUTED"},
            {"claim_id": "c2", "rung": "R3", "p": dist(0.1, 0.8, 0.1), "kunci": "REFUTED"},
        ]
        hasil = skor.abstract_overconfidence_gap(records)
        self.assertEqual(hasil["n_klaim"], 2)
        self.assertAlmostEqual(hasil["gap"], 0.575833, places=6)

    def test_duplikat_klaim_rung_ditolak(self):
        records = [
            {"claim_id": "c1", "rung": "R1", "p": dist(0.1, 0.1, 0.8), "kunci": "NEI"},
            {"claim_id": "c1", "rung": "R1", "p": dist(0.1, 0.1, 0.8), "kunci": "NEI"},
        ]
        with self.assertRaises(ValueError):
            skor.abstract_overconfidence_gap(records)


if __name__ == "__main__":
    unittest.main()
