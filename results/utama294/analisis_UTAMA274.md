# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Set UTAMA-274: 274 klaim tanpa pilot (dev+val+holdout)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash | set UTAMA-274 (ulangan 1)
- Jumlah observasi: 1918; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 274 | 0 | 0.0343 | 0.0343 | 0.0343 [0.0120; 0.0613] | 0.9781 | 0.0175 | 0.0008 | - | 0.0000 | 0 |
| near | R1 | anchor | 274 | 0 | 0.0517 | 0.0517 | 0.0517 [0.0250; 0.0867] | 0.9781 | 0.0284 | 0.0083 | 0.9781 | 1.0000 | 274 |
| near | R3 | anchor | 274 | 0 | 0.1441 | 0.1441 | 0.1441 [0.0937; 0.1985] | 0.9161 | 0.0261 | 0.0289 | 0.9161 | 1.0000 | 274 |
| far | R1 | anchor | 274 | 0 | 0.0276 | 0.0276 | 0.0276 [0.0085; 0.0534] | 0.9854 | 0.0120 | 0.0012 | 0.9854 | 1.0000 | 274 |
| far | R3 | anchor | 273 | 1 | 0.0934 | 0.1004 | 0.0934 [0.0542; 0.1399] | 0.9414 | 0.0251 | 0.0124 | 0.9414 | 1.0000 | 273 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 274 | 0.5146 [0.4562; 0.5730] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 274 | 0.4683 [0.4210; 0.5173] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 274 | 0.4439 [0.3961; 0.4925] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 274 | 0.0073 [0.0000; 0.0182] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0691 [0.0525; 0.0885] | 0.0357 [0.0237; 0.0511] | 0.0334 [0.0173; 0.0508] |
| R3 | 0.1233 [0.0957; 0.1537] | 0.0750 [0.0522; 0.1023] | 0.0483 [0.0190; 0.0790] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 94 | 0.6064 | 0.0213 | 0.0067 | 0.0148 |
| en | 143 | 0.4825 | 0.0000 | 0.0501 | 0.0624 |
| unk | 37 | 0.4054 | 0.0000 | 0.0365 | 0.0778 |

## Model: qwen4-max-preview | set UTAMA-274 (ulangan 1)
- Jumlah observasi: 1918; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 274 | 0 | 0.0235 | 0.0235 | 0.0235 [0.0103; 0.0408] | 0.9891 | 0.0438 | 0.0004 | - | 0.0000 | 0 |
| near | R1 | anchor | 274 | 0 | 0.1036 | 0.1036 | 0.1036 [0.0689; 0.1412] | 0.9307 | 0.0508 | 0.0133 | 0.9307 | 1.0000 | 274 |
| near | R3 | anchor | 274 | 0 | 0.2191 | 0.2191 | 0.2191 [0.1627; 0.2775] | 0.8613 | 0.0222 | 0.0683 | 0.8613 | 1.0000 | 274 |
| far | R1 | anchor | 274 | 0 | 0.0512 | 0.0512 | 0.0512 [0.0280; 0.0778] | 0.9635 | 0.0453 | 0.0023 | 0.9635 | 1.0000 | 274 |
| far | R3 | anchor | 274 | 0 | 0.1502 | 0.1502 | 0.1502 [0.1017; 0.2011] | 0.9015 | 0.0097 | 0.0283 | 0.9015 | 1.0000 | 274 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 274 | 0.5511 [0.4927; 0.6095] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 274 | 0.4090 [0.3648; 0.4547] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 274 | 0.3781 [0.3361; 0.4225] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 274 | 0.0073 [0.0000; 0.0182] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1404 [0.1188; 0.1641] | 0.0855 [0.0695; 0.1034] | 0.0549 [0.0338; 0.0757] |
| R3 | 0.2116 [0.1800; 0.2437] | 0.1485 [0.1212; 0.1783] | 0.0631 [0.0389; 0.0879] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 94 | 0.6383 | 0.0106 | 0.0239 | 0.0154 |
| en | 143 | 0.5315 | 0.0070 | 0.0744 | 0.0950 |
| unk | 37 | 0.4054 | 0.0000 | 0.0581 | 0.0605 |

## Model: deepseek-v4.1-flash | set UTAMA-274 (ulangan 1)
- Jumlah observasi: 1918; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 18; gagal setelah ulang (dicatat): 8

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 268 | 6 | 0.0981 | 0.1397 | 0.0981 [0.0584; 0.1436] | 0.9403 | 0.0262 | 0.0090 | - | 0.0000 | 0 |
| near | R1 | anchor | 274 | 0 | 0.0352 | 0.0352 | 0.0352 [0.0098; 0.0671] | 0.9818 | 0.0096 | 0.0090 | 0.9818 | 1.0000 | 274 |
| near | R3 | anchor | 274 | 0 | 0.0622 | 0.0622 | 0.0622 [0.0275; 0.1041] | 0.9672 | 0.0062 | 0.0125 | 0.9672 | 1.0000 | 274 |
| far | R1 | anchor | 274 | 0 | 0.0143 | 0.0143 | 0.0143 [0.0011; 0.0356] | 0.9927 | 0.0065 | 0.0007 | 0.9927 | 1.0000 | 274 |
| far | R3 | anchor | 274 | 0 | 0.0764 | 0.0764 | 0.0764 [0.0392; 0.1197] | 0.9562 | 0.0305 | 0.0039 | 0.9562 | 1.0000 | 274 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 268 | 0.5000 [0.4440; 0.5597] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 268 | 0.4162 [0.3643; 0.4682] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 268 | 0.4007 [0.3505; 0.4508] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 268 | 0.0187 [0.0037; 0.0373] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0437 [0.0302; 0.0604] | 0.0203 [0.0122; 0.0323] | 0.0235 [0.0053; 0.0418] |
| R3 | 0.0614 [0.0424; 0.0831] | 0.0528 [0.0324; 0.0766] | 0.0086 [-0.0133; 0.0275] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 91 | 0.6044 | 0.0220 | -0.0069 | -0.0085 |
| en | 140 | 0.4786 | 0.0143 | 0.0478 | 0.0203 |
| unk | 37 | 0.3243 | 0.0270 | 0.0065 | 0.0070 |
