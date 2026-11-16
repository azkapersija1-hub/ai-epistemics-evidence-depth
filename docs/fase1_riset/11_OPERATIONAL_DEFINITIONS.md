# 11 Definisi operasional (usulan, beku sebelum eksekusi)

## Unit dan label
- **Butir**: (klaim, 2-4 potongan bukti ber-ID, kunci). Dibangun dari artikel korpus yang punya abstract+results+conclusion dan DOI.
- **Label kunci**: SUPPORTED (bukti cukup mendukung), REFUTED (bukti cukup membantah), **NEI** (potongan bukti yang diberikan, dalam rentang yang dicatat, tidak cukup mendukung maupun membantah). NEI **bukan** "anotator tidak tahu".
- **Rentang bukti**: jenis sumber (abstrak/hasil/kesimpulan), langsung/tidak langsung, ada/tidak ada pertentangan; dicatat sebagai kovariat.
- **Kunci diadjudikasi**: minimal dua anotator independen + adjudikator; kesepakatan dicatat (Cohen kappa). Butir tak bulat menjadi stratum, tidak dibuang diam-diam.

## Keluaran model
- Distribusi `p = (p_S, p_R, p_N)`, jumlah 1 ± 0,01, format JSON tetap.
- Label terpilih = argmax p (seri → NEI, dipraregistrasi).

## Metrik
| Metrik | Definisi |
|---|---|
| Brier multikelas (primary) | BS = (1/N) Σ_i Σ_k (p_ik − y_ik)², rentang 0..2, baseline seragam = 0,6667 |
| Brier biner "terpilih benar" | (c − 1[benar])²; **bukan** Brier multikelas; jangan diberi nama sama |
| Akurasi | 1[label terpilih = kunci] (sekunder) |
| ECE | 10 bin pada confidence label terpilih; dilaporkan bersama jumlah butir per bin |
| Abstention quality | Rasio NEI tepat/ salah-NEI terhadap butir SUPPORTED/REFUTED |
| Evidence sensitivity | Perubahan distribusi antar kondisi bukti (Extended) |
| Parse failure rate | Proporsi keluaran tidak valid per model |

## Kondisi
- **A**: klaim+bukti+instruksi (baseline).
- **B**: A + skor F11x-adaptasi (intervensi).
- **C**: skor saja, tanpa bukti; hanya pada development split.
- **D**: A + angka plasebo acak dengan format, panjang, dan rentang sama dengan B.
Urutan elemen prompt dikontra-seimbangkan; jumlah token dilaporkan.

## Aturan kegagalan
Parse gagal: ulang sekali; bila gagal lagi, catat. Brier dilaporkan dalam dua batas: butir gagal dikeluarkan, dan butir gagal diberi BS=2.

## Larangan
Kunci/rasional/kolom kategori tidak boleh ada di prompt, nama berkas, atau metadata yang dikirim; uji otomatis wajib.
