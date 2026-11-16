# glm-5.3: dihentikan sebelum selesai (catatan saja)

Berkas ini hanya mencatat keputusan. Keluaran mentah glm-5.3 TIDAK disalin ke repositori dan TIDAK dianalisis.

## Yang terjadi

- glm-5.3 ditambahkan lewat Amandemen 3 pada protokol (`docs/prareg/PREREG_DIBEKUKAN.md`, bagian Amandemen 3), dicatat sebelum satu pun keluaran glm-5.3 dikumpulkan.
- Pengumpulan dihentikan sebelum selesai dengan alasan biaya token. Keputusan ini dicatat sebagai deviasi D2 di `docs/prareg/CATATAN_DEVIASI.md`.
- Akibatnya glm-5.3 TIDAK masuk perbandingan model utama.

## Yang tidak dilakukan (sesuai keputusan penulis di catatan deviasi)

- Holdout glm-5.3 yang parsial tidak dianalisis dan tidak dipakai untuk klaim apa pun. Alasannya, memilih sebagian data setelah melihat hasil dapat menjadi seleksi yang bias.
- Keluaran mentah parsial tidak disalin ke repositori ini.

## Jumlah baris yang tercatat (metadata, bukan hasil)

Jumlah baris pada berkas mentah yang tersimpan di folder sumber lama, hanya untuk pelacakan. Ini bukan jumlah observasi yang valid, dan tidak boleh dibaca sebagai hasil.

| Split | Baris tercatat |
|---|---|
| pilot | 146 |
| dev | 560 |
| val | 713 |
| holdout (parsial) | 594 |

## Status

Dihentikan. Tidak ada angka glm-5.3 dalam laporan utama. Bila laporan menyebut glm-5.3, sebut sebagai model yang dihentikan dan tidak dianalisis.
