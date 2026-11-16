# Catatan deviasi prosedur (dicatat apa adanya)

## D1: Gemini 3.8 Flash (Antigravity): sebagian batch diselesaikan sekaligus
- Prosedur di PROMPT_GEMINI.md: berhenti setiap 3 batch dan menunggu "LANJUT".
- Kejadian (keterangan peneliti, 12 November 2026): pilot dan sebagian besar holdout dikerjakan per 3 batch dengan "LANJUT" di chat berikutnya. Menjelang siklus ke-7, peneliti meminta sisa batch (sekitar 11 dari 26 batch holdout) diselesaikan sampai tuntas. Jadi sebagian batch dikerjakan per 3 batch dan sisanya sekaligus.
- Yang terlihat di LOG.txt (waktu penyelesaian per batch): selang antar-batch umumnya 1,2-2,6 menit untuk 20-35 baris; jeda panjang tercatat sebelum pilot_004 (13,5 menit), holdout_004 (8,6), holdout_010 (25,6), dan holdout_016 (5,3); holdout_016 sampai holdout_026 (11 batch) berjalan tanpa jeda panjang. Batas persis antara tahap berhenti dan tahap sekaligus TIDAK dapat dipastikan dari log; yang dilaporkan di sini adalah keterangan peneliti ditambah pola waktu.
- Hasil: 7 batch pilot (140 baris) dan 26 batch holdout (686 baris) lengkap; 0 baris SKIP; 0 pelanggaran format.
- Pemeriksaan penurunan kualitas (pasca-hoc): kecocokan pilihan terbanyak dengan model API pada sepertiga awal, tengah, dan akhir urutan batch holdout adalah 0,93 / 0,93 / 0,95 (Qwen3.8), 0,94 / 0,93 / 0,94 (DeepSeek), 0,94 / 0,88 / 0,93 (Qwen4). Rasio kombinasi probabilitas unik per baris: batch 1-9 = 0,26; 10-15 = 0,16; 16-26 = 0,24. Tidak ada tanda penurunan menuju akhir. Ini bukan bukti bahwa tidak ada penyingkatan; ini pemeriksaan kewajaran.
- Dampak yang mungkin tetap: ingatan lintas batch dalam satu sesi, dan pemeriksaan antara oleh peneliti tidak terjadi pada bagian yang diselesaikan sekaligus.

## D2: glm-5.3 dihentikan sebelum selesai (alasan biaya token)
- glm-5.3 ditambahkan lewat Amandemen 3 dan dijalankan dengan protokol yang sama.
- Pada 12 November 2026 peneliti memutuskan menghentikannya karena pemakaian token sangat besar dan anggaran dihemat untuk pekerjaan validasi.
- Keadaan saat dihentikan (baris keluaran mentah, termasuk percobaan ulang): pilot 146 (selesai), dev 560 (selesai), val 713 (selesai), holdout 594 dari target 686 observasi (TIDAK selesai).
- Keputusan penanganan: glm-5.3 TIDAK dimasukkan ke perbandingan model utama. Holdout glm-5.3 yang parsial TIDAK dianalisis dan TIDAK dipakai untuk klaim apa pun, karena memilih sebagian data setelah melihat hasil bisa menjadi seleksi. Keberadaan dan alasan penghentiannya dilaporkan di laporan (lampiran) agar tidak ada pelaporan selektif.
- Berkas mentah disimpan di HASIL_PENGUJIAN/glm-5.3_DIHENTIKAN/. Keluaran mentah tidak dihapus.

## D3: pilot ikut dalam subset yang dinilai tim dan dalam angka utama (dicatat 15 November 2026, setelah kejadian)
- Praregistrasi menyatakan pilot adalah tahap teknis dan tidak dilaporkan sebagai hasil. Amandemen 5 menetapkan objek penilaian kelayakan sebanyak 40 pernyataan (10 pilot + 30 dev), dan analisis utama tetap memakai seluruh 294 klaim.
- Akibatnya: (a) subset tervalidasi tim (lapis 40, 36, 26, 19) memuat klaim pilot (lapis 36: 9 klaim pilot dan 27 klaim dev); (b) analisis utama UTAMA-294 memasukkan 20 klaim pilot sesuai teks Amandemen 5; (c) varian UTAMA-274 (tanpa pilot) disediakan sebagai pembanding.
- Keputusan pelaporan akhir (apakah angka utama memuat pilot) diserahkan kepada penulis. Selisih nilai titik terbesar antara UTAMA-294 dan UTAMA-274 pada metrik yang dilaporkan adalah 0,0205 (hitungan agen, berkas HASIL_PENGUJIAN/_utama294).
- Sumber: harness/PREREG_DIBEKUKAN.md (bagian Aturan dan Amandemen 5); bahan/v2/hasil_olahan_final/lapis_36_claim_id.txt.

## D4: Penetapan set pelaporan utama 274 klaim non-pilot

Tercatat 16 November 2026, setelah seluruh pengumpulan data selesai.

- Amandemen 5 semula menetapkan 294 klaim (termasuk 20 klaim pilot) sebagai analisis utama.
- Untuk laporan akhir, set pelaporan utama ditetapkan sebagai 274 klaim non-pilot (dev 78, val 98, holdout 98; 1.918 observasi per model), karena praregistrasi menyatakan pilot adalah tahap teknis yang tidak dilaporkan sebagai hasil.
- Set 294 klaim (dengan pilot) tetap dilaporkan sebagai analisis tambahan, bersama kepekaan 290 dan 280 klaim.
- Keputusan ini dibuat setelah data dikumpulkan. Hasil UTAMA-274 dan UTAMA-294 dihitung oleh skrip yang sama dan tersimpan di `results/utama294/`.
