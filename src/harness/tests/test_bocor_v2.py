"""Tes uji kebocoran untuk skema JANGKAR v2: kolom kunci baru tidak boleh ada di items_model."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import bocor  # noqa: E402

KOLOM_V2_RAHASIA = ["label", "label_type", "pair_type", "article_id", "split", "anchor_note",
                    "evidence_article_id", "risiko_jangkar", "kunci"]
ITEM_BERSIH = {"obs_id": "C1_own_R1", "claim_id": "C1", "rung": "R1", "lang": "id",
               "claim_text": "x", "evidence_text": "y"}


class TestKolomV2(unittest.TestCase):
    def test_setiap_kolom_rahasia_v2_terdeteksi(self):
        for kolom in KOLOM_V2_RAHASIA:
            hasil = bocor.periksa_kolom_items([{**ITEM_BERSIH, kolom: "isi"}])
            self.assertEqual(len(hasil), 1, msg=kolom)
            self.assertIn(kolom, hasil[0])

    def test_item_v2_bersih_lulus(self):
        self.assertEqual(bocor.periksa_kolom_items([ITEM_BERSIH]), [])

    def test_kunci_null_dan_label_type_tidak_mengubah_pengecekan_obs_id(self):
        items = [ITEM_BERSIH]
        kunci = [{"obs_id": "C1_own_R1", "claim_id": "C1", "article_id": "A1",
                  "evidence_article_id": "A1", "split": "dev", "pair_type": "own",
                  "rung": "R1", "label": None, "label_type": "none"}]
        self.assertEqual(bocor.periksa_obs_id(items, kunci), [])


if __name__ == "__main__":
    unittest.main()
