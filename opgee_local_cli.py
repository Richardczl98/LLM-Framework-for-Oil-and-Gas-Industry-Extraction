import argparse
from pathlib import Path

from config import RESULT_DIR, RESULT_HISTORY_DIR
from lib.my_logger import logger, logger_config_instance
from extractor.extract_history import extract_history, parse_path
from lib.helper import find_raw_files
from model.models import MDL_MOCK
from model.chat_mocked_model import mocked_llm_client
from traceback import format_exc


def main():
    """
    A command line interface for the OPGEE local result extractor.

    Parameters:
        None

    Returns:
        None
    """
    desp = 'OPGEE Local LLM result extractor CLI. Result is in /opgee/result_history/paper-name/time-model/'
    parser = argparse.ArgumentParser(description=desp)
    model = MDL_MOCK

    #Generate-summary csv
    parser.add_argument("-f", '--raw_file',
                        type=str,
                        help="Path of raw output file from LLM model which needs to be re-evaluated. The file name must be 'extract_raw.xlsx'",
                        default=None,
                        )

    parser.add_argument("-r", '--raw_file_dir',
                        type=str,
                        default=RESULT_DIR,
                        help="Result dir which contain raw output files from LLM model needs to be re-evaluated. Default is '/opgee/result'",
                        )
    parser.add_argument("-d", '--destination_dir',
                        type=str,
                        default=RESULT_HISTORY_DIR,
                        help="Path to store re-evaluated results. If not provided, default is '/opgee/result_history'"
                        )

    parser.add_argument("-so", '--success_only',
                        action='store_true',
                        default=False,
                        help="Only display and evaluate successfully parsed values in result excels."
                        )

    args = parser.parse_args()

    if args.raw_file:
        if not args.raw_file.endswith('extract_raw.xlsx'):
            logger.error(f"{args.raw_file} does not end with 'extract_raw.xlsx'.")
            parser.print_help()
            return

        gt_path, dest_path, log_name = parse_path(
            raw_file_path=Path(args.raw_file).absolute().as_posix(),
            destination=args.destination_dir,
        )

        logger_config_instance.configure_logger(log_name)
        history_llm_answer_dir = Path(args.raw_file).parent / 'history_llm_answers.json'
        if history_llm_answer_dir.exists():
            mocked_llm_client.load(history_llm_answer_dir)

        try:
            extract_history(
                raw_file_path=Path(args.raw_file).absolute().as_posix(),
                dest_path=dest_path,
                gt_path=gt_path,
                model=model,
                success_only=args.success_only,
            )
        except ValueError as err:
            logger.error(err)
            logger.error(format_exc())
        # print(Path(args.destination_dir) / 'history_llm_answers.json')
        mocked_llm_client.dump(history_llm_answer_dir)
    else:
        raw_files = find_raw_files(args.raw_file_dir)
        for file in raw_files:
            gt_path, dest_path, log_name = parse_path(
                raw_file_path=Path(file).absolute().as_posix(),
                destination=args.destination_dir,
                      )
            logger_config_instance.configure_logger(log_name)

            history_llm_answer_dir = Path(file).parent / 'history_llm_answers.json'
            if history_llm_answer_dir.exists():
                mocked_llm_client.load(history_llm_answer_dir)

            try:
                extract_history(
                    raw_file_path=Path(file).absolute().as_posix(),
                    dest_path=dest_path,
                    gt_path=gt_path,
                    model=model,
                    success_only=args.success_only,

                )
            except FileNotFoundError as err:
                logger.error(err)
            except ValueError as err:
                logger.error(err)
            mocked_llm_client.dump(history_llm_answer_dir)


if __name__ == "__main__":
    main()
