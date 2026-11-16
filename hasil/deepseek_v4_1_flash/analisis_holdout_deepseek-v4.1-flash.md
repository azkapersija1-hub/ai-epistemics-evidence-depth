# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 5; gagal setelah ulang (dicatat): 3

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 96 | 2 | 0.0739 | 0.1132 | 0.0739 [0.0218; 0.1400] | 0.9583 | 0.0261 | 0.0057 | - | 0.0000 | 0 |
| near | R1 | anchor | 98 | 0 | 0.0426 | 0.0426 | 0.0426 [0.0031; 0.1023] | 0.9796 | 0.0106 | 0.0175 | 0.9796 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.0755 | 0.0755 | 0.0755 [0.0200; 0.1591] | 0.9592 | 0.0111 | 0.0108 | 0.9592 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0013 | 0.0013 | 0.0013 [0.0006; 0.0020] | 1.0000 | 0.0140 | 0.0000 | 1.0000 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.1097 | 0.1097 | 0.1097 [0.0367; 0.1972] | 0.9388 | 0.0479 | 0.0099 | 0.9388 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 96 | 0.4792 [0.3854; 0.5833] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 96 | 0.4091 [0.3218; 0.4946] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 96 | 0.3884 [0.3013; 0.4744] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 96 | 0.0312 [0.0000; 0.0729] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0502 [0.0269; 0.0822] | 0.0140 [0.0095; 0.0193] | 0.0362 [0.0146; 0.0661] |
| R3 | 0.0680 [0.0367; 0.1112] | 0.0733 [0.0340; 0.1202] | -0.0053 [-0.0497; 0.0350] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 33 | 0.6061 | 0.0606 | 0.0309 | -0.0003 |
| en | 52 | 0.4231 | 0.0192 | 0.0419 | 0.0004 |
| unk | 11 | 0.3636 | 0.0000 | 0.0255 | -0.0482 |
