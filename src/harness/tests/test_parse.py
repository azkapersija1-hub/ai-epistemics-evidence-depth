"""Tes parser keluaran model (epis/parse.py). Nilai harapan dihitung tangan."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import parse  # noqa: E402

VALID = '{"SUPPORTED": 0.2, "REFUTED": 0.1, "NEI": 0.7}'


class TestParseKeluaran(unittest.TestCase):
    def test_json_valid_diterima_apa_adanya(self):
        hasil = parse.parse_keluaran(VALID)
        self.assertTrue(hasil["ok"])
        self.assertFalse(hasil["normalized"])
        self.assertAlmostEqual(hasil["jumlah_mentah"], 1.0, places=9)
        self.assertAlmostEqual(hasil["p"]["NEI"], 0.7, places=12)

    def test_pagar_kode_json_diterima(self):
        teks = "```json\n" + VALID + "\n```"
        hasil = parse.parse_keluaran(teks)
        self.assertTrue(hasil["ok"])
        self.assertAlmostEqual(hasil["p"]["SUPPORTED"], 0.2, places=12)

    def test_pagar_kode_tanpa_label_bahasa_diterima(self):
        hasil = parse.parse_keluaran("```\n" + VALID + "\n```")
        self.assertTrue(hasil["ok"])

    def test_jumlah_097_dinormalisasi_dan_diberi_bendera(self):
        # jumlah 0,97 di luar 1 +/- 0,01 -> normalisasi p_k / 0,97
        # SUPPORTED 0,2/0,97 ; REFUTED 0,1/0,97 ; NEI 0,67/0,97
        raw = '{"SUPPORTED": 0.2, "REFUTED": 0.1, "NEI": 0.67}'
        hasil = parse.parse_keluaran(raw)
        self.assertTrue(hasil["ok"])
        self.assertTrue(hasil["normalized"])
        self.assertAlmostEqual(hasil["jumlah_mentah"], 0.97, places=9)
        self.assertAlmostEqual(hasil["p"]["SUPPORTED"], 0.2 / 0.97, places=9)
        self.assertAlmostEqual(sum(hasil["p"].values()), 1.0, places=9)

    def test_jumlah_099_masih_dalam_toleransi_tanpa_normalisasi(self):
        raw = '{"SUPPORTED": 0.2, "REFUTED": 0.1, "NEI": 0.69}'
        hasil = parse.parse_keluaran(raw)
        self.assertTrue(hasil["ok"])
        self.assertFalse(hasil["normalized"])

    def test_jumlah_13_dinormalisasi(self):
        # jumlah 1,3 -> normalisasi; SUPPORTED 0,5/1,3 = 0,384615
        raw = '{"SUPPORTED": 0.5, "REFUTED": 0.4, "NEI": 0.4}'
        hasil = parse.parse_keluaran(raw)
        self.assertTrue(hasil["ok"])
        self.assertTrue(hasil["normalized"])
        self.assertAlmostEqual(hasil["p"]["SUPPORTED"], 0.5 / 1.3, places=9)

    def test_label_hilang_gagal(self):
        hasil = parse.parse_keluaran('{"SUPPORTED": 0.5, "REFUTED": 0.5}')
        self.assertFalse(hasil["ok"])
        self.assertIn("NEI", hasil["error"])

    def test_label_asing_gagal(self):
        raw = '{"SUPPORTED": 0.4, "REFUTED": 0.3, "NEI": 0.2, "MAYBE": 0.1}'
        self.assertFalse(parse.parse_keluaran(raw)["ok"])

    def test_teks_bukan_json_gagal(self):
        hasil = parse.parse_keluaran("Saya rasa ini SUPPORTED.")
        self.assertFalse(hasil["ok"])
        self.assertIsNone(hasil["p"])

    def test_nan_gagal(self):
        raw = '{"SUPPORTED": NaN, "REFUTED": 0.1, "NEI": 0.9}'
        hasil = parse.parse_keluaran(raw)
        self.assertFalse(hasil["ok"])

    def test_infinity_gagal(self):
        raw = '{"SUPPORTED": Infinity, "REFUTED": 0.1, "NEI": 0.9}'
        self.assertFalse(parse.parse_keluaran(raw)["ok"])

    def test_nilai_negatif_gagal(self):
        raw = '{"SUPPORTED": -0.2, "REFUTED": 0.6, "NEI": 0.6}'
        self.assertFalse(parse.parse_keluaran(raw)["ok"])

    def test_nilai_string_gagal(self):
        raw = '{"SUPPORTED": "0.2", "REFUTED": 0.1, "NEI": 0.7}'
        self.assertFalse(parse.parse_keluaran(raw)["ok"])

    def test_nilai_boolean_gagal(self):
        raw = '{"SUPPORTED": true, "REFUTED": 0.0, "NEI": 0.0}'
        self.assertFalse(parse.parse_keluaran(raw)["ok"])

    def test_jumlah_nol_gagal(self):
        raw = '{"SUPPORTED": 0, "REFUTED": 0, "NEI": 0}'
        self.assertFalse(parse.parse_keluaran(raw)["ok"])

    def test_akar_bukan_objek_gagal(self):
        self.assertFalse(parse.parse_keluaran("[0.2, 0.1, 0.7]")["ok"])


class TestBrierDuaBatas(unittest.TestCase):
    def test_dua_batas_dengan_satu_gagal(self):
        # obs1 ok p=(1,0,0) kunci SUPPORTED -> BS 0
        # obs2 gagal
        # obs3 ok p=(0,1,0) kunci SUPPORTED -> BS 2,0
        # Batas 1 (gagal dikeluarkan): (0 + 2) / 2 = 1,0
        # Batas 2 (gagal = 2,0): (0 + 2,0 + 2,0) / 3 = 1,333333
        hasil_list = [
            parse.parse_keluaran('{"SUPPORTED": 1, "REFUTED": 0, "NEI": 0}'),
            parse.parse_keluaran("bukan json"),
            parse.parse_keluaran('{"SUPPORTED": 0, "REFUTED": 1, "NEI": 0}'),
        ]
        kunci = ["SUPPORTED", "SUPPORTED", "SUPPORTED"]
        hasil = parse.brier_dua_batas(hasil_list, kunci)
        self.assertAlmostEqual(hasil["batas1_tanpa_gagal"], 1.0, places=9)
        self.assertAlmostEqual(hasil["batas2_gagal_bs2"], 4 / 3, places=9)
        self.assertEqual(hasil["n_gagal"], 1)
        self.assertEqual(hasil["n_total"], 3)

    def test_semua_gagal_batas1_none(self):
        hasil_list = [parse.parse_keluaran("x"), parse.parse_keluaran("y")]
        hasil = parse.brier_dua_batas(hasil_list, ["NEI", "NEI"])
        self.assertIsNone(hasil["batas1_tanpa_gagal"])
        self.assertAlmostEqual(hasil["batas2_gagal_bs2"], 2.0, places=12)


if __name__ == "__main__":
    unittest.main()
