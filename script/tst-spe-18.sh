#!/bin/bash

# Mar 19, 2024
python opgee_cli.py -p ./data/tst/spe/zips/spe-195333-pa.zip -m gpt-4 -g ./data/tst/spe/spe-195333-pa_RZ.xlsx --grouped_by section
# 2 File not suitable for content extraction: 
# File permissions do not allow content extraction; 
# requestTrackingId=ba2f9fe6-8019-405a-a52e-6d591df7afea; statusCode=400; errorCode=DISQUALIFIED_PERMISSIONS
# need to use pdfX to remove password and extract again
python opgee_cli.py -p ./data/tst/spe/zips/spe-191536-18rptc-ms.zip -m gpt-4o -g ./data/tst/spe/spe-191536-18rptc-ms_RZ.xlsx --grouped_by section
# 3
python opgee_cli.py -p ./data/tst/spe/zips/spe-178303-ms.zip -m gpt-4o -g ./data/tst/spe/spe-178303-ms_RZ.xlsx --grouped_by section
# 4 missed first round
python opgee_cli.py -p ./data/tst/spe/zips/spe-132440-pa.zip -m gpt-4o -g ./data/tst/spe/spe-132440-pa_RZ.xlsx --grouped_by section
# 5
python opgee_cli.py -p ./data/tst/spe/zips/spe-137561-pa.zip -m gpt-4o -g ./data/tst/spe/spe-137561-pa_RZ.xlsx --grouped_by section
# 6
python opgee_cli.py -p ./data/tst/spe/zips/spe-128873-ms.zip -m gpt-4o -g ./data/tst/spe/spe-128873-ms_RZ.xlsx --grouped_by section
# 7
python opgee_cli.py -p ./data/tst/spe/zips/spe-115790-ms.zip -m gpt-4o -g ./data/tst/spe/spe-115790-ms_RZ.xlsx --grouped_by section
# 8  page 13 and 16 handwritten diagrams are not properly parsed, but it is ok
python opgee_cli.py -p ./data/tst/spe/zips/spe-30727-ms.zip -m gpt-4o -g ./data/tst/spe/spe-30727-ms_RZ.xlsx --grouped_by section
# 9 diagrams after 9 are not properly parsed, but that is ok
# Apr-1-2024 find out 26730 is already in traning set
# python opgee_cli.py -p ./data/tst/spe/zips/spe-26730-ms.zip -m gpt-4o -g ./data/tst/spe/spe-26730-ms_RZ.xlsx --grouped_by section
# replace with 196417
python opgee_cli.py -p ./data/tst/spe/spe-196417-ms.txt -m gpt-4o -g ./data/tst/spe/spe-196417-ms_RZ.xlsx --grouped_by section
# 10
python opgee_cli.py -p ./data/tst/spe/zips/spe-12377-pa.zip -m gpt-4o -g ./data/tst/spe/spe-12377-pa_RZ.xlsx --grouped_by section
# 11
python opgee_cli.py -p ./data/tst/spe/zips/seg-2014-0078.zip -m gpt-4o -g ./data/tst/spe/seg-2014-0078_RZ.xlsx --grouped_by section
# 12
python opgee_cli.py -p ./data/tst/spe/zips/seg-2008-2856.zip -m gpt-4o -g ./data/tst/spe/seg-2008-2856_RZ.xlsx --grouped_by section
# 13
python opgee_cli.py -p ./data/tst/spe/zips/otc-30780-ms.zip -m gpt-4o -g ./data/tst/spe/otc-30780-ms_RZ.xlsx --grouped_by section
# 14
python opgee_cli.py -p ./data/tst/spe/zips/iptc-18108-ms.zip -m gpt-4o -g ./data/tst/spe/iptc-18108-ms_RZ.xlsx --grouped_by section
# 15 missed first round
python opgee_cli.py -p ./data/tst/spe/zips/iptc-10233-ms.zip -m gpt-4o -g ./data/tst/spe/iptc-10233-ms_RZ.xlsx --grouped_by section
# ready in Mar 29 2024
#16
python opgee_cli.py -p ./data/tst/spe/zips/spe-94171-ms.zip -m gpt-4o -g ./data/tst/spe/spe-94171-ms_RZ.xlsx --grouped_by section
#17
python opgee_cli.py -p ./data/tst/spe/zips/spe-7422-ms.zip -m gpt-4o -g ./data/tst/spe/spe-7422-ms_RZ.xlsx --grouped_by section
#18
python opgee_cli.py -p ./data/tst/spe/zips/petsoc-2004-144.zip -m gpt-4o -g ./data/tst/spe/petsoc-2004-144_RZ.xlsx --grouped_by section
