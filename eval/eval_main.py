""" eval main entry """
import os
from collections import OrderedDict

from lib.my_logger import logger
from converter.dict2xls import fill_color_to_extract_and_ref
from eval.xls_parser import ParseExcel
from eval.evaluation_metric import EvaluationMetric


def evaluate(rslts: OrderedDict,
             ground_truth: ParseExcel,
             result_folder_path: str,
             success_only: bool = False,
             deep_run: bool = False,
             ) -> None:

    # evaluate the results against the ground truth
    # the full path of the result folder has to exsit
    # we won't make this directory as it contains time & model
    # in the path
    if not os.path.exists(result_folder_path):
        logger.error('%s does not exist', result_folder_path)
        return

    logger.info("Start evaluation for results against %s", ground_truth.file_path)
    gt = ground_truth.to_dict()

    metric = EvaluationMetric(success_only=success_only, deep_run=deep_run)
    metric.evaluate(result_folder_path, rslts, gt)

    # dt_errors = eval_metric(rslts, gt, result_folder_path)
    fill_color_to_extract_and_ref(result_folder_path, metric.dt_field_errors)

    logger.info("End evaluation and saving results to %s", result_folder_path)
    return


if __name__ == '__main__':
    pass
