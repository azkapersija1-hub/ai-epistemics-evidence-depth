"""Tes adapter terkunci (ProfilProvider) dan runner v2: gerbang, resume, retry, konkurensi.

TIDAK ADA panggilan model asli dan tidak ada jaringan. model_api diganti modul PALSU yang
disuntikkan ke sys.modules dengan signature yang sama dengan api_chat di sakti_core.
"""
import json
import os
import sys
import tempfile
import types
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import provider_profil, runner  # noqa: E402
from epis.jsonl_io import baca_jsonl, tulis_jsonl  # noqa: E402
from epis.provider_profil import ENV_IZIN, FLAG_CLI, ProfilProvider  # noqa: E402

ITEMS = [
    {"obs_id": f"C{i:04d}_own_R1", "claim_id": f"C{i:04d}", "rung": "R1", "lang": "id",
     "claim_text": f"Klaim uji {i}.", "evidence_text": f"Bukti uji {i}."}
    for i in range(1, 5)
]
JAWABAN_VALID = '{"SUPPORTED": 0.2, "REFUTED": 0.2, "NEI": 0.6}'


class ApiPalsu:
    """Pengganti api_chat dengan signature sama. Mencatat setiap panggilan."""

    def __init__(self, skrip=None):
        self.panggilan = []
        self._skrip = skrip  # fungsi (indeks_panggilan) -> str atau raise

    def __call__(self, nama, prompt, *, konten, max_tokens=512, model=None, timeout=60):
        self.panggilan.append({"nama": nama, "konten": konten, "max_tokens": max_tokens,
                               "model": model, "timeout": timeout})
        if self._skrip is None:
            return JAWABAN_VALID
        return self._skrip(len(self.panggilan))


def _pasang_modul_palsu(api):
    """Kembalikan (modul_palsu_lama) agar bisa dipulihkan. Modul palsu memakai signature asli."""
    modul = types.ModuleType("model_api")
    modul.api_chat = api
    lama = sys.modules.get("model_api")
    sys.modules["model_api"] = modul
    return lama


def _pulihkan(lama):
    if lama is None:
        sys.modules.pop("model_api", None)
    else:
        sys.modules["model_api"] = lama


def _env_izin():
    return {ENV_IZIN: "1"}


class _Berkas(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = self._tmp.name
        self.p_items = os.path.join(self.folder, "items.jsonl")
        tulis_jsonl(self.p_items, ITEMS)
        self.p_out = os.path.join(self.folder, "raw.jsonl")

    def tearDown(self):
        self._tmp.cleanup()


class TestGerbangProfil(unittest.TestCase):
    def test_tanpa_flag_dan_env_ditolak(self):
        with self.assertRaises(PermissionError):
            ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=False, environ={})

    def test_flag_tanpa_env_ditolak(self):
        with self.assertRaises(PermissionError):
            ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=True, environ={})

    def test_env_tanpa_flag_ditolak(self):
        with self.assertRaises(PermissionError):
            ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=False, environ=_env_izin())

    def test_env_bukan_satu_ditolak(self):
        with self.assertRaises(PermissionError):
            ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=True, environ={ENV_IZIN: "0"})

    def test_izin_aktif_hanya_dengan_kedua_syarat(self):
        self.assertTrue(provider_profil.izin_aktif([FLAG_CLI], _env_izin()))
        self.assertFalse(provider_profil.izin_aktif([], _env_izin()))
        self.assertFalse(provider_profil.izin_aktif([FLAG_CLI], {}))

    def test_konstruksi_tidak_memuat_model_api(self):
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        try:
            ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=True, environ=_env_izin())
            self.assertEqual(api.panggilan, [])
        finally:
            _pulihkan(lama)


class TestPanggilanProfil(unittest.TestCase):
    def test_argumen_api_chat_sesuai_signature(self):
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        try:
            prov = ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=True, environ=_env_izin())
            keluaran = prov.answer("prompt uji")
        finally:
            _pulihkan(lama)
        self.assertEqual(keluaran, JAWABAN_VALID)
        self.assertEqual(api.panggilan, [{"nama": "qwen_plan", "konten": True, "max_tokens": 512,
                                          "model": "qwen3.8-flash", "timeout": 60}])

    def test_temperature_dan_thinking_tidak_didukung_dicatat(self):
        # Signature palsu meniru api_chat asli: tidak ada temperature / thinking.
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        try:
            prov = ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=True, environ=_env_izin())
            prov.answer("p")
        finally:
            _pulihkan(lama)
        self.assertEqual(prov.param_didukung,
                         {"temperature": False, "thinking": False, "enable_thinking": False})

    def test_sys_path_tidak_tercemar(self):
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        sebelum = list(sys.path)
        try:
            prov = ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=True, environ=_env_izin())
            prov.answer("p")
        finally:
            _pulihkan(lama)
        self.assertEqual(sys.path, sebelum)

    def test_keluaran_bukan_string_ditolak(self):
        lama = _pasang_modul_palsu(lambda *a, **k: {"bukan": "string"})
        try:
            prov = ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=True, environ=_env_izin())
            with self.assertRaises(TypeError):
                prov.answer("p")
        finally:
            _pulihkan(lama)


class TestRunnerProfil(_Berkas):
    def _prov(self, **kw):
        return ProfilProvider("qwen_plan", "qwen3.8-flash", izin_cli=True, environ=_env_izin(), **kw)

    def test_runner_menerima_profil_dan_mencatat_meta(self):
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        try:
            n = runner.jalankan(self.p_items, self.p_out, self._prov(), sleep=lambda s: None)
        finally:
            _pulihkan(lama)
        rows = baca_jsonl(self.p_out)
        self.assertEqual(n, 4)
        self.assertTrue(all(r["parse_ok"] for r in rows))
        self.assertEqual(rows[0]["provider_id"], "profil_qwen_plan")
        self.assertEqual(rows[0]["model_id_diminta"], "qwen3.8-flash")
        self.assertIn("latensi_s", rows[0])
        self.assertEqual(rows[0]["panjang_keluaran"], len(JAWABAN_VALID))
        self.assertIsNone(rows[0]["panggilan_error"])

    def test_retry_backoff_eksponensial_lalu_berhasil(self):
        # Panggilan 1 dan 2 gagal, panggilan 3 berhasil. Backoff: 1,0 lalu 2,0 detik.
        def skrip(i):
            if i <= 2:
                raise ConnectionError("gangguan uji")
            return JAWABAN_VALID
        api = ApiPalsu(skrip)
        lama = _pasang_modul_palsu(api)
        tidur = []
        try:
            runner.jalankan(self.p_items, self.p_out, self._prov(), sleep=tidur.append)
        finally:
            _pulihkan(lama)
        self.assertEqual(tidur[:2], [1.0, 2.0])
        self.assertEqual(len(api.panggilan), 3 + 3)  # obs1: 3 panggilan; obs2-4: masing-masing 1
        rows = baca_jsonl(self.p_out)
        self.assertIsNone(rows[0]["panggilan_error"])
        self.assertTrue(rows[0]["parse_ok"])

    def test_retry_habis_dicatat_sebagai_galat(self):
        # Semua panggilan gagal: 3 kali coba, sleep 1,0 lalu 2,0; baris dicatat dengan galat.
        def skrip(i):
            raise ConnectionError("gangguan tetap")
        api = ApiPalsu(skrip)
        lama = _pasang_modul_palsu(api)
        tidur = []
        try:
            runner.jalankan(self.p_items, self.p_out, self._prov(), sleep=tidur.append)
        finally:
            _pulihkan(lama)
        obs1 = [r for r in baca_jsonl(self.p_out) if r["obs_id"] == "C0001_own_R1"]
        self.assertEqual(len(obs1), 1)  # galat panggilan tidak diulang sebagai percobaan parse
        self.assertFalse(obs1[0]["parse_ok"])
        self.assertIn("gangguan tetap", obs1[0]["panggilan_error"])
        self.assertEqual(tidur[:2], [1.0, 2.0])

    def test_resume_melewati_yang_sudah_ada(self):
        # Berkas parsial berisi obs C0001 dan C0002 untuk provider yang sama.
        sudah = [{"obs_id": "C0001_own_R1", "provider_id": "profil_qwen_plan", "ulangan": 1,
                  "parse_ok": True, "percobaan": 1, "p": None, "raw": "x"},
                 {"obs_id": "C0002_own_R1", "provider_id": "profil_qwen_plan", "ulangan": 1,
                  "parse_ok": True, "percobaan": 1, "p": None, "raw": "x"}]
        tulis_jsonl(self.p_out, sudah)
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        try:
            baru = runner.jalankan(self.p_items, self.p_out, self._prov(), sleep=lambda s: None)
        finally:
            _pulihkan(lama)
        self.assertEqual(baru, 2)  # hanya C0003 dan C0004
        self.assertEqual(len(api.panggilan), 2)
        rows = baca_jsonl(self.p_out)
        self.assertEqual(len(rows), 4)
        self.assertEqual(sorted(r["obs_id"] for r in rows), sorted(i["obs_id"] for i in ITEMS))

    def test_resume_abaikan_provider_lain(self):
        # Baris provider mock tidak menggugurkan observasi untuk profil.
        tulis_jsonl(self.p_out, [{"obs_id": "C0001_own_R1", "provider_id": "mock_konservatif",
                                  "ulangan": 1, "parse_ok": True, "percobaan": 1, "p": None,
                                  "raw": "x"}])
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        try:
            baru = runner.jalankan(self.p_items, self.p_out, self._prov(), sleep=lambda s: None)
        finally:
            _pulihkan(lama)
        self.assertEqual(baru, 4)

    def test_konkuren_empat_pekerja_tanpa_baris_hilang_atau_ganda(self):
        items = [{**ITEMS[0], "obs_id": f"K{i:03d}_own_R1", "claim_id": f"K{i:03d}"}
                 for i in range(20)]
        tulis_jsonl(self.p_items, items, timpa=True)
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        try:
            n = runner.jalankan(self.p_items, self.p_out, self._prov(),
                                workers=4, sleep=lambda s: None, timpa=True)
        finally:
            _pulihkan(lama)
        rows = baca_jsonl(self.p_out)
        self.assertEqual(n, 20)
        self.assertEqual(len(rows), 20)
        self.assertEqual(len({r["obs_id"] for r in rows}), 20)
        self.assertEqual(len(api.panggilan), 20)

    def test_items_terlarang_ditolak_sebelum_panggilan(self):
        tulis_jsonl(self.p_items, [{**ITEMS[0], "label_type": "anchor"}], timpa=True)
        api = ApiPalsu()
        lama = _pasang_modul_palsu(api)
        try:
            with self.assertRaises(ValueError):
                runner.jalankan(self.p_items, self.p_out, self._prov(), sleep=lambda s: None)
        finally:
            _pulihkan(lama)
        self.assertEqual(api.panggilan, [])

    def test_parse_gagal_diulang_sekali_untuk_profil(self):
        # Panggilan pertama mengembalikan teks bukan JSON; panggilan kedua valid.
        def skrip(i):
            return "maaf, tidak bisa" if i == 1 else JAWABAN_VALID
        api = ApiPalsu(skrip)
        tulis_jsonl(self.p_items, [ITEMS[0]], timpa=True)
        lama = _pasang_modul_palsu(api)
        try:
            runner.jalankan(self.p_items, self.p_out, self._prov(), sleep=lambda s: None)
        finally:
            _pulihkan(lama)
        rows = baca_jsonl(self.p_out)
        self.assertEqual([r["percobaan"] for r in rows], [1, 2])
        self.assertFalse(rows[0]["parse_ok"])
        self.assertTrue(rows[1]["parse_ok"])


if __name__ == "__main__":
    unittest.main()
