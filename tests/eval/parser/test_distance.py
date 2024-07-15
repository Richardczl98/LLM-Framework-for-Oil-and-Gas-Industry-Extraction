import unittest
from eval.parser.distance import cosin_similarity


class TestCosinSimilarity(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_single_diff_char(self):
        text1 = 'not_mentioned'
        text2 = 'Not_mentioned'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.9742989503
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_no_underline(self):
        text1 = 'not_mentioned'
        text2 = 'not mentioned'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.9333425018
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_all_upper_one_space(self):
        text1 = 'not_mentioned'
        text2 = 'NOT MENTIONED'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.9128429524
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_all_upper_two_space(self):
        text1 = 'not_mentioned'
        text2 = 'NOT  MENTIONED'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.8922494063
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_all_upper_three_space(self):
        text1 = 'not_mentioned'
        text2 = 'NOT   MENTIONED'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.8844565513
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_change_underline_to_hyphen(self):
        text1 = 'not_mentioned'
        text2 = 'not-mentioned'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.937052648999417
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_all_diff(self):
        text1 = 'not_mentioned'
        text2 = 'AAA_AAAAAAAAA'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.7592912947778314
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_mentioned_not_mentioned(self):
        text1 = 'not_mentioned'
        text2 = 'mentioned'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.8660547071950223
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_one_diff(self):
        text1 = 'not_mentioned'
        text2 = 'not_mentionet'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.9651230360477672
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_large_cutoff(self):
        text1 = 'not_mentioned'
        text2 = 'not'
        got = cosin_similarity(text1, text2)
        cos_sim = 0.8219118742225483
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_similar_meaning_1(self):
        text1 = 'not_mentioned'
        text2 = "don't_mentioned"
        got = cosin_similarity(text1, text2)
        cos_sim = 0.9372455395086008
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_similar_meaning_2(self):
        text1 = 'not_mentioned'
        text2 = "never_mentioned"
        got = cosin_similarity(text1, text2)
        cos_sim = 0.9439719334122304
        self.assertAlmostEqual(got, cos_sim, 3)

    def test_similar_meaning_3(self):
        text1 = 'not_mentioned'
        text2 = "not_shown"
        got = cosin_similarity(text1, text2)
        cos_sim = 0.8688974367381557
        self.assertAlmostEqual(got, cos_sim, 3)
