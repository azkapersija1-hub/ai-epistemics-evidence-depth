# 15 Rencana biaya dan sumber daya

Tidak ada API kandidat dipanggil untuk menyusun dokumen ini. Harga berasal dari halaman resmi yang dibaca 2026-11-11 (rincian dan URL di `09_MODEL_FEASIBILITY_MATRIX.csv`). **Jumlah token per panggilan adalah ASUMSI yang belum diukur** (1.500 masuk, 300 keluar, tanpa token berpikir); pilot 20 butir wajib mengukurnya. Skrip: `_data_audit/hitung_biaya.py`. Ini hitungan aritmetika, bukan hasil model.

## Status harga
| Model | Harga masuk / keluar per 1M token (USD) | Status |
|---|---|---|
| Qwen3.8-Max (`qwen3.8-max`) | 1,65 / 4,951 | Terverifikasi (halaman resmi) |
| DeepSeek Flash (`deepseek-flash`) | 0,3 / 1,2 (puncak); 0,15 / 0,6 (luar puncak) | Terverifikasi |
| GPT-6.1 Sol (`gpt-6.1-sol`) | 2 / 10 | Terverifikasi |
| Claude Haiku 5.5 (`claude-haiku-5-5`) | "From 0,10 / 0,50" saja | **Parsial (rentang, harga pasti unknown)** |
| Gemini 3.8 Flash (`gemini-3.8-flash`) | tidak ditemukan | **unknown** |
Catatan: ID lokal `deepseek-v4.1-flash` tidak ditemukan persis; ID resmi `deepseek-flash`. Logprobs/seed/sampling tidak tercantum di halaman resmi untuk semua model. Akses akun semua model TIDAK_DIVERIFIKASI.

## Estimasi per model (USD, asumsi token di atas)
| Skala | Panggilan/model | Qwen3.8-Max | DeepSeek Flash (puncak / luar puncak) | GPT-6.1 Sol | Haiku 5.5 | Gemini 3.8 Flash |
|---|---|---|---|---|---|---|
| Minimal (140 butir × 1 kondisi × 3 ulangan) | 420 | 1,7 | 0,3 / 0,2 | 2,5 | unknown | unknown |
| Standard (540 × 3 × 3) | 4.860 | 19,2 | 3,9 / 2,0 | 29,2 | unknown | unknown |
| Extended (1.710 × 5 × 3) | 25.650 | 101,6 | 20,8 / 10,4 | 153,9 | unknown | unknown |
Total 5 model: Minimal 2.100 panggilan; Standard 24.300; Extended 128.250. Token berpikir (thinking) dapat melipatgandakan sisi keluaran dan belum dihitung; angka di atas adalah **batas bawah** untuk model bernalar. Hasil tidak boleh dibaca sebagai anggaran pasti.

## Sumber daya non-API
- Waktu pelabelan ahli (dominan): Minimal ≈ 140 butir × 2 anotator; Standard ≈ 540 butir × 2 anotator + adjudikasi.
- Komputasi lokal: SQLite baca-saja; GPU tidak wajib. Embedding retrieval opsional memakai `mxbai-embed-large` (satu-satunya yang ada di korpus).
- Rate limit: halaman limit belum dibaca untuk sebagian besar model; gunakan backoff eksponensial dan kuota harian tercatat.
- Penyimpanan: keluaran mentah JSONL sebelum agregasi.

## Prinsip
Jangan menghabiskan dana API hanya untuk memeriksa proposal. Eksekusi hanya setelah persetujuan, dan mulai dari pilot 20 butir untuk mengukur token dan sigma.
