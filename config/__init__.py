import os
from pathlib import Path

BASE_DIRECTORY = Path(__file__).parent.parent
TEST_DIR = BASE_DIRECTORY / "tests"
CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = Path(os.path.dirname(CODE_DIR))
RESULT_DIR = Path(BASE_DIRECTORY, 'result')
RESULT_DIFF_DIR = Path(BASE_DIRECTORY, 'result_diff')
RESULT_HISTORY_DIR = Path(BASE_DIRECTORY, 'result_history')
DATA_DIR = Path(BASE_DIRECTORY, 'data')

SPLIT_BLOCK_CHAR = " | "
SPLIT_REFERENCE_CHAR = '@'
SPLET_KEY_VALUE_CHAR = ':'

REPLACE_SIGN = '#'

AGGREGATE_COLUMN_NAME_SPLITTER = ':'

YEAR_FOR_CALUCULATION = 2023
UNKNOWN_TEXT = 'unknown'
