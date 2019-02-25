'''
Description: check JSON integrity for given files. It will check the following functions:
    0. JSON syntax error, report line# where the error is at
    1. 'location'/'active_region'/'format' field must exist
    2. 'label' must be part of correct labels listed below
    3. 'start' and 'end' time is consistent
    Usage is
        python check_json.py <json_file.json> ...
Author: Vincent
'''
from __future__ import print_function
import sys
import json
import settings
import os

if len(sys.argv)!=3:
    print('Usage: python scr.find_missing.py <json_file.json> <directory of audios>')
    quit()

with open(sys.argv[1], 'r') as f:
    l = json.load(f)
    for filename in os.listdir(sys.argv[2]):
        if filename.endswith(".wav"):
            found = False
            for js in l:
                if os.path.basename(js['location'])==filename:
                    found = True
                    break
            if found == False:
                print (filename)
