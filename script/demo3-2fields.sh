#!/bin/bash

python opgee_cli.py --max_field 2 -p ./data/zips/spe-115712-ms.zip -m gpt-4 -g ./data/spe/spe-115712-ms-v2.xlsx
python opgee_cli.py --max_field 2 -p ./data/zips/spe-210009-ms.zip -m gpt-4 -g ./data/spe/spe-210009-ms-v2.xlsx
python opgee_cli.py --max_field 2 -p ./data/zips/spe-28002-ms.zip  -m gpt-4 -g ./data/spe/spe-28002-ms-v2.xlsx