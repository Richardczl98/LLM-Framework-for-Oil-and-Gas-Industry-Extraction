from __future__ import annotations

from typing import List
from collections import OrderedDict
import eval.parser.parser_response as pr
from lib.my_logger import logger


def merge_by_block(responses: List[pr.ParserResponse]) -> OrderedDict:
    merged_resp = OrderedDict()
    for resp in responses:
        var_name = resp.variable.name
        value = resp.result.data.value
        raw_text = resp.raw_text
        unit = resp.result.data.unit
        reference = resp.result.data.ref
        status = resp.result.status
        if var_name in merged_resp:
            merged_value = resp.variable.merger().merge(merged_resp[var_name][0], value)
            merged_ref = resp.variable.ref_merger().merge(merged_resp[var_name][2], reference)
            merged_raw_text = resp.variable.raw_text_merger().merge(merged_resp[var_name][3], raw_text)
            merged_unit = resp.variable.raw_text_merger().merge(merged_resp[var_name][1], unit)
            merged_status = resp.variable.status_merger().merge_status(merged_resp[var_name][4], status)
            merged_resp.update({var_name: [merged_value, merged_unit, merged_ref, merged_raw_text, merged_status]})
        else:
            merged_resp.update({var_name: [value, unit, reference, raw_text, status]})

    return merged_resp
