# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 546; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 78 | 0 | 0.0366 | 0.0366 | 0.0366 [0.0013; 0.0927] | 0.9744 | 0.0176 | 0.0010 | - | 0.0000 | 0 |
| near | R1 | anchor | 78 | 0 | 0.0299 | 0.0299 | 0.0299 [0.0063; 0.0858] | 0.9872 | 0.0317 | 0.0016 | 0.9872 | 1.0000 | 78 |
| near | R3 | anchor | 78 | 0 | 0.1211 | 0.1211 | 0.1211 [0.0367; 0.2260] | 0.9359 | 0.0554 | 0.0235 | 0.9359 | 1.0000 | 78 |
| far | R1 | anchor | 78 | 0 | 0.0265 | 0.0265 | 0.0265 [0.0020; 0.0934] | 0.9872 | 0.0113 | 0.0021 | 0.9872 | 1.0000 | 78 |
| far | R3 | anchor | 78 | 0 | 0.0449 | 0.0449 | 0.0449 [0.0059; 0.1026] | 0.9744 | 0.0283 | 0.0025 | 0.9744 | 1.0000 | 78 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 78 | 0.5256 [0.4231; 0.6410] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 78 | 0.4569 [0.3607; 0.5488] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 78 | 0.4361 [0.3408; 0.5267] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 78 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0544 [0.0335; 0.0849] | 0.0355 [0.0168; 0.0663] | 0.0188 [0.0056; 0.0335] |
| R3 | 0.1082 [0.0617; 0.1646] | 0.0518 [0.0247; 0.0885] | 0.0564 [0.0060; 0.1132] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 24 | 0.6667 | 0.0000 | 0.0017 | 0.0308 |
| en | 42 | 0.4762 | 0.0000 | 0.0150 | 0.0438 |
| unk | 12 | 0.4167 | 0.0000 | 0.0667 | 0.1517 |
