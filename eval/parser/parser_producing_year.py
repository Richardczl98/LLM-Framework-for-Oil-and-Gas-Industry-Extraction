from lib.my_logger import logger


def parse_producing_year(field_year_json: dict):
    # only handle years with a oil production value,
    # if the year text cannot be converted to integer or oil production is None, skip it.

    rslt_dict = {}
    for field, year_dict in field_year_json.items():
        if year_dict:
            years = []
            for year_text, oil_production in year_dict.items():
                if not oil_production:
                    continue
                try:
                    year_int = int(year_text)
                except ValueError:
                    logger.exception(
                        f'year text: {year_text} cannot be convert to int, it is not a valid year expression.')
                    continue
                years.append(year_int)

            rslt_dict.update({field: years})

    return rslt_dict
