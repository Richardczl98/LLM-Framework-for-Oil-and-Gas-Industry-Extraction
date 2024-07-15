#!/bin/bash

# add 10 more papers on Feb 15, 2024
python opgee_cli.py -p ./data/zips/spe-114174-ms.zip -m gpt-4 -g ./data/spe/spe-114174-ms_RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-126181-ms.zip -m gpt-4 -g ./data/spe/spe-126181-ms_RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-158716-ms.zip -m gpt-4 -g ./data/spe/spe-158716-ms_RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-191895-ms.zip -m gpt-4 -g ./data/spe/spe-191895_RZ.xlsx --grouped_by section
# 196417 cannot be parsed
# python opgee_cli.py -p ./data/zips/spe-196417-ms.zip -m gpt-4 -g ./data/spe/spe-196417-ms_RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-212005-ms.zip -m gpt-4 -g ./data/spe/spe-212005-ms_RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-217255-ms.zip -m gpt-4 -g ./data/spe/spe-217255-ms_RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-58782-ms.zip -m gpt-4 -g ./data/spe/spe-58782-ms_RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-65473-ms.zip -m gpt-4 -g ./data/spe/spe-65473-ms_RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-88967-ms.zip -m gpt-4 -g ./data/spe/spe-88967-ms-RZ.xlsx --grouped_by section
python opgee_cli.py -p ./data/zips/spe-28784-ms.zip -m gpt-4 -g ./data/spe/spe-28784-ms_RZ.xlsx --grouped_by section
