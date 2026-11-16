# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: codex_gpt61_sol_tak_terverifikasi (ulangan 1)
- Jumlah observasi: 133; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 19 | 0 | 0.0614 | 0.0614 | 0.0614 [0.0001; 0.1818] | 0.9474 | 0.0479 | 0.0028 | - | - | 0 |
| near | R1 | anchor | 19 | 0 | 0.0015 | 0.0015 | 0.0015 [0.0000; 0.0044] | 1.0000 | 0.0111 | 0.0000 | 1.0000 | 1.0000 | 19 |
| near | R3 | anchor | 19 | 0 | 0.0084 | 0.0084 | 0.0084 [0.0001; 0.0250] | 1.0000 | 0.0220 | 0.0000 | 1.0000 | 1.0000 | 19 |
| far | R1 | anchor | 19 | 0 | 0.0001 | 0.0001 | 0.0001 [0.0000; 0.0003] | 1.0000 | 0.0038 | 0.0000 | 1.0000 | 1.0000 | 19 |
| far | R3 | anchor | 19 | 0 | 0.0001 | 0.0001 | 0.0001 [0.0000; 0.0004] | 1.0000 | 0.0045 | 0.0000 | 1.0000 | 1.0000 | 19 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 19 | 0.7368 [0.5263; 0.9474] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 19 | 0.2311 [0.0859; 0.3930] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 19 | 0.2496 [0.0984; 0.4112] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 19 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0111 [0.0036; 0.0237] | 0.0038 [0.0021; 0.0070] | 0.0073 [-0.0005; 0.0203] |
| R3 | 0.0220 [0.0049; 0.0525] | 0.0045 [0.0021; 0.0083] | 0.0175 [-0.0002; 0.0484] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 10 | 0.8000 | 0.0000 | -0.0007 | -0.0015 |
| en | 5 | 0.8000 | 0.0000 | 0.0266 | 0.0618 |
| unk | 4 | 0.5000 | 0.0000 | 0.0030 | 0.0097 |
