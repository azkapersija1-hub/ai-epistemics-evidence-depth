"""Tes runner dan MockProvider (epis/runner.py, epis/provider.py)."""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import runner  # noqa: E402
from epis.jsonl_io import baca_jsonl, tulis_jsonl  # noqa: E402
from epis.provider import MockProvider, Provider  # noqa: E402

ITEMS = [
    {"obs_id": f"C{i:04d}_R1", "claim_id": f"C{i:04d}", "rung": "R1", "lang": "en",
     "claim_text": f"Klaim uji nomor {i}.", "evidence_text": f"Bukti uji nomor {i}."}
    for i in range(1, 5)
]


class ProviderNyataPalsu(Provider):
    provider_id = "palsu_nyata"
    model_id_deklarasi = "MODEL-NYATA"

    def answer(self, prompt):  # pragma: no cover - tidak boleh terpanggil
        raise AssertionError("provider nyata tidak boleh dipanggil")


class Perekam(MockProvider):
    """MockProvider yang menyimpan setiap prompt yang diterimanya."""

    def __init__(self, mode):
        super().__init__(mode)
        self.prompts = []

    def answer(self, prompt):
        self.prompts.append(prompt)
        return super().answer(prompt)


class TestMockProvider(unittest.TestCase):
    def test_mode_tidak_dikenal_ditolak(self):
        with self.assertRaises(ValueError):
            MockProvider("gaib")

    def test_konservatif_selalu_nei_dominan(self):
        out = json.loads(MockProvider("konservatif").answer("apa saja"))
        self.assertEqual(out, {"SUPPORTED": 0.2, "REFUTED": 0.2, "NEI": 0.6})

    def test_terlalu_yakin_satu_kelas_tinggi(self):
        out = json.loads(MockProvider("terlalu_yakin").answer("apa saja"))
        self.assertEqual(out["SUPPORTED"], 0.9)
        self.assertAlmostEqual(sum(out.values()), 1.0, places=9)

    def test_acak_deterministik_per_prompt(self):
        a = MockProvider("acak", seed=5).answer("prompt X")
        b = MockProvider("acak", seed=5).answer("prompt X")
        self.assertEqual(a, b)
        self.assertNotEqual(a, MockProvider("acak", seed=5).answer("prompt Y"))

    def test_acak_jumlah_dalam_toleransi(self):
        out = json.loads(MockProvider("acak").answer("prompt Z"))
        self.assertLessEqual(abs(sum(out.values()) - 1.0), 0.01)


class TestRunner(unittest.TestCase):
    def _siapkan(self, folder, items=ITEMS):
        p_items = os.path.join(folder, "items_model.jsonl")
        tulis_jsonl(p_items, items)
        return p_items, os.path.join(folder, "raw.jsonl")

    def test_provider_nyata_ditolak(self):
        with tempfile.TemporaryDirectory() as folder:
            p_items, p_out = self._siapkan(folder)
            with self.assertRaises(PermissionError) as ctx:
                runner.jalankan(p_items, p_out, ProviderNyataPalsu())
            self.assertIn("persetujuan peneliti", str(ctx.exception))
            self.assertFalse(os.path.exists(p_out))

    def test_konservatif_menulis_satu_baris_per_observasi(self):
        with tempfile.TemporaryDirectory() as folder:
            p_items, p_out = self._siapkan(folder)
            n = runner.jalankan(p_items, p_out, MockProvider("konservatif"))
            rows = baca_jsonl(p_out)
            self.assertEqual(n, 4)
            self.assertEqual(len(rows), 4)
            self.assertTrue(all(r["parse_ok"] for r in rows))
            self.assertEqual(rows[0]["provider_id"], "mock_konservatif")
            self.assertEqual(rows[0]["model_id_diminta"], "MOCK-TANPA-MODEL")
            self.assertEqual(len(rows[0]["prompt_hash"]), 64)

    def test_mode_rusak_ulang_sekali_panggilan_keempat(self):
        # Panggilan 1..3 sukses (obs 1..3). Panggilan 4 gagal (obs 4, percobaan 1).
        # Percobaan 2 = panggilan 5 sukses. Total baris = 3 + 2 = 5.
        with tempfile.TemporaryDirectory() as folder:
            p_items, p_out = self._siapkan(folder)
            n = runner.jalankan(p_items, p_out, MockProvider("rusak"))
            rows = baca_jsonl(p_out)
            self.assertEqual(n, 5)
            obs4 = [r for r in rows if r["obs_id"] == "C0004_R1"]
            self.assertEqual([r["percobaan"] for r in obs4], [1, 2])
            self.assertFalse(obs4[0]["parse_ok"])
            self.assertTrue(obs4[1]["parse_ok"])

    def test_prompt_tidak_memuat_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            p_items, p_out = self._siapkan(folder)
            perekam = Perekam("konservatif")
            runner.jalankan(p_items, p_out, perekam)
            for teks in perekam.prompts:
                self.assertNotIn("obs_id", teks)
                self.assertNotIn("R1", teks)
                self.assertNotIn("label", teks)

    def test_jalankan_ulang_adalah_resume_tanpa_baris_baru(self):
        # v2: timpa=False berarti resume. Semua (obs_id, ulangan, provider) sudah ada -> 0 baru.
        with tempfile.TemporaryDirectory() as folder:
            p_items, p_out = self._siapkan(folder)
            runner.jalankan(p_items, p_out, MockProvider("konservatif"))
            baru = runner.jalankan(p_items, p_out, MockProvider("konservatif"))
            self.assertEqual(baru, 0)
            self.assertEqual(len(baca_jsonl(p_out)), 4)

    def test_items_dengan_kolom_kunci_ditolak(self):
        bocor_items = [{**ITEMS[0], "label": "SUPPORTED"}]
        with tempfile.TemporaryDirectory() as folder:
            p_items, p_out = self._siapkan(folder, items=bocor_items)
            with self.assertRaises(ValueError):
                runner.jalankan(p_items, p_out, MockProvider("konservatif"))
            self.assertFalse(os.path.exists(p_out))


if __name__ == "__main__":
    unittest.main()
