#!/bin/bash

# replace model: mistral-large-latest, gpt-4

# world oil
python opgee_cli.py -p ./scraper/articles/worldoil/TRN01_Libya_restarts_production_exports_from_countrys_largest_oil_field.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN01_Libya_restarts_production_exports_from_countrys_largest_oil_field.xlsx
python opgee_cli.py -p ./scraper/articles/worldoil/TRN02_Libya_resumes_Wafa_oil_field_operations_following_protests.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN02_Libya_resumes_Wafa_oil_field_operations_following_protests.xlsx
python opgee_cli.py -p ./scraper/articles/worldoil/TRN03_Trio_Petroleum_restarts_production_from_Californias_McCool_Ranch_oil_field.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN03_Trio_Petroleum_restarts_production_from_Californias_McCool_Ranch_oil_field.xlsx
python opgee_cli.py -p ./scraper/articles/worldoil/TRN04_Eni_to_fast-track_natural_gas_discovery_development_offshore_Cypress_following_successful_production_test.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN04_Eni_to_fast-track_natural_gas_discovery_development_offshore_Cypress_following_successful_production_test.xlsx

# rig zone
python opgee_cli.py -p ./scraper/articles/rigzone/TRN05_LatAm_Explorer_Discovers_Chile_Gas_Field.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN05_LatAm_Explorer_Discovers_Chile_Gas_Field.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/TRN06_Aramco_Starts_Gas_Production_in_South_Ghawar.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN06_Aramco_Starts_Gas_Production_in_South_Ghawar.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/TRN07_Startup_Of_Malikai_Oil_Field_To_Boost_Malaysias_Kimanis_Exports.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN07_Startup_Of_Malikai_Oil_Field_To_Boost_Malaysias_Kimanis_Exports.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/TRN08_IPR_Make_Offshore_Egypt_Find.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN08_IPR_Make_Offshore_Egypt_Find.xlsx

# ogj
python opgee_cli.py -p ./scraper/articles/ogj/TRN09_New_associated_gas_plant_proposed_for_Kashagan_oil_field.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN09_New_associated_gas_plant_proposed_for_Kashagan_oil_field.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN10_Equinor_brings_Trestakk_oil_field_on_stream.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN10_Equinor_brings_Trestakk_oil_field_on_stream.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN11_CNOOC_brings_Weizhou_6-13_oil_field_on_stream.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN11_CNOOC_brings_Weizhou_6-13_oil_field_on_stream.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN12_Oil_production_restarts_from_Maari_field_offshore_New_Zealand.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN12_Oil_production_restarts_from_Maari_field_offshore_New_Zealand.xlsx

# added later on Mar-11th
python opgee_cli.py -p ./scraper/articles/worldoil/TRN13_Alberta_regulator_reconsiders_Suncor_oil_sands_expansion.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN13_Alberta_regulator_reconsiders_Suncor_oil_sands_expansion.xlsx
python opgee_cli.py -p ./scraper/articles/worldoil/TRN14_Suncor_Energy_replacing_CEO_after_oil_sands_mine_fatality.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN14_Suncor_Energy_replacing_CEO_after_oil_sands_mine_fatality.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN15_Albanian_gas-condensate_field_to_be_developed.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN15_Albanian_gas-condensate_field_to_be_developed.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN16_Sonatrach_lets_Tinrhert_conventional_gas_development_contract.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN16_Sonatrach_lets_Tinrhert_conventional_gas_development_contract.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN17_Algeria_gas_project_advances.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN17_Algeria_gas_project_advances.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN18_ENCORNORCEN_AWARDED_BIG_ALGERIA_BLOCK.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN18_ENCORNORCEN_AWARDED_BIG_ALGERIA_BLOCK.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN19_WORLDS_LPG_SUPPLY_PICTURE_WILL_CHANGE_BY_2000.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN19_WORLDS_LPG_SUPPLY_PICTURE_WILL_CHANGE_BY_2000.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN20_Double-expansion_valve_sequence_reduces_hydrate_formation.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN20_Double-expansion_valve_sequence_reduces_hydrate_formation.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN21_Imperial_commissioning_Kearl_oil_sands_mine.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN21_Imperial_commissioning_Kearl_oil_sands_mine.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN22_CNRL_to_buy_idle_Joslyn_oil_sands_project.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN22_CNRL_to_buy_idle_Joslyn_oil_sands_project.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN23_PTTEP_further_delays_Alberta_oil_sands_project.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN23_PTTEP_further_delays_Alberta_oil_sands_project.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/TRN24_ExxonMobil_Unit_Shuts_Oil_Sands_Mine_After_Pipeline_Spill.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN24_ExxonMobil_Unit_Shuts_Oil_Sands_Mine_After_Pipeline_Spill.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/TRN25_HNRA_Confirms_Boost_in_Untapped_Oil_in_Permian_Basin_Asset.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN25_HNRA_Confirms_Boost_in_Untapped_Oil_in_Permian_Basin_Asset.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/TRN26_Syncrude_Says_Alberta_Oil_Sands_Mine_Shut_Down_Because_of_Wildfire.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN26_Syncrude_Says_Alberta_Oil_Sands_Mine_Shut_Down_Because_of_Wildfirex.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/TRN27_Total_Suspends_Work_On_Alberta_Joslyn_Oil_Sands_Mine_Cites_Cost.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN27_Total_Suspends_Work_On_Alberta_Joslyn_Oil_Sands_Mine_Cites_Cost.xlsx
python opgee_cli.py -p ./scraper/articles/rigzone/TRN28_AMEC-Colt_JV_Wins_Athabasca_Oil_Sands_Mine_Expansion_Phase_3_Contract.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN28_AMEC-Colt_JV_Wins_Athabasca_Oil_Sands_Mine_Expansion_Phase_3_Contract.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN29_INDUSTRY_BRIEFS.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN29_INDUSTRY_BRIEFS.xlsx
python opgee_cli.py -p ./scraper/articles/ogj/TRN30_LPG_EXPORT_GROWTH_WILL_EXCEED_DEMAND_BY_2000.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN30_LPG_EXPORT_GROWTH_WILL_EXCEED_DEMAND_BY_2000.xlsx

# gov
python opgee_cli.py -p ./scraper/articles/misc/TRN-GOV01-2024_Canadian_Oil_Production_A_Short-Lived_Boom.txt -m claude-3-opus-20240229 --grouped_by section -g ./data/trn/news/TRN-GOV01-2024_Canadian_Oil_Production_A_Short-Lived_Boom.xlsx
