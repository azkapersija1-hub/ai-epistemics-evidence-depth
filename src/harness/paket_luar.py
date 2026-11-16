"""Bangun paket batch untuk penguji LUAR (mis. GPT-6.1 Sol, Gemini lewat Antigravity/Codex).

Prompt SAMA persis dengan yang dipakai Qwen/DeepSeek (templat dan urutan blok sama). Tidak ada kunci di paket.
Aturan batch: satu observasi per klaim per batch (mencegah penguji melihat klaim yang sama dua kali dalam satu konteks),
anggaran karakter per batch dibatasi, urutan diacak dengan seed tetap.
"""
import argparse
import hashlib
import json
import os
import random
import sys

HARNESS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HARNESS)

from epis.jsonl_io import baca_jsonl  # noqa: E402
from epis.prompt import bangun_prompt, muat_templat  # noqa: E402
from epis.subset import SPLITS, pilih_split  # noqa: E402

SEED = 20261112


def bentuk_batch(item_prompt, anggaran_char):
    """item_prompt: list (item, prompt). Mengembalikan list batch; tiap batch tanpa claim_id ganda."""
    sisa = list(item_prompt)
    batches = []
    while sisa:
        batch, klaim_terpakai, total, belum = [], set(), 0, []
        for it, pr in sisa:
            if it["claim_id"] in klaim_terpakai or (batch and total + len(pr) > anggaran_char):
                belum.append((it, pr))
                continue
            batch.append((it, pr))
            klaim_terpakai.add(it["claim_id"])
            total += len(pr)
        batches.append(batch)
        sisa = belum
    return batches


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--split", required=True, choices=SPLITS)
    p.add_argument("--items", required=True)
    p.add_argument("--kunci", required=True)
    p.add_argument("--keluar", required=True)
    p.add_argument("--anggaran-char", type=int, default=90000)
    a = p.parse_args()
    items = pilih_split(baca_jsonl(a.items), baca_jsonl(a.kunci), a.split)
    rng = random.Random(SEED)
    rng.shuffle(items)
    templat, hash_templat = muat_templat()
    pasangan = [(it, bangun_prompt(it, order="claim_first", templat=templat)) for it in items]
    batches = bentuk_batch(pasangan, a.anggaran_char)
    os.makedirs(a.keluar, exist_ok=True)
    manifest = {"split": a.split, "n_obs": len(items), "n_batch": len(batches), "prompt_hash": hash_templat,
                "seed": SEED, "anggaran_char": a.anggaran_char, "batch": []}
    for i, b in enumerate(batches, 1):
        nama = f"batch_{a.split}_{i:03d}.jsonl"
        isi = "".join(json.dumps({"obs_id": it["obs_id"], "prompt": pr}, ensure_ascii=False) + "\n" for it, pr in b)
        with open(os.path.join(a.keluar, nama), "w", encoding="utf-8", newline="\n") as f:
            f.write(isi)
        manifest["batch"].append({"berkas": nama, "n": len(b), "sha256": hashlib.sha256(isi.encode("utf-8")).hexdigest()})
    with open(os.path.join(a.keluar, f"manifest_{a.split}.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(a.split, "obs", len(items), "batch", len(batches), "maks_obs_per_batch", max(len(b) for b in batches))


if __name__ == "__main__":
    main()
