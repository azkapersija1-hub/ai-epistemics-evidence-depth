# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Set SPLIT-dev: split dev

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash | set SPLIT-dev (ulangan 1)
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

## Model: qwen4-max-preview | set SPLIT-dev (ulangan 1)
- Jumlah observasi: 546; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 78 | 0 | 0.0062 | 0.0062 | 0.0062 [0.0036; 0.0098] | 1.0000 | 0.0479 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 78 | 0 | 0.0669 | 0.0669 | 0.0669 [0.0251; 0.1249] | 0.9615 | 0.0768 | 0.0049 | 0.9615 | 1.0000 | 78 |
| near | R3 | anchor | 78 | 0 | 0.2064 | 0.2064 | 0.2064 [0.1183; 0.3077] | 0.8590 | 0.0292 | 0.0456 | 0.8590 | 1.0000 | 78 |
| far | R1 | anchor | 78 | 0 | 0.0604 | 0.0604 | 0.0604 [0.0212; 0.1131] | 0.9487 | 0.0701 | 0.0025 | 0.9487 | 1.0000 | 78 |
| far | R3 | anchor | 78 | 0 | 0.1729 | 0.1729 | 0.1729 [0.0821; 0.2782] | 0.8846 | 0.0717 | 0.0239 | 0.8846 | 1.0000 | 78 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 78 | 0.5769 [0.4615; 0.6923] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 78 | 0.4000 [0.3121; 0.4846] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 78 | 0.3711 [0.2870; 0.4535] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 78 | 0.0128 [0.0000; 0.0385] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1169 [0.0876; 0.1536] | 0.0924 [0.0626; 0.1276] | 0.0245 [-0.0008; 0.0503] |
| R3 | 0.2164 [0.1623; 0.2733] | 0.1637 [0.1106; 0.2205] | 0.0527 [0.0091; 0.0935] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 24 | 0.7083 | 0.0000 | -0.0212 | -0.0254 |
| en | 42 | 0.5476 | 0.0238 | 0.0519 | 0.1188 |
| unk | 12 | 0.4167 | 0.0000 | 0.0200 | -0.0225 |

## Model: deepseek-v4.1-flash | set SPLIT-dev (ulangan 1)
- Jumlah observasi: 546; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 5; gagal setelah ulang (dicatat): 2

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 76 | 2 | 0.0791 | 0.1284 | 0.0791 [0.0187; 0.1629] | 0.9474 | 0.0571 | 0.0029 | - | 0.0000 | 0 |
| near | R1 | anchor | 78 | 0 | 0.0026 | 0.0026 | 0.0026 [0.0015; 0.0039] | 1.0000 | 0.0256 | 0.0000 | 1.0000 | 1.0000 | 78 |
| near | R3 | anchor | 78 | 0 | 0.0305 | 0.0305 | 0.0305 [0.0032; 0.0826] | 0.9872 | 0.0206 | 0.0125 | 0.9872 | 1.0000 | 78 |
| far | R1 | anchor | 78 | 0 | 0.0466 | 0.0466 | 0.0466 [0.0007; 0.1210] | 0.9744 | 0.0113 | 0.0027 | 0.9744 | 1.0000 | 78 |
| far | R3 | anchor | 78 | 0 | 0.0643 | 0.0643 | 0.0643 [0.0016; 0.1366] | 0.9615 | 0.0221 | 0.0024 | 0.9615 | 1.0000 | 78 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 76 | 0.4868 [0.3684; 0.6053] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 76 | 0.4297 [0.3262; 0.5321] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 76 | 0.4193 [0.3177; 0.5215] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 76 | 0.0132 [0.0000; 0.0395] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0256 [0.0191; 0.0328] | 0.0371 [0.0105; 0.0751] | -0.0114 [-0.0497; 0.0151] |
| R3 | 0.0460 [0.0258; 0.0759] | 0.0474 [0.0132; 0.0876] | -0.0014 [-0.0362; 0.0235] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 24 | 0.6667 | 0.0000 | -0.0779 | -0.0588 |
| en | 40 | 0.4500 | 0.0000 | 0.0224 | 0.0207 |
| unk | 12 | 0.2500 | 0.0833 | 0.0033 | 0.0358 |
