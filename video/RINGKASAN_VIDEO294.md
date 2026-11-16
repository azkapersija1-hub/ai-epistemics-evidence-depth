# Ringkasan Video 294: Seberapa Banyak Bukti Itu Cukup?

Dibangun ulang dari data ANALISIS UTAMA 294 (294 klaim x 7 observasi = 2.058 per model, tiga model API). Video lama (lapis 36) di C:\EPIS_KERJA\RENDER\video tidak ditimpa.

Batasan kerja: tidak ada pemanggilan model/API, tidak ada statistik baru, tidak ada berkas sumber yang diubah, tidak ada yang ditulis di drive D:. Hanya satu pencocokan silang pooled Brier dengan CATATAN_WB.md (cocok).

## Berkas

| Berkas | Keterangan | Ukuran |
|---|---|---|
| C:\EPIS_KERJA\RENDER\video294\ringkasan294_en.mp4 | Versi Inggris (utama, untuk Apart) | 3.612.818 byte |
| C:\EPIS_KERJA\RENDER\video294\ringkasan294_id.mp4 | Versi Indonesia | 3.647.023 byte |
| C:\EPIS_KERJA\RENDER\video294\bangun_video294.py | Skrip pembangun (salinan dari bangun_video.py, sumber data diganti) | 33 KB |
| C:\EPIS_KERJA\RENDER\video294\angka_pencocokan294_en.txt / _id.txt | Log pencocokan angka, tata letak, dan suhu | kecil |
| C:\EPIS_KERJA\RENDER\video294\cek_bingkai294\*.png | 8 tangkapan per versi, satu per adegan | sekitar 3,7 MB total |

## Teknis (ffprobe, kedua versi)

- Codec: H.264 (h264_nvenc, preset p5, cq 23), pix_fmt yuv420p, faststart aktif
- Resolusi: 1920 x 1080, 30 fps, 2.415 bingkai
- Durasi: 80,5 detik (dalam rentang 70 sampai 90 detik)
- Audio: tidak ada (teks di layar)

## Adegan (sama untuk kedua versi)

| No | Adegan | Durasi (detik) | Isi |
|---|---|---|---|
| 1 | Judul | 9,0 | Judul, subjudul, pertanyaan penelitian |
| 2 | Desain | 12,0 | Satu klaim, tangga R1 ke R2 ke R3, pembanding near dan far dari artikel lain |
| 3 | Data | 10,0 | 294 klaim, 2.058 observasi per model, 3 model API, validasi tim 40 (36 setelah perundingan), kunci mekanis |
| 4 | Hasil | 14,0 | Brier R3: bukti sendiri, near, far, tiga model dalam satu layar; "lower is better; a pattern, not a ranking" |
| 5 | Salah dukung dan konsistensi | 11,0 | False support near vs far pada R3; label R1 sama dengan R3 |
| 6 | Kepekaan dan kestabilan | 11,0 | Brier sendiri per set (294, 290, 280); kestabilan uji ulang 19 klaim |
| 7 | Keterbatasan | 11,0 | 36 klaim tervalidasi, interval lebar, kunci mekanis, near/far belum independen, GPT-6.1 Sol belum terverifikasi, holdout sekali |
| 8 | Penutup | 6,0 | "A pattern, not a ranking of models" / "Pola, bukan peringkat model" |

Judul adegan tidak menyebut model terbaik. Tidak ada em dash di skrip maupun teks layar. Kunci jawaban dan teks klaim tidak ditampilkan.

GPT-6.1 Sol tidak dipakai di grafik mana pun (hanya disebut di adegan keterbatasan sebagai belum terverifikasi). Berkas KESTABILAN_codex.csv tidak dibuka.

## Sumber per angka dan hasil pencocokan

Semua angka dibaca dari CSV (kolom nilai), lalu dicek di log. Pembulatan hanya untuk tampilan.

| Angka di video | Sumber | Nilai |
|---|---|---|
| Brier own R3 (qwen3.8 / qwen4 / deepseek) | tabel_utama294_3model.csv, set UTAMA-294 | 0,032167 / 0,022180 / 0,091905 (n=288) |
| Brier near R3 | idem | 0,146559 / 0,231240 / 0,074864 |
| Brier far R3 | idem | 0,087131 (n=293) / 0,145517 / 0,071243 |
| False support near R3 | idem | 0,126973 / 0,219762 / 0,068878 (tampil 12,7% / 22,0% / 6,9%) |
| False support far R3 | idem | 0,070717 / 0,148673 / 0,049898 (tampil 7,1% / 14,9% / 5,0%) |
| Konsistensi R1 = R3 (Sesuai) | idem | 0,503401 / 0,530612 / 0,489583 (n=288) |
| Interval Sesuai qwen3.8 | idem | 0,445578 sampai 0,561224 (tampil 44,6% sampai 56,1%) |
| Kepekaan own R3, set 294 / 290 / 280 | tabel_kepekaan.csv (sumber 294, KEPEKAAN-A, KEPEKAAN-B) | qwen3.8: 0,032167 / 0,032597 / 0,027625; qwen4: 0,022180 / 0,022338 / 0,022754; deepseek: 0,091905 / 0,093052 / 0,090762 |
| Kestabilan uji ulang, SEMUA (19 klaim, 133 obs) | _retest_lapis19\KESTABILAN.csv | qwen3.8 0,894737; qwen4 0,947368; deepseek 0,938931 (gagal dihitung beda 0,924812) |
| Jumlah klaim dan observasi | jumlah_set.md, baris UTAMA-294 | 294 klaim, 2.058 observasi per model |
| 40 klaim dinilai | PREREG_DIBEKUKAN.md, frasa "40 pernyataan" | ditemukan |
| 36 klaim tervalidasi | bahan\v2\hasil_olahan_final\lapis_36_claim_id.txt | 36 baris |
| Pooled Brier (cek silang saja, tidak ditampilkan) | CATATAN_WB.md, rumus rerata berbobot n | qwen3.8 0,069089 (N=1469); qwen4 0,111862 (N=1470); deepseek 0,056929 (N=1464). Cocok dengan CSV. |

Pemeriksaan skrip: 3 model cocok di jumlah_set.md; cakupan kestabilan = 19 klaim; daftar 36 klaim dan frasa 294 serta 40 ada di praregistrasi. Semua pemeriksaan lulus (tidak ada keluaran yang dipaksakan).

## Catatan isi

- deepseek-v4.1-flash sendiri R3 memakai 288 dari 294 klaim (6 kegagalan parse dikecualikan). Catatan ini tampil di adegan hasil.
- Pooled Brier tidak ditampilkan di video karena menggabungkan observasi own, near, dan far yang berbeda kunci (SUPPORTED vs NEI). Hanya dipakai sebagai cek silang.
- Definisi "false support" di layar (model menyatakan DIDUKUNG padahal kuncinya NEI) diturunkan dari label metrik "(anchor NEI)" di CSV. Perlu dicek penulis.
- Kalimat "sekitar separuh label berubah" sejalan dengan konsistensi 49,0% sampai 53,1%.

## Suhu GPU

- Sebelum encode: 46 sampai 53 C (berbagai percobaan)
- Setelah encode: 52 sampai 55 C
- Suhu tertinggi selama sesi (sensor pemantau): 56 C, di bawah ambang 80 C. Tidak ada encode yang dihentikan.

## Pemeriksaan tata letak

- Pemeriksaan otomatis (kotak teks keluar batas atau tumpang tindih): 0 masalah, kedua versi.
- Pemeriksaan visual tangkapan 8 adegan per versi: satu masalah ditemukan di adegan kepekaan (kolom "Strict" melewati garis tabel). Sudah diperbaiki dan kedua versi di-render ulang. Tangkapan terbaru bersih.

## Masalah

- Tidak ada masalah NVENC.
- Mohon konfirmasi definisi false support dan bahwa tampilan near/far pada adegan desain sesuai dengan definisi di naskah.
