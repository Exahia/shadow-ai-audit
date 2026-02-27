"""Tests for shadow-ai-audit scoring CLI internals."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import score_audit as sa  # noqa: E402


class ScoreAuditTests(unittest.TestCase):
    def test_template_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "template.json"
            sa._write_template(target)
            self.assertTrue(target.exists())
            data = target.read_text(encoding="utf-8")
            self.assertIn('"rgpd"', data)
            self.assertIn('"partial"', data)

    def test_compute_low_risk_when_good_answers(self) -> None:
        answers = {}
        for section, questions in sa.QUESTION_SETS.items():
            section_answers = {}
            for question in questions:
                section_answers[question.id] = question.good_when
            answers[section] = section_answers
        summary = sa._compute(answers)
        self.assertLess(summary["overall"]["score"], 5.0)
        self.assertIn("nis2", summary["sections"])

    def test_html_report_generation(self) -> None:
        answers = {}
        for section, questions in sa.QUESTION_SETS.items():
            section_answers = {}
            for question in questions:
                section_answers[question.id] = "partial"
            answers[section] = section_answers

        summary = sa._compute(answers)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "score-summary.html"
            sa._write_html(target, summary)
            content = target.read_text(encoding="utf-8")

        self.assertIn("<html", content)
        self.assertIn("Score global", content)
        self.assertIn("Scores par section", content)
        self.assertIn("Priorites de remediation", content)
        self.assertIn("nis2", content)


if __name__ == "__main__":
    unittest.main()
