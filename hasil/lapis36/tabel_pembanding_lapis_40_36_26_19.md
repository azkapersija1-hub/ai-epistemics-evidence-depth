# Pembanding lapis 40, 36, 26, 19 per model (nilai titik saja)

Status: HASIL MODEL (BELUM DIVERIFIKASI). Nilai titik saja. Skrip tidak memberi CI untuk selisih antar lapis karena lapis bersarang (36 subset 40, 26 dan 19 subset 40).
Lapis 40, 26, dan 19 dihitung dengan skrip yang sama dan sudah dicocokkan dengan tabel Agen A dan Agen C.

| Model | Metrik | Lapis 40 | Lapis 36 | Lapis 26 | Lapis 19 |
|---|---|---|---|---|---|
| qwen3.8-flash | Brier batas 1 own R3 (anchor SUPPORTED) | 0.0689 | 0.0765 | 0.0398 | 0.0540 |
| qwen3.8-flash | Brier batas 1 near R1 (anchor NEI) | 0.0573 | 0.0589 | 0.0792 | 0.1075 |
| qwen3.8-flash | Brier batas 1 near R3 (anchor NEI) | 0.1253 | 0.1388 | 0.1776 | 0.2415 |
| qwen3.8-flash | Brier batas 1 far R1 (anchor NEI) | 0.0487 | 0.0541 | 0.0733 | 0.0991 |
| qwen3.8-flash | Brier batas 1 far R3 (anchor NEI) | 0.0813 | 0.0900 | 0.1213 | 0.1653 |
| qwen3.8-flash | Brier batas 2 own R3 (gagal = 2,0) | 0.0689 | 0.0765 | 0.0398 | 0.0540 |
| qwen3.8-flash | Brier batas 2 near R1 (gagal = 2,0) | 0.0573 | 0.0589 | 0.0792 | 0.1075 |
| qwen3.8-flash | Brier batas 2 near R3 (gagal = 2,0) | 0.1253 | 0.1388 | 0.1776 | 0.2415 |
| qwen3.8-flash | Brier batas 2 far R1 (gagal = 2,0) | 0.0487 | 0.0541 | 0.0733 | 0.0991 |
| qwen3.8-flash | Brier batas 2 far R3 (gagal = 2,0) | 0.0813 | 0.0900 | 0.1213 | 0.1653 |
| qwen3.8-flash | Sesuai (label R1 = R3) | 0.4750 | 0.5278 | 0.6154 | 0.6842 |
| qwen3.8-flash | Pergeseran dS | 0.5141 | 0.4689 | 0.3962 | 0.3406 |
| qwen3.8-flash | Pergeseran dN | 0.4896 | 0.4443 | 0.3721 | 0.3195 |
| qwen3.8-flash | Overkomit (tau 0,7) | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| qwen3.8-flash | False-support near R1 | 0.0725 | 0.0711 | 0.0838 | 0.1095 |
| qwen3.8-flash | False-support far R1 | 0.0462 | 0.0508 | 0.0588 | 0.0695 |
| qwen3.8-flash | Selisih FS near-far R1 | 0.0262 | 0.0203 | 0.0250 | 0.0400 |
| qwen3.8-flash | False-support near R3 | 0.1227 | 0.1336 | 0.1465 | 0.1900 |
| qwen3.8-flash | False-support far R3 | 0.0760 | 0.0814 | 0.0954 | 0.1221 |
| qwen3.8-flash | Selisih FS near-far R3 | 0.0467 | 0.0522 | 0.0512 | 0.0679 |
| qwen4-max-preview | Brier batas 1 own R3 (anchor SUPPORTED) | 0.0086 | 0.0083 | 0.0074 | 0.0084 |
| qwen4-max-preview | Brier batas 1 near R1 (anchor NEI) | 0.0634 | 0.0696 | 0.0859 | 0.1139 |
| qwen4-max-preview | Brier batas 1 near R3 (anchor NEI) | 0.1593 | 0.1725 | 0.1877 | 0.2436 |
| qwen4-max-preview | Brier batas 1 far R1 (anchor NEI) | 0.0701 | 0.0773 | 0.0794 | 0.1073 |
| qwen4-max-preview | Brier batas 1 far R3 (anchor NEI) | 0.2401 | 0.2630 | 0.2774 | 0.3065 |
| qwen4-max-preview | Brier batas 2 own R3 (gagal = 2,0) | 0.0086 | 0.0083 | 0.0074 | 0.0084 |
| qwen4-max-preview | Brier batas 2 near R1 (gagal = 2,0) | 0.0634 | 0.0696 | 0.0859 | 0.1139 |
| qwen4-max-preview | Brier batas 2 near R3 (gagal = 2,0) | 0.1593 | 0.1725 | 0.1877 | 0.2436 |
| qwen4-max-preview | Brier batas 2 far R1 (gagal = 2,0) | 0.0701 | 0.0773 | 0.0794 | 0.1073 |
| qwen4-max-preview | Brier batas 2 far R3 (gagal = 2,0) | 0.2401 | 0.2630 | 0.2774 | 0.3065 |
| qwen4-max-preview | Sesuai (label R1 = R3) | 0.5000 | 0.5556 | 0.6538 | 0.7368 |
| qwen4-max-preview | Pergeseran dS | 0.4581 | 0.4119 | 0.3133 | 0.2445 |
| qwen4-max-preview | Pergeseran dN | 0.4194 | 0.3749 | 0.2763 | 0.1988 |
| qwen4-max-preview | Overkomit (tau 0,7) | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| qwen4-max-preview | False-support near R1 | 0.1163 | 0.1217 | 0.1258 | 0.1489 |
| qwen4-max-preview | False-support far R1 | 0.1040 | 0.1100 | 0.1069 | 0.1316 |
| qwen4-max-preview | Selisih FS near-far R1 | 0.0122 | 0.0117 | 0.0188 | 0.0174 |
| qwen4-max-preview | False-support near R3 | 0.2027 | 0.2122 | 0.2127 | 0.2511 |
| qwen4-max-preview | False-support far R3 | 0.2095 | 0.2200 | 0.2112 | 0.2342 |
| qwen4-max-preview | Selisih FS near-far R3 | -0.0068 | -0.0078 | 0.0015 | 0.0168 |
| deepseek-v4.1-flash | Brier batas 1 own R3 (anchor SUPPORTED) | 0.1110 | 0.1225 | 0.1091 | 0.1477 |
| deepseek-v4.1-flash | Brier batas 1 near R1 (anchor NEI) | 0.0034 | 0.0035 | 0.0041 | 0.0053 |
| deepseek-v4.1-flash | Brier batas 1 near R3 (anchor NEI) | 0.0069 | 0.0076 | 0.0096 | 0.0129 |
| deepseek-v4.1-flash | Brier batas 1 far R1 (anchor NEI) | 0.0896 | 0.0994 | 0.0753 | 0.1027 |
| deepseek-v4.1-flash | Brier batas 1 far R3 (anchor NEI) | 0.0809 | 0.0898 | 0.0561 | 0.0756 |
| deepseek-v4.1-flash | Brier batas 2 own R3 (gagal = 2,0) | 0.1582 | 0.1746 | 0.1818 | 0.2452 |
| deepseek-v4.1-flash | Brier batas 2 near R1 (gagal = 2,0) | 0.0034 | 0.0035 | 0.0041 | 0.0053 |
| deepseek-v4.1-flash | Brier batas 2 near R3 (gagal = 2,0) | 0.0069 | 0.0076 | 0.0096 | 0.0129 |
| deepseek-v4.1-flash | Brier batas 2 far R1 (gagal = 2,0) | 0.0896 | 0.0994 | 0.0753 | 0.1027 |
| deepseek-v4.1-flash | Brier batas 2 far R3 (gagal = 2,0) | 0.0809 | 0.0898 | 0.0561 | 0.0756 |
| deepseek-v4.1-flash | Sesuai (label R1 = R3) | 0.3846 | 0.4286 | 0.5200 | 0.6111 |
| deepseek-v4.1-flash | Pergeseran dS | 0.4944 | 0.4449 | 0.3328 | 0.2417 |
| deepseek-v4.1-flash | Pergeseran dN | 0.4855 | 0.4359 | 0.3250 | 0.2356 |
| deepseek-v4.1-flash | Overkomit (tau 0,7) | 0.0256 | 0.0286 | 0.0400 | 0.0556 |
| deepseek-v4.1-flash | False-support near R1 | 0.0290 | 0.0289 | 0.0281 | 0.0326 |
| deepseek-v4.1-flash | False-support far R1 | 0.0583 | 0.0631 | 0.0500 | 0.0616 |
| deepseek-v4.1-flash | Selisih FS near-far R1 | -0.0292 | -0.0342 | -0.0219 | -0.0289 |
| deepseek-v4.1-flash | False-support near R3 | 0.0372 | 0.0394 | 0.0465 | 0.0579 |
| deepseek-v4.1-flash | False-support far R3 | 0.0560 | 0.0611 | 0.0435 | 0.0516 |
| deepseek-v4.1-flash | Selisih FS near-far R3 | -0.0188 | -0.0217 | 0.0031 | 0.0063 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 1 own R3 (anchor SUPPORTED) | 0.0305 | 0.0339 | 0.0450 | 0.0614 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 1 near R1 (anchor NEI) | 0.0010 | 0.0009 | 0.0011 | 0.0015 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 1 near R3 (anchor NEI) | 0.0044 | 0.0048 | 0.0064 | 0.0084 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 1 far R1 (anchor NEI) | 0.0005 | 0.0005 | 0.0001 | 0.0001 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 1 far R3 (anchor NEI) | 0.0010 | 0.0011 | 0.0003 | 0.0001 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 2 own R3 (gagal = 2,0) | 0.0797 | 0.0885 | 0.0450 | 0.0614 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 2 near R1 (gagal = 2,0) | 0.0509 | 0.0564 | 0.0011 | 0.0015 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 2 near R3 (gagal = 2,0) | 0.0543 | 0.0602 | 0.0064 | 0.0084 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 2 far R1 (gagal = 2,0) | 0.0504 | 0.0561 | 0.0001 | 0.0001 |
| codex (gpt-6.1-sol, tak terverifikasi) | Brier batas 2 far R3 (gagal = 2,0) | 0.0510 | 0.0567 | 0.0003 | 0.0001 |
| codex (gpt-6.1-sol, tak terverifikasi) | Sesuai (label R1 = R3) | 0.4615 | 0.5143 | 0.6538 | 0.7368 |
| codex (gpt-6.1-sol, tak terverifikasi) | Pergeseran dS | 0.4854 | 0.4301 | 0.3082 | 0.2311 |
| codex (gpt-6.1-sol, tak terverifikasi) | Pergeseran dN | 0.4928 | 0.4385 | 0.3214 | 0.2496 |
| codex (gpt-6.1-sol, tak terverifikasi) | Overkomit (tau 0,7) | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| codex (gpt-6.1-sol, tak terverifikasi) | False-support near R1 | 0.0099 | 0.0092 | 0.0096 | 0.0111 |
| codex (gpt-6.1-sol, tak terverifikasi) | False-support far R1 | 0.0053 | 0.0056 | 0.0033 | 0.0038 |
| codex (gpt-6.1-sol, tak terverifikasi) | Selisih FS near-far R1 | 0.0046 | 0.0036 | 0.0063 | 0.0073 |
| codex (gpt-6.1-sol, tak terverifikasi) | False-support near R3 | 0.0156 | 0.0160 | 0.0192 | 0.0220 |
| codex (gpt-6.1-sol, tak terverifikasi) | False-support far R3 | 0.0080 | 0.0086 | 0.0058 | 0.0045 |
| codex (gpt-6.1-sol, tak terverifikasi) | Selisih FS near-far R3 | 0.0076 | 0.0074 | 0.0135 | 0.0175 |
