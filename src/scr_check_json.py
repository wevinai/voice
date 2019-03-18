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
import os
import sys
import json
import settings

def check_json(dirs):
    va, vs, vt = 0, 0, 0
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
                if not os.path.isfile(e['location']):
                    print('ERROR: audio/video file {} does not exist'.format(e['location']))
                    quit()
                if not e['location'].lower().endswith(settings.all_formats):
                    print('ERROR: Format is not support in audio/video file {}'.format(e['location']))
                    quit()
                if 'active_region' not in e:
                    print('ERROR: "active_region" is missing in {}'.format(e))
                    quit()
                if 'format' not in e:
                    print('ERROR: "format" is missing in {}'.format(e))
                    quit()
                if len(e['active_region']) == 0:
                    print('ERROR: "active_region" is empty in {}'.format(e))
                valid = False
                for ar in e['active_region']:
                    if ar['start']==0 and ar['end']==0:
                        continue
                    if not isinstance(ar['start'], (int,float)) or not isinstance(ar['end'], (int,float)):
                        print('ERROR: type of start/end not (int,float) in {} : {} {}'.format(e['location'], 
                              type(ar['start']), type(ar['end'])))
                        quit()
                    if 'label' not in ar or ar['label'] == '':
                        print('Label is missing: {}'.format(e))
                        quit()
                    elif ar['label'] not in settings.all_labels:
                        print('Label is incorrect (label={}): {}'.format(ar['label'], e['location'].split('/')[-1]))
                        quit()
                    valid = True
                    if ar['start'] > ar['end']:
                        print('Start time > end time (s={}, e={}) in {}'.format(ar['start'], ar['end'], 
                              e['location'].split('/')[-1]))
                    elif ar['end'] - ar['start'] > 5 and ar['label']!='purring' and ar['label']!='growl':
                        # We allow long segments for purring sound!
                        print('WARN: Too large region in {}. Please shrink them into small pieces'.format(e['location']))
                    else:
                        vt += ar['end']-ar['start']
                    if ar['label']:
                        vs += 1
                if valid:
                    va += 1
    print('Check Finish, everything is good')
    print('There are {} valid and labelled audios and {} valid segments and a total of {} seconds'.format(va, vs, vt))
    
if __name__ == '__main__':
    if len(sys.argv)==1:
	print('Usage: python check_json.py <json_file.json> ...')
	quit()
    else:
	dirs = sys.argv[1:]
	check_json(dirs)


