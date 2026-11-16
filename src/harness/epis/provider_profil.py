"""Adapter profil TERKUNCI ke model_api (sakti_core). Tidak dijalankan di tes.

Gerbang ganda, dicek saat konstruksi:
  (i)  argumen CLI --izinkan-panggilan-nyata, dan
  (ii) variabel lingkungan EPIS_ALLOW_REAL_CALLS=1.
Tanpa keduanya, ProfilProvider melempar PermissionError dan tidak memuat apa pun.

model_api dimuat MALAS (saat answer pertama). Folder sakti_core hanya masuk sys.path
selama impor, lalu dikeluarkan lagi. Tidak ada akses ke profil_api.json, tidak ada
pemanggilan api_muat atau api_buka, dan kunci tidak pernah dicetak.

Catatan dari membaca signature (bukan tebakan):
  api_chat(nama, prompt, *, konten, max_tokens=512, model=None, timeout=60) -> str
  Badan permintaannya tidak memuat temperature maupun thinking, sehingga keduanya tidak
  bisa diatur dari harness. periksa_param mencatat ini; tidak ada nilai yang ditebak.
"""
import importlib
import inspect
import os
import sys

from epis.provider import Provider

LOKASI_MODEL_API = r"D:\kerjaan baru\25_Tools_Sakti_Terpadu\core\sakti_core"
FLAG_CLI = "--izinkan-panggilan-nyata"
ENV_IZIN = "EPIS_ALLOW_REAL_CALLS"
PARAM_DICATAT = ("temperature", "thinking", "enable_thinking")


def periksa_param(fungsi):
    """Catat apakah signature mendukung parameter pengendali. Tidak menebak nilai."""
    nama = set(inspect.signature(fungsi).parameters)
    return {p: (p in nama) for p in PARAM_DICATAT}


def izin_aktif(argv, environ):
    """True hanya bila flag CLI ada DAN env EPIS_ALLOW_REAL_CALLS == '1'."""
    return FLAG_CLI in argv and environ.get(ENV_IZIN) == "1"


def _muat_model_api(lokasi):
    """Impor model_api dengan folder sakti_core di sys.path hanya selama impor."""
    sudah = lokasi in sys.path
    if not sudah:
        sys.path.insert(0, lokasi)
    try:
        return importlib.import_module("model_api")
    finally:
        if not sudah and lokasi in sys.path:
            sys.path.remove(lokasi)


class ProfilProvider(Provider):
    """Provider nyata melalui model_api.api_chat. Hanya aktif di bawah gerbang ganda."""

    def __init__(self, profil, model, izin_cli, environ=None, konten=True,
                 max_tokens=512, timeout=60, lokasi=LOKASI_MODEL_API):
        environ = os.environ if environ is None else environ
        if not (izin_cli and environ.get(ENV_IZIN) == "1"):
            raise PermissionError(
                f"panggilan nyata terkunci: butuh {FLAG_CLI} DAN {ENV_IZIN}=1"
            )
        self.profil = profil
        self.model_id_deklarasi = model
        self.provider_id = f"profil_{profil}"
        self.konten = konten
        self.max_tokens = max_tokens
        self.timeout = timeout
        self._lokasi = lokasi
        self._fungsi = None
        self.param_didukung = None

    def _muat(self):
        if self._fungsi is None:
            modul = _muat_model_api(self._lokasi)
            self._fungsi = modul.api_chat
            self.param_didukung = periksa_param(self._fungsi)
        return self._fungsi

    def answer(self, prompt):
        fungsi = self._muat()
        keluaran = fungsi(
            self.profil, prompt,
            konten=self.konten,
            max_tokens=self.max_tokens,
            model=self.model_id_deklarasi,
            timeout=self.timeout,
        )
        if not isinstance(keluaran, str):
            raise TypeError("api_chat mengembalikan bukan string")
        return keluaran
