"""Uji kebocoran kunci ke berkas yang dikirim ke model.

(a) items_model.jsonl tidak memuat kolom kunci.
(b) tidak ada string label benar pada nama berkas atau metadata.
(c) himpunan obs_id items_model sama dengan kunci.
(d) tidak ada article_id yang muncul di lebih dari satu split.

Setiap fungsi mengembalikan daftar pelanggaran (string). Daftar kosong = lulus.
"""
import os
import re

from epis.jsonl_io import baca_jsonl
from epis.skor import LABELS

KOLOM_TERLARANG = frozenset({
    "label", "kunci", "answer", "split", "article_id", "annotator_agreement",
    "rationale", "rasional", "kategori", "gold", "truth", "jawaban",
    "label_benar", "kategori_bukti",
    # skema v2 (keputusan peneliti): semua ini rahasia
    "label_type", "pair_type", "evidence_article_id", "anchor_note",
    "risiko_jangkar",
})
# Batas huruf (bukan \b) agar "items_REFUTED.jsonl" dan "kunci-NEI" tetap terdeteksi.
_POLA_LABEL = re.compile(
    r"(?<![A-Za-z])(" + "|".join(LABELS) + r")(?![A-Za-z])", re.IGNORECASE
)


def periksa_kolom_items(items):
    """(a) Kembalikan pelanggaran bila ada kolom terlarang di item mana pun."""
    pelanggaran = []
    for i, item in enumerate(items, start=1):
        for kolom in sorted(set(item) & KOLOM_TERLARANG):
            pelanggaran.append(f"(a) baris {i}: kolom terlarang '{kolom}'")
    return pelanggaran


def periksa_nama_dan_metadata(nama_berkas, metadata):
    """(b) Label benar tidak boleh muncul di nama berkas atau nilai metadata."""
    pelanggaran = []
    for teks in [nama_berkas] + [str(v) for v in metadata.values()]:
        for cocok in _POLA_LABEL.findall(str(teks)):
            pelanggaran.append(f"(b) label '{cocok}' ditemukan di '{teks}'")
    return pelanggaran


def periksa_obs_id(items, kunci):
    """(c) Himpunan obs_id harus sama persis di kedua berkas."""
    id_items = [it.get("obs_id") for it in items]
    id_kunci = [k.get("obs_id") for k in kunci]
    pelanggaran = []
    if len(set(id_items)) != len(id_items):
        pelanggaran.append("(c) obs_id ganda di items_model")
    if len(set(id_kunci)) != len(id_kunci):
        pelanggaran.append("(c) obs_id ganda di kunci")
    hanya_items = sorted(set(id_items) - set(id_kunci), key=str)
    hanya_kunci = sorted(set(id_kunci) - set(id_items), key=str)
    for oid in hanya_items:
        pelanggaran.append(f"(c) obs_id {oid} ada di items_model tetapi tidak di kunci")
    for oid in hanya_kunci:
        pelanggaran.append(f"(c) obs_id {oid} ada di kunci tetapi tidak di items_model")
    return pelanggaran


def periksa_split_artikel(kunci):
    """(d) Setiap article_id hanya boleh berada di satu split."""
    split_per_artikel = {}
    for k in kunci:
        split_per_artikel.setdefault(k.get("article_id"), set()).add(k.get("split"))
    pelanggaran = []
    for artikel, splits in sorted(split_per_artikel.items(), key=lambda x: str(x[0])):
        if len(splits) > 1:
            pelanggaran.append(f"(d) article_id {artikel} muncul di split {sorted(map(str, splits))}")
    return pelanggaran


def jalankan_semua(path_items, path_kunci, nama_berkas_items=None, metadata=None):
    """Jalankan (a)-(d) dari berkas. Kembalikan daftar pelanggaran gabungan."""
    items = baca_jsonl(path_items)
    kunci = baca_jsonl(path_kunci)
    nama = nama_berkas_items if nama_berkas_items is not None else os.path.basename(path_items)
    pelanggaran = periksa_kolom_items(items)
    pelanggaran += periksa_nama_dan_metadata(nama, metadata or {})
    pelanggaran += periksa_obs_id(items, kunci)
    pelanggaran += periksa_split_artikel(kunci)
    return pelanggaran
