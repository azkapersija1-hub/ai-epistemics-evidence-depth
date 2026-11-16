# INDEKS gambar: Agen E (grafik statis)

Dibangun: 2026-11-13 18:11 oleh `C:\EPIS_KERJA\RENDER\gambar\bangun_gambar.py`. Ulang dengan: `py -3.12 -I -X utf8 C:\EPIS_KERJA\RENDER\gambar\bangun_gambar.py`.

Status angka: HASIL MODEL (BELUM DIVERIFIKASI), sesuai berkas sumber. Tidak ada model dipanggil, tidak ada statistik baru, tidak ada berkas sumber diubah. Semua keluaran hanya di `C:\EPIS_KERJA\RENDER\`.

## Daftar gambar

Setiap gambar ada dalam dua bahasa (`_en`, `_id`) dengan format PNG 300 dpi dan SVG.

| Gambar | Isi | Sumber data |
|---|---|---|
| G1 `G1_alur_desain` | Diagram desain: tujuh bentuk bukti, label jangkar, tiga metrik | Desain studi (skema, tanpa data); label dari aturan jangkar |
| G2 `G2_corong_butir` | Corong 294 kolam, 40 jangkar, 36 utama, lapis 26 dan 19; kotak kesepakatan penilai | Angka 294 dari `bahan/v2/LAPORAN_AGEN_1_V2.md`; status dari `bahan/v2/hasil_olahan_final/status_butir.csv` (hanya hitungan dan ID keluar); kesepakatan dari `RINGKASAN_KELAYAKAN.md` |
| G3 `G3_brier_bukti_lapis36` | Brier batas 1 per model dan jenis bukti, lapis 36, batang galat 95% CI | `_lapis36/tabel_lapis36_4model.csv` |
| G4 `G4_konsistensi_r1_r3` | Proporsi R1 = R3 per model pada lapis 40, 36, 26, 19 | `_lapis36/tabel_pembanding_lapis_40_36_26_19.csv` (nilai titik); CI lapis 36 dari `tabel_lapis36_4model.csv` |
| G5 `G5_false_support` | Massa false-support near dan far, R1 dan R3, lapis 36, CI 95% | `_lapis36/tabel_lapis36_4model.csv` |
| G6 `G6_kestabilan_ulang` | Persen argmax sama per tingkat bukti, uji ulang 19 klaim | `_retest_lapis19/KESTABILAN.csv` (tiga model API, kolom gagal dihitung beda); `gpt61_codex/KESTABILAN_codex.csv` (GPT-6.1 Sol, sesi terpisah) |
| G7 `G7_panel_ringkas` | Panel 2x2 dari G3, G4, G5, G6 | Sama dengan G3 sampai G6 |

Nama berkas lengkap: `<nama>_en.png`, `<nama>_en.svg`, `<nama>_id.png`, `<nama>_id.svg`.

## Pencocokan angka (CSV dibaca, MD dicocokkan)

Setiap angka gambar dibaca dari CSV. Setelah itu, angka yang sama di MD dibandingkan (toleransi 0,00005 untuk 4 desimal, 0,05 poin untuk persen 1 desimal). Skrip berhenti bila ada beda.

| Berkas | Cocok | Beda |
|---|---|---|
| tabel_lapis36_4model.md | 80 | 0 |
| tabel_pembanding_lapis_40_36_26_19.md | 320 | 0 |
| KESTABILAN.md | 9 | 0 |
| KESTABILAN_codex.md | 3 | 0 |
| RINGKASAN_KELAYAKAN.md (pembacaan regex) | 1 | 0 |

Contoh nilai yang dicocokkan (CSV = MD):

- G3 own R3, qwen3.8-flash: 0.0765 [0.0004; 0.1985] (md: 0.0765 [0.0004; 0.1985]).
- G3 near R3, qwen4-max-preview: 0.1725 (md: 0.1725 [0.0755; 0.2937]).
- G5 far R3, qwen4-max-preview: 0.2200 [0.1308; 0.3200] (md: 0.2200 [0.1308; 0.3200]).
- G4 lapis 36, sesuai R1 = R3, deepseek-v4.1-flash: 42.9% (md: 0.4286).
- G6 R3, deepseek-v4.1-flash (gagal dihitung beda): 89.5% (valid saja: 92.7%; md: 89.5% dan 92.7%).
- G6 R1, GPT-6.1 Sol (unverified): 98.2% [94.7; 100.0] (md: 98.2% [94.7; 100.0]).
- G2 persen sepakat 61.7% (120 pasangan), kappa Fleiss -0.025 (n = 40), kappa Cohen 0.030, 0.122, -0.063.
- G2 jumlah: kolam 294; jangkar 40 (dipakai 35, direvisi 1, keluar 4); lapis 40/36/26/19 = 40/36/26/19 klaim unik (dihitung dari items, 7 observasi per klaim).

## Pemeriksaan tata letak

Setiap teks diperiksa: tumpang tindih antar teks, teks keluar figur, dan teks keluar kotak diagram.

| Gambar | Tumpang tindih | Keluar figur | Keluar kotak |
|---|---|---|---|
| G1_alur_desain_en | 0 | 0 | 0 |
| G2_corong_butir_en | 0 | 0 | 0 |
| G3_brier_bukti_lapis36_en | 0 | 0 | 0 |
| G4_konsistensi_r1_r3_en | 0 | 0 | 0 |
| G5_false_support_en | 0 | 0 | 0 |
| G6_kestabilan_ulang_en | 0 | 0 | 0 |
| G7_panel_ringkas_en | 0 | 0 | 0 |
| G1_alur_desain_id | 0 | 0 | 0 |
| G2_corong_butir_id | 0 | 0 | 0 |
| G3_brier_bukti_lapis36_id | 0 | 0 | 0 |
| G4_konsistensi_r1_r3_id | 0 | 0 | 0 |
| G5_false_support_id | 0 | 0 | 0 |
| G6_kestabilan_ulang_id | 0 | 0 | 0 |
| G7_panel_ringkas_id | 0 | 0 | 0 |

## Catatan dan masalah

1. **Footnote lapis 36 belum cocok dengan sumber.** Footnote diminta berbunyi "Pilot+dev claims only", tetapi `_lapis36/tabel_lapis36_4model.md` menulis keluaran API berasal dari pilot, dev, dan val. `items_lapis_36.jsonl` tidak memuat field split, jadi tidak bisa diverifikasi dari berkas. Footnote dipakai persis seperti diminta. Perlu dicek penulis.
2. **CI hanya untuk lapis 36.** CSV pembanding (lapis 40, 26, 19) hanya memuat nilai titik. G4 menampilkan CI hanya untuk lapis 36; tidak ada CI yang dikarang.
3. **G6 memakai footnote khusus.** Kestabilan memakai lapis 19 klaim (133 observasi per model), bukan 36 klaim dan 252 observasi, sehingga footnote standar tidak akurat. Footnote khusus dipakai dan dicatat.
4. **G6 memakai angka konservatif untuk model API.** Kolom `persen_argmax_sama_gagal_dihitung_beda` dipakai, sehingga gagal parse dihitung sebagai beda. Untuk deepseek-v4.1-flash R3: 89,5% (konservatif) dan 92,7% (hanya pasangan valid). Kedua angka ada di KESTABILAN.csv.
5. **Jumlah n tidak 36 di beberapa batang G3.** deepseek-v4.1-flash own R3 n = 35 (satu gagal parse final), dan semua batang Brier batas 1 GPT-6.1 Sol (unverified) n = 35 (satu klaim SKIP, C0230). Keterangan n tercetak di footnote G3.
6. **Label codex.** Semua gambar memakai `GPT-6.1 Sol (unverified)`. Sumber menulis `codex (gpt-6.1-sol, tak terverifikasi)`. Uji ulang codex berasal dari sesi terpisah dan belum terverifikasi (diarsir di G6).
7. **Kesepakatan penilai.** Penilai adalah tiga anggota tim penulis, bukan panel ahli eksternal. Kappa mendekati nol. Keterangan ini ada di G2 dan di ringkasan sumber.
8. **Judul tanpa kesimpulan model.** Semua judul hanya menyebut isi grafik. Gambar menunjukkan pola, bukan peringkat.
9. **Angka desimal.** Gambar ID memakai koma desimal. Footnote memakai teks Inggris persis seperti diminta di kedua bahasa.
10. **Pembacaan lapis 26 dan 19.** Jumlah klaim dihitung dari `items_lapis_26.jsonl` dan `items_lapis_19.jsonl`, yang sama dengan sumber skrip pembanding. Tidak ada angka yang diketik dari ingatan.

