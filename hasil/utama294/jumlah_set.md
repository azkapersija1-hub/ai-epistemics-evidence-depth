# Jumlah klaim, observasi, dan parse gagal per set

| Set | Split | n klaim | n observasi | Model | n klaim uji konsistensi | n baris keluaran | parse gagal percobaan 1 | parse gagal final |
|---|---|---|---|---|---|---|---|---|
| UTAMA-294 | semua | 294 | 2058 | qwen3.8-flash | 294 | 2058 | 1 | 1 |
| UTAMA-294 | semua | 294 | 2058 | qwen4-max-preview | 294 | 2059 | 1 | 0 |
| UTAMA-294 | semua | 294 | 2058 | deepseek-v4.1-flash | 288 | 2078 | 20 | 8 |
| UTAMA-274 | dev+val+holdout | 274 | 1918 | qwen3.8-flash | 274 | 1918 | 1 | 1 |
| UTAMA-274 | dev+val+holdout | 274 | 1918 | qwen4-max-preview | 274 | 1919 | 1 | 0 |
| UTAMA-274 | dev+val+holdout | 274 | 1918 | deepseek-v4.1-flash | 268 | 1936 | 18 | 8 |
| KEPEKAAN-A | semua | 290 | 2030 | qwen3.8-flash | 290 | 2030 | 1 | 1 |
| KEPEKAAN-A | semua | 290 | 2030 | qwen4-max-preview | 290 | 2031 | 1 | 0 |
| KEPEKAAN-A | semua | 290 | 2030 | deepseek-v4.1-flash | 284 | 2050 | 20 | 8 |
| KEPEKAAN-B | semua | 280 | 1960 | qwen3.8-flash | 280 | 1960 | 1 | 1 |
| KEPEKAAN-B | semua | 280 | 1960 | qwen4-max-preview | 280 | 1961 | 1 | 0 |
| KEPEKAAN-B | semua | 280 | 1960 | deepseek-v4.1-flash | 274 | 1980 | 20 | 8 |
| SPLIT-pilot | pilot | 20 | 140 | qwen3.8-flash | 20 | 140 | 0 | 0 |
| SPLIT-pilot | pilot | 20 | 140 | qwen4-max-preview | 20 | 140 | 0 | 0 |
| SPLIT-pilot | pilot | 20 | 140 | deepseek-v4.1-flash | 20 | 142 | 2 | 0 |
| SPLIT-dev | dev | 78 | 546 | qwen3.8-flash | 78 | 546 | 0 | 0 |
| SPLIT-dev | dev | 78 | 546 | qwen4-max-preview | 78 | 546 | 0 | 0 |
| SPLIT-dev | dev | 78 | 546 | deepseek-v4.1-flash | 76 | 551 | 5 | 2 |
| SPLIT-val | val | 98 | 686 | qwen3.8-flash | 98 | 686 | 1 | 1 |
| SPLIT-val | val | 98 | 686 | qwen4-max-preview | 98 | 686 | 0 | 0 |
| SPLIT-val | val | 98 | 686 | deepseek-v4.1-flash | 96 | 694 | 8 | 3 |
| SPLIT-holdout | holdout | 98 | 686 | qwen3.8-flash | 98 | 686 | 0 | 0 |
| SPLIT-holdout | holdout | 98 | 686 | qwen4-max-preview | 98 | 687 | 1 | 0 |
| SPLIT-holdout | holdout | 98 | 686 | deepseek-v4.1-flash | 96 | 691 | 5 | 3 |

## Daftar keluar yang dipakai

KEPEKAAN-A (ID_KELUAR.txt, JANGKAR): 4 klaim: C0056, C0057, C0225, C0295

KEPEKAAN-B (ID_KELUAR_KETAT.txt, JANGKAR dengan suara TIDAK_LAYAK): 14 klaim: C0025, C0056, C0057, C0101, C0107, C0109, C0144, C0152, C0162, C0224, C0225, C0230, C0287, C0295

Baris UBAHAN di ID_KELUAR_KETAT.txt (C0085, C0233) tidak dikurangkan; keduanya tetap ada di pool JANGKAR dengan keputusan DIPAKAI.

Silang dengan status_butir.csv: A sama = True (status: 4 KELUAR); B sama = True (status: 14 JANGKAR dengan TIDAK_LAYAK).
Selisih status tanpa daftar A: []; tanpa daftar B: [].

