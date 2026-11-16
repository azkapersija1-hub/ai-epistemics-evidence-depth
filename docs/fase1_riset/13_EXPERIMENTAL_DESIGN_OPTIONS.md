# 13 Opsi desain eksperimen (untuk fase eksekusi nanti; belum dijalankan)

Semua angka ukuran sampel berasal dari hitungan Agent B dengan **sigma = 0,35 (ASUMSI, belum diukur)**; pilot wajib mengestimasinya.

## Komponen umum (20 butir yang diminta)
1. **Research questions**: RQ1 seberapa baik model memilih SUPPORTED/REFUTED/NEI dan memberi distribusi terkalibrasi pada klaim akademik? RQ2 (sekunder) apakah sinyal eksternal (F11x-adaptasi) mengubah kualitas Brier dibanding plasebo?
2. **Hipotesis** (dua arah, dipraregistrasi): H1 Brier multikelas model lebih baik dari baseline seragam (0,6667). H2 perbedaan Brier antar model signifikan setelah klaster-per-artikel. H3 (sekunder) B−A ≠ 0 dan B−D ≠ 0.
3. **Definisi**: `11_OPERATIONAL_DEFINITIONS.md`.
4. **Model**: Qwen3.8-Max, DeepSeek Flash, Claude Haiku 5.5, Gemini 3.8 Flash, GPT-6.1 Sol (akses akun TIDAK_DIVERIFIKASI untuk semuanya; lihat `09`). Prompt tunggal untuk semua.
5. **Dataset**: butir baru dari `core_academic` (dokumen berDOI dengan abstract+results+conclusion ≈ 5.450), split **berbasis artikel**: pilot, development, validation, final holdout (sekali pakai). 45 butir lama hanya pilot.
6. **Retrieval bukti**: potongan bukti diambil dari bagian dokumen yang sama (abstract/results/conclusion) atau dari artikel lain untuk kondisi NEI/bertentangan; aturan pemilihan dibekukan.
7. **Konstruksi butir**: SUPPORTED/REFUTED dari klaim yang ditegaskan atau dibalik secara terkontrol; NEI dari bukti yang sengaja tidak menjawab klaim. Aturan tertulis, bukan LLM bebas.
8. **Expert review**: ≥2 anotator independen + adjudikasi; sampel 20% butir dianotasi ulang untuk kappa.
9. **Ground truth**: kunci disimpan di berkas terpisah; uji otomatis kebocoran.
10. **Standardisasi prompt**: satu templat, format JSON tetap, hash prompt dicatat.
11. **Integrasi F11x**: hanya Kondisi B (dan D plasebo); definisi beku; tanpa pelatihan ulang pada butir uji.
12. **Kelompok**: A, B, D di semua; C hanya development.
13. **Protokol kalibrasi**: distribusi 3 kelas langsung (primer); k=5 sampel pada subset; logprob hanya jika tersedia dan dicatat sebagai kondisi terpisah.
14. **Statistik**: `14_STATISTICAL_ANALYSIS_PLAN.md`.
15. **QC**: audit manual 5%; cek sebaran label per kondisi.
16. **Reproduksibilitas**: seed, versi/snapshot, tanggal, hash prompt, commit, keluaran mentah JSONL.
17. **Kegagalan**: coba ulang sekali; catat; dua batas Brier.
18. **API/GPU**: hanya API; tidak perlu GPU kecuali embedding retrieval lokal.
19. **Sumber daya**: `15_COST_AND_RESOURCE_PLAN.md`.
20. **Pelaporan**: varians, baseline seragam, interval klaster, jumlah parse gagal, batas.

## Tiga skala
| Skala | Butir | Kondisi | Model | Ulangan | Tujuan | Kemampuan inferensial |
|---|---|---|---|---|---|---|
| **Minimal** | ~140 (≈47 artikel × 3) | A | 3-5 | 3 | Evaluasi inti + estimasi sigma, ICC | Deteksi delta Brier 0,10 (n≈97; DEFF 1,4 → ≈136) |
| **Standard** | ~540 (≈180 artikel × 3) | A, B, D (+C di dev) | 5 | 3 | Perbandingan model dan F11x-vs-plasebo | Deteksi delta 0,05 (n=385; DEFF 1,4 → 539) |
| **Extended** | ~1.710 | A, B, D + 2 kondisi bukti bertentangan | 5 | 3 | Bukti bertentangan, pembaruan keputusan, robustness | Delta 0,03 dengan DEFF 1,6 |

## Evaluasi kelayakan 3 hari (jujur)
- **Hambatan terbesar adalah pelabelan ahli**, bukan API. Minimal (~140 butir dengan 2 anotator) mungkin dikerjakan; Standard (~540) **tidak realistis** untuk peneliti tunggal dalam 3 hari kecuali pelabelan sebagian besar otomatis berbasis aturan, yang melemahkan klaim ground truth.
- Rekomendasi: **Minimal sebagai komitmen**, Standard hanya sebagai target dan dilaporkan sebagai "terbatas daya" bila butir kurang. Extended: jangan dijanjikan.
- Bila butir kurang dari 385, laporkan sebagai studi eksploratif dengan interval, bukan konfirmatori.

## Pilihan desain yang ditolak
- Satu confidence verbal tunggal sebagai primer (Brier bergantung asumsi pembagian sisa).
- Dua primary (tidak ada koreksi daya).
- 45 butir lama sebagai holdout.
- Pelatihan ulang F11x pada butir uji.
