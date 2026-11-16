# Daftar yang sengaja TIDAK disalin

Daftar ini hanya menyebut nama dan alasan. Isi berkas yang dikecualikan tidak ditampilkan di sini. Nama berkas penilai individual disamarkan dengan `<penilai>`.

## A. Kunci jawaban (rahasia)

| Yang dikecualikan | Alasan |
|---|---|
| `bahan/v2/RAHASIA/` (kunci.jsonl, lapis_data/kunci_lapis_19, 26, 36, 40, kunci_retest_lapis19, pemetaan_lembar_jangkar_30.csv) | Kunci jawaban. Membocorkannya merusak pengujian holdout dan validitas hasil. |
| `bahan/contoh_palsu/out/RAHASIA/kunci.jsonl` | Kunci contoh (folder RAHASIA). |
| `bahan/v2/arsip_v2_0/kunci.jsonl` | Kunci arsip. |
| `harness/fixture_tiruan/kunci.jsonl` | Kunci fixture tiruan. |

## B. Teks klaim atau bukti (hak cipta artikel)

| Yang dikecualikan | Alasan |
|---|---|
| Semua `items_*.jsonl` (bahan/v2, arsip, hasil_olahan_3penilai, hasil_olahan_final, harness/log, _retest_lapis19, fixture_tiruan, contoh_palsu) | Memuat kolom `claim_text` dan `evidence_text`. |
| `bahan/v2/pool_v2.jsonl`, `bahan/v2/kolam_bukti_v2_1.jsonl`, `bahan/arsip_v1_600/pool_kandidat.jsonl` (16 MB) | Memuat teks artikel atau klaim asli. Berkas kandidat terlalu besar dan berisi teks bagian artikel. |
| `bahan/v2/lembar_ahli_40.csv`, `lembar_ahli_jangkar_30.csv`, salinan di arsip, `bahan/arsip_v1_600/pilot_dev_kandidat_klaim.csv`, `bahan/contoh_palsu/lembar_CONTOH_PALSU.csv` | Memuat kolom `claim_original` dan `claim_altered_draft`. |
| `paket_luar/batch_*.jsonl`, `SESI_LUAR/*/batches/*.jsonl`, `SESI_LUAR/gpt61_codex_19/data/semua_19.jsonl`, `SESI_LUAR/gpt61_codex_40/data/semua_40.jsonl` | Kolom `prompt` berisi teks artikel. |
| `bahan/v2/pasangan_v2*.jsonl` dan `bahan/v2/items_model.jsonl` | Berkas pasangan dan item dari pipeline. Tidak disalin dan tidak diperiksa lebih lanjut. |
| `ALAT_VALIDASI_AHLI.html`, `ALAT_VALIDASI_KELAYAKAN.html`, dan templat di `bahan/v2/skrip/` | Alat penilaian lengkap dengan data item. Tidak diperiksa isinya. Tidak masuk struktur. |

## C. Berkas penilai individual (nama dan catatan)

| Yang dikecualikan | Alasan |
|---|---|
| `bahan/v2/hasil_ahli/` dan `hasil_ahli_dengan_diskusi/` (kelayakan_butir_<penilai>_*.csv, pasangan_<penilai>_*.csv) | Penilaian per penilai dengan catatan. |
| `bahan/v2/hasil_ahli_dengan_diskusi/diskusi.csv` | Catatan diskusi per butir. |
| `status_butir.csv` dan `daftar_revisi.csv` pada `hasil_olahan_final/`, `hasil_olahan_3penilai/` (dan `hasil_olahan/`) | Memuat suara per nama penilai dan catatan per penilai. KEPUTUSAN AGEN R: tidak disalin. Perlu persetujuan penulis untuk disalin dalam bentuk ringkas. |

## D. Data parsial dan keluaran tidak lengkap

| Yang dikecualikan | Alasan |
|---|---|
| `HASIL_PENGUJIAN/glm-5.3_DIHENTIKAN/` (berkas keluaran mentah) | Pengumpulan dihentikan. Holdout parsial tidak dianalisis dan tidak disalin (lihat `results/glm_dihentikan/CATATAN.md`). |
| `harness/log/` (seluruhnya) | Folder log berisi items, keluaran sementara, dan laporan simulasi. Keluaran model yang dipakai sudah ada di `results/`. |

## E. Cache, lingkungan, dan kunci API

| Yang dikecualikan | Alasan |
|---|---|
| `__pycache__/`, `*.pyc` | Cache Python. |
| `RENDER/mplcache/` | Cache font. |
| Venv | Lingkungan lokal. |
| Profil API, berkas pemakaian, kunci API | Tidak ditemukan di folder sumber yang dipindai. Pola `.gitignore` sudah disiapkan. |

## F. Di luar struktur target (tidak disalin, bukan karena sensitif)

| Yang dikecualikan | Alasan |
|---|---|
| `harness/LAPORAN_AGEN_2.md`, `harness/LAPORAN_AGEN_2_V2.md`, `bahan/v2/LAPORAN_AGEN_1_V2.md`, `bahan/arsip_v1_600/LAPORAN_AGEN_1.md` | Laporan internal agen. Bisa ditambahkan setelah ditelaah penulis. |
| `harness/PREREG_TEMPLATE.md` | Templat prareg. |
| `bahan/PEDOMAN_ANOTATOR.md`, `bahan/v2/log/`, `bahan/skrip/`, `bahan/v2/skrip/` (skrip pembangun pool dan alat) | Di luar struktur target. Skrip analisis yang diperlukan sudah ada di `src/analisis/`. |
| `bahan/v2/hasil_olahan/` (olahan awal) | Digantikan oleh `data/kelayakan/`. |
| `REFERENSI/LAMPIRAN_SUMBER_DATA.md` (v1), `REFERENSI/artikel_asal_36_klaim.csv` | Versi lama atau ringkas dari berkas yang sudah disalin. |
| `RENDER/video/cek_bingkai/` | Bingkai pemeriksaan visual. Tidak diperlukan untuk reproduksi. |
| `SESI_LUAR/gemini_antigravity/results/` dan `HASIL_PENGUJIAN/gemini_antigravity/PROMPT_GEMINI.md` | Duplikat dari berkas yang sudah disalin ke `results/` dan `external_sessions/`. |
| Folder `_kerja_*`, `_data_audit` pada tahap 1 riset, dan berkas di atas 5 MB | Pekerjaan kerja tahap 1 dan berkas besar. Di luar struktur. |
| `CORE_ACADEMIC_DATA_AUDIT.md` dan `MODEL_FEASIBILITY_MATRIX.csv` di akar tahap 1 | Duplikat dari 06 dan 09 yang sudah disalin. |
| `_template_src/apart_template.docx` (folder GITHUB_REPO) | Templat dokumen, bukan bagian repo. |

## G. Hasil utama 294 (ditambahkan 2026-11-15)

| Yang dikecualikan | Alasan |
|---|---|
| `results/utama294/hash_cek.md` (sumber: `_utama294/hash_cek.md`) | Memuat path lokal absolut (`C:/EPIS_KERJA/...`) dan nama berkas di folder RAHASIA. |
| `_utama294/hash_sebelum.txt` dan `_utama294/daftar_hash_input.txt` | Daftar hash internal yang memuat nama berkas di folder RAHASIA dan path relatif ke berkas harness. |
| `_utama294/run_log.txt` | Log internal eksekusi skrip. Isinya sudah tercakup oleh `replikasi_cek.md` dan `CATATAN_UTAMA294.md`. |
| Berkas kunci dan item (`bahan/v2/RAHASIA/`, `bahan/v2/items_model.jsonl`) | Kunci jawaban dan teks klaim atau bukti. Sama seperti bagian A dan B. |

Berkas di `results/utama294/` dan `figures_294/` yang disalin: 18 berkas (tabel, analisis, catatan, dan skrip) dan 22 berkas (gambar H1 sampai H5, indeks, dan skrip pembangun). Daftar lengkap ada di `docs/PATH_MAP.md`.
