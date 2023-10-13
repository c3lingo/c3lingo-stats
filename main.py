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
    data.groupby(data.name.str.lower())["duration"]
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

people_with_shirts = ['Yann0u',
 'ironic',
 'Ben',
 'eibwen',
 'SimplySayM',
 'sebalis',
 'franzt',
 'damok',
 'remy_o',
 'lemeda',
 'Scriptkiddi',
 'ningwie',
 'tribut',
 'MrBronze',
 'waffle',
 'DuckMan',
 'sirenensang',
 'Ludwig',
 'Vassago',
 'guillermo',
 'joern',
 'ToniHDS',
 'KetieSaner',
 'informancer',
 'morkowka',
 'yila',
 'whitey_chan',
 'os10000',
 'db0',
 'hnms',
 'afrowson',
 'korfuri',
 'cami',
 'genbi',
 'phlo',
 'dimir',
 'Iggle',
 'IconI',
 'gooniesbro',
 'kaste',
 'MissSensei',
 'comoelcometa',
 'saltunza',
 'shesapirate',
 'kwiii',
 'problame',
 'pharmafirma',
 'mary',
 'max_eaxedx',
 'snakey',
 'LuKaRo',
 'PetePriority',
 'pinkdispatcher',
 'bubbler',
 'oskar',
 'Aegy',
 'sasha',
 'breakthesystem',
 'os10000',
 'db0',
 'hnms',
 'afrowson',
 'korfuri',
 'cami',
 'genbi',
 'phlo',
 'dimir',
 'Iggle',
 'IconI',
 'gooniesbro',
 'kaste',
 'MissSensei',
 'comoelcometa',
 'saltunza',
 'shesapirate',
 'kwiii',
 'problame',
 'pharmafirma',
 'mary',
 'max_eaxedx',
 'snakey',
 'LuKaRo',
 'PetePriority',
 'pinkdispatcher',
 'bubbler',
 'oskar',
 'Aegy',
 'sasha',
 'breakthesystem']
people_with_shirts = [name.lower() for name in people_with_shirts]

# print('Manual hours:')
manual_hours = duration_by_translator[[name not in people_with_shirts for name in duration_by_translator.index]] * 1.5
manual_hours = manual_hours.dt.ceil(freq='15min')
# print(manual_hours)
