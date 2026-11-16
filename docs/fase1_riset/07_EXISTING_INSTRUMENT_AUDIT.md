# 07 Audit instrumen terdahulu: FEVER 45 butir

Lokasi: `D:\PELATIHAN AI ART\alat pengukur AI\UJI_FEVER_45\` (29 Oktober 2026). Dibaca baca-saja; tidak ada model dijalankan hari ini. Diperiksa: `butir_45_publik.jsonl`, `RAHASIA\kunci_45.jsonl` (hanya distribusi), `hasil_per_butir.csv`, daftar `hasil\`, `PETUNJUK_UJI_MANUAL.md`.

## Isi
- 45 butir F01-F45. Publik: `id, level, tema, klaim, bukti` (2-3 potongan bukti ber-ID, 209-504 karakter). Kunci terpisah: `id, label, bukti_minimum`.
- Label: **SUPPORTS 15, REFUTES 15, NOT ENOUGH INFO 15** (seimbang). Tingkat 1-5, masing-masing 9 butir. 19 tema.
- Butir adalah **skenario fiktif** (mis. "Distrik Aruna"), bukan klaim dari artikel akademik dan bukan dari `core_academic`. Bahasa Indonesia.

## Riwayat pemakaian
`hasil\` berisi respons yang SUDAH dikumpulkan 29 Oktober: `respons_codex_k1..k5` (GPT-6.1 Sol), `respons_gemini_k1..k5`, `respons_haiku_k1..k5`, `pilot_haiku_urutan_asli`; laporan "UNTUK PENILAI AHLI" v1-v4 dan Lampiran D. `hasil_per_butir.csv` memuat 90 baris Haiku 5.5. Hasil lama (bukan baru): akurasi 0,944, Brier rata-rata 0,0885; per kunci SUPPORTS 1,00, REFUTES 1,00, **NEI 0,833**. Haiku dijalankan sebagai agen dalam Claude Code (bukan API murni), 45 butir berurutan dalam satu sesi per klon.

## Kelayakan
| Peran | Layak? | Alasan |
|---|---|---|
| Pilot instrument | **Ya** | Menguji pipeline, parsing, menaksir sigma/ICC |
| Development set | Ya, dengan catatan | Sudah dilihat dan diperbaiki peneliti dan penilai ahli |
| Validation set | Tidak disarankan | Sudah memandu prompt dan pemeringkatan |
| Final benchmark / holdout | **Tidak** | Sudah dijawab banyak model dan dibahas; kontaminasi |

## Masalah metodologis
- **Efek langit-langit**: SUPPORTS/REFUTES 94-100%; daya diskriminasi rendah. Simulasi Agent B: daya ≈0,16 untuk selisih Brier 0,05 pada 45 butir (sigma 0,35 asumsi).
- Ketergantungan antarbutir (19 tema untuk 45 butir).
- Validitas konstruk: butir fiktif menguji penalaran dari teks buatan, bukan penilaian bukti literatur akademik.
- Bahasa seluruhnya Indonesia; korpus separuh Inggris.
- Kunci dan hasil model berdampingan di satu folder; pastikan `RAHASIA` tidak dimuat pipeline inferensi.
- Penilaian ahli hanya bukti kesesuaian isi, bukan validitas konstruk menyeluruh.

## Rekomendasi
Perlakukan 45 butir sebagai **pilot dan sumber kalibrasi parameter**, tandai preexisting, bukan holdout. Butir final harus baru, lebih sulit, berbasis klaim akademik, dan dibekukan sebelum model dijalankan.
