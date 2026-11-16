# 14 Rencana analisis statistik (usulan; dipraregistrasi sebelum data)

## Primary outcome (satu)
**Selisih Brier multikelas berpasangan per butir** antara dua kondisi (B−A dan D−A) dan, untuk RQ1, antara tiap model dan baseline seragam 0,6667. Alasan: proper scoring rule memakai seluruh distribusi; tidak bergantung ambang NEI; sensitif terhadap kalibrasi sekaligus diskriminasi.

## Sekunder (koreksi Holm)
Akurasi; ECE (10 bin, dilaporkan dengan n per bin); komponen reliabilitas Brier (estimasi); kualitas abstensi (NEI tepat vs salah-NEI); parse failure rate.

## Ketergantungan dan inferensi
- Butir berpasangan antar-kondisi; **bootstrap berkluster per artikel** (resampel artikel, bukan klaim), 95% CI.
- Opsional: model efek campuran (acak: butir, artikel, model; tetap: kondisi). Ketergantungan: artikel sama, klaim kembar, ulangan, domain, bahasa.
- Perbandingan antar-model: selisih Brier berpasangan per butir; jangan menafsir perbedaan provider sebagai perbedaan arsitektur.

## Reliabilitas
Fleiss kappa antar-k ulangan; SD Brier antar-run; Krippendorff alpha (nominal) antar-model; proporsi butir tak bulat; kurva reliability per stratum bukti.
**Tidak dipakai**: KR-20/Cronbach, Rasch, CFA (butir heterogen, nominal, terlalu sedikit).

## Ukuran sampel (asumsi eksplisit)
alpha 0,05 dua sisi, daya 0,80, sigma 0,35 (ASUMSI, wajib diestimasi dari pilot), paired.
| delta Brier | n (DEFF 1) | n (DEFF 1,4; m=3, ICC 0,2) |
|---|---|---|
| 0,10 | 97 | 136 |
| 0,05 | 385 | 539 |
| 0,02 | 2.404 | - |
Simulasi daya (SIMULASI TEORETIS): n=100 → 0,32; 200 → 0,53; 400 → 0,83 (delta 0,05). 45 butir lama: daya ≈0,16. Bila sigma sebenarnya 0,25, n Standard turun ke ≈197. Seluruh angka bergantung sigma dan ICC.

## Kegagalan dan data hilang
Dua batas Brier (butir gagal dikeluarkan / diberi BS=2). Normalisasi jumlah p hanya bila 1 ± 0,01; di luar itu diberi bendera.

## Kontrol
Kondisi D (plasebo) wajib bagi klaim apa pun tentang F11x. Urutan elemen prompt dikontra-seimbangkan (Latin square). Hipotesis F11x dua arah.

## Yang tidak boleh
Mengubah primary setelah melihat hasil; memilih ambang NEI setelah melihat data; melaporkan hanya model terbaik; menafsir p<0,05 tanpa interval dan ukuran efek.
