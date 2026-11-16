# INDEKS294: gambar set 294 (analisis tambahan; tiga model API)

> Catatan (diperbarui): gambar H1 sampai H5 memakai set UTAMA-294, yaitu 294 klaim termasuk 20 pilot. Set ini adalah analisis tambahan, bukan set pelaporan utama. Set pelaporan utama adalah 274 klaim non-pilot (dev 78, val 98, holdout 98). Gambar G1 sampai G7 ada di `figures/`. Teks di bawah ini adalah catatan pembangunan asli dan tidak diubah, sehingga istilah "utama" di dalamnya merujuk pada nama set UTAMA-294.

Dibangun: 2026-11-15 11:32 oleh `C:\EPIS_KERJA\RENDER\gambar294\bangun_gambar294.py`. Ulang dengan: `py -3.12 -I -X utf8 C:\EPIS_KERJA\RENDER\gambar294\bangun_gambar294.py`.

Status angka: HASIL MODEL (BELUM DIVERIFIKASI), sesuai berkas sumber. Tidak ada model dipanggil, tidak ada statistik baru, tidak ada berkas sumber diubah. Keluaran hanya di `C:\EPIS_KERJA\RENDER\gambar294\`. Gambar lama di `C:\EPIS_KERJA\RENDER\gambar\` tidak disentuh.

## Daftar gambar

Setiap gambar ada dalam dua bahasa (`_en`, `_id`) dengan PNG 300 dpi dan SVG. Keterangan kaki selalu dalam bahasa Inggris, sesuai permintaan.

| Gambar | Isi | Sumber data (CSV) |
|---|---|---|
| H1 `H1_brier_bukti_utama294` | Brier batas 1 per model: own R3, near R3, far R3, batang galat 95% CI | `tabel_utama294_3model.csv`, set UTAMA-294 |
| H2 `H2_kesesuaian_pergeseran_utama294` | Kesesuaian label R1 = R3, pergeseran dS, pergeseran dN, dengan CI (tiga panel) | `tabel_utama294_3model.csv`, set UTAMA-294 |
| H3 `H3_false_support_overkomit_utama294` | False-support near R3 dan far R3 dengan CI; panel kecil overkomit tau 0,7 | `tabel_utama294_3model.csv`, set UTAMA-294 |
| H4 `H4_kepekaan_set_bersarang_utama294` | Nilai titik dan CI: Brier own R3, Brier near R3, kesesuaian R1 = R3 untuk UTAMA-294, KEPEKAAN-A, KEPEKAAN-B | `tabel_kepekaan.csv` (kolom sumber 294, KEPEKAAN-A, KEPEKAAN-B) |
| H5 `H5_panel_ringkas_utama294` | Panel 2x2 ringkas: (a) H1, (b) H2 kesesuaian, (c) H3 false-support, (d) H4 Brier own R3 antar set | Sama dengan H1 sampai H4 |

Nama berkas lengkap: `<nama>_en.png`, `<nama>_en.svg`, `<nama>_id.png`, `<nama>_id.svg`.

## Pencocokan angka

Setiap angka gambar dibaca dari CSV. Angka yang sama di MD dibandingkan (toleransi 0,00005 untuk 4 desimal). Skrip berhenti bila ada beda. Pencocokan lintas berkas juga dilakukan untuk kolom 294 dan jumlah klaim.

| Berkas yang dicocokkan | Cocok | Beda |
|---|---|---|
| tabel_utama294_3model.md | 60 | 0 |
| tabel_kepekaan.md | 180 | 0 |
| tabel_kepekaan.csv (294) vs tabel_utama294_3model.csv | 60 | 0 |
| jumlah_set.md (klaim, observasi, uji konsistensi) | 9 | 0 |

Contoh angka yang dicocokkan (CSV = MD):

- H1 own R3, qwen3.8-flash: 0.0322 [0.0112; 0.0579] (md: 0.0322 [0.0112; 0.0579]).
- H1 near R3, qwen4-max-preview: 0.2312 [0.1753; 0.2932] (md: 0.2312 [0.1753; 0.2932]).
- H1 own R3, deepseek-v4.1-flash (n = 288): 0.0919 [0.0547; 0.1340] (md: 0.0919 [0.0547; 0.1340]).
- H3 false-support far R3, qwen3.8-flash (n = 293): 0.0707 [0.0503; 0.0952] (md: 0.0707 [0.0503; 0.0952]).
- H2 kesesuaian R1 = R3, deepseek-v4.1-flash (n = 288): 0.4896 [0.4340; 0.5486] (md: 0.4896 [0.4340; 0.5486]).
- H4 own R3, qwen4-max-preview, KEPEKAAN-B: 0.0228 [0.0093; 0.0399] (md: 0.0228 [0.0093; 0.0399]).
- Jumlah: UTAMA-294 294 klaim, 2058 observasi; KEPEKAAN-A 290 klaim, 2030 observasi; KEPEKAAN-B 280 klaim, 1960 observasi; uji konsistensi DeepSeek 288 / 284 / 274 klaim.

## Pemeriksaan tata letak

Setiap teks diperiksa untuk tumpang tindih antar teks dan keluar dari figur. Pemeriksaan visual dengan membaca PNG dilakukan terpisah (lihat catatan).

| Gambar | Tumpang tindih | Keluar figur |
|---|---|---|
| H1_brier_bukti_utama294_en | 0 | 0 |
| H2_kesesuaian_pergeseran_utama294_en | 0 | 0 |
| H3_false_support_overkomit_utama294_en | 0 | 0 |
| H4_kepekaan_set_bersarang_utama294_en | 0 | 0 |
| H5_panel_ringkas_utama294_en | 0 | 0 |
| H1_brier_bukti_utama294_id | 0 | 0 |
| H2_kesesuaian_pergeseran_utama294_id | 0 | 0 |
| H3_false_support_overkomit_utama294_id | 0 | 0 |
| H4_kepekaan_set_bersarang_utama294_id | 0 | 0 |
| H5_panel_ringkas_utama294_id | 0 | 0 |

## Catatan dan masalah

1. **Tidak ada GPT-6.1 Sol (codex) di set ini.** Set UTAMA-294 hanya memuat tiga model API. Codex tidak digambar karena datanya tidak ada di sumber ini.
2. **n di bawah 294.** deepseek-v4.1-flash punya n = 288 pada uji konsistensi, pergeseran, dan overkomit, serta pada own R3 Brier. qwen3.8-flash punya n = 293 pada far R3. Pengecualian ini ditulis di keterangan kaki H1 sampai H5, dan keterangan kaki juga memuat n uji konsistensi DeepSeek 288.
3. **Definisi pergeseran dS dan dN tidak tertulis di CSV atau MD.** Skrip sumber hanya memakai nama metrik. Gambar memakai nama seperti di CSV dengan skala 0 sampai 1 sesuai berkas. Definisi perlu dicek penulis sebelum dikutip di laporan.
4. **Definisi overkomit tau 0,7 tidak diulang di gambar.** Gambar hanya menulis 'as in CSV'. Pemakaian tau 0,7 sama dengan judul kolom sumber.
5. **Set bersarang.** KEPEKAAN-B (280) adalah subset dari KEPEKAAN-A (290), yang adalah subset dari UTAMA-294 (294). Keterangan kaki H4 dan H5 menyatakan hal ini. Titik antar set tidak independen, dan garis di H4 hanya menunjukkan urutan set.
6. **Lapis 36 tidak dipakai.** `tabel_kepekaan.csv` juga memuat kolom lapis36 dengan cakupan berbeda (36 klaim, 252 observasi). Kolom itu sengaja dikeluarkan dari H4 karena permintaan hanya tiga set.
7. **Kepekaan hanya nilai titik dan CI.** Brier batas 2 tidak dipakai karena tidak ada CI di sumber.
8. **Versi ringkas H5 lebih sedikit dari H2, H3, H4.** Panel (b) H5 hanya kesesuaian R1 = R3. Panel (c) H5 hanya near dan far R3 tanpa overkomit. Panel (d) H5 hanya Brier own R3 antar set.
9. **Pilot ikut dalam UTAMA-294** sesuai permintaan. Keterangan kaki menyatakan bahwa pilot adalah tahap teknis menurut praregistrasi.
10. **Judul tanpa kesimpulan model.** Judul hanya menyebut isi grafik. Keterangan kaki memuat 'pattern not ranking'.
11. **Angka ID memakai koma desimal.** Keterangan kaki tetap berbahasa Inggris di kedua versi.

