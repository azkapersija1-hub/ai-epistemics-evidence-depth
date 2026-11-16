# AI x Epistemics Research Sprint 2026: Fase 1 (riset saja)

Dibuat 2026-11-11. **Tidak ada model kandidat dijalankan, tidak ada benchmark, tidak ada API uji, tidak ada hasil statistik, tidak ada publikasi/submisi.** Terpisah dari Swarm Alignment Hackathon (6-8 Nov).

## Isi
| Berkas | Isi |
|---|---|
| 01 | Persyaratan resmi sprint |
| 02, 03 | Laporan Agent A (literatur) dan Agent B (metode), salinan utuh |
| 04 | Matriks perbedaan A vs B |
| 05 | Matriks bukti literatur (24 entri, kolom bersih) |
| 06 | Audit `core_academic` (baca-saja) |
| 07 | Audit instrumen FEVER 45 butir |
| 08 | Audit kelayakan F11x |
| 09 | Matriks kelayakan model (6 baris; juga `MODEL_FEASIBILITY_MATRIX.csv`) |
| 10-15 | Teori, definisi, judul, opsi desain, analisis statistik, biaya |
| 16 | Daftar pekerjaan terdahulu |
| 17-19 | Kontribusi, risiko, referensi dan status verifikasi |
| 20 | Rekomendasi akhir (17 pertanyaan) |
| `CORE_ACADEMIC_DATA_AUDIT.md` | Salinan 06 |
| `_kerja_*`, `_data_audit` | Bahan kerja mentah, skrip hitung |

## Catatan metode
- Dua agen Haiku 5.5 bekerja terpisah secara prosedural, bukan independen statistik.
- Matriks CSV mentah kedua agen memiliki titik koma di dalam sel sehingga kolom bergeser; `05` dibangun ulang bersih (`_data_audit/bangun_matriks_bersih.py`). CSV mentah dibiarkan apa adanya di folder kerja.
- Tidak ada angka yang berasal dari hasil model. Simulasi daya dan biaya adalah hitungan dengan asumsi yang dinyatakan (sigma 0,35; 1.500/300 token).
- Bahasa: penjelasan Indonesia, istilah teknis Inggris.

## Status
Menunggu persetujuan peneliti sebelum Fase 2 (lihat butir 17 di `20`).
