"""Baca dan tulis JSONL (satu objek JSON per baris, UTF-8). Stdlib saja."""
import json


def baca_jsonl(path):
    """Kembalikan daftar dict. Baris kosong dilewati; baris rusak melempar ValueError beserta nomornya."""
    hasil = []
    with open(path, "r", encoding="utf-8") as f:
        for nomor, baris in enumerate(f, start=1):
            isi = baris.strip()
            if not isi:
                continue
            try:
                objek = json.loads(isi)
            except json.JSONDecodeError as e:
                raise ValueError(f"{path} baris {nomor}: JSON rusak ({e})") from None
            if not isinstance(objek, dict):
                raise ValueError(f"{path} baris {nomor}: bukan objek")
            hasil.append(objek)
    return hasil


def tulis_jsonl(path, rows, timpa=False):
    """Tulis JSONL. Secara default menolak menimpa berkas yang sudah ada."""
    import os
    if os.path.exists(path) and not timpa:
        raise FileExistsError(f"berkas sudah ada, tidak ditimpa: {path}")
    mode = "w" if timpa else "x"
    with open(path, mode, encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
