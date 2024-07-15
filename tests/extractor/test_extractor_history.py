import unittest
from pathlib import Path

from extractor.extract_history import parse_history, extract_history
from config import TEST_DIR


class TestExtractorHistory(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_parse_history(self):
        raw_file_path = 'extract_raw.xlsx'
        got = parse_history(raw_file_path)
        for field in got['fields']:
            print(field)
            for var, value in got[field].items():
                print('\t', var, ": ", value)

        print(got)

    def test_parse_history_case_1(self):
        raw_file_path = TEST_DIR / 'extractor/test_results_history/spe-140630-ms/240223_2110-mistral-medium-section/extract_raw.xlsx'
        got = parse_history(raw_file_path)
        # for field in got['fields']:
        #     print(field)
        #     for var, value in got[field].items():
        #         print('\t', var, ": ", value)

        print(got)

    def test_extract_history(self):
        raw_file_path = 'test_results/spe-182043-ms/231103_1340-gpt-4-individual/extract_raw.xlsx'
        destination = Path(TEST_DIR, 'extractor', 'test_results_history').absolute().as_posix()
        extract_history(raw_file_path, destination)



