'''
Description: check JSON integrity for given files. It will check the following functions:
    0. JSON syntax error, report line# where the error is at
    1. 'location'/'active_region'/'format' field must exist
    2. 'label' must be part of correct labels listed below
    3. 'start' and 'end' time is consistent
    Usage is
        python check_json.py <json_file.json> ...
Author: Yuan
'''
from __future__ import print_function
import sys
import json
import settings

if len(sys.argv)==1:
    print('Usage: python check_json.py <json_file.json> ...')
    quit()

for jf in sys.argv[1:]:
    with open(jf, 'r') as f:
        try:
            l = json.load(f)
        except Exception as ex:
            print('ERROR: JSON file {} has syntax errors {}'.format(jf, ex))
            quit()
        for e in l:
            if 'location' not in e:
                print('ERROR: "location" is missing in {}'.format(e))
                quit()
            if 'active_region' not in e:
                print('ERROR: "active_region" is missing in {}'.format(e))
                quit()
            if 'format' not in e:
                print('ERROR: "format" is missing in {}'.format(e))
                quit()
            for ar in e['active_region']:
                if 'label' not in ar:
                    print('Label is missing: {}'.format(e))
                    quit()
                elif ar['label'] not in settings.all_labels:
                    print('Label is inconsistent (label={}): {}'.format(ar['label'], e['location'].split('/')[-1]))
                    quit()
                if ar['start'] > ar['end']:
                    print('Start time > end time (s={}, e={}) in {}'.format(ar['start'], ar['end'], 
                          e['location'].split('/')[-1]))
print('Check Finish, everything is good')

