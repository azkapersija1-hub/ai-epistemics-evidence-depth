# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: codex_gpt61_sol_tak_terverifikasi (ulangan 1)
- Jumlah observasi: 182; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 26 | 0 | 0.0450 | 0.0450 | 0.0450 [0.0002; 0.1330] | 0.9615 | 0.0387 | 0.0015 | - | - | 0 |
| near | R1 | anchor | 26 | 0 | 0.0011 | 0.0011 | 0.0011 [0.0000; 0.0033] | 1.0000 | 0.0096 | 0.0000 | 1.0000 | 1.0000 | 26 |
| near | R3 | anchor | 26 | 0 | 0.0064 | 0.0064 | 0.0064 [0.0001; 0.0186] | 1.0000 | 0.0192 | 0.0000 | 1.0000 | 1.0000 | 26 |
| far | R1 | anchor | 26 | 0 | 0.0001 | 0.0001 | 0.0001 [0.0000; 0.0002] | 1.0000 | 0.0033 | 0.0000 | 1.0000 | 1.0000 | 26 |
| far | R3 | anchor | 26 | 0 | 0.0003 | 0.0003 | 0.0003 [0.0000; 0.0008] | 1.0000 | 0.0058 | 0.0000 | 1.0000 | 1.0000 | 26 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 26 | 0.6538 [0.4615; 0.8462] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 26 | 0.3082 [0.1688; 0.4621] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 26 | 0.3214 [0.1777; 0.4712] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 26 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0096 [0.0037; 0.0194] | 0.0033 [0.0020; 0.0057] | 0.0063 [0.0003; 0.0164] |
| R3 | 0.0192 [0.0056; 0.0426] | 0.0058 [0.0022; 0.0108] | 0.0135 [0.0001; 0.0372] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 14 | 0.6429 | 0.0000 | -0.0001 | -0.0017 |
| en | 7 | 0.7143 | 0.0000 | 0.0219 | 0.0479 |
| unk | 5 | 0.6000 | 0.0000 | 0.0024 | 0.0078 |
