#!/usr/bin/env python3

import argparse
import pandas as pd
from pandas.io.json import json_normalize
from parse import parse_file
import json
from datetime import timedelta

pd.set_option("display.max_rows", None)

argparser = argparse.ArgumentParser(
    description="Summarize c3lingo interpreter workloads"
)
argparser.add_argument(
    "files",
    nargs="+",
    help="Path(s) to the file(s) to parse. Choose Etherpad's Plain Text export",
)
args = argparser.parse_args()

parsed = []
for path in args.files:
    with open(path) as fp:
        parsed += parse_file(fp.read())

data = json_normalize(
    [shift.to_json() for talk in parsed for shift in talk.translation_shifts]
)
duration_by_translator = (
    data.groupby(data.name.str.lower())["talk.duration"]
    .sum()
    .sort_values(ascending=False)
)
print(duration_by_translator)
print()
print('Median:', duration_by_translator.median())
print(
    'Translators with more than six hours:',
    len(duration_by_translator[duration_by_translator > timedelta(hours=6)])
)
print(
    'All translators:',
    len(duration_by_translator),
)
