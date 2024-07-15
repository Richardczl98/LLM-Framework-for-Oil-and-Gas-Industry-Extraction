#!/bin/bash

python opgee_cli.py -p ./scraper/articles/ogj/VAL01_WHAT_ARE_WE_PAYING_TO_FIND_OIL_GAS_IN_MISSISSIPPI_ALABAMA.txt -m gemini-1.5-pro-latest --grouped_by section -g ./data/val/news/VAL01_WHAT_ARE_WE_PAYING_TO_FIND_OIL_GAS_IN_MISSISSIPPI_ALABAMA.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/VAL02_Lukoil_to_develop_Caspian_oil_gas_field.txt -m gemini-1.5-pro-latest --grouped_by section -g ./data/val/news/VAL02_Lukoil_to_develop_Caspian_oil_gas_field.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/VAL03_Gas_Discovered_at_Snadd_North_Prospect.txt -m gemini-1.5-pro-latest --grouped_by section  -g ./data/val/news/VAL03_Gas_Discovered_at_Snadd_North_Prospect.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/VAL04_StatoilHydro_to_Drill_Production_Wells_on_Gjoa.txt -m gemini-1.5-pro-latest --grouped_by section -g ./data/val/news/VAL04_StatoilHydro_to_Drill_Production_Wells_on_Gjoa.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/VAL05_Gawler_Reports_Production_Increases_on_High_Island_in_GoM.txt -m gemini-1.5-pro-latest --grouped_by section -g ./data/val/news/VAL05_Gawler_Reports_Production_Increases_on_High_Island_in_GoM.xlsx

# gov
python opgee_cli.py -p ./scraper/articles/misc/VAL_GOV01_A_day_after_IEA_calls.txt -m gemini-1.5-pro-latest --grouped_by section -g ./data/val/news/VAL_GOV01_A_day_after_IEA_calls.xlsx

