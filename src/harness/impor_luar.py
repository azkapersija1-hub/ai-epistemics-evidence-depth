"""Impor hasil penguji LUAR ke format keluaran harness (agar dianalisis dengan alat yang sama).

Masukan: berkas hasil_<split>_*.jsonl, tiap baris {"obs_id", "SUPPORTED", "REFUTED", "NEI"}.
Validasi lewat parse_keluaran yang sama. obs_id harus ada di items split; duplikat dan hilang dilaporkan.
"""
import argparse
import datetime
import glob
import json
import os
import sys

HARNESS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HARNESS)

from epis.jsonl_io import baca_jsonl  # noqa: E402
from epis.parse import parse_keluaran  # noqa: E402
from epis.prompt import muat_templat  # noqa: E402
from epis.subset import SPLITS, pilih_split  # noqa: E402


def baca_hasil(pola):
    baris, rusak = [], 0
    for jalur in sorted(glob.glob(pola)):
        with open(jalur, encoding="utf-8") as f:
            for teks in f:
                if not teks.strip():
                    continue
                try:
                    d = json.loads(teks)
                except ValueError:
                    rusak += 1
                    continue
                if isinstance(d, dict) and "obs_id" in d:
                    baris.append(d)
                else:
                    rusak += 1
    return baris, rusak


def konversi(d, provider_id, model_id, hash_templat):
    raw = json.dumps({k: d.get(k) for k in ("SUPPORTED", "REFUTED", "NEI")}, ensure_ascii=False)
    h = parse_keluaran(raw)
    return {"obs_id": d["obs_id"], "provider_id": provider_id, "model_id_diminta": model_id,
            "prompt_hash": hash_templat, "order": "claim_first", "ulangan": 1, "percobaan": 1, "raw": raw,
            "waktu": datetime.datetime.now(datetime.timezone.utc).isoformat(), "latensi_s": None,
            "panjang_keluaran": len(raw), "parse_ok": h["ok"], "normalized": h["normalized"], "p": h["p"],
            "parse_error": h["error"], "panggilan_error": None}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--split", required=True, choices=SPLITS)
    p.add_argument("--hasil", required=True, help="pola glob, mis. paket\\hasil_gemini\\hasil_dev_*.jsonl")
    p.add_argument("--items", required=True)
    p.add_argument("--kunci", required=True)
    p.add_argument("--provider-id", required=True)
    p.add_argument("--model-id", required=True)
    p.add_argument("--keluaran", required=True)
    a = p.parse_args()
    ids = {it["obs_id"] for it in pilih_split(baca_jsonl(a.items), baca_jsonl(a.kunci), a.split)}
    baris, rusak = baca_hasil(a.hasil)
    _, hash_templat = muat_templat()
    terlihat, asing, ganda, keluar = set(), 0, 0, []
    for d in baris:
        if d["obs_id"] not in ids:
            asing += 1
            continue
        if d["obs_id"] in terlihat:
            ganda += 1
            continue
        terlihat.add(d["obs_id"])
        keluar.append(konversi(d, a.provider_id, a.model_id, hash_templat))
    with open(a.keluaran, "w", encoding="utf-8", newline="\n") as f:
        for r in keluar:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"split={a.split} diharapkan={len(ids)} terimpor={len(keluar)} hilang={len(ids) - len(terlihat)} "
          f"asing={asing} ganda={ganda} baris_rusak={rusak} parse_gagal={sum(1 for r in keluar if not r['parse_ok'])}")


if __name__ == "__main__":
    main()
