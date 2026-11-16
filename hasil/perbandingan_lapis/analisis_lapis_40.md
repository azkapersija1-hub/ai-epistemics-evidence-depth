# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 280; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 40 | 0 | 0.0689 | 0.0689 | 0.0689 [0.0005; 0.1786] | 0.9500 | 0.0320 | 0.0025 | - | 0.0000 | 0 |
| near | R1 | anchor | 40 | 0 | 0.0573 | 0.0573 | 0.0573 [0.0070; 0.1480] | 0.9750 | 0.0568 | 0.0040 | 0.9750 | 1.0000 | 40 |
| near | R3 | anchor | 40 | 0 | 0.1253 | 0.1253 | 0.1253 [0.0202; 0.2636] | 0.9250 | 0.0767 | 0.0215 | 0.9250 | 1.0000 | 40 |
| far | R1 | anchor | 40 | 0 | 0.0487 | 0.0487 | 0.0487 [0.0015; 0.1414] | 0.9750 | 0.0110 | 0.0040 | 0.9750 | 1.0000 | 40 |
| far | R3 | anchor | 40 | 0 | 0.0813 | 0.0813 | 0.0813 [0.0060; 0.1921] | 0.9500 | 0.0453 | 0.0053 | 0.9500 | 1.0000 | 40 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 40 | 0.4750 [0.3250; 0.6250] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 40 | 0.5141 [0.3859; 0.6414] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 40 | 0.4896 [0.3648; 0.6151] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 40 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0725 [0.0315; 0.1310] | 0.0462 [0.0135; 0.1032] | 0.0262 [0.0005; 0.0583] |
| R3 | 0.1227 [0.0625; 0.1978] | 0.0760 [0.0258; 0.1420] | 0.0467 [-0.0340; 0.1273] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 16 | 0.5625 | 0.0000 | 0.0038 | -0.0063 |
| en | 16 | 0.4375 | 0.0000 | 0.0319 | 0.0731 |
| unk | 8 | 0.3750 | 0.0000 | 0.0600 | 0.1000 |

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 280; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 40 | 0 | 0.0086 | 0.0086 | 0.0086 [0.0035; 0.0151] | 1.0000 | 0.0516 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 40 | 0 | 0.0634 | 0.0634 | 0.0634 [0.0166; 0.1478] | 0.9750 | 0.0730 | 0.0071 | 0.9750 | 1.0000 | 40 |
| near | R3 | anchor | 40 | 0 | 0.1593 | 0.1593 | 0.1593 [0.0721; 0.2743] | 0.9000 | 0.1370 | 0.0393 | 0.9000 | 1.0000 | 40 |
| far | R1 | anchor | 40 | 0 | 0.0701 | 0.0701 | 0.0701 [0.0135; 0.1423] | 0.9250 | 0.0910 | 0.0045 | 0.9250 | 1.0000 | 40 |
| far | R3 | anchor | 40 | 0 | 0.2401 | 0.2401 | 0.2401 [0.1017; 0.4084] | 0.8500 | 0.0893 | 0.0476 | 0.8500 | 1.0000 | 40 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 40 | 0.5000 [0.3500; 0.6500] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 40 | 0.4581 [0.3395; 0.5789] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 40 | 0.4194 [0.3086; 0.5354] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 40 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1163 [0.0798; 0.1668] | 0.1040 [0.0590; 0.1593] | 0.0122 [-0.0233; 0.0435] |
| R3 | 0.2027 [0.1447; 0.2715] | 0.2095 [0.1278; 0.3033] | -0.0068 [-0.0705; 0.0518] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 16 | 0.6250 | 0.0000 | -0.0175 | -0.0562 |
| en | 16 | 0.4375 | 0.0000 | 0.0506 | 0.0581 |
| unk | 8 | 0.3750 | 0.0000 | -0.0050 | -0.0375 |

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 280; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 3; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 39 | 1 | 0.1110 | 0.1582 | 0.1110 [0.0070; 0.2356] | 0.9231 | 0.0672 | 0.0055 | - | 0.0000 | 0 |
| near | R1 | anchor | 40 | 0 | 0.0034 | 0.0034 | 0.0034 [0.0013; 0.0073] | 1.0000 | 0.0290 | 0.0000 | 1.0000 | 1.0000 | 40 |
| near | R3 | anchor | 40 | 0 | 0.0069 | 0.0069 | 0.0069 [0.0024; 0.0140] | 1.0000 | 0.0372 | 0.0000 | 1.0000 | 1.0000 | 40 |
| far | R1 | anchor | 40 | 0 | 0.0896 | 0.0896 | 0.0896 [0.0004; 0.2191] | 0.9500 | 0.0360 | 0.0046 | 0.9500 | 1.0000 | 40 |
| far | R3 | anchor | 40 | 0 | 0.0809 | 0.0809 | 0.0809 [0.0006; 0.2048] | 0.9500 | 0.0333 | 0.0025 | 0.9500 | 1.0000 | 40 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 39 | 0.3846 [0.2308; 0.5385] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 39 | 0.4944 [0.3405; 0.6300] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 39 | 0.4855 [0.3324; 0.6187] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 39 | 0.0256 [0.0000; 0.0769] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0290 [0.0198; 0.0418] | 0.0583 [0.0095; 0.1283] | -0.0292 [-0.0978; 0.0215] |
| R3 | 0.0372 [0.0225; 0.0555] | 0.0560 [0.0088; 0.1235] | -0.0188 [-0.0840; 0.0307] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 16 | 0.5625 | 0.0000 | -0.1075 | -0.0906 |
| en | 15 | 0.3333 | 0.0000 | 0.0300 | 0.0281 |
| unk | 8 | 0.1250 | 0.1250 | 0.0088 | 0.0312 |
