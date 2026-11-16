"""Jalankan provider NYATA (TERKUNCI) pada satu split. Tahap persiapan ini TIDAK menjalankannya.

Gerbang ganda: flag --izinkan-panggilan-nyata DAN env EPIS_ALLOW_REAL_CALLS=1.
Tanpa keduanya skrip berhenti dengan kode 3 dan tidak menulis apa pun.
Holdout: hanya sekali. Wajib --konfirmasi-holdout-sekali, dan menolak bila keluaran sudah ada.

Contoh (JANGAN dijalankan sebelum persetujuan peneliti):
  set EPIS_ALLOW_REAL_CALLS=1
  py -3.12 -I -X utf8 harness/jalankan_provider_nyata.py --split pilot --model qwen3.8-flash --limit 5 --izinkan-panggilan-nyata
"""
import argparse
import os
import sys

HARNESS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HARNESS)

from epis import runner  # noqa: E402
from epis.jsonl_io import baca_jsonl, tulis_jsonl  # noqa: E402
from epis.provider_profil import FLAG_CLI, ProfilProvider  # noqa: E402
from epis.subset import SPLITS, pilih_split  # noqa: E402

FOLDER_FIXTURE = os.path.join(HARNESS, "fixture_tiruan")
FOLDER_LOG = os.path.join(HARNESS, "log")
KODE_TERKUNCI = 3
KODE_HOLDOUT = 2


def bangun_parser():
    p = argparse.ArgumentParser(description="Provider nyata terkunci per split")
    p.add_argument("--split", required=True, choices=SPLITS)
    p.add_argument("--model", required=True, help="ID model yang diminta, mis. qwen3.8-flash")
    p.add_argument("--profil", default="qwen_plan")
    p.add_argument("--ulangan", type=int, default=1)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--limit", type=int, default=0, help="0 = semua observasi di split")
    p.add_argument("--items", default=os.path.join(FOLDER_FIXTURE, "items_model.jsonl"))
    p.add_argument("--kunci", default=os.path.join(FOLDER_FIXTURE, "kunci.jsonl"))
    p.add_argument("--izinkan-panggilan-nyata", action="store_true")
    p.add_argument("--konfirmasi-holdout-sekali", action="store_true")
    p.add_argument("--bukan-konten-pribadi", action="store_true",
                   help="Deklarasi: isi = kutipan artikel jurnal, bukan buku/soal/data siswa. "
                        "Tanpa flag ini konten=True dan model_api menolak bila izin_isi_cloud tidak ada.")
    p.add_argument("--max-tokens", type=int, default=512)
    p.add_argument("--timeout", type=int, default=120)
    return p


def _tulis_subset(args):
    items = baca_jsonl(args.items)
    kunci = baca_jsonl(args.kunci)
    subset = pilih_split(items, kunci, args.split)
    if args.limit > 0:
        subset = subset[: args.limit]
    path = os.path.join(FOLDER_LOG, f"items_{args.split}_{args.model}.jsonl")
    tulis_jsonl(path, subset, timpa=True)  # items tanpa kolom kunci
    return path, len(subset)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    args = bangun_parser().parse_args(argv)
    if args.split == "holdout" and not args.konfirmasi_holdout_sekali:
        print("holdout hanya boleh sekali: butuh --konfirmasi-holdout-sekali")
        return KODE_HOLDOUT
    os.makedirs(FOLDER_LOG, exist_ok=True)
    out = os.path.join(FOLDER_LOG, f"nyata_{args.split}_{args.model}_u{args.ulangan}.jsonl")
    if args.split == "holdout" and os.path.exists(out):
        print("holdout sudah pernah dijalankan (keluaran ada); tidak diulang")
        return KODE_HOLDOUT
    try:
        prov = ProfilProvider(args.profil, args.model,
                              izin_cli=args.izinkan_panggilan_nyata,
                              konten=not args.bukan_konten_pribadi,
                              max_tokens=args.max_tokens, timeout=args.timeout)
    except PermissionError as e:
        print(f"ditolak: {e} (flag {FLAG_CLI})")
        return KODE_TERKUNCI
    path_items, n_items = _tulis_subset(args)
    n = runner.jalankan(path_items, out, prov, ulangan=args.ulangan,
                        workers=args.workers)
    print(f"split={args.split} model={args.model} observasi={n_items} baris_baru={n} keluaran={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
