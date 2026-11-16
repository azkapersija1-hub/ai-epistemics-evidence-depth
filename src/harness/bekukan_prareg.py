"""Membekukan praregistrasi: menghitung sha256 berkas kunci sebelum model dijalankan. Tidak memanggil model."""
import hashlib
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blok in iter(lambda: f.read(1 << 20), b""):
            h.update(blok)
    return h.hexdigest()


berkas = {
    "prompt_templates/prompt_v1.txt": os.path.join(ROOT, "harness", "prompt_templates", "prompt_v1.txt"),
    "bahan/v2/items_model.jsonl": os.path.join(ROOT, "bahan", "v2", "items_model.jsonl"),
    "bahan/v2/RAHASIA/kunci.jsonl": os.path.join(ROOT, "bahan", "v2", "RAHASIA", "kunci.jsonl"),
    "bahan/v2/pasangan_v2_1.jsonl": os.path.join(ROOT, "bahan", "v2", "pasangan_v2_1.jsonl"),
    "bahan/v2/pool_manifest.json": os.path.join(ROOT, "bahan", "v2", "pool_manifest.json"),
}
hasil = {k: sha(v) for k, v in berkas.items()}
kunci = [json.loads(l) for l in open(berkas["bahan/v2/RAHASIA/kunci.jsonl"], encoding="utf-8")]
holdout_art = sorted({k["article_id"] for k in kunci if k["split"] == "holdout"})
hasil["sha256_daftar_article_holdout"] = hashlib.sha256("\n".join(holdout_art).encode("utf-8")).hexdigest()
per_split = {}
for k in kunci:
    per_split.setdefault(k["split"], set()).add(k["claim_id"])
ringkas = {s: len(v) for s, v in sorted(per_split.items())}

baris = [
    "# PRAREGISTRASI DIBEKUKAN (sebelum ada jawaban model yang dikumpulkan)",
    "",
    "Dibekukan: " + time.strftime("%Y-%m-%d %H:%M:%S (waktu lokal)"),
    "",
    "## Pertanyaan",
    "Saat LLM hanya membaca bagian awal artikel ilmiah (R1 abstrak; R2 abstrak+hasil; R3 teks relevan penuh), "
    "seberapa terkalibrasi distribusi SUPPORTED/REFUTED/NEI-nya, dan seberapa sering ia terlalu yakin pada R1 "
    "dibanding R3, serta mengisi dukungan palsu pada bukti artikel lain (near/far).",
    "",
    "## Desain dan label",
    "- 294 klaim x 7 observasi (own R1,R2,R3; near R1,R3; far R1,R3). Split per artikel: " + json.dumps(ringkas) + ".",
    "- LABEL JANGKAR (bukan label ahli): own+R3 = SUPPORTED (kesimpulan penulis); near/far = NEI (bukti artikel lain, bahasa sama); own R1/R2 = tanpa label.",
    "- REFUTED tidak ada pada jangkar; label ahli (lembar_ahli_40, lembar_ahli_jangkar_30) BELUM diisi.",
    "",
    "## Primary dan sekunder",
    "- Primary: Brier multikelas pada observasi berjangkar (SUPPORTED own R3 dan NEI near/far), dilaporkan dengan CI bootstrap klaster per article_id.",
    "- Sekunder: akurasi, ECE, AURC, konsistensi R1 vs R3 (sesuai/tidak sesuai), pergeseran dS dan dN, overkomit R1 (tau = 0,7), "
    "false-support mass near vs far, per bahasa (en/id/unk).",
    "- Hipotesis dua arah. Tidak ada koreksi p untuk analisis eksploratif; interval dilaporkan apa adanya.",
    "",
    "## Aturan",
    "- tau overkomit = 0,7 (dibekukan). Aturan seri argmax: NEI menang.",
    "- Parse gagal: ulang sekali; lalu dicatat. Brier dilaporkan dua batas (butir gagal dikeluarkan / diberi 2,0).",
    "- Temperature tidak dapat diatur lewat model_api (default penyedia); dicatat sebagai keterbatasan. Ulangan 1 utama; stabilitas pada subset dev.",
    "- Urutan: pilot (teknis; tidak dilaporkan sebagai hasil) -> dev -> val -> holdout SEKALI. Tidak ada penyetelan prompt, tau, atau aturan setelah melihat hasil dev/val.",
    "- Model: qwen3.8-flash dan deepseek-v4.1-flash via profil qwen_plan. Model lain (GPT-6.1 Sol, Gemini) menyusul lewat jalur lain dan akan dilaporkan terpisah.",
    "- max_tokens 512, timeout 120 detik. Kutipan artikel jurnal dinyatakan bukan konten pribadi (flag --bukan-konten-pribadi).",
    "",
    "## Hash berkas beku (sha256)",
]
for k, v in hasil.items():
    baris.append(f"- {k}: `{v}`")
teks = "\n".join(baris) + "\n"
out = os.path.join(ROOT, "harness", "PREREG_DIBEKUKAN.md")
with open(out, "w", encoding="utf-8") as f:
    f.write(teks)
print("tulis", out)
print("sha256 prareg:", hashlib.sha256(teks.encode("utf-8")).hexdigest())
print(json.dumps(ringkas), "holdout_artikel", len(holdout_art))
