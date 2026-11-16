# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 98 | 0 | 0.0394 | 0.0394 | 0.0394 [0.0097; 0.0813] | 0.9796 | 0.0528 | 0.0013 | - | 0.0000 | 0 |
| near | R1 | anchor | 98 | 0 | 0.1401 | 0.1401 | 0.1401 [0.0719; 0.2199] | 0.9082 | 0.0542 | 0.0218 | 0.9082 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.2075 | 0.2075 | 0.2075 [0.1205; 0.3127] | 0.8673 | 0.0227 | 0.0876 | 0.8673 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0334 | 0.0334 | 0.0334 [0.0092; 0.0693] | 0.9796 | 0.0492 | 0.0011 | 0.9796 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.1313 | 0.1313 | 0.1313 [0.0658; 0.2123] | 0.9082 | 0.0359 | 0.0179 | 0.9082 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 98 | 0.5204 [0.4184; 0.6224] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 98 | 0.4362 [0.3634; 0.5089] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 98 | 0.4085 [0.3408; 0.4777] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 98 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1547 [0.1140; 0.2023] | 0.0735 [0.0537; 0.0978] | 0.0812 [0.0387; 0.1283] |
| R3 | 0.1959 [0.1487; 0.2522] | 0.1381 [0.1000; 0.1842] | 0.0579 [0.0248; 0.0972] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 36 | 0.5833 | 0.0000 | 0.0425 | 0.0278 |
| en | 48 | 0.5000 | 0.0000 | 0.1029 | 0.0665 |
| unk | 14 | 0.4286 | 0.0000 | 0.1064 | 0.1057 |
