# Harness pengujian (Agen 2, v2): AI x Epistemics, Fase 2-PERSIAPAN

Tanggal: 2026-11-11. Ini harness, bukan eksperimen. Semua perintah di bawah ini dijalankan
dari folder `D:\kerjaan baru\AI_EPISTEMICS_2026_PHASE_2_PREP`.

Status saat ini: TIDAK ADA panggilan model nyata yang dijalankan. Tes memakai modul palsu.
Adapter nyata `ProfilProvider` sudah ditulis, tetapi TERKUNCI oleh gerbang ganda dan
belum dijalankan terhadap model mana pun.

## 1. Tes (tanpa jaringan, tanpa model)

```
py -3.12 -I -X utf8 -m unittest discover -s harness/tests -v
```
Hasil terakhir: lihat `harness/log/tes_v2.txt`.

## 2. Fixture tiruan (FIKTIF)

```
py -3.12 -I -X utf8 harness/fixture_tiruan/buat_fixture.py
```
Hasil: 294 observasi = 42 klaim x 7 (own R1, R2, R3; near R1, R3; far R1, R3).
Label jangkar tiruan: own R3 = SUPPORTED; near dan far = NEI; own R1 dan R2 = null.

## 3. Uji pipeline dengan mock (SIMULASI, BUKAN HASIL MODEL)

```
py -3.12 -I -X utf8 harness/jalankan_uji_pipeline.py
```
Keluaran: `harness/log/laporan_uji_pipeline.md` (header SIMULASI) dan
`harness/log/keluaran_mentah_<mode>.jsonl`. Mode: konservatif, terlalu_yakin, acak, rusak,
overkomit_r1.

## 4. Provider nyata per split (TERKUNCI; JANGAN dijalankan tanpa persetujuan peneliti)

Gerbang ganda: flag `--izinkan-panggilan-nyata` DAN variabel lingkungan `EPIS_ALLOW_REAL_CALLS=1`.
Tanpa keduanya skrip berhenti dengan kode 3 dan tidak menulis apa pun. Kunci API tidak pernah
dicetak atau ditulis di harness; model_api di sakti_core yang mengurusnya.

Urutan wajib: pilot (teknis) -> dev -> val -> holdout SEKALI.

Pilot teknis (kecil; mis. 5 observasi):
```
$env:EPIS_ALLOW_REAL_CALLS = "1"
py -3.12 -I -X utf8 harness/jalankan_provider_nyata.py --split pilot --model qwen3.8-flash --limit 5 --workers 1 --izinkan-panggilan-nyata
```

Dev (semua observasi split dev):
```
$env:EPIS_ALLOW_REAL_CALLS = "1"
py -3.12 -I -X utf8 harness/jalankan_provider_nyata.py --split dev --model qwen3.8-flash --workers 1 --izinkan-panggilan-nyata
```

Val (semua observasi split val):
```
$env:EPIS_ALLOW_REAL_CALLS = "1"
py -3.12 -I -X utf8 harness/jalankan_provider_nyata.py --split val --model qwen3.8-flash --workers 1 --izinkan-panggilan-nyata
```

Holdout (SEKALI; wajib konfirmasi; menolak bila keluaran sudah ada):
```
$env:EPIS_ALLOW_REAL_CALLS = "1"
py -3.12 -I -X utf8 harness/jalankan_provider_nyata.py --split holdout --model qwen3.8-flash --workers 1 --izinkan-panggilan-nyata --konfirmasi-holdout-sekali
```

Stabilitas (ulangan 2 dan 3 pada subset; ganti --ulangan dan --limit sesuai PREREG):
```
$env:EPIS_ALLOW_REAL_CALLS = "1"
py -3.12 -I -X utf8 harness/jalankan_provider_nyata.py --split dev --model qwen3.8-flash --ulangan 2 --limit 30 --izinkan-panggilan-nyata
```

Model kedua (deepseek-v4.1-flash) memakai perintah yang sama dengan `--model deepseek-v4.1-flash`.
Flag `--workers` default 1. Nilai lebih dari 1 hanya setelah pilot sukses.
Runner melakukan resume: menjalankan ulang perintah yang sama melewati observasi yang sudah ada
(kecuali holdout, yang ditolak bila keluaran sudah ada).

## 5. Analisis

Analisis keluaran per split dan provider. Header otomatis: SIMULASI bila semua mock,
HASIL MODEL (BELUM DIVERIFIKASI) bila ada provider nyata.
```
py -3.12 -I -X utf8 harness/analisis_keluaran.py --split pilot --keluaran harness/log/nyata_pilot_qwen3.8-flash_u1.jsonl --items harness/log/items_pilot_qwen3.8-flash.jsonl --out harness/log/analisis_pilot.md
py -3.12 -I -X utf8 harness/analisis_keluaran.py --split dev --keluaran harness/log/nyata_dev_qwen3.8-flash_u1.jsonl --items harness/log/items_dev_qwen3.8-flash.jsonl --out harness/log/analisis_dev.md
py -3.12 -I -X utf8 harness/analisis_keluaran.py --split holdout --keluaran harness/log/nyata_holdout_qwen3.8-flash_u1.jsonl --items harness/log/items_holdout_qwen3.8-flash.jsonl --out harness/log/analisis_holdout.md
```
Catatan: `--items` harus berkas subset split yang ditulis `jalankan_provider_nyata.py`
(`harness/log/items_<split>_<model>.jsonl`). Keduanya tidak memuat kolom kunci.

## 6. Verifikasi silang Brier

Dilakukan dengan `agent_b_calc.py` (lihat `harness/log/verifikasi_silang.txt` dan
`harness/log/verifikasi_n_harness.txt`).

## 7. Struktur folder

```
harness/
  epis/
    skor.py              Brier, akurasi, ECE, AURC, NEI; ringkas_berlabel (label null dikecualikan)
    parse.py             objek JSON TERAKHIR yang memuat label; normalisasi; dua batas Brier
    stats.py             bootstrap klaster; bootstrap selisih klaster; Holm; n_sampel; DEFF; daya
    bocor.py             uji kebocoran (a)-(d); kolom v2 terlarang
    konsistensi.py       sesuai, pergeseran, overkomit, false-support near/far, per bahasa
    prompt.py            pembangun prompt; hash sha256 templat
    provider.py          Provider (antarmuka) dan MockProvider (5 mode)
    provider_profil.py   ProfilProvider TERKUNCI ke model_api.api_chat (gerbang ganda)
    runner.py            resume, konkurensi, retry backoff, keluaran mentah JSONL
    subset.py            pilih items per split (tanpa kolom kunci)
    laporan.py           skor berjangkar, konsistensi, per bahasa
    laporan_teks.py      Markdown; header SIMULASI atau HASIL MODEL
    jsonl_io.py          baca/tulis JSONL
  prompt_templates/prompt_v1.txt
  fixture_tiruan/        buat_fixture.py; items_model.jsonl; kunci.jsonl (FIKTIF)
  tests/                 unittest (9 berkas + tes baru)
  log/                   keluaran nyata perintah di atas
  jalankan_uji_pipeline.py     uji pipeline mock
  jalankan_provider_nyata.py   provider nyata terkunci per split
  analisis_keluaran.py         analisis per provider dan ulangan
  PREREG_TEMPLATE.md           templat praregistrasi (kosong; bagian jangkar, tau, model, urutan)
  LAPORAN_AGEN_2.md            laporan v1
  LAPORAN_AGEN_2_V2.md         laporan v2 (jujur; ini versi terbaru)
```

## 8. Skema berkas (kontrak v2)

`items_model.jsonl` (satu-satunya yang boleh dikirim ke model):
`{obs_id, claim_id, rung, lang, claim_text, evidence_text}`.

`kunci.jsonl` (rahasia; tidak pernah dibaca runner):
`{obs_id, claim_id, article_id, evidence_article_id, split, pair_type, rung, label, label_type, anchor_note, risiko_jangkar}`
dengan `label` = SUPPORTED | REFUTED | NEI | null dan `label_type` = anchor | expert | none.

Keluaran mentah: `obs_id, provider_id, model_id_diminta, prompt_hash, order, ulangan, percobaan, raw, waktu, latensi_s, panjang_keluaran, parse_ok, normalized, p, parse_error, panggilan_error`.

## 9. Aturan yang ditegakkan kode

- Runner menerima hanya MockProvider atau ProfilProvider. Lainnya ditolak.
- ProfilProvider menolak konstruksi tanpa `--izinkan-panggilan-nyata` DAN `EPIS_ALLOW_REAL_CALLS=1`.
- model_api dimuat malas dan folder sakti_core hanya masuk sys.path selama impor.
- Runner menolak items yang memuat kolom kunci (termasuk kolom v2).
- Prompt tidak memuat obs_id, rung, label, atau metadata.
- Laporan mock diberi header SIMULASI; laporan model diberi header HASIL MODEL.
- Holdout: wajib konfirmasi, dan menolak bila keluaran sudah ada.

## 10. Yang BELUM ada (daftar jujur)

1. Model nyata belum dijalankan. Belum ada satu pun keluaran dari model.
2. Temperature 0 TIDAK bisa diatur: `api_chat` tidak punya parameter temperature dan tidak
   mengirimkannya. Thinking juga tidak bisa diatur. Lihat PREREG bagian 11d.
3. Akses, kuota, dan ID tepat model di penyedia belum diverifikasi.
4. `api_chat` punya `konten` yang default-nya True di adapter. model_api sendiri bisa menolak
   sampai peneliti memutuskan (`_izin`). Belum diuji karena tidak ada panggilan.
5. Butir nyata dan label ahli: tidak ada. Fixture FIKTIF.
6. Pilot untuk sigma, ICC, dan kappa: belum ada.
7. Kondisi B, C, D (intervensi F11x, plasebo) dan Latin square penuh: belum diimplementasi.
8. Mock tidak membedakan near dan far (hanya membaca penanda prompt). Selisih near-far pada mock = 0.
9. Tinjauan kode oleh subagen ECC belum dijalankan.

## 11. Pertanyaan keputusan untuk peneliti

1. Model dan ID persis di penyedia untuk qwen3.8-flash dan deepseek-v4.1-flash.
2. Temperature 0: terima temperature default penyedia (dicatat), atau ubah model_api atas persetujuan?
3. Setujui `konten=True` sebagai default dan siapa yang memutuskan kapan model_api mengizinkannya?
4. Setujui tau = 0,7 sebagai beku, atau ganti sebelum dev dibuka?
5. Setujui urutan pilot -> dev -> val -> holdout SEKALI, dan ukuran subset stabilitas?
