"""Tes uji kebocoran (epis/bocor.py). Data bersih dibangun di folder sementara."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import bocor  # noqa: E402
from epis.jsonl_io import tulis_jsonl  # noqa: E402

BERSIH_ITEMS = [
    {"obs_id": "C1_R1", "claim_id": "C1", "rung": "R1", "lang": "en",
     "claim_text": "x", "evidence_text": "y"},
    {"obs_id": "C2_R1", "claim_id": "C2", "rung": "R1", "lang": "id",
     "claim_text": "x2", "evidence_text": "y2"},
]
BERSIH_KUNCI = [
    {"obs_id": "C1_R1", "claim_id": "C1", "article_id": "A1", "split": "dev",
     "label": "SUPPORTED", "annotator_agreement": None},
    {"obs_id": "C2_R1", "claim_id": "C2", "article_id": "A2", "split": "val",
     "label": "NEI", "annotator_agreement": None},
]


class TestPeriksaFungsi(unittest.TestCase):
    def test_kolom_bersih_lulus(self):
        self.assertEqual(bocor.periksa_kolom_items(BERSIH_ITEMS), [])

    def test_setiap_kolom_terlarang_terdeteksi(self):
        for kolom in ["label", "kunci", "answer", "split", "article_id", "annotator_agreement"]:
            item = [{**BERSIH_ITEMS[0], kolom: "isi"}]
            hasil = bocor.periksa_kolom_items(item)
            self.assertEqual(len(hasil), 1, msg=kolom)
            self.assertIn(kolom, hasil[0])

    def test_nama_berkas_dengan_label_terdeteksi(self):
        hasil = bocor.periksa_nama_dan_metadata("items_REFUTED.jsonl", {})
        self.assertEqual(len(hasil), 1)
        self.assertIn("REFUTED", hasil[0])

    def test_metadata_dengan_label_terdeteksi(self):
        hasil = bocor.periksa_nama_dan_metadata("items_model.jsonl", {"catatan": "kunci NEI"})
        self.assertEqual(len(hasil), 1)

    def test_nama_dan_metadata_bersih_lulus(self):
        hasil = bocor.periksa_nama_dan_metadata("items_model.jsonl", {"versi": "v1", "n": "204"})
        self.assertEqual(hasil, [])

    def test_obs_id_tidak_cocok_terdeteksi(self):
        kunci_rusak = [BERSIH_KUNCI[0], {**BERSIH_KUNCI[1], "obs_id": "C9_R1"}]
        hasil = bocor.periksa_obs_id(BERSIH_ITEMS, kunci_rusak)
        self.assertEqual(len(hasil), 2)

    def test_obs_id_cocok_lulus(self):
        self.assertEqual(bocor.periksa_obs_id(BERSIH_ITEMS, BERSIH_KUNCI), [])

    def test_artikel_di_dua_split_terdeteksi(self):
        kunci_rusak = [BERSIH_KUNCI[0], {**BERSIH_KUNCI[1], "article_id": "A1"}]
        hasil = bocor.periksa_split_artikel(kunci_rusak)
        self.assertEqual(len(hasil), 1)
        self.assertIn("A1", hasil[0])

    def test_artikel_satu_split_lulus(self):
        self.assertEqual(bocor.periksa_split_artikel(BERSIH_KUNCI), [])


class TestJalankanSemuaDariBerkas(unittest.TestCase):
    def _tulis(self, folder, items, kunci):
        p_items = os.path.join(folder, "items_model.jsonl")
        p_kunci = os.path.join(folder, "kunci.jsonl")
        tulis_jsonl(p_items, items)
        tulis_jsonl(p_kunci, kunci)
        return p_items, p_kunci

    def test_data_bersih_lulus_dari_berkas(self):
        with tempfile.TemporaryDirectory() as folder:
            p_items, p_kunci = self._tulis(folder, BERSIH_ITEMS, BERSIH_KUNCI)
            self.assertEqual(bocor.jalankan_semua(p_items, p_kunci, metadata={"versi": "v1"}), [])

    def test_data_dengan_kebocoran_terdeteksi_dari_berkas(self):
        with tempfile.TemporaryDirectory() as folder:
            items_bocor = [{**BERSIH_ITEMS[0], "label": "SUPPORTED"}, BERSIH_ITEMS[1]]
            p_items, p_kunci = self._tulis(folder, items_bocor, BERSIH_KUNCI)
            hasil = bocor.jalankan_semua(p_items, p_kunci)
            self.assertTrue(any(h.startswith("(a)") for h in hasil))


if __name__ == "__main__":
    unittest.main()
