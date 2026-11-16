# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: codex_gpt61_sol_tak_terverifikasi (ulangan 1)
- Jumlah observasi: 280; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 7; gagal setelah ulang (dicatat): 7

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 39 | 1 | 0.0305 | 0.0797 | 0.0305 [0.0003; 0.0890] | 0.9744 | 0.0300 | 0.0007 | - | - | 0 |
| near | R1 | anchor | 39 | 1 | 0.0010 | 0.0509 | 0.0010 [0.0001; 0.0026] | 1.0000 | 0.0099 | 0.0000 | 1.0000 | 1.0000 | 39 |
| near | R3 | anchor | 39 | 1 | 0.0044 | 0.0543 | 0.0044 [0.0002; 0.0127] | 1.0000 | 0.0156 | 0.0000 | 1.0000 | 1.0000 | 39 |
| far | R1 | anchor | 39 | 1 | 0.0005 | 0.0504 | 0.0005 [0.0000; 0.0013] | 1.0000 | 0.0053 | 0.0000 | 1.0000 | 1.0000 | 39 |
| far | R3 | anchor | 39 | 1 | 0.0010 | 0.0510 | 0.0010 [0.0000; 0.0028] | 1.0000 | 0.0080 | 0.0000 | 1.0000 | 1.0000 | 39 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 39 | 0.4615 [0.3077; 0.6154] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 39 | 0.4854 [0.3547; 0.6169] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 39 | 0.4928 [0.3584; 0.6239] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 39 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0099 [0.0049; 0.0175] | 0.0053 [0.0022; 0.0105] | 0.0046 [-0.0020; 0.0132] |
| R3 | 0.0156 [0.0061; 0.0329] | 0.0080 [0.0028; 0.0155] | 0.0076 [-0.0048; 0.0262] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 16 | 0.5625 | 0.0000 | -0.0042 | -0.0079 |
| en | 15 | 0.4000 | 0.0000 | 0.0157 | 0.0255 |
| unk | 8 | 0.3750 | 0.0000 | 0.0016 | 0.0049 |
