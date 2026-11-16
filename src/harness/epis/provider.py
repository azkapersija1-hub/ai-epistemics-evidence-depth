"""Antarmuka provider dan MockProvider.

Fase ini HANYA mengizinkan MockProvider. Adapter model nyata tidak ditulis di sini:
ia menunggu persetujuan peneliti (lihat README_HARNESS.md). MockProvider tidak
memanggil model, jaringan, atau API. Keluarannya dihasilkan dari aturan tetap.
"""
import hashlib
import json
import random

MODES = ("konservatif", "terlalu_yakin", "acak", "rusak", "overkomit_r1")
MARKA_KESIMPULAN = "Conclusion (FIKTIF)"  # ada hanya pada bukti R3 di fixture tiruan


class Provider:
    """Antarmuka kosong. Adapter nyata akan mengimplementasikan answer(prompt) -> str."""

    provider_id = "tanpa_provider"
    model_id_deklarasi = None

    def answer(self, prompt):
        raise NotImplementedError("adapter nyata menunggu persetujuan peneliti")


def _dist_json(s, r, n):
    return json.dumps({"SUPPORTED": s, "REFUTED": r, "NEI": n})


def _seed_dari_prompt(prompt, seed):
    """Seed deterministik dari teks prompt (bukan hash() yang diacak per proses)."""
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    return int(digest[:16], 16) ^ seed


class MockProvider(Provider):
    """Penjawab tiruan dengan pola yang diketahui.

    konservatif   : selalu condong ke NEI (0,2 / 0,2 / 0,6).
    terlalu_yakin : selalu yakin pada SUPPORTED (0,9 / 0,05 / 0,05).
    acak          : distribusi acak deterministik per prompt (seed tetap).
    rusak         : mode konservatif, tetapi setiap panggilan ke-4 mengembalikan teks bukan JSON.
    """

    def __init__(self, mode, seed=1):
        if mode not in MODES:
            raise ValueError(f"mode mock tidak dikenal: {mode!r}")
        self.mode = mode
        self.seed = seed
        self.provider_id = f"mock_{mode}"
        self.model_id_deklarasi = "MOCK-TANPA-MODEL"
        self._panggilan = 0

    def answer(self, prompt):
        self._panggilan += 1
        if self.mode == "konservatif":
            return _dist_json(0.2, 0.2, 0.6)
        if self.mode == "terlalu_yakin":
            return _dist_json(0.9, 0.05, 0.05)
        if self.mode == "acak":
            return self._acak(prompt)
        if self.mode == "overkomit_r1":
            # Tanpa kesimpulan (R1/R2): yakin SUPPORTED. Dengan kesimpulan (R3): NEI.
            if MARKA_KESIMPULAN in prompt:
                return _dist_json(0.2, 0.1, 0.7)
            return _dist_json(0.85, 0.05, 0.10)
        if self._panggilan % 4 == 0:
            return "maaf, saya tidak yakin dengan jawabannya"
        return _dist_json(0.2, 0.2, 0.6)

    def _acak(self, prompt):
        rnd = random.Random(_seed_dari_prompt(prompt, self.seed))
        mentah = [rnd.random() for _ in range(3)]
        total = sum(mentah)
        s, r, n = (round(x / total, 4) for x in mentah)
        return _dist_json(s, r, n)
