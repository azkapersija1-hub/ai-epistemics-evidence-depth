"""Pembangun prompt dari satu baris items_model.jsonl.

Hanya claim_text dan evidence_text yang masuk prompt. Kolom lain (obs_id, rung,
claim_id, lang) tidak pernah dikirim. Urutan dua blok bisa dikontra-seimbangkan
lewat opsi order. Hash sha256 templat dicatat pada setiap keluaran.
"""
import hashlib
import os
import re

HARNESS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLAT_DIR = os.path.join(HARNESS_DIR, "prompt_templates")
TEMPLAT_DEFAULT = "prompt_v1.txt"
URUTAN = ("claim_first", "evidence_first")
_PLACEHOLDER = re.compile(r"\{(BLOK_1|BLOK_2)\}")


def muat_templat(nama=TEMPLAT_DEFAULT):
    """Kembalikan (teks_templat, sha256_hex). Newline dinormalisasi ke LF agar hash stabil."""
    path = os.path.join(TEMPLAT_DIR, nama)
    with open(path, "rb") as f:
        mentah = f.read()
    teks = mentah.decode("utf-8").replace("\r\n", "\n")
    digest = hashlib.sha256(teks.encode("utf-8")).hexdigest()
    return teks, digest


def _blok(item, urutan_blok):
    """Blok 'Claim:' dan 'Evidence:' sesuai urutan yang diminta."""
    klaim = f"Claim: {item['claim_text']}"
    bukti = f"Evidence: {item['evidence_text']}"
    if urutan_blok == "claim_first":
        return klaim, bukti
    return bukti, klaim


def bangun_prompt(item, order="claim_first", templat=None):
    """Bangun prompt satu observasi. Melempar ValueError bila kolom wajib hilang."""
    if order not in URUTAN:
        raise ValueError(f"order tidak dikenal: {order!r}")
    for kolom in ("claim_text", "evidence_text"):
        if not isinstance(item.get(kolom), str) or not item[kolom].strip():
            raise ValueError(f"kolom wajib kosong atau bukan teks: {kolom}")
    teks = templat if templat is not None else muat_templat()[0]
    blok_1, blok_2 = _blok(item, order)
    peta = {"BLOK_1": blok_1, "BLOK_2": blok_2}
    # Satu kali lewat: isi klaim/bukti tidak ikut diganti.
    return _PLACEHOLDER.sub(lambda m: peta[m.group(1)], teks)
