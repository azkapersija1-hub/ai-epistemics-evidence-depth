# Ringkasan Video 274: Seberapa Banyak Bukti Itu Cukup?

Video ringkasan untuk set UTAMA-274 (274 klaim non-pilot, 7 kondisi, 1.918 observasi per model, tiga model API). Set 294 (termasuk pilot) hanya analisis tambahan dan disebut demikian di adegan Data. Berkas 294 tidak diubah.

Batasan: tanpa API/model, tanpa statistik baru. Semua angka dibaca dari baris UTAMA-274 di results/utama294/tabel_utama294_3model.csv (identik byte per byte dengan CSV sumber di C:\EPIS_KERJA), jumlah_set.md, dan KESTABILAN.csv.

## Berkas

| Berkas | Keterangan |
|---|---|
| video/ringkasan274_en.mp4 | Versi Inggris, 1920x1080, 30 fps, H.264, 83,5 detik, 4.041.899 byte |
| video/ringkasan274_id.mp4 | Versi Indonesia, spesifikasi sama, 4.081.242 byte |
| video/angka_pencocokan274_en.txt / _id.txt | Log pencocokan angka dan tata letak |
| src/analisis/bangun_video274.py | Skrip pembangun (salinan bangun_video294.py) |

## Adegan (8)

Judul; Desain; Data (274 non-pilot, 1.918 obs, validasi 40/36, set 294 hanya tambahan); Hasil (Brier own/near/far R3); Salah dukung R3 dan Sesuai R1-R3; Selisih near-far R1 dan R3 (CI) dan kestabilan uji ulang; Keterbatasan; Penutup.

## Catatan

- Adegan kepekaan 294/290/280 dihilangkan: tidak ada baris UTAMA-274 pada tabel_kepekaan.csv. Diganti selisih near-far R1 dan R3 (nilai dan CI tersimpan; sama dengan Figure 2 G2_near_far_en.svg).
- Kestabilan uji ulang (19 klaim, 133 observasi) adalah sampel terpisah yang tidak dihitung ulang pada 274; dilabeli demikian di layar.
- Klaim "holdout dijalankan sekali" dihilangkan (tidak diverifikasi). Pooled Brier tidak ditampilkan.
- Definisi salah dukung di layar mengikuti keterangan Figure 2 (massa pada SUPPORTED atau REFUTED saat label jangkar NEI); perlu dicek penulis.
- Jumlah n: deepseek own R3 dan Sesuai 268 dari 274; qwen3.8 far R3 273 dari 274 (gagal parse dikecualikan).
