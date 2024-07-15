"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-11-06
Description: OPGEE AGGR "TN TP FP FN" statistics.
"""

"""
OPGEE AGGR Command Line Interface (CLI) module.

This module provides a command line interface for the OPGEE 'TP,FP,TN,FN' statistics,
allowing users to input the path of a result and, optionally, 
a path to an paper containing.

Usage:
    python eval/eval_agger.py -c "Path of the paper result or The path to the results of a certain paper" [-t '%y%m%d 231019']
"""
import os
import sys


this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

import argparse
from lib.file_op import generate_summary_csv, combined_excel
from lib.result_op import merge_results, compare_multi_results
from lib.my_logger import logger


def main():
    desp = 'OPGEE AGGR CLI.Generate "TN,TP,FN,FP" statistics & Output multiple excels to one excel containing multiple sheets'

    parser = argparse.ArgumentParser(description=desp)

    # Generate-summary csv
    parser.add_argument("-c", '--csv-path',
                        type=str,
                        default="result",
                        help="Path of the dir to generate 'TN TP FP FN' statistics, default is 'result'")

    # Generate-summary csv begin from the csv-time format '%y%m%d' 231019
    parser.add_argument("-t", '--time',
                        type=str,
                        help="Produce 'TN TP FP FN' statistics from the input time format is '%%y%%m%%d like '231019'")

    # Generate combine excel from the input path
    parser.add_argument("-e", '--excel-path',
                        nargs="+",
                        help="Path of the dir to generate combined excel"
                             " like: 'result/otc-26509-ms/231110_1626-gpt-4-individual/extract_ref.xlsx'"
                             " Please note that the data table in excel must be in the sheet named Sheet1")

    # Generate combine excel from the input path
    parser.add_argument("-m", '--merge_results',
                        default=None,
                        help="Path of the dir to generate combined excel with ground truth, extracted_ref, "
                             "and extracted_raw values "
                             "like: 'result' "
                             "The generated excel file - extracted_summary.xlsx would also be save in this path."
                        )
    # Generate excel with different batch of results multi.
    parser.add_argument("-d", '--diff_results',
                        default=None,
                        nargs='+',
                        help="Path list of you results. To generate the difference table, "
                             "at least 2 or more batch of results need to be provide."
                             "Difference table would be saved in 'result_diff/extract_diff.xlsx'."
                        )

    # Parse arguments
    args = parser.parse_args()
    if args.merge_results:
        merge_results('extract_ref.xlsx', args.merge_results, create=True)
        merge_results('extract_raw.xlsx', args.merge_results)
        return

    if n_batchs := args.diff_results:
        if len(n_batchs) < 2:
            logger.error(f'At least 2 result path is required. {n_batchs} is provided')
        else:
            compare_multi_results(args.diff_results)
        return

    if args.excel_path:
        combined_excel(args.excel_path)
        return

    if not os.path.exists(os.path.join(os.path.dirname(this_file_path), args.csv_path)):
        logger.error('%s does not exist', os.path.join(os.path.dirname(this_file_path), args.csv_path))
    generate_summary_csv(args.csv_path, args.time)
    return


if __name__ == "__main__":
    '''
    generate_summary_csv('result')
    '''
    main()
