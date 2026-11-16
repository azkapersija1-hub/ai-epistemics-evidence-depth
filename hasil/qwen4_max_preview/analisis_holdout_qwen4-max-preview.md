# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 98 | 0 | 0.0212 | 0.0212 | 0.0212 [0.0063; 0.0464] | 0.9898 | 0.0461 | 0.0002 | - | - | 0 |
| near | R1 | anchor | 98 | 0 | 0.0962 | 0.0962 | 0.0962 [0.0472; 0.1560] | 0.9286 | 0.0709 | 0.0100 | 0.9286 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.2409 | 0.2409 | 0.2409 [0.1478; 0.3516] | 0.8571 | 0.0493 | 0.0701 | 0.8571 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0618 | 0.0618 | 0.0618 [0.0194; 0.1215] | 0.9592 | 0.0410 | 0.0042 | 0.9592 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.1511 | 0.1511 | 0.1511 [0.0750; 0.2456] | 0.9082 | 0.0365 | 0.0468 | 0.9082 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 98 | 0.5612 [0.4694; 0.6531] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 98 | 0.3889 [0.3164; 0.4611] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 98 | 0.3533 [0.2847; 0.4203] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 98 | 0.0102 [0.0000; 0.0306] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1447 [0.1115; 0.1838] | 0.0919 [0.0642; 0.1262] | 0.0528 [0.0230; 0.0849] |
| R3 | 0.2235 [0.1730; 0.2820] | 0.1469 [0.1021; 0.1998] | 0.0765 [0.0305; 0.1227] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 34 | 0.6471 | 0.0294 | 0.0362 | 0.0312 |
| en | 53 | 0.5472 | 0.0000 | 0.0664 | 0.1021 |
| unk | 11 | 0.3636 | 0.0000 | 0.0382 | 0.0936 |
