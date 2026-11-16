"""Runner v2: items -> prompt -> provider -> keluaran mentah JSONL (tulis per observasi).

Setiap baris keluaran: obs_id, provider_id, model_id_diminta, prompt_hash, order, ulangan,
percobaan (1|2), raw, waktu (UTC), latensi_s, panjang_keluaran, parse_ok, normalized,
p, parse_error, panggilan_error.

- Parse gagal diulang sekali (percobaan 2). Percobaan kedua tetap dicatat walau gagal.
- Galat panggilan (jaringan, kuota, izin) diulang hingga MAKS_COBA_PANGGILAN dengan
  backoff eksponensial: backoff_dasar * 2^(k-1). Bila habis, baris dicatat dengan panggilan_error.
- Resume: bila timpa=False dan berkas sudah ada, pasangan (obs_id, ulangan, provider_id)
  yang sudah ada dilewati. Setiap observasi ditulis sekaligus, jadi tidak ada baris setengah jadi.
- Konkurensi: ThreadPoolExecutor(max_workers=workers); penulisan dikunci.
- Prompt dan kunci tidak pernah dicetak. Runner tidak membuka kunci.jsonl.
"""
import datetime
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from epis import bocor
from epis.jsonl_io import baca_jsonl
from epis.parse import parse_keluaran
from epis.prompt import bangun_prompt, muat_templat
from epis.provider import MockProvider
from epis.provider_profil import ProfilProvider

MAKS_PERCOBAAN = 2          # percobaan awal + satu ulang bila parse gagal
MAKS_COBA_PANGGILAN = 3     # galat panggilan: maks 3 kali coba
BACKOFF_DASAR_DEFAULT = 1.0


def _cek_provider(provider):
    if not isinstance(provider, (MockProvider, ProfilProvider)):
        raise PermissionError(
            "adapter nyata menunggu persetujuan peneliti: "
            f"provider {type(provider).__name__} ditolak"
        )


def _cek_items_aman(items):
    pelanggaran = bocor.periksa_kolom_items(items)
    if pelanggaran:
        raise ValueError("items_model mengandung kolom terlarang: " + "; ".join(pelanggaran))


def _panggil_dengan_retry(provider, prompt, backoff_dasar, sleep):
    """Kembalikan (raw, latensi_s, galat). raw None berarti semua coba gagal."""
    galat = None
    for k in range(1, MAKS_COBA_PANGGILAN + 1):
        mulai = time.monotonic()
        try:
            raw = provider.answer(prompt)
            return raw, time.monotonic() - mulai, None
        except Exception as e:  # galat panggilan dicatat, bukan dilempar ke luar
            galat = f"{type(e).__name__}: {e}"
            if k < MAKS_COBA_PANGGILAN:
                sleep(backoff_dasar * (2 ** (k - 1)))
    return None, 0.0, galat


def _baris(item, provider, order, hash_templat, ulangan, percobaan, raw, latensi, galat):
    if raw is None:
        hasil = {"ok": False, "p": None, "normalized": False, "error": galat}
    else:
        hasil = parse_keluaran(raw)
    return {
        "obs_id": item["obs_id"],
        "provider_id": provider.provider_id,
        "model_id_diminta": provider.model_id_deklarasi,
        "prompt_hash": hash_templat,
        "order": order,
        "ulangan": ulangan,
        "percobaan": percobaan,
        "raw": raw,
        "waktu": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "latensi_s": round(latensi, 4),
        "panjang_keluaran": 0 if raw is None else len(raw),
        "parse_ok": hasil["ok"],
        "normalized": hasil["normalized"],
        "p": hasil["p"],
        "parse_error": hasil["error"],
        "panggilan_error": galat,
    }


def _satu_observasi(item, provider, order, templat, hash_templat, ulangan, backoff_dasar, sleep):
    """Daftar baris untuk satu observasi (1 atau 2 percobaan)."""
    rows = []
    for percobaan in range(1, MAKS_PERCOBAAN + 1):
        prompt = bangun_prompt(item, order=order, templat=templat)
        raw, latensi, galat = _panggil_dengan_retry(provider, prompt, backoff_dasar, sleep)
        rows.append(_baris(item, provider, order, hash_templat, ulangan,
                           percobaan, raw, latensi, galat))
        if raw is None or rows[-1]["parse_ok"]:
            break
    return rows


def _kunci_selesai(path, provider_id):
    """Himpunan (obs_id, ulangan, provider_id) yang sudah ada di berkas keluaran."""
    if not os.path.exists(path):
        return set()
    return {(r["obs_id"], r["ulangan"], r["provider_id"]) for r in baca_jsonl(path)
            if r.get("provider_id") == provider_id}


def jalankan(path_items, path_keluaran, provider, order="claim_first", ulangan=1,
             timpa=False, workers=1, backoff_dasar=BACKOFF_DASAR_DEFAULT, sleep=time.sleep):
    """Jalankan items melalui provider. Kembalikan jumlah baris BARU yang ditulis.

    timpa=True: berkas ditulis ulang dari nol (tanpa resume).
    timpa=False: resume; observasi yang sudah ada dilewati.
    """
    _cek_provider(provider)
    items = baca_jsonl(path_items)
    _cek_items_aman(items)
    templat, hash_templat = muat_templat()
    selesai = set() if timpa else _kunci_selesai(path_keluaran, provider.provider_id)
    todo = [it for it in items if (it["obs_id"], ulangan, provider.provider_id) not in selesai]
    kunci_tulis = threading.Lock()
    mode = "w" if timpa else "a"

    with open(path_keluaran, mode, encoding="utf-8", newline="\n") as f:
        def kerjakan(item):
            rows = _satu_observasi(item, provider, order, templat, hash_templat,
                                   ulangan, backoff_dasar, sleep)
            with kunci_tulis:
                for row in rows:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
            return len(rows)

        if workers <= 1:
            return sum(kerjakan(it) for it in todo)
        with ThreadPoolExecutor(max_workers=workers) as ex:
            return sum(ex.map(kerjakan, todo))
