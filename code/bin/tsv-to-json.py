#!/usr/bin/env python3
# coding: utf-8

import json
import os
import glob
import re

secs = re.compile(r'\d+')

# DOC = """ Tries to keep only the good text lines from the FoHM OCR transcripts """

# import argparse
# import sys
# parser = argparse.ArgumentParser(description=DOC)
# parser.add_argument("--aflag", action="store_true", dest="AFLAG",help="help text")
# parser.add_argument('--indata', type = argparse.FileType('r'), default=sys.stdin)
# parser.add_argument('top_directory')


# args = parser.parse_args()

# top_directory = os.path.relpath(args.top_directory)

# i = open('test.json', errors="replace") 
# mattt = json.load(fi)

def process_data(data):
    result = []
    caps = data.split("\t")
    for cap in caps:
        out_cap = {}
        in_cap = cap.split("\n")
        try:
            out_cap['timestamp'] = secs.match(in_cap[1]).group()
        except (IndexError, AttributeError):
            continue
        out_cap['text'] = in_cap[2:]
        result.append(out_cap)
    return result


for filename in (glob.glob('./tsvs/*.tsv')):
    fi = open(filename, errors="replace", encoding = 'utf-8') 
    data = fi.read()
    result = process_data(data)
    fo = open(filename + '.json', mode='w', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
    json.dump(result,fo, ensure_ascii=False)

                                                                                          
