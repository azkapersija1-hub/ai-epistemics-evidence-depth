"""Tes unit untuk hitung_kelayakan.py (Amandemen 5 dan 6). SEMUA data tiruan di folder sementara (tempfile).

Nilai harapan dihitung TANGAN dan ditulis di komentar. Tes ini TIDAK membaca bahan\\v2\\hasil_ahli\\.
Jalankan: py -3.12 -I -X utf8 bahan/v2/skrip/test_hitung_kelayakan.py
"""
import csv
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hitung_kelayakan as hk  # noqa: E402

L, R, T = "LAYAK", "PERLU_REVISI", "TIDAK_LAYAK"
STAT = {L: "DIPAKAI", R: "DIREVISI", T: "KELUAR"}
PEN = ["budi", "siti", "andi"]


def tulis_rujukan(d):
    with open(os.path.join(d, "lembar_ahli_40.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["butir_no", "claim_id", "claim_original", "claim_altered_draft"])
        for i, cid in enumerate(["T01", "T02", "T03", "T04", "T05", "T06"], 1):
            w.writerow([i, cid, "pernyataan tiruan " + cid, "draf tiruan" if cid == "T05" else ""])
    with open(os.path.join(d, "lembar_ahli_jangkar_30.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pair_id", "claim_original", "ringkasan_bukti_R1"])
        for pid in ["P1", "P2", "P3", "P4"]:
            w.writerow([pid, "pernyataan tiruan", "bukti tiruan"])


def baris(cid, kep="", alasan="", catatan="", jenis="JANGKAR", status=None):
    """Satu baris berkas penilai. status_akhir default sesuai keputusan (bila tidak diberi)."""
    if status is None:
        status = STAT.get(kep, "") if kep else ""
    return {"butir_no": "", "claim_id": cid, "jenis": jenis, "keputusan": kep, "alasan_kode": alasan,
            "catatan": catatan, "anotator": "", "detik": "1", "status_akhir": status}


def tulis_butir(masukan, pen, rows):
    p = os.path.join(masukan, f"kelayakan_butir_{pen}_20261112-0000.csv")
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(hk.HDR_BUTIR)
        for r in rows:
            r = dict(r, anotator=pen)
            w.writerow([r[h] for h in hk.HDR_BUTIR])


def tulis_pasangan(masukan, pen, rows):
    p = os.path.join(masukan, f"pasangan_{pen}_20261112-0000.csv")
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(hk.HDR_PAS)
        for r in rows:
            w.writerow([r["pair_id"], r.get("jawab", ""), r.get("catatan", ""), pen, "1"])


def tulis_diskusi(masukan, rows):
    with open(os.path.join(masukan, "diskusi.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(hk.HDR_DISKUSI)
        for r in rows:
            w.writerow(r)


def baca_status(keluar):
    with open(os.path.join(keluar, "status_butir.csv"), encoding="utf-8-sig", newline="") as f:
        return {(r["claim_id"], r["jenis"]): r for r in csv.DictReader(f)}


def baca_id(path):
    """Kembalikan {'JANGKAR': [...], 'UBAHAN': [...]} dari berkas ID (bagian dipisah oleh baris '# JANGKAR'/'# UBAHAN')."""
    out, bagian = {"JANGKAR": [], "UBAHAN": []}, None
    with open(path, encoding="utf-8") as f:
        for ln in f:
            s = ln.strip()
            if s.startswith("# JANGKAR"):
                bagian = "JANGKAR"
            elif s.startswith("# UBAHAN"):
                bagian = "UBAHAN"
            elif s and not s.startswith("#") and bagian:
                out[bagian].append(s)
    return out


class DasarTes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="tes_kelayakan_")
        self.ref = os.path.join(self.tmp, "rujukan")
        self.mas = os.path.join(self.tmp, "masukan")
        self.kel = os.path.join(self.tmp, "keluar")
        os.makedirs(self.ref)
        os.makedirs(self.mas)
        tulis_rujukan(self.ref)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def jalan(self):
        return hk.hitung(self.mas, self.kel, self.ref)


class TesAturanSuara(DasarTes):
    # Tiga penilai. Mayoritas >=2 sama -> FINAL. Tiga beda -> PERLU_DISKUSI (keputusan kosong).
    KASUS = [
        ((L, L, L), ("FINAL", "DIPAKAI")),
        ((L, L, R), ("FINAL", "DIPAKAI")),
        ((L, L, T), ("FINAL", "DIPAKAI")),
        ((R, R, L), ("FINAL", "DIREVISI")),
        ((R, R, R), ("FINAL", "DIREVISI")),
        ((R, R, T), ("FINAL", "DIREVISI")),
        ((T, T, L), ("FINAL", "KELUAR")),
        ((T, T, R), ("FINAL", "KELUAR")),
        ((T, T, T), ("FINAL", "KELUAR")),
        ((L, R, T), ("PERLU_DISKUSI", "")),
    ]

    def test_semua_kombinasi_tiga_penilai(self):
        for suara, harap in self.KASUS:
            with self.subTest(suara=suara):
                tmp = tempfile.mkdtemp(prefix="kasus_")
                try:
                    mas = os.path.join(tmp, "m")
                    os.makedirs(mas)
                    for pen, k in zip(PEN, suara):
                        tulis_butir(mas, pen, [baris("T01", k, alasan=("AMBIGU" if k == R else "BUKTI_DERAU" if k == T else ""),
                                                      catatan=("ubah" if k == R else ""))])
                    kode, pesan = hk.hitung(mas, os.path.join(tmp, "k"), self.ref)
                    self.assertEqual(kode, 0, pesan)
                    st = baca_status(os.path.join(tmp, "k"))[("T01", "JANGKAR")]
                    self.assertEqual((st["status"], st["keputusan_akhir"]), harap)
                    self.assertEqual(st["n_penilai"], "3")
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)

    def test_satu_penilai_sementara(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        self.assertEqual(self.jalan()[0], 0)
        st = baca_status(self.kel)[("T01", "JANGKAR")]
        self.assertEqual((st["n_penilai"], st["status"], st["keputusan_akhir"]), ("1", "SEMENTARA", "DIPAKAI"))

    def test_dua_penilai_sama_dan_beda(self):
        # T01: budi LAYAK, siti LAYAK -> SEMENTARA, DIPAKAI.
        # T02: budi LAYAK, siti PERLU_REVISI -> PERLU_PENILAI_KETIGA, keputusan kosong.
        tulis_butir(self.mas, "budi", [baris("T01", L), baris("T02", L)])
        tulis_butir(self.mas, "siti", [baris("T01", L), baris("T02", R, catatan="perjelas")])
        self.assertEqual(self.jalan()[0], 0)
        s = baca_status(self.kel)
        self.assertEqual((s[("T01", "JANGKAR")]["status"], s[("T01", "JANGKAR")]["keputusan_akhir"]), ("SEMENTARA", "DIPAKAI"))
        self.assertEqual((s[("T02", "JANGKAR")]["status"], s[("T02", "JANGKAR")]["keputusan_akhir"]), ("PERLU_PENILAI_KETIGA", ""))

    def test_butir_kosong_bukan_suara(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        tulis_butir(self.mas, "siti", [baris("T01", "")])
        self.assertEqual(self.jalan()[0], 0)
        st = baca_status(self.kel)[("T01", "JANGKAR")]
        self.assertEqual((st["n_penilai"], st["status"]), ("1", "SEMENTARA"))

    def test_butir_tanpa_penilai_belum_dinilai(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        self.assertEqual(self.jalan()[0], 0)
        st = baca_status(self.kel)[("T04", "JANGKAR")]
        self.assertEqual((st["n_penilai"], st["status"], st["keputusan_akhir"]), ("0", "BELUM_DINILAI", ""))


class TesDaftarKeluar(DasarTes):
    """Skenario tiga penilai dengan hasil dihitung tangan (lihat komentar)."""

    def siapkan(self):
        # JANGKAR:
        #   T01: budi, siti, andi = TIDAK_LAYAK x3       -> FINAL, KELUAR        -> ID_KELUAR, KETAT
        #   T02: budi L, siti R, andi T                  -> PERLU_DISKUSI        -> bukan ID_KELUAR; KETAT (ada T)
        #   T03: budi TIDAK_LAYAK saja                   -> SEMENTARA, KELUAR    -> ID_KELUAR_SEMENTARA; KETAT
        #   T04: budi L, siti R                          -> PERLU_PENILAI_KETIGA -> bukan ID_KELUAR; bukan KETAT
        #   T05: budi, siti, andi = LAYAK x3             -> FINAL, DIPAKAI       -> tidak masuk daftar keluar
        # UBAHAN (draf T05):
        #   T05: budi, siti, andi = TIDAK_LAYAK x3       -> FINAL, KELUAR        -> ID_KELUAR (bagian UBAHAN), KETAT
        tulis_butir(self.mas, "budi", [
            baris("T01", T, alasan="BUKAN_TEMUAN"), baris("T02", L), baris("T03", T, alasan="BUKTI_DERAU"),
            baris("T04", L), baris("T05", L),
            baris("T01", "", jenis="UBAHAN"),
            baris("T05", T, alasan="BUKAN_TEMUAN", jenis="UBAHAN")])
        tulis_butir(self.mas, "siti", [
            baris("T01", T, alasan="BUKTI_TERPOTONG"), baris("T02", R, catatan="ubah"),
            baris("T04", R, catatan="ubah"), baris("T05", L),
            baris("T05", T, alasan="BUKAN_TEMUAN", jenis="UBAHAN")])
        tulis_butir(self.mas, "andi", [
            baris("T01", T, alasan="BUKAN_TEMUAN"), baris("T02", T, alasan="BUKAN_TEMUAN"),
            baris("T05", L),
            baris("T05", T, alasan="BUKAN_TEMUAN", jenis="UBAHAN")])

    def test_tiga_berkas_id_keluar_sesuai_aturan(self):
        self.siapkan()
        self.assertEqual(self.jalan()[0], 0)
        s = baca_status(self.kel)
        self.assertEqual((s[("T01", "JANGKAR")]["status"], s[("T01", "JANGKAR")]["keputusan_akhir"]), ("FINAL", "KELUAR"))
        self.assertEqual((s[("T02", "JANGKAR")]["status"], s[("T02", "JANGKAR")]["keputusan_akhir"]), ("PERLU_DISKUSI", ""))
        self.assertEqual((s[("T03", "JANGKAR")]["status"], s[("T03", "JANGKAR")]["keputusan_akhir"]), ("SEMENTARA", "KELUAR"))
        self.assertEqual((s[("T04", "JANGKAR")]["status"], s[("T04", "JANGKAR")]["keputusan_akhir"]), ("PERLU_PENILAI_KETIGA", ""))
        self.assertEqual((s[("T05", "JANGKAR")]["status"], s[("T05", "JANGKAR")]["keputusan_akhir"]), ("FINAL", "DIPAKAI"))
        self.assertEqual((s[("T05", "UBAHAN")]["status"], s[("T05", "UBAHAN")]["keputusan_akhir"]), ("FINAL", "KELUAR"))

        utama = baca_id(os.path.join(self.kel, "ID_KELUAR.txt"))
        self.assertEqual(utama, {"JANGKAR": ["T01"], "UBAHAN": ["T05"]})
        sementara = baca_id(os.path.join(self.kel, "ID_KELUAR_SEMENTARA.txt"))
        self.assertEqual(sementara, {"JANGKAR": ["T03"], "UBAHAN": []})
        ketat = baca_id(os.path.join(self.kel, "ID_KELUAR_KETAT.txt"))
        # T02 dan T03 punya suara TIDAK_LAYAK; T01 juga; T05 ubahan juga. T04 tidak punya suara TIDAK_LAYAK.
        self.assertEqual(ketat, {"JANGKAR": ["T01", "T02", "T03"], "UBAHAN": ["T05"]})

    def test_diskusi_menimpa_dan_masuk_id_keluar(self):
        self.siapkan()
        # Diskusi memutuskan T02 (PERLU_DISKUSI) menjadi KELUAR; status DISKUSI.
        tulis_diskusi(self.mas, [["T02", "JANGKAR", "KELUAR", "dibahas bersama, bukti tidak relevan"]])
        self.assertEqual(self.jalan()[0], 0)
        s = baca_status(self.kel)
        self.assertEqual((s[("T02", "JANGKAR")]["status"], s[("T02", "JANGKAR")]["keputusan_akhir"]), ("DISKUSI", "KELUAR"))
        self.assertIn("[diskusi] dibahas bersama", s[("T02", "JANGKAR")]["catatan_gabungan"])
        utama = baca_id(os.path.join(self.kel, "ID_KELUAR.txt"))
        self.assertEqual(utama["JANGKAR"], ["T01", "T02"])
        ketat = baca_id(os.path.join(self.kel, "ID_KELUAR_KETAT.txt"))
        self.assertEqual(ketat["JANGKAR"], ["T01", "T02", "T03"], "diskusi tidak mengubah daftar KETAT")


class TesCatatanHilang(DasarTes):
    def test_catatan_hilang_tidak_menghentikan_dan_jadi_peringatan(self):
        # budi PERLU_REVISI tanpa catatan; siti PERLU_REVISI dengan catatan; andi PERLU_REVISI dengan catatan
        # -> 3 suara PERLU_REVISI -> FINAL DIREVISI. Tetap dihitung. Ditandai CATATAN_HILANG.
        tulis_butir(self.mas, "budi", [baris("T06", R, catatan="")])
        tulis_butir(self.mas, "siti", [baris("T06", R, catatan="ganti kata")])
        tulis_butir(self.mas, "andi", [baris("T06", R, catatan="perjelas angka")])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 0)
        st = baca_status(self.kel)[("T06", "JANGKAR")]
        self.assertEqual((st["status"], st["keputusan_akhir"]), ("FINAL", "DIREVISI"))
        self.assertIn("CATATAN_HILANG", st["catatan_gabungan"])
        self.assertTrue(any("PERLU_REVISI tanpa catatan" in p for p in pesan))
        with open(os.path.join(self.kel, "RINGKASAN_KELAYAKAN.md"), encoding="utf-8") as f:
            ring = f.read()
        self.assertIn("## Catatan hilang", ring)
        self.assertIn("T06 (JANGKAR)", ring)

    def test_tidak_layak_tanpa_alasan_tetap_dihitung(self):
        tulis_butir(self.mas, "budi", [baris("T06", T, alasan="")])
        tulis_butir(self.mas, "siti", [baris("T06", T, alasan="BUKAN_TEMUAN")])
        self.assertEqual(self.jalan()[0], 0)
        st = baca_status(self.kel)[("T06", "JANGKAR")]
        self.assertEqual((st["n_penilai"], st["status"], st["keputusan_akhir"]), ("2", "SEMENTARA", "KELUAR"))
        self.assertIn("CATATAN_HILANG", st["catatan_gabungan"])


class TesDiskusiValidasi(DasarTes):
    def test_diskusi_claim_tak_dikenal_galat(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        tulis_diskusi(self.mas, [["T99", "JANGKAR", "KELUAR", ""]])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("T99" in p and "tidak dikenal" in p for p in pesan))
        self.assertFalse(os.path.exists(self.kel))

    def test_diskusi_keputusan_final_tak_sah_galat(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        tulis_diskusi(self.mas, [["T01", "JANGKAR", "LAYAK", ""]])  # harus DIPAKAI/DIREVISI/KELUAR
        self.assertEqual(self.jalan()[0], 2)

    def test_diskusi_ganda_galat(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        tulis_diskusi(self.mas, [["T01", "JANGKAR", "DIPAKAI", ""], ["T01", "JANGKAR", "KELUAR", ""]])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("dua kali" in p for p in pesan))

    def test_diskusi_ubahan_untuk_butir_tanpa_draf_galat(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        tulis_diskusi(self.mas, [["T01", "UBAHAN", "KELUAR", ""]])
        self.assertEqual(self.jalan()[0], 2)

    def test_diskusi_kolom_salah_galat(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        with open(os.path.join(self.mas, "diskusi.csv"), "w", encoding="utf-8-sig", newline="") as f:
            f.write("claim_id,jenis,keputusan\nT01,JANGKAR,KELUAR\n")
        self.assertEqual(self.jalan()[0], 2)

    def test_tanpa_diskusi_berkas_diabaikan(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 0)
        self.assertIn("diskusi.csv: tidak ada", pesan)


class TesValidasiIntegritas(DasarTes):
    def test_nilai_tak_sah_ditolak(self):
        tulis_butir(self.mas, "budi", [baris("T01", "MUNGKIN")])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("tidak sah" in p for p in pesan))
        self.assertFalse(os.path.exists(self.kel), "tidak boleh ada keluaran bila ada galat integritas")

    def test_claim_id_tak_dikenal_ditolak(self):
        tulis_butir(self.mas, "budi", [baris("T99", L)])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("T99" in p and "tidak dikenal" in p for p in pesan))

    def test_baris_ganda_satu_penilai_ditolak(self):
        tulis_butir(self.mas, "budi", [baris("T01", L), baris("T01", T, alasan="BUKTI_DERAU")])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("baris ganda" in p for p in pesan))

    def test_ubahan_hanya_untuk_butir_yang_punya_draf(self):
        tulis_butir(self.mas, "budi", [baris("T01", L, jenis="UBAHAN")])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("draf ubahan" in p for p in pesan))

    def test_status_akhir_tidak_cocok_ditolak(self):
        tulis_butir(self.mas, "budi", [baris("T01", L, status="KELUAR")])
        self.assertEqual(self.jalan()[0], 2)

    def test_pasangan_jawaban_dan_id_tak_sah(self):
        tulis_pasangan(self.mas, "budi", [{"pair_id": "P1", "jawab": "MUNGKIN"}])
        self.assertEqual(self.jalan()[0], 2)
        tulis_pasangan(self.mas, "budi", [{"pair_id": "P9", "jawab": "RAGU"}])
        self.assertEqual(self.jalan()[0], 2)

    def test_folder_keluar_tidak_boleh_di_dalam_masukan(self):
        tulis_butir(self.mas, "budi", [baris("T01", L)])
        kode, _ = hk.hitung(self.mas, os.path.join(self.mas, "keluar"), self.ref)
        self.assertEqual(kode, 1)


class TesDiskusiStatus(DasarTes):
    """diskusi.csv hanya boleh menimpa butir PERLU_DISKUSI (keputusan pengguna, Amandemen 6)."""

    def _suara_tiga(self, cid, kep_per_pen):
        for pen, k in zip(PEN, kep_per_pen):
            if k is None:
                continue
            tulis_butir(self.mas, pen, [baris(cid, k, alasan=("BUKAN_TEMUAN" if k == T else ""), catatan=("ubah" if k == R else ""))])

    def test_a_diskusi_untuk_perlu_diskusi_diterima_dan_menimpa(self):
        self._suara_tiga("T02", [L, R, T])          # tiga suara berbeda -> PERLU_DISKUSI
        tulis_diskusi(self.mas, [["T02", "JANGKAR", "DIPAKAI", "dibahas, bukti relevan"]])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 0, pesan)
        st = baca_status(self.kel)[("T02", "JANGKAR")]
        self.assertEqual((st["status"], st["keputusan_akhir"]), ("DISKUSI", "DIPAKAI"))

    def test_b_diskusi_untuk_butir_final_ditolak(self):
        self._suara_tiga("T01", [L, L, L])          # FINAL DIPAKAI
        tulis_diskusi(self.mas, [["T01", "JANGKAR", "KELUAR", "coba balik"]])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("T01" in p and "berstatus FINAL" in p for p in pesan), pesan)
        self.assertFalse(os.path.exists(self.kel))

    def test_c_diskusi_untuk_butir_sementara_ditolak(self):
        self._suara_tiga("T03", [T, None, None])    # satu penilai -> SEMENTARA
        tulis_diskusi(self.mas, [["T03", "JANGKAR", "DIPAKAI", ""]])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("T03" in p and "berstatus SEMENTARA" in p for p in pesan), pesan)
        self.assertFalse(os.path.exists(self.kel))

    def test_d_diskusi_untuk_perlu_penilai_ketiga_ditolak(self):
        self._suara_tiga("T04", [L, R, None])       # dua penilai beda -> PERLU_PENILAI_KETIGA
        tulis_diskusi(self.mas, [["T04", "JANGKAR", "DIREVISI", ""]])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("T04" in p and "berstatus PERLU_PENILAI_KETIGA" in p for p in pesan), pesan)
        self.assertFalse(os.path.exists(self.kel))

    def test_e_diskusi_untuk_butir_belum_dinilai_ditolak(self):
        tulis_butir(self.mas, "budi", [baris("T05", L)])   # ada penilai lain untuk berkas, tetapi T06 kosong
        tulis_diskusi(self.mas, [["T06", "JANGKAR", "KELUAR", ""]])
        kode, pesan = self.jalan()
        self.assertEqual(kode, 2)
        self.assertTrue(any("T06" in p and "BELUM_DINILAI" in p for p in pesan), pesan)


class TesKesepakatan(unittest.TestCase):
    def test_cohen_kappa_hitung_tangan(self):
        # xs = L L R T ; ys = L R R T. po = 3/4 = 0.75.
        # px: L=2/4 R=1/4 T=1/4 ; py: L=1/4 R=2/4 T=1/4
        # pe = 2/16 + 2/16 + 1/16 = 5/16 = 0.3125
        # kappa = (0.75 - 0.3125) / (1 - 0.3125) = 0.4375 / 0.6875 = 7/11
        po, kap = hk.cohen([L, L, R, T], [L, R, R, T], hk.KEP)
        self.assertAlmostEqual(po, 0.75)
        self.assertAlmostEqual(kap, 7 / 11, places=9)

    def test_fleiss_kappa_hitung_tangan(self):
        # Tabel per item (jumlah kategori A, B): [3,0], [2,1], [0,3]; n = 3.
        # P_i = (sum n_ij^2 - n)/(n(n-1)): (9-3)/6 = 1 ; (4+1-3)/6 = 1/3 ; (9-3)/6 = 1
        # P_bar = (1 + 1/3 + 1)/3 = 7/9
        # p_A = (3+2+0)/9 = 5/9 ; p_B = (0+1+3)/9 = 4/9 ; P_e = 25/81 + 16/81 = 41/81
        # kappa = (7/9 - 41/81) / (1 - 41/81) = (22/81) / (40/81) = 0.55
        self.assertAlmostEqual(hk.fleiss([[3, 0], [2, 1], [0, 3]], 3), 0.55, places=9)

    def test_kappa_tidak_terdefinisi_saat_satu_kategori(self):
        po, kap = hk.cohen([L, L, L], [L, L, L], hk.KEP)
        self.assertEqual((po, kap), (1.0, None))

    def test_kesepakatan_terpisah_jangkar_dan_ubahan(self):
        # JANGKAR (a,b): T1 L/L sama; T2 L/R beda; T3 R/R sama; T4 T/T sama.
        #   persen = 3/4 = 0.75 ; kappa Cohen = 7/11 (lihat tes di atas).
        # UBAHAN (a,b): U1 T/L beda; U2 T/T sama.
        #   persen = 1/2 = 0.5 ; xs = T,T ; ys = L,T ; px T=1 ; py L=0.5,T=0.5
        #   pe = 1*0.5 = 0.5 ; kappa = (0.5-0.5)/(1-0.5) = 0.0
        # GABUNGAN: perbandingan pasangan penilai per item = 4 item jangkar (1 pasangan tiap item) + 2 item ubahan = 6
        #   sepakat = 3 (jangkar) + 1 (ubahan) = 4 -> persen gabungan = 4/6 = 0.6667
        jk = {("T1", "JANGKAR"): {"a": L, "b": L}, ("T2", "JANGKAR"): {"a": L, "b": R},
              ("T3", "JANGKAR"): {"a": R, "b": R}, ("T4", "JANGKAR"): {"a": T, "b": T}}
        ub = {("U1", "UBAHAN"): {"a": T, "b": L}, ("U2", "UBAHAN"): {"a": T, "b": T}}
        h_jk = hk.analisis_sepakat(jk, hk.KEP, ["a", "b"])
        h_ub = hk.analisis_sepakat(ub, hk.KEP, ["a", "b"])
        h_gab = hk.analisis_sepakat({**jk, **ub}, hk.KEP, ["a", "b"])
        self.assertAlmostEqual(h_jk["keseluruhan"], 0.75)
        self.assertAlmostEqual(h_jk["pasangan"][0]["kappa"], 7 / 11, places=9)
        self.assertAlmostEqual(h_ub["keseluruhan"], 0.5)
        self.assertAlmostEqual(h_ub["pasangan"][0]["kappa"], 0.0, places=9)
        self.assertAlmostEqual(h_gab["keseluruhan"], 4 / 6)
        self.assertEqual(h_gab["n_banding"], 6)

    def test_putus_satu_suara_dan_kosong(self):
        self.assertEqual(hk.putus([("a", L)]), ("SEMENTARA", "DIPAKAI"))
        self.assertEqual(hk.putus([]), ("BELUM_DINILAI", ""))
        self.assertEqual(hk.putus([("a", L), ("b", T), ("c", R)]), ("PERLU_DISKUSI", ""))
        self.assertEqual(hk.putus([("a", L), ("b", T), ("c", R)], {"keputusan_final": "KELUAR"}), ("DISKUSI", "KELUAR"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
