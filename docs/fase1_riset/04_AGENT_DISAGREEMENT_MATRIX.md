# 04 Matriks perbedaan Agent A vs Agent B

Kedua agen adalah **Claude Haiku 5.5 (claude-haiku-5-5)**, dijalankan sebagai asisten riset, bukan subjek uji. Independensi bersifat **prosedural** (folder kerja terpisah, Agent B tidak membaca berkas Agent A dan sebaliknya), **bukan independensi statistik**: keduanya satu keluarga model, dengan bias dan data latih yang sama, sehingga kesepakatan keduanya tidak boleh dibaca sebagai konfirmasi independen.

| Topik | Agent A | Agent B | Status |
|---|---|---|---|
| Judul terkuat | Judul (3) "Knowing When Evidence Is Insufficient" | Judul (3) paling kuat, tetapi "Knowing when" mengklaim introspeksi yang belum diuji; ganti "whether" | Sepakat arah, beda redaksi |
| Judul (2) dengan F11x | Cadangan, hanya bila F11x dapat dioperasionalkan | Tidak disarankan: "improve" memuat kesimpulan; ganti ke bentuk pertanyaan netral dengan plasebo | Beda tegas (B lebih keras) |
| Judul (1) "When Evidence Disagrees" | Layak sebagai payung, lingkup dipangkas | Tiga klaim = tiga primary; jadikan kontra-bukti satu kondisi atau studi lanjutan | Sepakat dipangkas |
| Variabel utama | Maksimal dua: label, kekuatan/arah kontra-bukti | Satu primary: selisih Brier multikelas berpasangan | Beda (B lebih ketat; diambil B) |
| Elisitasi keyakinan | Bandingkan verbal vs probabilitas turunan sampel | Primer: distribusi 3 kelas langsung; sampel k=5 pada subset; logprob hanya jika tersedia | Dilengkapi, tidak bertentangan |
| F11x | Tidak ada literatur; TIDAK_TERVERIFIKASI; jangan diasumsikan valid | Pengukuran di sisi kita tetapi intervensi di prompt; butuh Kondisi D plasebo | Sepakat; B lebih operasional |
| Kebaruan | Sedang; abstensi di SciFact sudah ada (2602.14189, belum dibuka) | Tidak menilai kebaruan secara literatur; fokus metode | A menandai risiko tumpang tindih |
| Ukuran sampel | Tidak menghitung | n=385 (DEFF 1) / 539 (DEFF 1,4) untuk delta 0,05, sigma 0,35 (asumsi) | Hanya B |
| 45 butir lama | Tidak membahas | Tidak boleh jadi holdout; pilot saja | Sejalan dengan audit lokal |
| Sumber 2026 | Tandai RINGKASAN_WEB, jangan dikutip | Tandai hanya daftar pencarian | Sepakat |

## Perbedaan yang memengaruhi keputusan
1. **Primary outcome**: A menyebut dua variabel utama, B satu. Saya mengikuti B (satu primary, Brier multikelas berpasangan) agar daya terjaga dan tidak ada ambiguitas konfirmatori.
2. **Peran F11x**: keduanya menolak mengasumsikan F11x membantu; B menambahkan plasebo. Diikuti.
3. **Redaksi judul**: A menyarankan judul 3 apa adanya; B meminta klaim introspektif dilunakkan. Diikuti B.

## Yang tidak dapat diputuskan dari kedua agen
- Apakah SciFact punya label NEI (A tidak mengonfirmasi) — harus dicek langsung sebelum dipakai.
- Kebaruan terhadap arXiv 2602.14189 — belum dibuka siapa pun.
- Nilai sigma dan ICC — asumsi; hanya pilot yang bisa mengukur.
