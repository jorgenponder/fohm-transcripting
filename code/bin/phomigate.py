#!/usr/bin/env python3

import json
import os
import glob


DOC = """ Tries to keep only the good text lines from the FoHM OCR transacripts """

import argparse
import sys
parser = argparse.ArgumentParser(description=DOC)
parser.add_argument("--aflag", action="store_true", dest="AFLAG",help="help text")
parser.add_argument('--indata', type = argparse.FileType('r'), default=sys.stdin)
parser.add_argument('top_directory')


args = parser.parse_args()

top_directory = os.path.relpath(args.top_directory)

# i = open('test.json', errors="replace") 
# mattt = json.load(fi)

def process_data(data):
    
    old_pair = []
    for text_pair in text_pairs:
        print(text_pair)

for filename in (glob.glob(top_directory + '/*.json')):
    fi = open(filename, errors="replace") 
    text_pairs = json.load(fi)
    process_data(text_pairs)