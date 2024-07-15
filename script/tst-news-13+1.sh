#!/bin/bash

python opgee_cli.py -p scraper/articles/rigzone/TST01_Roxar_to_Supply_Wet_Gas_Meters_for_Statoil.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST01_Roxar_to_Supply_Wet_Gas_Meters_for_Statoil.xlsx

python opgee_cli.py -p scraper/articles/rigzone/TST02_TNK-BP_to_Invest_1B_by_2012_for_Samotlor_Field_Development.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST02_TNK-BP_to_Invest_1B_by_2012_for_Samotlor_Field_Development.xlsx

python opgee_cli.py -p scraper/articles/rigzone/TST03_Elixir_Provides_Production_Update_on_Gulf_of_Mexico_Fields.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST03_Elixir_Provides_Production_Update_on_Gulf_of_Mexico_Fields.xlsx

python opgee_cli.py -p scraper/articles/rigzone/TST04_Norways_Offshore_Knarr_Field_to_Deliver_Gas_to_Britain.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST04_Norways_Offshore_Knarr_Field_to_Deliver_Gas_to_Britain.xlsx

python opgee_cli.py -p scraper/articles/rigzone/TST05_Petrobras_Halts_Oil_Natgas_Platform_Output_For_Second_Time_In_8_Days.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST05_Petrobras_Halts_Oil_Natgas_Platform_Output_For_Second_Time_In_8_Days.xlsx

python opgee_cli.py -p scraper/articles/rigzone/TST06_Kosmos_Boosts_Profit_Set_to_Take_Over_BP_Operatorship_of_Senegal_Field.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST06_Kosmos_Boosts_Profit_Set_to_Take_Over_BP_Operatorship_of_Senegal_Field.xlsx

python opgee_cli.py -p scraper/articles/rigzone/TST07_CNOOC_Starts_Production_at_Several_Oil_Gas_Projects.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST07_CNOOC_Starts_Production_at_Several_Oil_Gas_Projects.xlsx

python opgee_cli.py -p scraper/articles/ogj/TST08_Statoil_to_develop_Tyrihans_oil_gas_field.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST08_Statoil_to_develop_Tyrihans_oil_gas_field.xlsx

python opgee_cli.py -p scraper/articles/ogj/TST09_New_Zealand_Oil_Gas_to_buy_back_into_Kupe_field.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST09_New_Zealand_Oil_Gas_to_buy_back_into_Kupe_field.xlsx

python opgee_cli.py -p scraper/articles/ogj/TST10_Dana_Gas_to_develop_south_Egypt_oil_field.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST10_Dana_Gas_to_develop_south_Egypt_oil_field.xlsx

python opgee_cli.py -p scraper/articles/ogj/TST11_Russians_Chinese_to_develop_eastern_Siberias_Chayandin_gas_field_construct_pipeline_to_Xinyang.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST11_Russians_Chinese_to_develop_eastern_Siberias_Chayandin_gas_field_construct_pipeline_to_Xinyang.xlsx

python opgee_cli.py -p scraper/articles/ogj/TST12_Japex_to_boost_Iwafune-oki_oil_gas_production.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST12_Japex_to_boost_Iwafune-oki_oil_gas_production.xlsx

python opgee_cli.py -p scraper/articles/ogj/TST13_American_Noble_Gas_farms_in_to_Hugoton_gas_field.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST13_American_Noble_Gas_farms_in_to_Hugoton_gas_field.xlsx

# gov
python opgee_cli.py -p scraper/articles/ogj/TST-GOV01_Norwegian_government_approves_Equinor-led_Snhvit_Future_project.txt -m gpt-4o --grouped_by section -g ./data/tst/news/TST-GOV01_Norwegian_government_approves_Equinor-led_Snhvit_Future_project.xlsx
