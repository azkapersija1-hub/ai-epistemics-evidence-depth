# Catatan Utama-294 (hitung ulang analisis utama dan kepekaan)

Status: HASIL MODEL (BELUM DIVERIFIKASI). Tidak ada kesimpulan tentang model atau set yang lebih benar.

## Cara hitung
- Skrip: skrip_analisis_utama294.py (memakai modul harness yang sama: laporan, laporan_teks, subset; tau 0,7; B=2000; seed default).
- Tidak ada pemanggilan model atau API. Berkas input hanya dibaca. Kunci dibaca untuk evaluasi saja, isinya tidak dicetak.
- Input: bahan/v2/items_model.jsonl (2058 observasi) dan bahan/v2/RAHASIA/kunci.jsonl; keluaran nyata_<split>_<model>_u1.jsonl untuk qwen3.8-flash, qwen4-max-preview, deepseek-v4.1-flash.
- Hash input sebelum dan sesudah skrip sama untuk semua 42 berkas (lihat hash_cek.md). Hash sebelum juga dicek ulang lewat sha256sum: 28 dari 28 cocok.

## Set analisis dan jumlah klaim
| Set | Klaim | Observasi | Keterangan |
|---|---|---|---|
| UTAMA-294 | 294 | 2058 | Semua klaim, termasuk pilot (sesuai permintaan) |
| UTAMA-274 | 274 | 1918 | Tanpa pilot (20 klaim) |
| KEPEKAAN-A | 290 | 2030 | Dikurangi 4 JANGKAR KELUAR: C0056, C0057, C0225, C0295 |
| KEPEKAAN-B | 280 | 1960 | Dikurangi 14 JANGKAR dengan suara TIDAK_LAYAK |
| SPLIT pilot / dev / val / holdout | 20 / 78 / 98 / 98 | 140 / 546 / 686 / 686 | Urutan eksploratif lalu konfirmatif |

- Daftar KEPEKAAN-B: C0025, C0056, C0057, C0101, C0107, C0109, C0144, C0152, C0162, C0224, C0225, C0230, C0287, C0295.
- C0085 dan C0233 muncul di ID_KELUAR_KETAT.txt hanya di bagian UBAHAN, sehingga tidak dikurangkan. Keduanya tetap berstatus JANGKAR DIPAKAI.
- Silang daftar dengan status_butir.csv: cocok untuk A (4 KELUAR) dan B (14 JANGKAR dengan TIDAK_LAYAK).
- C0230 berstatus DIREVISI (bukan KELUAR). Ia tetap di UTAMA-294, UTAMA-274, dan KEPEKAAN-A, tetapi dikeluarkan di KEPEKAAN-B karena punya suara TIDAK_LAYAK.

## Pilot
- Pilot adalah tahap teknis menurut praregistrasi dan tidak dilaporkan sebagai hasil. Baris UTAMA-294 memasukkannya sesuai permintaan. UTAMA-274 adalah baris tanpa pilot. Semua tabel per split menampilkan pilot hanya untuk kelengkapan.

## Validasi replikasi
- Teks per split dihasilkan ulang dan dibandingkan byte per byte dengan analisis_<split>_<model>.md yang sudah ada: 9 dari 9 IDENTIK (3 model x dev, val, holdout). Detail di replikasi_cek.md.
- Split pilot tidak punya berkas pembanding.
- Pemilihan split lewat pilih_split() sama dengan jalur harness; subset per klaim dicek setara.

## Perubahan jumlah klaim dan observasi
- 294 turun ke 290 (KEPEKAAN-A) dan 280 (KEPEKAAN-B). Observasi 2058 turun ke 2030 dan 1960.
- Lapis36 memakai 36 klaim dan 252 observasi, hanya pilot+dev+val. Angkanya tidak setara dengan KEPEKAAN-A karena cakupan berbeda. Disalin apa adanya ke tabel_kepekaan.md.
- Nama metrik "Sesuai" di CSV lapis36 ditulis "label R1 = R3". Dinormalisasi ke "label R1 = label R3" saat dibaca. Tidak mengubah angka.

## Klaim gagal parse (dari jumlah_set.md, set UTAMA-294)
- qwen3.8-flash: 1 observasi gagal percobaan pertama, 1 gagal final (tidak pulih setelah ulang).
- qwen4-max-preview: 1 gagal percobaan pertama, 0 gagal final.
- deepseek-v4.1-flash: 20 gagal percobaan pertama, 8 gagal final. Akibatnya 6 klaim tidak masuk uji konsistensi (288 dari 294). Brier batas 1 mengeluarkan butir gagal; batas 2 memberi 2,0 untuk butir gagal.
- Keterbatasan dari praregistrasi berlaku: temperature tidak dapat diatur lewat model_api.

## Holdout
- Praregistrasi menyebut holdout dijalankan sekali. Pada eksekusi ini log tidak dibuka ulang, sehingga klaim "dijalankan sekali" tidak diverifikasi di sini. Sumber: CATATAN_DEVIASI.md dan log harness.

## Catatan lain
- Angka UTAMA-294 dan KEPEKAAN di tabel adalah hasil mentah harness tanpa penyetelan. Tidak ada aturan, tau, atau prompt yang diubah.
- Tidak ada kunci API atau isi kunci jawaban dalam keluaran.
