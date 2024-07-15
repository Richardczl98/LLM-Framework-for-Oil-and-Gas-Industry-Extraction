from collections import OrderedDict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, \
    ConfusionMatrixDisplay
from typing import Any, List
import pandas as pd
import numpy as np

from config import SPLIT_BLOCK_CHAR
from converter.dict2xls import convert_dict_to_dataframe, check_to_replace_value
from eval.parser.parser_result import SUCCESS, ERROR
from lib.my_logger import logger
from lib.file_op import write_to_csv
from extractor.chat_llm import ask_llm_is_same_country
from lib.helper import convert_to_one_if_positive
from schema.variables import get_v2_variables, is_gt_variable

# Continuous Value
CV_THRESHOLD = 5
ORANGE = 'orange-fp'
RED = 'red-fp'
BLUE = 'blue-fn'
MERGED = 'merged'
WHITE = 'white-tp'
WHITE_TN = "white-tn"


def uniform_data_type(value: Any) -> Any:
    # Convert np.nan and None to None
    if pd.isna(value):
        return

    # Convert int, float, string number to float
    try:
        return float(value)
    except ValueError:
        pass

    return value


class EvaluationMetric:
    def __init__(self, success_only: bool = False, deep_run: bool = False):
        self.success_only: bool = success_only
        self.deep_run = deep_run

        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0

        self.old_tp = 0
        self.old_fp = 0
        self.old_tn = 0
        self.old_fn = 0

        self.prediction_binary = []
        self.gt_binary = []
        self.eval_count = 0
        self.eval_dict = {}
        self.dt_field_errors = OrderedDict()

    def _update_metric(self,
                       field: str,
                       variable: str,
                       metric: str = None,
                       old_metric: str = None,
                       pred_bin_val: int = None,
                       eval_dict_val: int = None,
                       gt_bin_val: int = None,
                       dt_error_val: int = None,
                       ):
        if metric:
            if metric not in self.__dict__:
                logger.error(f"Not support metric: {metric}")
                return
            self.__dict__[metric] += 1

        if old_metric:
            if old_metric not in self.__dict__:
                logger.error(f"Not support old metric: {old_metric}")
                return
            if variable not in get_v2_variables():
                self.__dict__[old_metric] += 1

        if pred_bin_val is not None:
            self.prediction_binary.append(pred_bin_val)

        if gt_bin_val is not None:
            self.gt_binary.append(gt_bin_val)

        if eval_dict_val is not None:
            self.eval_dict[variable] = eval_dict_val

        if dt_error_val is not None:
            self.dt_field_errors[field].update({variable: dt_error_val})

    def evaluate(self, filepath: str, pred_fields: OrderedDict, gt_fields: OrderedDict):
        for field_dp_name, field_od in pred_fields.items():
            self.dt_field_errors[field_dp_name] = OrderedDict()
            gt_field = _find_ground_truth(field_dp_name, field_od, gt_fields, self.deep_run)
            self.evaluate_field(field_dp_name, field_od, gt_field)
            self.eval_count += 1

        acc = accuracy_score(self.gt_binary, self.prediction_binary)
        pre_score = precision_score(self.gt_binary, self.prediction_binary)
        rec = recall_score(self.gt_binary, self.prediction_binary)
        f1 = f1_score(self.gt_binary, self.prediction_binary)

        score = f'''Evaluation score:
                    accuracy_score:{acc},
                    precision_score:{pre_score},
                    recall_score:{rec},
                    f1_score:{f1}'''

        logger.info(score)
        with open(f"{filepath}/eval_matrix_report.txt", 'w') as file:
            file.write(score)

        self.plot_matrices()
        self.write_files(filepath)

    def evaluate_field(self, field: str, pred_values: OrderedDict, gt_values: OrderedDict):
        for var, pred in pred_values.items():
            if not is_gt_variable(var):
                logger.info(f"assistant variable '{var}' is skipped to evaluation.")
                continue

            if check_to_replace_value(self.success_only, values=pred):
                pred_value = None
            else:
                pred_value = uniform_data_type(pred[0])
            gt_value = uniform_data_type(gt_values.get(var, np.nan))
            self._evaluate_same_type(field, variable=var, pred_value=pred_value, gt_value=gt_value)
            self._evaluate_diff_type(field, variable=var, pred_value=pred_value, gt_value=gt_value)

    def _evaluate_number(self, field: str, variable: str, pred_value: float, gt_value: float):
        if gt_value == pred_value:
            self._update_metric(field=field, variable=variable, metric='tp', old_metric='old_tp',
                                pred_bin_val=1, gt_bin_val=1, dt_error_val=0)
            self._count_field(variable, field, WHITE)
        else:
            if (gt_value == float(1) and pred_value != float(1)) or (gt_value == float(0) and pred_value != float(0)):
                self._update_metric(field=field, variable=variable, metric='fp', old_metric='old_fp',
                                    pred_bin_val=0, gt_bin_val = 1, dt_error_val = 3)
                self._count_field(variable, field, ORANGE)
            elif abs(gt_value - pred_value) > get_threshold(variable, gt_value):
                self._update_metric(field=field, variable=variable, metric='fp', old_metric='old_fp',
                                    pred_bin_val=0, gt_bin_val=1, dt_error_val=3)
                self._count_field(variable, field, ORANGE)
            else:
                self._update_metric(field=field, variable=variable, metric='tp', old_metric='old_tp',
                                    pred_bin_val=1, gt_bin_val=1, dt_error_val=0)
                self._count_field(variable, field, WHITE)

    def _evaluate_none(self, field: str, variable: str):
        self._update_metric(field=field, variable=variable, metric='tn', old_metric='old_tn',
                            pred_bin_val=0,
                            gt_bin_val=0, dt_error_val=0)
        self._count_field(variable, field, WHITE_TN)

    def _evaluate_string(self, field: str, variable: str, pred_value: str, gt_value: str):
        # Ask llm for field location (country).
        if gt_value.strip().lower() == pred_value.strip().lower() or (
                variable == 'Field location (Country)' and ask_llm_is_same_country(pred_value, gt_value)
        ):
            self._update_metric(field=field, variable=variable, metric='tp', old_metric='old_tp', pred_bin_val=1,
                                gt_bin_val=1, dt_error_val=0)
            self._count_field(variable, field, WHITE)
        else:
            self._update_metric(field=field, variable=variable, metric='fp', old_metric='old_fp', pred_bin_val=0,
                                gt_bin_val=1, dt_error_val=3)

            if '|' in pred_value:
                self._count_field(variable, field, MERGED)
            else:
                self._count_field(variable, field, ORANGE)

    def _evaluate_same_type(self, field, variable: str, pred_value: Any, gt_value: Any):
        if type(pred_value) == type(gt_value):
            if isinstance(gt_value, float):
                self._evaluate_number(field, variable=variable, pred_value=float(pred_value),
                                      gt_value=float(gt_value))
            if gt_value is None:
                self._evaluate_none(field, variable=variable)

            if isinstance(gt_value, str):
                self._evaluate_string(field, variable=variable, pred_value=pred_value, gt_value=gt_value)

    def _evaluate_diff_type(self, field, variable: str, pred_value: Any, gt_value: Any):
        if type(pred_value) != type(gt_value):
            logger.error(
                f"Different type of prediction value and ground truth value, "
                f"prediction_key:{variable}, "
                f"prediction_value:{pred_value}, {type(pred_value)}, "
                f"ground_truth_value:{gt_value},{type(gt_value)}. "
            )

            if gt_value is None:
                # red color
                self._update_metric(field=field, variable=variable, metric='fp', old_metric='old_fp', pred_bin_val=1,
                                    gt_bin_val=0, dt_error_val=1)

                if '|' in str(pred_value):
                    self._count_field(variable, field, MERGED)
                else:
                    self._count_field(variable, field, RED)
            else:
                if pred_value is None:
                    # blue color
                    self._update_metric(field=field, variable=variable, metric='fn', old_metric='old_fn', pred_bin_val=0,
                                        gt_bin_val=1, dt_error_val=2)
                    self._count_field(variable, field, BLUE)
                else:
                    self._update_metric(field=field, variable=variable, metric='fp', old_metric='old_fp', pred_bin_val=0,
                                        gt_bin_val=1, dt_error_val=3)

                    if '|' in str(pred_value):
                        self._count_field(variable, field, MERGED)
                    else:
                        self._count_field(variable, field, ORANGE)

    def _count_field(self, variable: str, field, error_type: str):
        # find bad model outputs and convert to ordereddict
        field_dic = self.eval_dict.get(field, {})
        tmp = field_dic.get(variable, {})
        count = tmp.get(error_type, 0)
        count += 1
        tmp[error_type] = count
        field_dic[variable] = tmp
        self.eval_dict[field] = field_dic

    def plot_matrices(self):
        matrices = confusion_matrix(self.gt_binary, self.prediction_binary)
        cm_display = ConfusionMatrixDisplay(matrices, display_labels=[1, 0])
        cm_display.plot()

    def write_files(self, filepath: str):
        write_to_csv(f"{filepath}/eval_matrix.csv", ['TP', 'FP', 'TN', 'FN'],
                     [[self.tp, self.fp, self.tn, self.fn]])
        df = convert_dict_to_dataframe(self.eval_dict)
        df = df.applymap(convert_to_one_if_positive)
        df = pd.concat([df, pd.DataFrame({"EvalCount": [self.eval_count]}, index=['count'])])
        df.to_excel(f"{filepath}/eval_field_errors.xlsx")


def get_threshold(variable: str, gt_value: float):
    no_threshold_vars = ['Field age']

    if variable in no_threshold_vars:
        return 0

    if gt_value > 1:
        return CV_THRESHOLD
    else:
        return gt_value * (CV_THRESHOLD / 100)


def _find_ground_truth(field_dp_name: str, pred_odict: OrderedDict, gt_odict: OrderedDict, deep_run: bool = False):
    pred_name = pred_odict['Field name'][0]
    pred_age = pred_odict['Field age'][0]

    for field_dp_gt, variables in gt_odict.items():
        # In deep run mode, because the order field display name in prediction is different to the name in ground truth,
        # we use field name and field age to find the value column in ground truth.
        # If not use deep run, field display name can be used to identify the correct value column in ground truth.
        if deep_run:
            if variables.get('Field name') == pred_name and variables.get('Field age', np.nan) == pred_age:
                return variables
        else:
            if field_dp_gt.strip().lower() == field_dp_name.strip().lower():

                return variables
    return {}


if __name__ == '__main__':
    pass
