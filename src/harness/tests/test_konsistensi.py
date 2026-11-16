"""Tes konsistensi.py (kesesuaian, pergeseran, overkomit, false-support mass).

Nilai harapan dihitung TANGAN di komentar. Tidak ada pemanggilan fungsi sebagai pembanding.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epis import konsistensi  # noqa: E402


def rec(claim, article, pair, rung, p, label=None, lang="id"):
    return {"claim_id": claim, "article_id": article, "pair_type": pair, "rung": rung,
            "lang": lang, "label": label, "ok": p is not None,
            "p": None if p is None else {"SUPPORTED": p[0], "REFUTED": p[1], "NEI": p[2]}}


# Tiga klaim own (artikel A1, A1, A2). Tau default 0,7.
#   c1 (A1, id): R1 p=(0,8;0,1;0,1) -> label S ; R3 p=(0,1;0,1;0,8) -> label NEI
#        sesuai = 0 ; dS = 0,1-0,8 = -0,7 ; dN = 0,1-0,8 = -0,7
#        overkomit: max(0,8;0,1)=0,8 >= 0,7 DAN NEI != S -> 1
#   c2 (A1, en): R1 p=(0,2;0,2;0,6) -> NEI ; R3 p=(0,1;0,1;0,8) -> NEI
#        sesuai = 1 ; dS = 0,1-0,2 = -0,1 ; dN = 0,6-0,8 = -0,2
#        overkomit: max=0,2 < 0,7 -> 0
#   c3 (A2, id): R1 p=(0,1;0,75;0,15) -> label R ; R3 p=(0,6;0,2;0,2) -> label S
#        sesuai = 0 ; dS = 0,6-0,1 = 0,5 ; dN = 0,15-0,2 = -0,05
#        overkomit: max(0,1;0,75)=0,75 >= 0,7 DAN S != R -> 1
RECS_OWN = [
    rec("c1", "A1", "own", "R1", (0.8, 0.1, 0.1), lang="id"),
    rec("c1", "A1", "own", "R3", (0.1, 0.1, 0.8), lang="id"),
    rec("c2", "A1", "own", "R1", (0.2, 0.2, 0.6), lang="en"),
    rec("c2", "A1", "own", "R3", (0.1, 0.1, 0.8), lang="en"),
    rec("c3", "A2", "own", "R1", (0.1, 0.75, 0.15), lang="id"),
    rec("c3", "A2", "own", "R3", (0.6, 0.2, 0.2), lang="id"),
]


class TestIndikatorOwn(unittest.TestCase):
    def test_indikator_per_klaim_tangan(self):
        ind = {x["claim_id"]: x for x in konsistensi.indikator_own(RECS_OWN)}
        self.assertEqual(ind["c1"]["sesuai"], 0.0)
        self.assertAlmostEqual(ind["c1"]["dS"], -0.7, places=9)
        self.assertAlmostEqual(ind["c1"]["dN"], -0.7, places=9)
        self.assertEqual(ind["c1"]["overkomit"], 1.0)
        self.assertEqual(ind["c2"]["sesuai"], 1.0)
        self.assertAlmostEqual(ind["c2"]["dS"], -0.1, places=9)
        self.assertAlmostEqual(ind["c2"]["dN"], -0.2, places=9)
        self.assertEqual(ind["c2"]["overkomit"], 0.0)
        self.assertEqual(ind["c3"]["sesuai"], 0.0)
        self.assertAlmostEqual(ind["c3"]["dS"], 0.5, places=9)
        self.assertAlmostEqual(ind["c3"]["dN"], -0.05, places=9)
        self.assertEqual(ind["c3"]["overkomit"], 1.0)

    def test_tau_mengubah_overkomit(self):
        # c3 max(R1)=0,75 ; dengan tau 0,8 -> tidak overkomit
        ind = {x["claim_id"]: x for x in konsistensi.indikator_own(RECS_OWN, tau=0.8)}
        self.assertEqual(ind["c3"]["overkomit"], 0.0)
        self.assertEqual(ind["c1"]["overkomit"], 1.0)

    def test_klaim_tanpa_r3_dilewati(self):
        recs = [rec("cx", "A9", "own", "R1", (0.5, 0.3, 0.2))]
        self.assertEqual(konsistensi.indikator_own(recs), [])

    def test_observasi_gagal_dikecualikan(self):
        recs = RECS_OWN + [rec("c4", "A2", "own", "R1", None), rec("c4", "A2", "own", "R3", (0.1, 0.1, 0.8))]
        ids = [x["claim_id"] for x in konsistensi.indikator_own(recs)]
        self.assertNotIn("c4", ids)


class TestRingkasOwn(unittest.TestCase):
    def test_rerata_tangan(self):
        # sesuai: (0+1+0)/3 = 0,333333 ; overkomit: (1+0+1)/3 = 0,666667
        # dS: (-0,7-0,1+0,5)/3 = -0,1 ; dN: (-0,7-0,2-0,05)/3 = -0,316667
        r = konsistensi.ringkas(RECS_OWN, b=200)
        self.assertEqual(r["n_klaim"], 3)
        self.assertAlmostEqual(r["sesuai"]["rerata"], 1 / 3, places=6)
        self.assertAlmostEqual(r["overkomit"]["rerata"], 2 / 3, places=6)
        self.assertAlmostEqual(r["dS"]["rerata"], -0.1, places=6)
        self.assertAlmostEqual(r["dN"]["rerata"], -0.316667, places=6)

    def test_ringkas_per_bahasa_memisah(self):
        pb = konsistensi.ringkas_per_bahasa(RECS_OWN, b=200)
        self.assertEqual(set(pb), {"id", "en"})
        # id: c1 dan c3 -> sesuai (0+0)/2 = 0 ; en: c2 -> sesuai 1
        self.assertAlmostEqual(pb["id"]["sesuai"]["rerata"], 0.0, places=9)
        self.assertAlmostEqual(pb["en"]["sesuai"]["rerata"], 1.0, places=9)


# False-support mass: observasi near/far berjangkar NEI. Massa = p_S + p_R.
#   near R1 (0,6;0,3;0,1) -> 0,9 ; near R3 (0,2;0,1;0,7) -> 0,3
#   far  R1 (0,1;0,1;0,8) -> 0,2 ; far  R3 (0,0;0,0;1,0) -> 0,0
# Selisih near - far: R1 = 0,9 - 0,2 = 0,7 ; R3 = 0,3 - 0,0 = 0,3
RECS_FS = [
    rec("c1", "A1", "near", "R1", (0.6, 0.3, 0.1), label="NEI"),
    rec("c1", "A1", "near", "R3", (0.2, 0.1, 0.7), label="NEI"),
    rec("c1", "A1", "far", "R1", (0.1, 0.1, 0.8), label="NEI"),
    rec("c1", "A1", "far", "R3", (0.0, 0.0, 1.0), label="NEI"),
]


class TestFalseSupport(unittest.TestCase):
    def test_massa_dan_selisih_tangan(self):
        r = konsistensi.ringkas(RECS_FS, b=200)
        fs = r["false_support"]
        self.assertAlmostEqual(fs["R1"]["near"]["rerata"], 0.9, places=9)
        self.assertAlmostEqual(fs["R1"]["far"]["rerata"], 0.2, places=9)
        self.assertAlmostEqual(fs["R1"]["selisih"]["rerata"], 0.7, places=9)
        self.assertAlmostEqual(fs["R3"]["selisih"]["rerata"], 0.3, places=9)

    def test_hanya_berjangkar_nei(self):
        # observasi near berlabel SUPPORTED tidak masuk false-support mass
        recs = RECS_FS + [rec("c2", "A2", "near", "R1", (0.9, 0.05, 0.05), label="SUPPORTED")]
        r = konsistensi.ringkas(recs, b=200)
        self.assertAlmostEqual(r["false_support"]["R1"]["near"]["rerata"], 0.9, places=9)

    def test_tanpa_pasangan_far_selisih_none(self):
        recs = [x for x in RECS_FS if x["pair_type"] == "near"]
        r = konsistensi.ringkas(recs, b=200)
        self.assertIsNone(r["false_support"]["R1"]["selisih"])
        self.assertIsNone(r["false_support"]["R1"]["far"])


if __name__ == "__main__":
    unittest.main()
