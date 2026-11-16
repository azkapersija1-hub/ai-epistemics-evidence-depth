# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 8; gagal setelah ulang (dicatat): 3

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 96 | 2 | 0.1373 | 0.1753 | 0.1373 [0.0562; 0.2321] | 0.9167 | 0.0350 | 0.0186 | - | 0.0000 | 0 |
| near | R1 | anchor | 98 | 0 | 0.0537 | 0.0537 | 0.0537 [0.0025; 0.1186] | 0.9694 | 0.0098 | 0.0078 | 0.9694 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.0742 | 0.0742 | 0.0742 [0.0178; 0.1530] | 0.9592 | 0.0087 | 0.0120 | 0.9592 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0015 | 0.0015 | 0.0015 [0.0007; 0.0027] | 1.0000 | 0.0132 | 0.0000 | 1.0000 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.0528 | 0.0528 | 0.0528 [0.0006; 0.1223] | 0.9694 | 0.0198 | 0.0012 | 0.9694 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 96 | 0.5312 [0.4375; 0.6250] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 96 | 0.4127 [0.3292; 0.5002] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 96 | 0.3983 [0.3164; 0.4823] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 96 | 0.0104 [0.0000; 0.0312] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0516 [0.0239; 0.0864] | 0.0132 [0.0081; 0.0194] | 0.0385 [0.0102; 0.0735] |
| R3 | 0.0671 [0.0356; 0.1096] | 0.0366 [0.0085; 0.0733] | 0.0305 [0.0023; 0.0635] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 34 | 0.5588 | 0.0000 | 0.0047 | 0.0172 |
| en | 48 | 0.5625 | 0.0208 | 0.0767 | 0.0419 |
| unk | 14 | 0.3571 | 0.0000 | -0.0057 | 0.0257 |
