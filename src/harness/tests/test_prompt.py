"""Tes pembangun prompt (epis/prompt.py)."""
import hashlib
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import prompt  # noqa: E402

ITEM = {
    "obs_id": "C0007_R3", "claim_id": "C0007", "rung": "R3", "lang": "en",
    "claim_text": "Remote learning raised test scores in grade 5.",
    "evidence_text": "The trial reported a 4 point gain in grade 5 (p < .01).",
}
# Hash templat yang dicatat saat dibuat. Jika templat berubah, tes ini gagal
# dan hash baru harus dicatat di PREREG_TEMPLATE.md (bukan diam-diam diganti).
HASH_TEMPLAT_DICATAT = "0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530"


class TestIsiPrompt(unittest.TestCase):
    def test_tidak_memuat_istilah_terlarang(self):
        teks = prompt.bangun_prompt(ITEM)
        for istilah in ["R1", "R2", "R3", "label", "Label", "LABEL", "rung", "obs_id", "kunci"]:
            self.assertNotIn(istilah, teks, msg=istilah)

    def test_tidak_memuat_kolom_metadata(self):
        teks = prompt.bangun_prompt(ITEM)
        self.assertNotIn("C0007_R3", teks)
        self.assertNotIn("C0007", teks)

    def test_memuat_definisi_nei_persis(self):
        teks = prompt.bangun_prompt(ITEM)
        self.assertIn("NEI: the evidence shown is not sufficient to decide.", teks)

    def test_memuat_klaim_dan_bukti_apa_adanya(self):
        teks = prompt.bangun_prompt(ITEM)
        self.assertIn(ITEM["claim_text"], teks)
        self.assertIn(ITEM["evidence_text"], teks)

    def test_isi_yang_menyerupai_placeholder_tidak_diganti_ulang(self):
        item = {**ITEM, "claim_text": "bukan {BLOK_2} sungguhan", "evidence_text": "bukti"}
        teks = prompt.bangun_prompt(item)
        self.assertIn("bukan {BLOK_2} sungguhan", teks)

    def test_format_json_diminta(self):
        teks = prompt.bangun_prompt(ITEM)
        self.assertIn('"SUPPORTED": <number>, "REFUTED": <number>, "NEI": <number>', teks)


class TestHashDanUrutan(unittest.TestCase):
    def test_hash_stabil_dan_sesuai_catatan(self):
        _, h1 = prompt.muat_templat()
        _, h2 = prompt.muat_templat()
        self.assertEqual(h1, h2)
        self.assertEqual(h1, HASH_TEMPLAT_DICATAT)

    def test_hash_sama_dengan_sha256_berkas_mentah(self):
        path = os.path.join(prompt.TEMPLAT_DIR, prompt.TEMPLAT_DEFAULT)
        with open(path, "rb") as f:
            mentah = f.read()
        self.assertEqual(prompt.muat_templat()[1], hashlib.sha256(mentah).hexdigest())

    def test_dua_urutan_berisi_baris_yang_sama(self):
        a = prompt.bangun_prompt(ITEM, order="claim_first").splitlines()
        b = prompt.bangun_prompt(ITEM, order="evidence_first").splitlines()
        self.assertEqual(sorted(a), sorted(b))
        self.assertNotEqual(a, b)

    def test_claim_first_menempatkan_klaim_lebih_dulu(self):
        teks = prompt.bangun_prompt(ITEM, order="claim_first")
        self.assertLess(teks.index("Claim:"), teks.index("Evidence:"))

    def test_evidence_first_menempatkan_bukti_lebih_dulu(self):
        teks = prompt.bangun_prompt(ITEM, order="evidence_first")
        self.assertLess(teks.index("Evidence:"), teks.index("Claim:"))

    def test_order_tidak_dikenal_ditolak(self):
        with self.assertRaises(ValueError):
            prompt.bangun_prompt(ITEM, order="acak")

    def test_kolom_bukti_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            prompt.bangun_prompt({**ITEM, "evidence_text": "   "})

    def test_templat_tanpa_placeholder_sisa(self):
        teks = prompt.bangun_prompt(ITEM)
        self.assertIsNone(re.search(r"\{BLOK_[12]\}", teks))


if __name__ == "__main__":
    unittest.main()
