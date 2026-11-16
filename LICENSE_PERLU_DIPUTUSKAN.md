# Lisensi: BELUM DIPUTUSKAN

Berkas ini hanya memaparkan pilihan. Agen restrukturisasi TIDAK memilih lisensi. Keputusan ada pada penulis.

Repositori ini memuat tiga jenis isi yang sebaiknya diberi aturan berbeda.

## 1. Kode (`src/`)

| Lisensi | Ringkas | Catatan |
|---|---|---|
| MIT | Izin luas, syarat hanya pencantuman hak cipta | Sederhana, banyak dipakai |
| Apache-2.0 | Izin luas, ada klausul hak paten | Lebih rinci tentang paten |
| GPL-3.0 | Turunan wajib memakai lisensi yang sama | Membatasi penggunaan dalam produk tertutup |

## 2. Dokumen dan gambar (`docs/`, `gambar/`, `video/`, `referensi/`)

| Lisensi | Ringkas | Catatan |
|---|---|---|
| CC BY 4.0 | Boleh dipakai dengan pencantuman | Umum untuk dokumen riset |
| CC BY-SA 4.0 | Turunan wajib lisensi serupa | |
| Tanpa lisensi terbuka | Hak cipta penuh pada penulis | Pilihan bila belum ingin dibagikan ulang |

Catatan: `referensi/` memuat catatan verifikasi sumber. Sumber pustaka itu sendiri tetap milik penerbitnya.

## 3. Data dan keluaran model (`data/`, `hasil/`, `sesi_luar/`)

Hal yang perlu ditelaah sebelum memilih:

- Keluaran model berasal dari penyedia API (qwen, deepseek, Gemini melalui Antigravity, GPT-6.1 Sol melalui Codex). Ketentuan penggunaan penyedia dapat membatasi redistribusi keluaran. Telaah ketentuan masing-masing penyedia.
- Ringkasan penilaian kelayakan berasal dari tim penulis. Pertimbangkan apakah ringkasan itu boleh dibagikan.
- Teks klaim dan bukti dari artikel TIDAK ada di repositori ini. Hak cipta artikel tetap berlaku bagi sumbernya.

## Pilihan yang harus diputuskan penulis

1. Lisensi untuk `src/` (MIT, Apache-2.0, GPL-3.0, atau lainnya).
2. Lisensi untuk dokumen dan gambar (CC BY 4.0, CC BY-SA 4.0, atau tanpa lisensi terbuka).
3. Apakah `data/` dan `hasil/` dibagikan dengan lisensi tertentu atau ditahan.
4. Setelah keputusan, tambahkan berkas `LICENSE` di akar repositori dan perbarui `CITATION.cff`.
