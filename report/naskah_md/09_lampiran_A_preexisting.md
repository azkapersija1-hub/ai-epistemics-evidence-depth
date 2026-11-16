# Lampiran A. Pekerjaan sebelum sprint (preexisting)

## A.1 Daftar pekerjaan terdahulu

Bagian ini merangkum register pekerjaan terdahulu yang disusun pada fase riset sebelumnya. Pekerjaan yang dibuat sebelum periode sprint (13 sampai 15 November 2026) dicatat sebagai preexisting.

| Aset | Dibuat | Keterangan |
|---|---|---|
| Persiapan protokol sanggahan berulang (skoring, fixture, templat, validasi FEVER dev) | 4 Nov 2026 | Belum ada hasil model. Desain berbeda (biner FEVER, tekanan sanggahan). Jika dipakai, wajib dinyatakan. |
| Instrumen FEVER 45 butir dan respons tiga model | 29 Okt 2026 | Tahap pilot dan pengembangan. |
| Alat ukur ARAL versi 1 sampai 7 (mode FEVER, ECE, Brier) | Okt 2026 | Alat dan tes. |
| Kode F11x dan proyek Swarm | 6 sampai 8 Nov 2026 | Penelitian berbeda. Hasil Swarm tidak dipakai sebagai hasil baru. |
| Basis data korpus akademik dan basis kemiripan | Agustus 2026 | Bahan, bukan item uji. 24.054 dokumen. |
| Embedding buku TLS | 6 Nov 2026 | Tidak relevan. Domain dan model berbeda. |
| Formula STP, MOI, dan RCC | Jul sampai Sep 2026 | Dasar sebagian fitur F11x. |
| Alat bantu bot dan toolkit terpadu | Okt sampai Nov 2026 | Alat bantu, bukan kontribusi penelitian ini. |

Pekerjaan yang dibuat pada 13 sampai 15 November 2026, yaitu butir uji baru dari korpus, protokol tiga label baru, skrip skoring multikelas baru, run model, dan analisis, dicatat sebagai baru. Selebihnya dicatat sebagai preexisting.

## A.2 Tabel fakta tanggal

Semua waktu di bawah dalam WIB (UTC+07:00). Status diisi sama untuk seluruh baris.

| No | Pekerjaan atau tahap | Awal (WIB) | Akhir (WIB) | Status | Catatan sumber |
|---|---|---|---|---|---|
| 1 | Pembekuan praregistrasi | 2026-11-11 23:08:13 | sama dengan awal | DIPUTUSKAN OLEH PENULIS | PREREG_DIBEKUKAN |
| 2 | qwen3.8-flash, semua split, ulangan 1 (2.058 baris) | 2026-11-11 23:08:36 | 2026-11-12 00:27:31 | DIPUTUSKAN OLEH PENULIS | nyata_*_u1 |
| 3 | deepseek-v4.1-flash, semua split, ulangan 1 (2.078 baris termasuk ulangan parse) | 2026-11-11 23:14:48 | 2026-11-12 00:37:34 | DIPUTUSKAN OLEH PENULIS | nyata_*_u1 |
| 4 | deepseek-v4.1-flash, arsip pilot max_tokens 512 (169 baris) | 2026-11-11 23:12:12 | 2026-11-11 23:14:06 | DIPUTUSKAN OLEH PENULIS | arsip pilot |
| 5 | qwen4-max-preview, semua split, ulangan 1 (2.059 baris) | 2026-11-12 09:18:16 | 2026-11-12 10:27:09 | DIPUTUSKAN OLEH PENULIS | nyata_*_u1 |
| 6 | GLM-5.3, dihentikan (2.013 baris) | 2026-11-12 11:04:47 | 2026-11-12 12:48:24 | DIPUTUSKAN OLEH PENULIS | glm_dihentikan |
| 7 | Gemini 3.8 Flash, per batch (catatan LOG) | 2026-11-12 11:04:45 | 2026-11-12 12:49:05 | DIPUTUSKAN OLEH PENULIS | LOG.txt |
| 8 | Gemini 3.8 Flash, stempel waktu kolom `waktu` berkas nyata (bukan waktu batch) | 2026-11-12 12:51:06 | 2026-11-12 12:51:06 | DIPUTUSKAN OLEH PENULIS | nyata_*_antigravity_u1 |
| 9 | Uji ulang kestabilan lapis 19, tiga model API, ulangan 2 (400 baris) | 2026-11-13 17:00:53 | 2026-11-13 17:41:46 | DIPUTUSKAN OLEH PENULIS | _retest_lapis19 |
| 10 | Sesi GPT-6.1 Sol (tidak terverifikasi), sesi 40, 280 baris | 2026-11-13 17:15:25 | 2026-11-13 17:23:55 | DIPUTUSKAN OLEH PENULIS | IDENTITAS dan LOG |
| 11 | Sesi GPT-6.1 Sol (tidak terverifikasi), sesi 19, 133 baris | 2026-11-13 17:31:46 | 2026-11-13 17:35:48 | DIPUTUSKAN OLEH PENULIS | IDENTITAS dan LOG |
| 12 | Amandemen 4, 5, dan 6 (tanggal tercatat tanpa jam) | 2026-11-12 | 2026-11-12 | DIPUTUSKAN OLEH PENULIS | PREREG_DIBEKUKAN |
| 13 | Penilaian pasangan dan perundingan empat klaim (tanggal tercatat tanpa jam) | 2026-11-13 | 2026-11-13 | DIPUTUSKAN OLEH PENULIS | ringkasan kelayakan |
| 14 | Sprint resmi (jadwal) | 2026-11-13 | 2026-11-15 (batas 23.59 AoE) | DIPUTUSKAN OLEH PENULIS | halaman sprint |

Catatan untuk tabel: pada baris 8, stempel waktu seragam dalam satu detik untuk seluruh batch, sehingga kolom tersebut bukan waktu batch. Waktu batch Gemini ada pada baris 7. Berkas Codex sesi 40 dan sesi 19 tidak memiliki kolom `waktu`, sehingga tanggal sesi diambil dari berkas identitas dan log.

Hash prompt API (`prompt_v1.txt`, sha256): 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530.
