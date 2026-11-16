# 1. Pendahuluan

Model bahasa besar makin sering dipakai untuk menilai apakah bukti mendukung, membantah, atau belum menjawab suatu klaim akademik. Vonis ini memengaruhi apa yang dipercaya pembaca, sehingga kualitasnya berkaitan dengan epistemik AI. Penelitian ini menguji penilaian tiga label, yaitu SUPPORTED, REFUTED, dan NEI (not enough information), pada klaim ilmiah. Ada tiga pertanyaan. Pertama, seberapa baik distribusi probabilitas ketiga label terkalibrasi ketika model hanya membaca abstrak (R1). Kedua, apakah vonis stabil ketika bukti diperdalam ke hasil dan kesimpulan (R2) lalu ke teks relevan penuh (R3). Ketiga, seberapa sering model memberi dukungan palsu (false-support) pada bukti dari artikel lain. Kalibrasi dinilai lewat Brier per jenis bukti, akurasi, dan ECE (Lampiran D, Tabel D6); istilah ini tidak berarti model telah terkalibrasi.

Pertanyaan ketiga penting karena NEI dapat berarti dua hal. Bukti memang belum menjawab klaim, atau bukti tersedia tetapi belum dibaca sampai bagian metodologi dan keterbatasan. Model yang terlalu yakin pada bukti sempit membuat pembaca menerima vonis yang belum diuji, sedangkan model yang menolak memberi vonis kehilangan kegunaannya. Penelitian tentang kejujuran (Ren dkk., 2025), sikofansi (Fanous dkk., 2025; Cheng dkk., 2025), dan pembaruan keyakinan (Kim dkk., 2025) menyentuh sebagian persoalan ini. Dalam pencarian yang terbatas, belum ditemukan karya yang memisahkan tiga label pada klaim akademik dengan tangga bukti yang sama untuk setiap klaim.

Kontribusi penelitian ini adalah sebagai berikut.

1. Desain tangga bukti R1, R2, dan R3 dengan label jangkar mekanis, tujuh bentuk bukti per klaim, dan pengukuran false-support pada bukti yang tidak menjawab klaim.
2. Pengujian 294 klaim dengan tiga model API pada seluruh split, serta pembandingan jalur agen, yaitu GPT-6.1 Sol (tidak terverifikasi), pada subset. Sesi Gemini 3.8 Flash dicatat di repositori, tetapi tidak dianalisis dalam laporan ini.
3. Protokol praregistrasi yang dibekukan sebelum keluaran pertama tercatat, dengan enam amandemen dan pelaporan penyimpangan. Kelayakan butir dinilai oleh tiga penulis hanya untuk 40 dari 294 klaim. Penilaian ini bukan validasi isi oleh panel ahli eksternal.

Penelitian ini tidak menetapkan model terbaik. Label jangkar yang berupa proksi dibahas sebagai keterbatasan utama.
