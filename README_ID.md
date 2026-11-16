# Seberapa Banyak Bukti yang Cukup?
## Kalibrasi verdict LLM lintas kedalaman bukti pada klaim akademik

*How Much Evidence Is Enough? Calibration of LLM Verdicts Across Evidence Depth on Academic Claims*

> **Status: persiapan dan hasil awal.** Keluaran model di folder `results/` ditandai oleh harness sebagai "HASIL MODEL (BELUM DIVERIFIKASI)" dan hanya sah sesuai praregistrasi. Repositori ini bukan kesimpulan.
>
> Konteks: Apart Research AI x Epistemics sprint. Lisensi belum diputuskan (lihat `LICENSE_PERLU_DIPUTUSKAN.md`).

## Ringkasan

Model bahasa sering diminta menilai apakah sebuah klaim ilmiah didukung, dibantah, atau belum cukup bukti (SUPPORTED, REFUTED, NEI). Studi ini menanyakan apakah penilaian itu tetap terkalibrasi ketika model hanya membaca bagian awal artikel (R1: abstrak; R2: abstrak dan hasil) dibanding teks relevan penuh (R3). Desain dibekukan sebelum jawaban model dikumpulkan dan memakai label jangkar mekanis, bukan label ahli penuh. Analisis utama praregistrasi memakai 294 klaim untuk tiga model API. Lapis subset yang dinilai tim (40, 36, 26, dan 19) dan dua set kepekaan (290 dan 280 klaim) adalah analisis kepekaan, bukan analisis utama. Hasil yang ada bersifat deskriptif dan belum diverifikasi ulang, sehingga belum mendukung kesimpulan.

## Pertanyaan penelitian

1. Seberapa terkalibrasi distribusi SUPPORTED, REFUTED, dan NEI keluaran model pada tiap kedalaman bukti (R1, R2, R3)?
2. Seberapa sering model terlalu yakin pada R1 dibanding R3 (overkomit, tau = 0,7)?
3. Seberapa besar dukungan palsu (false-support mass) pada bukti dari artikel lain (near dan far)?

## Hasil utama

Analisis utama (UTAMA-294) memakai 294 klaim dan 2058 observasi untuk tiga model API: qwen3.8-flash, qwen4-max-preview, dan deepseek-v4.1-flash. Set ini mencakup pilot (20 klaim) sesuai Amandemen 5. Varian tanpa pilot (UTAMA-274) disediakan sebagai pembanding. Tidak ada aturan, parameter tau, atau prompt yang disetel setelah melihat hasil.

Lapis subset tim dan dua set kepekaan (KEPEKAAN-A dengan 290 klaim, KEPEKAAN-B dengan 280 klaim) adalah analisis kepekaan. Keduanya tidak menggantikan analisis utama. GPT-6.1 Sol (identitas dan konfigurasi tidak terverifikasi) dan Gemini 3.8 Flash (Antigravity) hanya dijalankan lewat jalur agen pada subset dan tidak masuk analisis utama. glm-5.3 dihentikan (lihat Keterbatasan).

Angka terpilih (rerata atau proporsi, tanpa penyetelan):

| Metrik (UTAMA-294) | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash |
|---|---|---|---|
| Brier batas 1, own R3 | 0,0322 | 0,0222 | 0,0919 |
| Overkomit (tau 0,7) | 0,0068 | 0,0068 | 0,0208 |
| False-support near R1 | 0,0718 | 0,1473 | 0,0446 |
| Sesuai (label R1 = label R3) | 0,5034 | 0,5306 | 0,4896 |

Tabel lengkap dengan interval kepercayaan bootstrap ada di `results/utama294/tabel_utama294_3model.md`. Set lain dan uji per split ada di `results/utama294/` (`analisis_*.md`, `results/utama294/tabel_kepekaan.md`, `results/utama294/tabel_per_split.md`). Grafik H1 sampai H5 (versi en dan id) ada di `figures_294/`, dengan indeks di `figures_294/INDEKS294.md`.

Status: HASIL MODEL (BELUM DIVERIFIKASI). Angka ini tidak menunjukkan model mana yang lebih benar.

## Struktur folder

```
repo/
  .gitignore
  CITATION.cff
  EXCLUDED.md
  LICENSE_PERLU_DIPUTUSKAN.md
  README.md
  README.md
  data/  (1 berkas langsung)
    claim_id/  (4 berkas)
    kelayakan/  (12 berkas)
  docs/  (3 berkas langsung)
    fase1_riset/  (21 berkas)
    panduan_penilai/  (2 berkas)
    prareg/  (2 berkas)
  figures/  (29 berkas langsung)
  figures_294/  (22 berkas)
  results/  (0 berkas langsung)
    codex_gpt61_sol_tak_terverifikasi/  (16 berkas)
    deepseek_v4_1_flash/  (9 berkas)
    gemini_antigravity/  (38 berkas)
    glm_dihentikan/  (1 berkas)
    lapis36/  (5 berkas)
    perbandingan_lapis/  (5 berkas)
    qwen3_8_flash/  (7 berkas)
    qwen4_max_preview/  (7 berkas)
    retest_lapis19/  (12 berkas)
    utama294/  (18 berkas)
  report/  (draf Indonesia: Word, PDF, naskah md)
  references/  (daftar pustaka v2 dan katalog sumber artikel)
  external_sessions/  (5 berkas langsung)
  src/  (0 berkas langsung)
    analisis/  (6 berkas)
    harness/  (35 berkas)
  video/  (video ringkasan 294 klaim, dua bahasa)
```

Rincian yang tidak disalin dan alasannya ada di `EXCLUDED.md`. Path absolut yang tertanam di kode ada di `docs/PATH_MAP.md`.

## Pekerjaan sebelum sprint (preexisting)

Bagian ini wajib dibaca sebelum memakai repositori. Daftar di bawah disalin dari `docs/PEKERJAAN_PREEXISTING.md`. Setiap aset yang dipakai atau disinggung dalam laporan harus ditandai "preexisting".

| Aset | Lokasi | Dibuat | Status | Catatan |
|---|---|---|---|---|
| Persiapan Apart P1 (protokol "repeated unsupported rebuttal", skoring, fixture, templat, validasi FEVER dev) | `D:\kerjaan baru\P1_APART_EPISTEMICS\` | 4 Nov 2026 | PRA-SPRINT, HOLD, tanpa hasil model | Desain BERBEDA (binary FEVER, tekanan sanggahan). FEVER dev 19.998 klaim, 6.666/kelas, sha256 `e89865bf...`. Bila dipakai, nyatakan |
| Instrumen FEVER 45 butir + respons 3 model | `D:\PELATIHAN AI ART\alat pengukur AI\UJI_FEVER_45\` | 29 Okt 2026 | PRA-SPRINT; pilot/development | Sudah dijawab GPT-6.1 Sol, Gemini, Haiku 5.5 |
| ARAL v1-v7 (alat ukur, mode FEVER, ECE, Brier) | `D:\PELATIHAN AI ART\alat pengukur AI\ARAL_V*` | Okt 2026 | PRA-SPRINT | Alat dan tes |
| F11x dan kode Swarm | `D:\kerjaan baru\SWARM_ALIGNMENT_2026_FINAL\`, `GITHUB_SWARM_ALIGNMENT\` | 6-8 Nov 2026 | PRA-SPRINT, penelitian BERBEDA | Jangan pakai hasil Swarm sebagai hasil baru |
| DB `core_academic` + `similarity_engine` | `...\art_python\core_academic_db\` | Agustus 2026 | PRA-SPRINT (bahan) | 24.054 dokumen; bukan item uji |
| Embedding 184 buku TLS | `D:\kerjaan baru\26_Embedding_Korpus\` | 6 Nov 2026 | Tidak relevan | Domain dan model berbeda |
| Formula STP/MOI/RCC | `RND_Formula_Discovery` | Jul-Sep 2026 | PRA-SPRINT | Dasar beberapa fitur F11x |
| Bot 70 / Tools Sakti | `D:\kerjaan baru\25_Tools_Sakti_Terpadu\` | Okt-Nov 2026 | PRA-SPRINT, alat bantu | Tidak jadi kontribusi |

**Fakta tanggal pengujian model.** Tanggal di bawah diambil dari kolom `waktu` pada berkas keluaran (zona UTC, apa adanya). Praregistrasi dibekukan pada 2026-11-11 23:08:13 waktu lokal (`docs/prareg/PREREG_DIBEKUKAN.md`).

| Jalur | Jumlah baris bertanggal | Paling awal | Paling akhir |
|---|---|---|---|
| qwen3.8-flash (u1 semua split) | 2058 | 2026-11-11T16:08:36.112169+00:00 | 2026-11-11T17:27:31.006704+00:00 |
| qwen4-max-preview (u1 semua split) | 2059 | 2026-11-12T02:18:16.260977+00:00 | 2026-11-12T03:27:09.594482+00:00 |
| deepseek-v4.1-flash (u1 semua split) | 2078 | 2026-11-11T16:14:48.508147+00:00 | 2026-11-11T17:37:34.523344+00:00 |
| deepseek-v4.1-flash (ARSIP pilot max512, bukan hasil utama) | 169 | 2026-11-11T16:12:12.224614+00:00 | 2026-11-11T16:14:06.105175+00:00 |
| gemini-3.8-flash (Antigravity, pilot dan holdout) | 826 | 2026-11-12T05:51:06.146167+00:00 | 2026-11-12T05:51:06.579439+00:00 |
| GPT-6.1 Sol (Codex, tak terverifikasi, impor lapis 19/26/40) | 728 | 2026-11-13T10:39:27.931011+00:00 | 2026-11-13T10:39:31.133005+00:00 |
| Uji stabilitas ulangan 2 (retest lapis 19, tiga model) | 400 | 2026-11-13T10:00:53.001816+00:00 | 2026-11-13T10:41:46.253155+00:00 |

Tanggal-tanggal ini hanya fakta. Apakah suatu aset termasuk preexisting dalam arti sprint, dan apakah pengujian model di atas dihitung sebagai pekerjaan sprint, **DIPUTUSKAN OLEH PENULIS**.

## Cara mereproduksi

Lingkungan yang dimaksud: Windows, Python 3.12 (perintah memakai `py -3.12`). Skrip memakai path absolut dari lokasi lama. Baca `docs/PATH_MAP.md` sebelum menjalankan apa pun.

Yang dapat dijalankan dari repositori ini:

1. Baca praregistrasi: `docs/prareg/PREREG_DIBEKUKAN.md`, lalu `docs/prareg/CATATAN_DEVIASI.md`.
2. Tes unit harness (tanpa jaringan dan tanpa model):
   `py -3.12 -I -X utf8 -m unittest discover -s src/harness/tests -v`
   Hasil pada salinan ini: 152 tes, 135 lulus, 17 error. Semua error berasal dari `src/harness/tests/test_pipeline.py` dan `src/harness/tests/test_cli_subset.py`, yang membutuhkan `src/harness/fixture_tiruan/items_model.jsonl`. Fixture itu tidak disalin karena memuat kolom `claim_text` dan `evidence_text`. Mengisinya kembali memerlukan pembuatan ulang dengan `src/harness/fixture_tiruan/buat_fixture.py`, yang belum diverifikasi.
3. Tes kelayakan (data tiruan di folder sementara):
   `py -3.12 -I -X utf8 src/analisis/test_hitung_kelayakan.py`
   Hasil pada salinan ini: 32 tes, semua lulus.
4. Lihat ringkasan penilaian kelayakan dan daftar claim_id: `data/kelayakan/` dan `data/claim_id/`.
5. Lihat keluaran analisis yang sudah jadi: `results/utama294/` (analisis utama 294), `results/lapis36/`, `results/perbandingan_lapis/`, `results/retest_lapis19/`, dan per model di `results/`.

Yang TIDAK dapat dijalankan dari repositori ini:

- `src/analisis/skrip_analisis_lapis36.py` dan `src/analisis/skrip_analisis_codex.py` membaca kunci di folder RAHASIA dan berkas item yang tidak disertakan.
- `src/analisis/hitung_kelayakan.py` memerlukan berkas penilaian per penilai (folder hasil_ahli tidak disertakan) dan lembar ahli yang tidak disertakan.
- Panggilan model nyata. Harness mengunci panggilan dengan dua gerbang (flag dan variabel lingkungan) dan memerlukan modul `sakti_core` yang berada di drive D (lihat `docs/PATH_MAP.md`). Urutan wajib: pilot, dev, val, lalu holdout sekali.
- `src/analisis/bangun_gambar.py` dan `src/analisis/bangun_video.py` membaca dan menulis di `C:\EPIS_KERJA\` dan tidak berjalan dari lokasi lain tanpa penyesuaian.
- `results/utama294/skrip_analisis_utama294.py` membaca kunci di folder RAHASIA yang tidak disertakan dan memakai path absolut di `C:\EPIS_KERJA\`. `figures_294/bangun_gambar294.py` juga memakai path absolut di `C:\EPIS_KERJA\`. Keduanya tercatat di `docs/PATH_MAP.md`.

**Kunci jawaban tidak termasuk.** Akses ke kunci ditentukan penulis. Untuk meminta akses, hubungi [Penulis 1] (penulis korespondensi) dengan menyebut tujuan penelitian dan afiliasi. Teks klaim dan bukti dari artikel juga tidak disertakan karena hak cipta.

## Keterbatasan

- Analisis utama memakai 294 klaim, tetapi lapis subset (40, 36, 26, 19) dan set kepekaan lebih kecil. Daya statistik per subset terbatas, dan interval kepercayaan dilaporkan apa adanya.
- Pilot (20 klaim) ikut dalam analisis utama 294 sesuai Amandemen 5 (lihat D3 di `docs/prareg/CATATAN_DEVIASI.md`). Keputusan cara pelaporan pilot ada pada penulis.
- Pelaksanaan holdout yang dijalankan sekali belum diverifikasi ulang dari log harness.
- Label jangkar bersifat mekanis (own R3 = SUPPORTED; near dan far = NEI), bukan penilaian ahli per butir.
- Penilai kelayakan adalah tim penulis sendiri, bukan penilai independen. Kesepakatan tim tercatat di `data/kelayakan/final/`.
- Keluaran GPT-6.1 Sol melalui Codex tidak terverifikasi identitas dan konfigurasinya. Ditandai "tak terverifikasi" di seluruh berkas.
- glm-5.3 dihentikan karena biaya token. Holdout parsialnya tidak dianalisis (`results/glm_dihentikan/CATATAN.md`).
- Temperature tidak dapat diatur lewat jalur model_api (memakai default penyedia).
- Untuk deepseek-v4.1-flash, max_tokens dinaikkan dari 512 ke 4000 setelah pilot teknis (Amandemen 1). Keluaran pilot lama diarsipkan di `results/deepseek_v4_1_flash/arsip/`.
- Gemini (Antigravity): sebagian batch diselesaikan sekaligus, tidak per tiga batch seperti prosedur (deviasi D1).
- Path absolut tertanam di kode untuk satu mesin (`docs/PATH_MAP.md`). Kode tidak diubah.

## Peringatan: gambar G3 sampai G7

Gambar G3 sampai G7 di `figures/` dibangun dari subset lapis 36, bukan dari analisis utama 294. Angkanya tidak sama dengan `results/utama294/`; untuk hasil utama pakai `figures_294/`. Video ringkasan sudah dibuat ulang dari analisis utama 294 (`video/ringkasan294_en.mp4` dan `video/ringkasan294_id.mp4`).

## Katalog sumber dan referensi

- `references/REFERENSI_LAPORAN_v2.md`: daftar pustaka (APA 7) berisi rujukan yang terverifikasi pada halaman sumbernya (24 entri), dengan bagian rujukan yang ditahan. `references/PEMERIKSAAN_SITASI.md` mencatat sitasi yang masih perlu dilengkapi.
- `references/katalog_sumber/`: metadata bibliografis artikel asal 294 klaim (`katalog_sumber_artikel_asal_294.csv`) dan artikel bukti near dan far (`katalog_sumber_bukti_near_far.csv`). Metadata berasal dari katalog internal dan rekaman Crossref (kolom `sumber_metadata` mencatat asal tiap sel). Metadata belum diverifikasi ke penerbit, dan sebagian judul pada berkas bahan keliru sehingga ditandai di kolom `beda_judul_*`. Teks klaim dan teks bukti tidak dibagikan.

## Status naskah

Draf laporan berbahasa Indonesia (Word, PDF, dan naskah Markdown) ada di `report/` dan masih disunting penulis. Penanda `[PENULIS ...]` menunjukkan keputusan yang menunggu penulis. Versi Inggris disiapkan penulis.

## Lisensi

Belum diputuskan. Lihat `LICENSE_PERLU_DIPUTUSKAN.md`.

## Penulis

- [Penulis 1]
- [Penulis 2]
- [Penulis 3]
