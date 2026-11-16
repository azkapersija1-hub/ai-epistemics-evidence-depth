# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Set UTAMA-294: semua 294 klaim (pilot+dev+val+holdout). Pilot adalah tahap teknis menurut praregistrasi dan tidak dilaporkan sebagai hasil. Baris UTAMA-294 memasukkannya sesuai permintaan; UTAMA-274 adalah baris tanpa pilot.

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash | set UTAMA-294 (ulangan 1)
- Jumlah observasi: 2058; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 294 | 0 | 0.0322 | 0.0322 | 0.0322 [0.0112; 0.0579] | 0.9796 | 0.0171 | 0.0007 | - | 0.0000 | 0 |
| near | R1 | anchor | 294 | 0 | 0.0537 | 0.0537 | 0.0537 [0.0273; 0.0841] | 0.9762 | 0.0292 | 0.0080 | 0.9762 | 1.0000 | 294 |
| near | R3 | anchor | 294 | 0 | 0.1466 | 0.1466 | 0.1466 [0.0977; 0.2013] | 0.9150 | 0.0284 | 0.0293 | 0.9150 | 1.0000 | 294 |
| far | R1 | anchor | 294 | 0 | 0.0259 | 0.0259 | 0.0259 [0.0082; 0.0505] | 0.9864 | 0.0116 | 0.0012 | 0.9864 | 1.0000 | 294 |
| far | R3 | anchor | 293 | 1 | 0.0871 | 0.0936 | 0.0871 [0.0505; 0.1307] | 0.9454 | 0.0226 | 0.0111 | 0.9454 | 1.0000 | 293 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 294 | 0.5034 [0.4456; 0.5612] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 294 | 0.4788 [0.4316; 0.5263] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 294 | 0.4525 [0.4068; 0.4974] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 294 | 0.0068 [0.0000; 0.0170] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0718 [0.0551; 0.0907] | 0.0347 [0.0235; 0.0489] | 0.0371 [0.0210; 0.0546] |
| R3 | 0.1270 [0.0998; 0.1580] | 0.0707 [0.0503; 0.0952] | 0.0563 [0.0262; 0.0853] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 100 | 0.5900 | 0.0200 | 0.0098 | 0.0212 |
| en | 155 | 0.4774 | 0.0000 | 0.0539 | 0.0679 |
| unk | 39 | 0.3846 | 0.0000 | 0.0405 | 0.0990 |

## Model: qwen4-max-preview | set UTAMA-294 (ulangan 1)
- Jumlah observasi: 2058; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 294 | 0 | 0.0222 | 0.0222 | 0.0222 [0.0092; 0.0381] | 0.9898 | 0.0437 | 0.0003 | - | 0.0000 | 0 |
| near | R1 | anchor | 294 | 0 | 0.1121 | 0.1121 | 0.1121 [0.0786; 0.1492] | 0.9286 | 0.0416 | 0.0151 | 0.9286 | 1.0000 | 294 |
| near | R3 | anchor | 294 | 0 | 0.2312 | 0.2312 | 0.2312 [0.1753; 0.2932] | 0.8537 | 0.0286 | 0.0757 | 0.8537 | 1.0000 | 294 |
| far | R1 | anchor | 294 | 0 | 0.0482 | 0.0482 | 0.0482 [0.0263; 0.0746] | 0.9660 | 0.0460 | 0.0020 | 0.9660 | 1.0000 | 294 |
| far | R3 | anchor | 294 | 0 | 0.1455 | 0.1455 | 0.1455 [0.1010; 0.1938] | 0.9082 | 0.0097 | 0.0276 | 0.9082 | 1.0000 | 294 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 294 | 0.5306 [0.4728; 0.5850] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 294 | 0.4226 [0.3798; 0.4656] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 294 | 0.3897 [0.3490; 0.4311] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 294 | 0.0068 [0.0000; 0.0170] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1473 [0.1261; 0.1696] | 0.0834 [0.0689; 0.1005] | 0.0639 [0.0433; 0.0837] |
| R3 | 0.2198 [0.1890; 0.2523] | 0.1487 [0.1230; 0.1765] | 0.0711 [0.0464; 0.0953] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 100 | 0.6200 | 0.0100 | 0.0286 | 0.0220 |
| en | 155 | 0.5097 | 0.0065 | 0.0835 | 0.1010 |
| unk | 39 | 0.3846 | 0.0000 | 0.0762 | 0.0779 |

## Model: deepseek-v4.1-flash | set UTAMA-294 (ulangan 1)
- Jumlah observasi: 2058; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 20; gagal setelah ulang (dicatat): 8

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 288 | 6 | 0.0919 | 0.1308 | 0.0919 [0.0547; 0.1340] | 0.9444 | 0.0241 | 0.0083 | - | 0.0000 | 0 |
| near | R1 | anchor | 294 | 0 | 0.0339 | 0.0339 | 0.0339 [0.0098; 0.0625] | 0.9830 | 0.0128 | 0.0085 | 0.9830 | 1.0000 | 294 |
| near | R3 | anchor | 294 | 0 | 0.0749 | 0.0749 | 0.0749 [0.0361; 0.1164] | 0.9592 | 0.0071 | 0.0139 | 0.9592 | 1.0000 | 294 |
| far | R1 | anchor | 294 | 0 | 0.0134 | 0.0134 | 0.0134 [0.0011; 0.0318] | 0.9932 | 0.0073 | 0.0007 | 0.9932 | 1.0000 | 294 |
| far | R3 | anchor | 294 | 0 | 0.0712 | 0.0712 | 0.0712 [0.0355; 0.1144] | 0.9592 | 0.0277 | 0.0035 | 0.9592 | 1.0000 | 294 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 288 | 0.4896 [0.4340; 0.5486] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 288 | 0.4282 [0.3747; 0.4773] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 288 | 0.4102 [0.3574; 0.4575] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 288 | 0.0208 [0.0069; 0.0382] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0446 [0.0312; 0.0599] | 0.0201 [0.0124; 0.0295] | 0.0245 [0.0089; 0.0414] |
| R3 | 0.0689 [0.0479; 0.0908] | 0.0499 [0.0304; 0.0731] | 0.0190 [-0.0040; 0.0407] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 97 | 0.5876 | 0.0206 | -0.0029 | 0.0024 |
| en | 152 | 0.4737 | 0.0197 | 0.0468 | 0.0267 |
| unk | 39 | 0.3077 | 0.0256 | 0.0064 | 0.0308 |
