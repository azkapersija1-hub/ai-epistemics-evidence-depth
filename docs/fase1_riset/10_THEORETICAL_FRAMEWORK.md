# 10 Kerangka teori

Prinsip: hanya teori yang benar-benar dipakai oleh desain; setiap konsep dihubungkan ke operasionalisasi di `11_OPERATIONAL_DEFINITIONS.md`.

| Konsep | Peran dalam studi | Rujukan (status) | Catatan |
|---|---|---|---|
| Evidence-based judgment | Variabel respons: label SUPPORTED/REFUTED/NEI terhadap klaim dan potongan bukti | FEVER (abstrak), SciFact (abstrak) | NEI harus operasional, bukan "tidak tahu" |
| Probabilistic calibration | Kualitas distribusi 3 kelas: Brier multikelas (utama), ECE dan reliability (sekunder) | Guo 2017, Kadavath 2022, Xiong 2023, Tian 2023 (ringkasan web) | Dekomposisi Murphy multikelas = turunan sendiri, laporkan sebagai estimasi |
| Appropriate abstention | Kemampuan memilih NEI saat bukti tidak cukup | Kalai et al. 2025 (abstrak) | Skor biner menghukum abstensi; gunakan proper scoring rule |
| Evidence sensitivity | Apakah distribusi bergeser sebanding dengan arah dan kekuatan bukti | Kim et al. 2025 (abstrak) | Membedakan pembaruan sah dari sikofansi |
| Belief updating | Pembanding normatif (Bayes) untuk kondisi bukti bertentangan (Extended) | Kim et al. 2025 | Bayes = pembanding, bukan kebenaran |
| Resistance to misleading counterevidence | Hanya di Extended; bukti menyesatkan vs bukti benar yang kontradiktif | MASK, SycEval (abstrak) | Bukan inti Minimal/Standard |
| Verifikasi bukti eksternal (F11x) | Intervensi sekunder, bukan inti | Tidak ada literatur (TIDAK_TERVERIFIKASI) | Lihat `08_F11X_FEASIBILITY_AUDIT.md` |

## Pernyataan konseptual wajib
- Keluaran angka dari model adalah **laporan terukur**, bukan keyakinan internal. Tulis "stated probability" atau "elicited distribution", bukan "model believes".
- Provider tidak dapat dipisahkan dari model (sistem prompt, penyaringan, versi).
- Kesepakatan dengan label bukan bukti bahwa model "memahami" bukti.

## Yang sengaja tidak dipakai
KR-20/Cronbach alpha (butir tidak homogen, label nominal, tidak ada konstruk laten tunggal); Rasch/CFA (butuh ratusan butir, unidimensional); klaim "epistemic virtue" umum (tidak operasional di 3 hari).
