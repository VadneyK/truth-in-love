#!/usr/bin/env python3
"""Run: python3 scripts/test_checks.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import heart_check as hc  # noqa: E402
import reader_check as rc  # noqa: E402


def groups(text):
    return [g for g, _p, _c in hc.find(text)]


class Heart(unittest.TestCase):
    def test_stock_phrase(self):
        self.assertIn("stock", groups("I hope this finds you well."))

    def test_promise_of_time(self):
        self.assertIn("promise", groups("Anytime you need a hand, I'll make sure it gets done."))

    def test_self_positioning(self):
        self.assertIn("promise", groups("I'd rather support what you do than build something of my own."))

    def test_heart_claim_is_listed_not_failed(self):
        hits = hc.find("I'm really excited about the mission.")
        self.assertEqual([h[0] for h in hits], ["heart"])

    def test_plain_ask_passes(self):
        self.assertEqual(groups("How do students get matched with a mentor right now?"), [])

    def test_extra_phrases(self):
        self.assertTrue(hc.find("as discussed, synergy", extra=[r"\bsynergy\b"]))


class Reader(unittest.TestCase):
    def test_plain_email_passes(self):
        _score, problems = rc.check("Thanks for your note. The form is ready. Please open it and tell me what you see.")
        self.assertEqual(problems, [])

    def test_technical_words_fail_for_nontech(self):
        _score, problems = rc.check("Please merge the pull request and check the staging deploy for me today.")
        self.assertTrue(any("technical" in p for p in problems))

    def test_same_words_pass_for_tech(self):
        _score, problems = rc.check("Please merge the pull request and check the staging deploy for me today.", "tech")
        self.assertFalse(any("technical" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
