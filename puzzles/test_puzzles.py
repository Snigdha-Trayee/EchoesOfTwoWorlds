
import unittest
from puzzle_logic import get_puzzle, check_answer, get_hint


class PuzzleTests(unittest.TestCase):

    def test_existing_puzzle(self):
        self.assertIsNotNone(get_puzzle("forgotten_symbols"))

    def test_correct_answer(self):
        self.assertTrue(check_answer("forgotten_symbols", "STAR"))

    def test_answer_ignores_case_and_spaces(self):
        self.assertTrue(check_answer("forgotten_symbols", " star "))

    def test_wrong_answer(self):
        self.assertFalse(check_answer("forgotten_symbols", "LEAF"))

    def test_unknown_puzzle(self):
        self.assertFalse(check_answer("unknown", "STAR"))

    def test_hint_exists(self):
        self.assertIsNotNone(get_hint("final_riddle"))


if __name__ == "__main__":
    unittest.main()
