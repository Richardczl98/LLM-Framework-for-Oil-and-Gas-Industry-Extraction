#!/bin/bash

python opgee_cli.py -p ./data/zips/spe-115712-ms.zip -s individual -m gpt-4 -g ./data/spe/SPE-115712-ms.xlsx
python opgee_cli.py -p ./data/zips/spe-210009-ms.zip -s individual -m gpt-4 -g ./data/spe/SPE-210009-ms.xlsx
python opgee_cli.py -p ./data/zips/spe-28002-ms.zip  -s individual -m gpt-4 -g ./data/spe/SPE-28002-ms.xlsx

