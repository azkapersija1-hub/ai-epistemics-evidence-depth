# 5. Diskusi dan Keterbatasan

## 5.1 Arti hasil

Pada analisis utama, proporsi klaim dengan label R1 sama dengan label R3 berada pada rentang 0,4896 sampai 0,5306. Sekitar separuh klaim berubah label ketika bukti diperdalam dari abstrak ke teks penuh. Perubahan ini tidak menunjukkan vonis mana yang benar, sehingga laporan vonis LLM perlu menyebut kedalaman bukti yang dipakai. Pola false-support near R3 (0,2198 pada qwen4-max-preview) hanya dapat dibaca setelah pasangan near dan far divalidasi. Hasil ini tidak memberi peringkat model.

## 5.2 Implikasi untuk keselamatan

Brier own R3 deepseek-v4.1-flash yang paling besar (0,0919) belum dapat dibaca sebagai kelemahan model. Pembacaan itu perlu diuji dengan jangkar yang divalidasi ahli. Standar evaluasi juga perlu menyatakan lapis klaim yang dipakai, karena kestabilan vonis dapat tampak berubah hanya karena pemilihan klaim.

[PENULIS MENGISI: posisikan temuan terhadap kajian terkait dengan rujukan dari referensi_terverifikasi.csv.]

## 5.3 Keterbatasan utama

1. **Validasi kecil.** Hanya 40 dari 294 klaim yang dinilai kelayakannya oleh tim, dan subset tervalidasi memuat 36 klaim.
2. **Kunci mekanis.** Label own R3 SUPPORTED dan near serta far NEI bukan penilaian ahli. REFUTED tidak memiliki jangkar.
3. **Penilai mengetahui hipotesis.** Tiga penulis menilai kelayakan, dengan persen sepakat 61,7 persen dan kappa Fleiss -0,025 (n = 40). Validitas isi belum terbukti secara independen.
4. **Jangkar NEI belum tervalidasi.** Dua versi penilaian pasangan near tidak sejalan: kesepakatan tim mencatat 30 pasangan membahas klaim, sedangkan pemeriksaan agen menilai 22 dari 30 tidak membahas klaim. [PENULIS MEMUTUSKAN: versi mana yang menjadi dasar label NEI.]
5. **Jalur agen tidak terverifikasi.** GPT-6.1 Sol (tidak terverifikasi) diuji pada 40 klaim, dengan 39 klaim efektif, sebagai pembanding jalur agen.
6. **Pilot dan holdout.** Pilot ikut dalam angka 294. Holdout dijalankan sekali pada tiga model API. Holdout tidak murni konfirmatori bagi semua model, karena Amandemen 2 dan 3 menambah model setelah hasil holdout model lain dilihat (Lampiran E, butir 9). [PENULIS MEMASTIKAN: pelaksanaan itu belum diverifikasi dari log.]
7. **Setelan model.** Suhu dan mode berpikir tidak dapat diatur, dan qwen4-max-preview adalah model pratinjau.

Keterbatasan lengkap ada di Lampiran B dan Lampiran C. Daftar rinci juga tersedia di Lampiran E.

## 5.4 Penelitian lanjutan

Penelitian lanjutan perlu mencakup validasi butir oleh panel ahli eksternal, validasi independen pasangan near dan far, jumlah klaim yang lebih besar agar selisih antar model dapat diuji, serta pengaturan suhu dan mode berpikir bila penyedia mendukungnya.
