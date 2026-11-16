# Peta path absolut yang tertanam di kode

Daftar ini dibuat dengan memindai `src/` (berkas .py, .txt, .html). Kode TIDAK diubah. Path di bawah ini ditulis apa adanya dan akan salah bila repositori dijalankan dari lokasi lain. Berkas ini hanya mencatat; penggantian path adalah keputusan penulis.

## Tabel path

| Berkas (di repo) | Baris | Path tertanam (variabel) | Fungsi | Catatan |
|---|---|---|---|---|
| `src/analisis/bangun_gambar.py` | 17 | `C:\EPIS_KERJA\RENDER` (ROOT) | Lokasi keluaran gambar dan cache | Juga disebut di docstring baris 4, 6, 8, 800, 801, 805 |
| `src/analisis/bangun_gambar.py` | 47 | `C:\EPIS_KERJA\AI_EPISTEMICS_2026_PHASE_2_PREP` (SRC) | Sumber baca data hasil | Hanya dibaca |
| `src/analisis/bangun_video.py` | 25 | `C:\EPIS_KERJA\AI_EPISTEMICS_2026_PHASE_2_PREP` (SRC_ROOT) | Sumber baca | Docstring baris 4 |
| `src/analisis/bangun_video.py` | 34 | `C:\EPIS_KERJA\RENDER\video` (OUT) | Keluaran video | |
| `src/analisis/bangun_video.py` | 36 | `C:\Windows\Fonts` (FONT_DIR) | Font sistem Windows | Khusus Windows |
| `src/analisis/skrip_analisis_codex.py` | 14 | `C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP/harness` (H) | Akar harness | |
| `src/analisis/skrip_analisis_codex.py` | 15 | `C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP` (P) | Akar sumber | |
| `src/analisis/skrip_analisis_codex.py` | 19 | `P + /bahan/v2/RAHASIA/lapis_data` (KUN) | Kunci mekanis | Berkas tidak ada di repo (dikecualikan) |
| `src/analisis/skrip_analisis_lapis36.py` | 18 | `C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP` (P) | Akar sumber | |
| `src/analisis/skrip_analisis_lapis36.py` | 23 | `P + /bahan/v2/RAHASIA/lapis_data` (KUNCI_SUMBER) | Kunci lapis 40 | Berkas tidak ada di repo |
| `src/analisis/skrip_analisis_lapis36.py` | 25 | `.../RAHASIA/lapis_data/kunci_lapis_36.jsonl` (KUNCI_36) | Kunci lapis 36 | Berkas tidak ada di repo |
| `src/harness/epis/provider_profil.py` | 24 | `D:\kerjaan baru\25_Tools_Sakti_Terpadu\core\sakti_core` (LOKASI_MODEL_API) | Lokasi modul API (sakti_core) | Di drive D, di luar repo. Modul ini tidak disertakan. Tanpa itu, adapter model nyata tidak dapat dijalankan |

Catatan: `src/analisis/hitung_kelayakan.py` tidak memuat path absolut, tetapi `ROOT` dihitung dari lokasi berkas (`bahan/v2` di struktur sumber lama). Dari repo, nilai default `--masukan`, `--keluar`, dan `--rujukan` menunjuk ke folder yang tidak ada.

## Ketergantungan pada berkas yang dikecualikan

- `skrip_analisis_codex.py` dan `skrip_analisis_lapis36.py` membaca kunci di `bahan/v2/RAHASIA/lapis_data/` dan berkas item (`items_*.jsonl`) yang memuat teks klaim dan bukti. Keduanya tidak disalin (lihat `DIKECUALIKAN.md`). Skrip ini tidak bisa dijalankan dari repositori ini.
- `hitung_kelayakan.py` secara default membaca `hasil_ahli/` (berkas penilaian per penilai, `kelayakan_butir_*.csv` dan `pasangan_*.csv`), `lembar_ahli_40.csv`, dan `lembar_ahli_jangkar_30.csv`. Ketiganya tidak disalin. Keluarannya (`status_butir.csv`, `daftar_revisi.csv`) juga tidak disalin. Repo hanya menyimpan keluaran ringkas di `data/kelayakan/`. Tes di `test_hitung_kelayakan.py` memakai data tiruan dan dapat dijalankan dari repo ini (hasil belum diverifikasi ulang, lihat laporan verifikasi).
- `analisis_keluaran.py` dan `jalankan_provider_nyata.py` membaca dan menulis `log/` relatif terhadap lokasi skrip (`HARNESS = dirname(__file__)`). Folder `log/` tidak disalin.

## Path relatif

Skrip harness menghitung folder `log/` dari lokasi berkas. Docstring dan contoh perintah memakai `harness/log/...` dan diasumsikan dijalankan dari folder sumber lama (lihat `docs/README_HARNESS.md`). Dari struktur repo ini folder `log/` tidak ada, sehingga perintah pada README_HARNESS perlu penyesuaian path oleh penulis. Kode tidak diubah.

## Ringkasan

- 5 berkas kode memuat path absolut (10 entri di tabel, termasuk entri docstring).
- 1 path menunjuk ke drive D (`provider_profil.py`), di luar repo.
- 3 path mengarah ke folder kunci RAHASIA yang tidak disalin.
- `hitung_kelayakan.py` membaca 3 sumber penilaian yang tidak disalin.

## Tambahan: berkas hasil utama 294 (ditambahkan 2026-11-15)

Dua berkas kode dan satu berkas teks baru memuat path absolut. Kode tidak diubah.

| Berkas (di repo) | Baris | Path tertanam (variabel) | Fungsi | Catatan |
|---|---|---|---|---|
| `hasil/utama294/skrip_analisis_utama294.py` | 23 | `C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP` (P) | Akar sumber | Hanya dibaca |
| `hasil/utama294/skrip_analisis_utama294.py` | 29 | `P + /bahan/v2/RAHASIA/kunci.jsonl` (KUNCI) | Kunci evaluasi | Berkas tidak ada di repo (dikecualikan). Skrip tidak bisa dijalankan dari repo |
| `gambar294/bangun_gambar294.py` | 18 | `C:\EPIS_KERJA\RENDER` (ROOT) | Keluaran gambar294 dan cache font (`mplcache`) | Juga di docstring baris 4, 6, dan 8 |
| `gambar294/bangun_gambar294.py` | 48 | `C:\EPIS_KERJA\AI_EPISTEMICS_2026_PHASE_2_PREP\HASIL_PENGUJIAN\_utama294` (SRC) | Sumber baca (hanya dibaca) | Folder asal berada di luar repo |
| `gambar294/bangun_gambar294.py` | 635 sampai 640 | teks `C:\EPIS_KERJA\RENDER\gambar294\` | Pesan catatan pembangunan di INDEKS294.md | Hanya teks |
| `gambar294/INDEKS294.md` | 3 dan 5 | teks `C:\EPIS_KERJA\RENDER\gambar294\bangun_gambar294.py` | Catatan pembangunan | Teks, bukan kode. Tidak diubah |

Catatan: `hasil/utama294/` tidak memuat `hash_cek.md`, `hash_sebelum.txt`, `daftar_hash_input.txt`, dan `run_log.txt`, karena berkas hash itu memuat path lokal dan nama berkas RAHASIA (lihat `DIKECUALIKAN.md` bagian G).

Ringkasan tambahan: 7 berkas kode di repo kini memuat path absolut (5 sebelumnya ditambah 2 dari `hasil/utama294/` dan `gambar294/`).

## Tambahan 15 November 2026
- `referensi/katalog_sumber/skrip_bangun_katalog_sumber.py` memakai salinan katalog internal di folder sementara dan membaca berkas bahan di mesin asal; tidak dapat dijalankan ulang dari repositori ini tanpa berkas tersebut.
- Skrip video 294 (`bangun_video294.py`) tidak disertakan di repositori; video disertakan sebagai hasil.
