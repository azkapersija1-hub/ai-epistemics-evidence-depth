# Catatan WB: perbaikan v3 (berdasarkan LAPORAN_PEMERIKSAAN_K2.md)

Berkas yang diperbaiki: 04_hasil.md, 05_diskusi_keterbatasan.md, 06_kesimpulan.md (tidak berubah), 07_pernyataan_llm.md, 10_kontribusi_penulis.md (tidak berubah), 13_lampiran_D_tabel_lengkap.md, 14_lampiran_E_keterbatasan_lengkap.md. Folder v2 tidak diubah. Penanda [PENULIS ...] tidak dihapus.

## 1. Perbaikan per nomor tugas

1. **Arah near-far pada R3.** 04 kini menulis bahwa pada R1 selisih false-support near dan far positif pada ketiga model dengan interval tidak mencakup nol. Pada R3, selisih positif tanpa mencakup nol hanya pada qwen3.8-flash (0,0563 [0,0262; 0,0853]) dan qwen4-max-preview (0,0711 [0,0464; 0,0953]); interval deepseek-v4.1-flash (0,0190 [-0,0040; 0,0407]) mencakup nol. Tafsiran di 04 disesuaikan. Tabel D1 tidak memuat kalimat tafsiran, sehingga tidak perlu diubah.
2. **Brier gabungan.** Ditambahkan sebagai baris pada Tabel 2 di 04, dengan keterangan tanpa CI. Rumus dan nilai ada di bagian 2 catatan ini.
3. **Akurasi, ECE, AURC.** Ditambahkan Tabel D6 di Lampiran D, disalin dari analisis_UTAMA294.md bagian A, dengan koma desimal. Di 04 ditambahkan satu paragraf yang merujuk Tabel D6: ECE berada pada rentang 0,0071 sampai 0,0460 dan akurasi pada rentang 0,8537 sampai 0,9932 pada seluruh sel. Akurasi pada observasi NEI sama dengan recall NEI.
4. **GPT-6.1 Sol 39 klaim efektif.** 04 (4.4), Tabel D4 (keterangan n lengkap per model), Lampiran E (butir 7), dan 05 (poin 5) kini menyebut 40 klaim dengan 39 efektif, karena C0230 gagal pada seluruh 7 observasi. Di 07 kata "Empat model API" diganti dengan tiga model API, dan GPT-6.1 Sol disebut sebagai jalur agen.
5. **Tabel 2 terbelah halaman.** Tidak diubah di berkas ini, sesuai instruksi (diperbaiki saat perakitan).
6. **Holdout bukan murni konfirmatori.** 05 poin 6 dan Lampiran E butir 9 menyebut bahwa Amandemen 2 dan 3 menambah model setelah hasil holdout model lain dilihat. Penanda [PENULIS MEMASTIKAN] tetap ada.

Perbaikan tambahan dari K2 yang menyangkut berkas saya: 04 bagian 4.5 kini menyebut 92,5 persen bila gagal parse dihitung sebagai beda, dan 78,9 persen pada R2 qwen3.8-flash (19 observasi). Lampiran E butir 5 tidak lagi memuat nama field "bahasa_longgar" dan menyebut 39 klaim unk. Istilah "Codex" pada 05 dan Lampiran D diseragamkan menjadi GPT-6.1 Sol (tidak terverifikasi).

## 2. Brier gabungan: rumus dan nilai (set 294, analisis tambahan; tidak ada padanan 274)

Rumus: Brier gabungan (model m) = sum_i (n_i x B_i) / sum_i n_i, dengan i adalah lima baris own R3, near R1, near R3, far R1, far R3 (batas 1), B_i adalah Brier batas 1 pada CSV tabel_utama294_3model.csv (set UTAMA-294), dan n_i adalah n pada baris CSV yang sama. Ini aritmetika langsung dari CSV dan tidak mengulang bootstrap.

| Model | n_i (own R3, near R1, near R3, far R1, far R3) | N = sum n_i | Brier gabungan |
|---|---|---|---|
| qwen3.8-flash | 294, 294, 294, 294, 293 | 1469 | 0,0691 (0,069089) |
| qwen4-max-preview | 294, 294, 294, 294, 294 | 1470 | 0,1119 (0,111862) |
| deepseek-v4.1-flash | 288, 294, 294, 294, 294 | 1464 | 0,0569 (0,056929) |

Nilai ini adalah rerata seluruh observasi berjangkar berlabel, sehingga N sama dengan jumlah observasi berlabel. Interval bootstrap gabungan tidak dihitung. Ini deviasi dari rencana praregistrasi, dan naskah mencatatnya di 04.

## 3. Yang tidak dilakukan

- Interval bootstrap untuk Brier gabungan tidak dihitung. Menghitungnya memerlukan skrip bootstrap yang sama dengan harness dan membaca ulang nyata_*_u1.jsonl. Tugas ini hanya aritmetika dari CSV.
- Temuan K3 (D3 tidak tercatat di CATATAN_DEVIASI.md), K6 (path lokal di Lampiran A), K7 (nama penilai di berkas sumber), dan P1 sampai P5 sebagian besar berada di berkas Penulis A atau memerlukan keputusan penulis. Tidak diubah oleh WB.
- Gemini (P6): hasil holdout Gemini belum dilaporkan di 04 atau Lampiran D. Keputusan ada di tangan penulis (07 dan Lampiran D).
- Judul dan kata "kalibrasi" (K2) berada di berkas Penulis A dan pendahuluan. Tidak diubah oleh WB.
