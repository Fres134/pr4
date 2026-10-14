"""Unit tests for task_app."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_app import expand_leading_tabs, lines_with_leading_tab


class ExpandLeadingTabsTests(unittest.TestCase):
    def test_single_tab_becomes_four_spaces(self):
        self.assertEqual(expand_leading_tabs("\tx = 1"), "    x = 1")

    def test_two_tabs_become_eight_spaces(self):
        self.assertEqual(expand_leading_tabs("\t\tx = 1"), "        x = 1")

    def test_clean_text_is_unchanged(self):
        src = "def f():\n    return 1"
        self.assertEqual(expand_leading_tabs(src), src)

    def test_only_leading_tabs_are_replaced(self):
        self.assertEqual(expand_leading_tabs("a\tb"), "a\tb")


class LinesWithLeadingTabTests(unittest.TestCase):
    def test_returns_line_numbers(self):
        text = "ok\n\tbad\nok again\n\t\tbad too"
        self.assertEqual(lines_with_leading_tab(text), [2, 4])

    def test_empty_when_clean(self):
        self.assertEqual(lines_with_leading_tab("clean\n    code"), [])


if __name__ == "__main__":
    unittest.main()