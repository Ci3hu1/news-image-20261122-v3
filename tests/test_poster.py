#!/usr/bin/env python3
"""Tests for news-image-20261122 v3.

Run: python3 -m pytest tests/  (or python3 tests/test_poster.py)

Covers the three judge fixes from v2 plus the invariants the poster
must keep:
  1. DATE CHECK is 2 items, neutral title, and none of its stories
     appear in the main list.
  2. Legibility: every featured headline wraps to at most 2 lines at
     17px bold in a 186px card (no truncation), every ALSO ON headline
     fits its 298px column, and the poster is 1024x1024 under 1 MiB.
  3. Hong Kong figure carries its denominator and a source (EAC).
Plus: 30 stories total, region counts sum to 30, ALSO ON numbering
14-30 sequential, one drone number, main.py pure stdlib.
"""

import ast
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, "/home/hatch/workspace/custom-skills/"
                   "editorial-illustration")
sys.path.insert(0, ROOT)

import render_poster as rp  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

EXCLUDED_MARKERS = ("peru", "bulgari")


class TestStoryCount(unittest.TestCase):
    def test_total_is_30(self):
        total = len(rp.LEADS) + len(rp.FEATURED) + len(rp.ALSO_ON)
        self.assertEqual(total, 30)

    def test_sections(self):
        self.assertEqual(len(rp.LEADS), 3)
        self.assertEqual(len(rp.FEATURED), 10)
        self.assertEqual(len(rp.ALSO_ON), 17)

    def test_region_counts_sum_to_30(self):
        total = sum(int(label.split()[-1]) for label, _ in rp.REGIONS)
        self.assertEqual(total, 30)

    def test_seven_regions(self):
        self.assertEqual(len(rp.REGIONS), 7)


class TestAlsoOn(unittest.TestCase):
    def test_numbering_14_to_30_sequential(self):
        nums = [n for n, _, _ in rp.ALSO_ON]
        self.assertEqual(nums, list(range(14, 31)))

    def test_no_duplicate_numbers(self):
        nums = [n for n, _, _ in rp.ALSO_ON]
        self.assertEqual(len(nums), len(set(nums)))

    def test_headlines_fit_column(self):
        # Column is 336px wide; dot (12px) + number (26px) leaves 298px.
        img = Image.new("RGB", (10, 10))
        d = ImageDraw.Draw(img)
        f = rp.fnt("sans", 15)
        for n, txt, _ in rp.ALSO_ON:
            w = d.textlength(txt, font=f) / rp.SS
            self.assertLessEqual(
                w, 298,
                "ALSO ON %d headline too wide for its column: %r (%.1fpx)"
                % (n, txt, w))


class TestDateCheck(unittest.TestCase):
    def test_at_most_two_items(self):
        self.assertLessEqual(len(rp.DATE_CHECK), 2)

    def test_excluded_stories_not_in_main_list(self):
        main = " ".join(
            [h["headline"] for h in rp.LEADS]
            + [s["headline"] for s in rp.FEATURED]
            + [txt for _, txt, _ in rp.ALSO_ON]).lower()
        for marker in EXCLUDED_MARKERS:
            self.assertNotIn(marker, main,
                             "excluded story %r leaked into the main list"
                             % marker)

    def test_date_check_items_are_off_day(self):
        # Both items carry a date that is not Sunday 22 Nov.
        for item in rp.DATE_CHECK:
            self.assertTrue("20 Nov" in item or "21 Nov" in item, item)


class TestHongKong(unittest.TestCase):
    def test_card_carries_denominator(self):
        hk = [s for s in rp.FEATURED if s["place"] == "HONG KONG"]
        self.assertEqual(len(hk), 1)
        self.assertIn("5,640 of 5,709", hk[0]["headline"])

    def test_card_source_is_eac(self):
        hk = [s for s in rp.FEATURED if s["place"] == "HONG KONG"][0]
        self.assertEqual(hk["source"], "EAC")

    def test_kpi_carries_denominator(self):
        kpi = dict((lab, val) for val, lab in rp.KPIS)
        self.assertEqual(kpi.get("OF 5,709 HK VOTERS"), "5,640")

    def test_no_bare_turnout_percentage(self):
        # The judge read a bare "98.79%" as implausible. It must never
        # appear on the poster without its denominator beside it.
        for val, _ in rp.KPIS:
            self.assertNotEqual(val, "98.79%")
        for s in rp.FEATURED:
            self.assertNotIn("98.79%", s["headline"])


class TestLegibility(unittest.TestCase):
    def test_featured_headlines_fit_two_lines(self):
        # The v2 judge's core complaint was truncation/blur. Every
        # featured headline must wrap to at most 2 lines in its card.
        img = Image.new("RGB", (10, 10))
        d = ImageDraw.Draw(img)
        f = rp.fnt("sans_bold", 17)
        for s in rp.FEATURED:
            lines = rp.wrap(d, s["headline"], f, rp.px(186))
            self.assertLessEqual(
                len(lines), 2,
                "featured %d headline wraps to %d lines: %r"
                % (s["n"], len(lines), s["headline"]))

    def test_lead_headlines_fit(self):
        img = Image.new("RGB", (10, 10))
        d = ImageDraw.Draw(img)
        for i, h in enumerate(rp.LEADS):
            size = 28 if i == 0 else 21
            width = 1000 if i == 0 else 478
            f = rp.fnt("sans_bold", size)
            lines = rp.wrap(d, h["headline"], f, rp.px(width))
            self.assertLessEqual(len(lines), 2, h["headline"])

    def test_poster_dimensions_and_size(self):
        path = os.path.join(ROOT, "entry.png")
        self.assertTrue(os.path.isfile(path), "entry.png missing")
        with Image.open(path) as im:
            self.assertEqual(im.size, (1024, 1024))
        size = os.path.getsize(path)
        self.assertLessEqual(size, 1024 * 1024,
                             "entry.png over 1 MiB: %d bytes" % size)


class TestConsistency(unittest.TestCase):
    def test_one_drone_number(self):
        # 186 launched / 161 shot down everywhere it appears.
        kpi = dict((lab, val) for val, lab in rp.KPIS)
        self.assertEqual(kpi["DRONES IN A NIGHT"], "186")
        self.assertEqual(kpi["SHOT DOWN"], "161")
        dymer = rp.LEADS[1]
        self.assertIn("186", dymer["headline"])
        self.assertIn("161", dymer["deck"])

    def test_dymer_toll(self):
        self.assertIn("4 killed, 14 missing", rp.LEADS[1]["deck"])

    def test_delta_delays(self):
        kpi = dict((lab, val) for val, lab in rp.KPIS)
        self.assertEqual(kpi["DELTA DELAYS"], "1,169")
        delta = [s for s in rp.FEATURED if s["place"] == "ATLANTA"][0]
        self.assertIn("1,169", delta["headline"])

    def test_main_py_pure_stdlib(self):
        # The grader is pure Python stdlib: main.py must not import
        # anything outside the standard library.
        with open(os.path.join(ROOT, "main.py")) as fh:
            src = fh.read()
        tree = ast.parse(src)
        allowed = set(sys.stdlib_module_names)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    self.assertIn(a.name.split(".")[0], allowed, a.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.assertIn(node.module.split(".")[0], allowed,
                                  node.module)


if __name__ == "__main__":
    unittest.main(verbosity=2)
