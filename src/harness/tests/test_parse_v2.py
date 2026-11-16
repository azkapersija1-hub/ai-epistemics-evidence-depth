"""Tes parser v2: objek JSON TERAKHIR yang memuat label, teks penalaran sebelum JSON."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import parse  # noqa: E402


class TestObjekTerakhir(unittest.TestCase):
    def test_teks_penalaran_sebelum_json(self):
        # Teks berisi kurung kurawal bukan JSON ({draf}) dilewati; objek valid dipakai.
        raw = 'Saya pertimbangkan {draf} dulu. Jawaban: {"SUPPORTED": 0.2, "REFUTED": 0.1, "NEI": 0.7}'
        hasil = parse.parse_keluaran(raw)
        self.assertTrue(hasil["ok"])
        self.assertAlmostEqual(hasil["p"]["NEI"], 0.7, places=12)

    def test_dua_objek_json_ambil_yang_terakhir(self):
        # Objek pertama: NEI 0,8 ; objek terakhir: SUPPORTED 0,6 -> dipakai yang terakhir
        raw = ('Draf: {"SUPPORTED": 0.1, "REFUTED": 0.1, "NEI": 0.8}\n'
               'Final: {"SUPPORTED": 0.6, "REFUTED": 0.2, "NEI": 0.2}')
        hasil = parse.parse_keluaran(raw)
        self.assertTrue(hasil["ok"])
        self.assertAlmostEqual(hasil["p"]["SUPPORTED"], 0.6, places=12)

    def test_json_terakhir_terpotong_gagal(self):
        # Objek pertama lengkap, objek terakhir terpotong -> objek TERAKHIR yang memuat label
        # tidak bisa didekode, jadi hanya objek pertama yang tersisa dan dipakai.
        # Harapan: dipakai objek pertama (NEI 0,8).
        raw = '{"SUPPORTED": 0.1, "REFUTED": 0.1, "NEI": 0.8} lalu {"SUPPORTED": 0.6, "REF'
        hasil = parse.parse_keluaran(raw)
        self.assertTrue(hasil["ok"])
        self.assertAlmostEqual(hasil["p"]["NEI"], 0.8, places=12)

    def test_satu_objek_terpotong_gagal(self):
        raw = '{"SUPPORTED": 0.6, "REFUTED": 0.2, "NE'
        hasil = parse.parse_keluaran(raw)
        self.assertFalse(hasil["ok"])
        self.assertIn("tidak ada objek", hasil["error"])

    def test_keluaran_kosong_gagal(self):
        for raw in ["", "   ", None]:
            self.assertFalse(parse.parse_keluaran(raw)["ok"], msg=repr(raw))

    def test_objek_terakhir_nan_gagal_tidak_diam_diam_pakai_yang_lama(self):
        # Objek terakhir memuat NaN -> gagal (tidak jatuh ke objek sebelumnya).
        raw = '{"SUPPORTED": 0.1, "REFUTED": 0.1, "NEI": 0.8} {"SUPPORTED": NaN, "REFUTED": 0.1, "NEI": 0.9}'
        self.assertFalse(parse.parse_keluaran(raw)["ok"])

    def test_pagar_kode_dengan_penalaran(self):
        raw = "Penalaran...\n```json\n{\"SUPPORTED\": 0.97, \"REFUTED\": 0.0, \"NEI\": 0.0}\n```"
        hasil = parse.parse_keluaran(raw)
        self.assertTrue(hasil["ok"])
        self.assertTrue(hasil["normalized"])
        self.assertAlmostEqual(hasil["p"]["SUPPORTED"], 1.0, places=9)


if __name__ == "__main__":
    unittest.main()
