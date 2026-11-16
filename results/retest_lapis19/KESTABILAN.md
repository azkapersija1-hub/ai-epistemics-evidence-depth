# KESTABILAN uji ulang (test-retest) lapis-19: putaran asli (u1) vs uji ulang (u2)
HASIL UJI ULANG UNTUK MENGUKUR KESTABILAN SAJA. Tidak digabung ke hasil utama; tidak menimpa berkas lama.
Cakupan: 19 klaim lapis-19. Holdout dikecualikan (lihat laporan). Observasi per model: 133 (19 klaim x 7).
Definisi: argmax memakai aturan seri di skor.py (NEI menang bila seri). Brier multikelas per observasi, selisih = Brier(u2) - Brier(u1) hanya untuk observasi berlabel jangkar (own R3 = SUPPORTED; near/far = NEI). Observasi gagal parse di salah satu putaran TIDAK dibuang diam-diam: dihitung terpisah dan ditampilkan dua cara (kolom 'gagal dihitung beda').

## Cakupan dan kelengkapan
| Model | u1 belum ada | u2 belum ada |
|---|---|---|
| qwen3.8-flash | 0 | 0 |
| deepseek-v4.1-flash | 0 | 0 |
| qwen4-max-preview | 0 | 0 |

## Kestabilan per model dan tingkat bukti
| Model | Tingkat | n obs | n pasangan valid | n gagal (salah satu) | % argmax sama | % argmax sama (gagal = beda) | rerata abs selisih p(SUPPORTED) | n berlabel valid | n klaim-tingkat berlabel | rerata selisih Brier per klaim (u2-u1) | rerata abs selisih Brier per klaim |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.8-flash | R1 | 57 | 57 | 0 | 93.0% | 93.0% | 0.0449 | 38 | 19 | -0.0520 | 0.0629 |
| qwen3.8-flash | R2 | 19 | 19 | 0 | 78.9% | 78.9% | 0.0932 | 0 | 0 | - | - |
| qwen3.8-flash | R3 | 57 | 57 | 0 | 89.5% | 89.5% | 0.0302 | 57 | 19 | 0.0142 | 0.1409 |
| qwen3.8-flash | SEMUA | 133 | 133 | 0 | 89.5% | 89.5% | 0.0455 | 95 | 38 | -0.0189 | 0.1019 |
| deepseek-v4.1-flash | R1 | 57 | 57 | 0 | 94.7% | 94.7% | 0.0321 | 38 | 19 | -0.0503 | 0.0534 |
| deepseek-v4.1-flash | R2 | 19 | 19 | 0 | 94.7% | 94.7% | 0.0468 | 0 | 0 | - | - |
| deepseek-v4.1-flash | R3 | 57 | 55 | 2 | 92.7% | 89.5% | 0.0207 | 55 | 19 | 0.0309 | 0.1205 |
| deepseek-v4.1-flash | SEMUA | 133 | 131 | 2 | 93.9% | 92.5% | 0.0295 | 93 | 38 | -0.0097 | 0.0870 |
| qwen4-max-preview | R1 | 57 | 57 | 0 | 94.7% | 94.7% | 0.0218 | 38 | 19 | 0.0226 | 0.0551 |
| qwen4-max-preview | R2 | 19 | 19 | 0 | 94.7% | 94.7% | 0.0297 | 0 | 0 | - | - |
| qwen4-max-preview | R3 | 57 | 57 | 0 | 94.7% | 94.7% | 0.0115 | 57 | 19 | -0.0008 | 0.0581 |
| qwen4-max-preview | SEMUA | 133 | 133 | 0 | 94.7% | 94.7% | 0.0185 | 95 | 38 | 0.0109 | 0.0566 |

Catatan: R2 tidak punya observasi berlabel jangkar (own R1 dan R2 tanpa label), sehingga kolom Brier untuk R1 hanya berasal dari near/far R1 dan untuk R2 kosong.

## Observasi gagal parse di salah satu putaran (ditandai, tidak dibuang diam-diam)
| Model | obs_id | Tingkat | u1 ok | u2 ok | u1 percobaan | u2 percobaan |
|---|---|---|---|---|---|---|
| deepseek-v4.1-flash | C0099_7 | R3 | True | False | 1 | 2 |
| deepseek-v4.1-flash | C0246_2 | R3 | False | True | 2 | 1 |

Rincian galat per observasi: KESTABILAN_gagal_parse.csv. Selisih per klaim: KESTABILAN_per_klaim.csv.
