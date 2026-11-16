# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 133; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 19 | 0 | 0.0540 | 0.0540 | 0.0540 [0.0001; 0.1602] | 0.9474 | 0.0457 | 0.0028 | - | 0.0000 | 0 |
| near | R1 | anchor | 19 | 0 | 0.1075 | 0.1075 | 0.1075 [0.0067; 0.2823] | 0.9474 | 0.0921 | 0.0121 | 0.9474 | 1.0000 | 19 |
| near | R3 | anchor | 19 | 0 | 0.2415 | 0.2415 | 0.2415 [0.0163; 0.5259] | 0.8421 | 0.1511 | 0.0521 | 0.8421 | 1.0000 | 19 |
| far | R1 | anchor | 19 | 0 | 0.0991 | 0.0991 | 0.0991 [0.0003; 0.2903] | 0.9474 | 0.0511 | 0.0088 | 0.9474 | 1.0000 | 19 |
| far | R3 | anchor | 19 | 0 | 0.1653 | 0.1653 | 0.1653 [0.0085; 0.4011] | 0.8947 | 0.1121 | 0.0178 | 0.8947 | 1.0000 | 19 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 19 | 0.6842 [0.4737; 0.8947] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 19 | 0.3406 [0.1688; 0.5165] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 19 | 0.3195 [0.1542; 0.4923] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 19 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1095 [0.0332; 0.2147] | 0.0695 [0.0053; 0.1789] | 0.0400 [-0.0037; 0.0916] |
| R3 | 0.1900 [0.0716; 0.3411] | 0.1221 [0.0195; 0.2579] | 0.0679 [-0.0895; 0.2442] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 10 | 0.8000 | 0.0000 | 0.0050 | -0.0480 |
| en | 5 | 0.6000 | 0.0000 | 0.1160 | 0.1740 |
| unk | 4 | 0.5000 | 0.0000 | 0.0325 | 0.2250 |

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 133; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 19 | 0 | 0.0084 | 0.0084 | 0.0084 [0.0016; 0.0178] | 1.0000 | 0.0508 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 19 | 0 | 0.1139 | 0.1139 | 0.1139 [0.0183; 0.2790] | 0.9474 | 0.1011 | 0.0234 | 0.9474 | 1.0000 | 19 |
| near | R3 | anchor | 19 | 0 | 0.2436 | 0.2436 | 0.2436 [0.0817; 0.4631] | 0.8421 | 0.2132 | 0.0874 | 0.8421 | 1.0000 | 19 |
| far | R1 | anchor | 19 | 0 | 0.1073 | 0.1073 | 0.1073 [0.0083; 0.2340] | 0.8947 | 0.1058 | 0.0116 | 0.8947 | 1.0000 | 19 |
| far | R3 | anchor | 19 | 0 | 0.3065 | 0.3065 | 0.3065 [0.0715; 0.5799] | 0.7895 | 0.1095 | 0.0630 | 0.7895 | 1.0000 | 19 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 19 | 0.7368 [0.5263; 0.9474] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 19 | 0.2445 [0.0921; 0.4016] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 19 | 0.1988 [0.0727; 0.3392] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 19 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1489 [0.0789; 0.2437] | 0.1316 [0.0526; 0.2274] | 0.0174 [-0.0458; 0.0716] |
| R3 | 0.2511 [0.1532; 0.3700] | 0.2342 [0.1016; 0.3842] | 0.0168 [-0.0884; 0.1137] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 10 | 0.9000 | 0.0000 | -0.0130 | -0.0360 |
| en | 5 | 0.6000 | 0.0000 | 0.0980 | 0.1540 |
| unk | 4 | 0.5000 | 0.0000 | -0.0075 | -0.0225 |

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 133; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 3; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 18 | 1 | 0.1477 | 0.2452 | 0.1477 [0.0040; 0.3671] | 0.8889 | 0.0878 | 0.0094 | - | 0.0000 | 0 |
| near | R1 | anchor | 19 | 0 | 0.0053 | 0.0053 | 0.0053 [0.0009; 0.0125] | 1.0000 | 0.0326 | 0.0000 | 1.0000 | 1.0000 | 19 |
| near | R3 | anchor | 19 | 0 | 0.0129 | 0.0129 | 0.0129 [0.0038; 0.0252] | 1.0000 | 0.0579 | 0.0000 | 1.0000 | 1.0000 | 19 |
| far | R1 | anchor | 19 | 0 | 0.1027 | 0.1027 | 0.1027 [0.0002; 0.3071] | 0.9474 | 0.0421 | 0.0088 | 0.9474 | 1.0000 | 19 |
| far | R3 | anchor | 19 | 0 | 0.0756 | 0.0756 | 0.0756 [0.0000; 0.2261] | 0.9474 | 0.0511 | 0.0028 | 0.9474 | 1.0000 | 19 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 18 | 0.6111 [0.3889; 0.8333] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 18 | 0.2417 [0.0367; 0.4456] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 18 | 0.2356 [0.0303; 0.4369] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 18 | 0.0556 [0.0000; 0.1667] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0326 [0.0147; 0.0547] | 0.0616 [0.0047; 0.1679] | -0.0289 [-0.1421; 0.0405] |
| R3 | 0.0579 [0.0305; 0.0905] | 0.0516 [0.0021; 0.1426] | 0.0063 [-0.0916; 0.0747] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 10 | 0.8000 | 0.0000 | -0.0880 | -0.0520 |
| en | 4 | 0.5000 | 0.0000 | 0.0540 | 0.0780 |
| unk | 4 | 0.2500 | 0.2500 | 0.0150 | 0.0625 |
