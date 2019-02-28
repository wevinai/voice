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

def check_json(dirs):
    va, vs = 0, 0
    for jf in dirs:
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
                if len(e['active_region']) == 0:
                    print('ERROR: "active_region" is empty in {}'.format(e))
                for ar in e['active_region']:
                    if ar['start']==0 and ar['end']==0:
                        continue
                    if ar['label'] == '':
                        print('Label is missing: {}'.format(e))
                        quit()
                    elif ar['label'] not in settings.all_labels:
                        print('Label is inconsistent (label={}): {}'.format(ar['label'], e['location'].split('/')[-1]))
                        quit()
                    if ar['start'] > ar['end']:
                        print('Start time > end time (s={}, e={}) in {}'.format(ar['start'], ar['end'], 
                              e['location'].split('/')[-1]))
                    if ar['label']:
                        vs += 1
                if e['active_region'][0]['label']:
                    va += 1
    print('Check Finish, everything is good')
    print('There are {} valid and labelled audios and {} valid segments'.format(va, vs))

if __name__ == '__main__':
	if len(sys.argv)==1:
		print('Usage: python check_json.py <json_file.json> ...')
		quit()
	else:
		dirs = sys.argv[1:]
		check_json(dirs)


