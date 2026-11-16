# Log katalog metadata (36 artikel asal klaim)

Tanggal: 2026-11-13. Sumber: KATALOG_METADATA_LENGKAP.xlsx (salinan baca saja di _tmp, dihapus setelah selesai). Tidak ada internet, tidak ada model, tidak ada penulisan ke drive D:.

## 1. Berkas dan hash

| Item | Nilai |
|---|---|
| Ukuran berkas asli | 3.698.258 byte (3,53 MB), di bawah batas 300 MB, disalin satu kali |
| SHA-256 asli di D: sebelum salin | 6312528964D264E0642586FA197C2BBE4D503D49CBD3CB01F59C33F20DB2EA93 |
| SHA-256 salinan setelah salin | 6312528964D264E0642586FA197C2BBE4D503D49CBD3CB01F59C33F20DB2EA93 (identik) |
| SHA-256 asli di D: sesudah pekerjaan | lihat bagian 8 |

## 2. Struktur katalog

Lembar yang ada: 3.

| Lembar | Baris (max_row, termasuk header) | Kolom | Dipakai |
|---|---|---|---|
| Ringkasan | 71 | 2 | Tidak |
| Katalog Lengkap | 6.091 (6.090 baris data) | 19 | Ya |
| Kandidat Meta-Analisis | 656 | 8 | Tidak |

Kolom lembar "Katalog Lengkap": No, Folder Variabel, Judul, Penulis, Tahun, Jurnal, Volume, Issue, DOI, Bahasa, Desain Penelitian, N (Sampel), p-value, Abstrak, Kata Kunci, Sumber Tambahan (Antigravity), Status Ekstraksi, Nama File, Path File.

Tidak ada kolom doc_id, halaman, atau jenis dokumen di katalog. Kolom "Issue" dipetakan ke nomor, "Jurnal" ke venue. Kolom halaman dan jenis dokumen dikosongkan. Kolom Abstrak, Desain Penelitian, N, dan p-value tidak disalin.

Kualitas kolom di lembar utama: 1.724 baris tanpa DOI. Kolom Jurnal terisi hanya 283 dari 6.090 baris.

## 3. Metode pencocokan

- Kunci utama: DOI, dinormalisasi (huruf kecil, awalan https://doi.org/ dibuang).
- Hasil: 36 dari 36 artikel cocok lewat DOI, masing-masing tepat satu baris katalog.
- Judul ternormalisasi (huruf kecil, tanda baca dan spasi ganda dibuang) sama persis untuk 11 artikel (metode DOI+judul). Untuk 25 artikel metode tetap DOI.
- Tidak ada yang cocok lewat judul saja, tidak ada yang tidak ditemukan, tidak ada yang ganda.
- DOI mentah di katalog dan di CSV identik untuk ke-36 artikel (0 beda format).

## 4. Beda judul (dicatat, tidak dipilih)

Judul di katalog dan di artikel_asal_36_klaim.csv berbeda untuk 25 artikel (normalisasi). Untuk 6 artikel, kolom judul di CSV berisi teks halaman yang panjang (lebih dari 200 karakter), bukan judul saja: C0014, C0025, C0032, C0085, C0088, C0216. Untuk 19 artikel lainnya, CSV dan katalog berbeda dalam judul yang pendek atau berbeda redaksi.

Daftar claim_id dengan judul beda: C0006, C0014, C0025, C0032, C0052, C0066, C0085, C0088, C0094, C0099, C0101, C0102, C0105, C0107, C0109, C0119, C0151, C0152, C0162, C0168, C0176, C0191, C0216, C0230, C0246.

## 5. Judul katalog yang tampak bukan judul artikel (ditandai, tidak diperbaiki)

Judul di katalog untuk 15 artikel tampak berisi nama jurnal, nama konferensi, header halaman, afiliasi, atau kutipan, bukan judul artikel: C0006, C0022, C0025, C0066, C0094, C0099, C0101, C0102, C0107, C0109, C0119, C0151, C0162, C0216, C0246. Tanda ini penilaian visual, bukan aturan otomatis, dan judul katalog tetap disalin persis.

## 6. Beda bahasa (katalog vs label pool di CSV)

Label bahasa di katalog berbeda dari kolom bahasa di artikel_asal_36_klaim.csv untuk 8 artikel: C0014, C0035, C0100, C0102, C0110, C0154, C0162, C0230. Enam di antaranya (C0014, C0035, C0100, C0102, C0110, C0162) berlabel "unk" di CSV. Dua merupakan konflik nyata: C0154 (CSV id, katalog en) dan C0230 (CSV en, katalog id). Semua dicatat, tidak dipilih. Katalog: id 19, en 17. CSV: id 16, en 14, unk 6.

## 7. Artikel tidak ditemukan, ganda, dan kolom kosong

- Tidak ditemukan: 0.
- Ganda: 0.
- Status: LENGKAP 1 (C0224), SEBAGIAN 35.
- Penulis kosong di katalog: 1 (C0152).
- Jurnal (venue) kosong: 35 artikel. Hanya C0224 yang punya venue di katalog.
- Volume kosong: 5. Issue kosong: 8.
- Tahun: terisi untuk 36 artikel, rentang 2016 sampai 2026.

## 8. Hash akhir

Hash berkas asli di D: diperiksa ulang sesudah semua pekerjaan selesai dan sebelum folder _tmp dihapus. Hasil dicatat di laporan akhir. Berkas asli tidak diubah, tidak ditimpa, dan tidak ada yang ditulis ke D:.

## 9. Keluaran

- artikel_asal_36_klaim_lengkap.csv (36 baris, 14 kolom). Berkas artikel_asal_36_klaim.csv tidak diubah.
- LAMPIRAN_SUMBER_DATA_v2.md
- LOG_KATALOG.md (berkas ini)
- Folder _tmp dihapus setelah selesai.

## 10. Masalah dan batasan

- Metadata berasal dari katalog internal dan belum diverifikasi ulang ke penerbit.
- DOI di CSV diperoleh dari hasil pindai teks (menurut LOG_VERIFIKASI dan LAMPIRAN v1), sehingga kecocokan DOI bergantung pada DOI tersebut. Ke-36 DOI ditemukan di katalog, tetapi beberapa DOI di CSV tampak terpotong (misalnya 10.23917/bik.v, 10.2478/pcssr), dan kecocokannya hanya karena DOI yang sama juga ada di katalog. Ini perlu dicek manusia.
- Kolom halaman dan jenis dokumen tidak ada di katalog.
- Tidak ada metadata yang dikarang atau diperbaiki. Sel kosong tetap kosong.
