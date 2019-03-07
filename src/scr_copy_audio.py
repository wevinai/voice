'''
Description: This script takes a JSON file as input and copy all valid audios to
    our destinated directory (default to /hdd/mlrom/Data/animal_voice/audio/). Valid is defined as:
        1. The entries must be labelled
        2. The format should be complete including at least 'location', 'format', 'active_region' fields
    Usage:
    python scr_copy_audio.py data.json dest_dir
Author: Aaron
'''
from __future__ import print_function
from shutil import copyfile
from pathlib2 import Path
import sys
import json
import settings
import os

if len(sys.argv) == 1:
    print('Usage: python scr_copy_audio.py <json_file.json> <destinated_directory>')
    quit()

jf = sys.argv[1]
if not os.path.isfile(jf):
    print('ERROR: JSON file {} does not exist'.format(jf))
if len(sys.argv) == 3:
    dest = sys.argv[2]
    if not os.path.isdir(dest):
        print('ERROR: Destinated directory {} does not exist'.format(dest))
else:
    dest = "/hdd/mlrom/Data/animal_voice/audio/"

with open(jf, 'r') as f:
    l = json.load(f)
    for e in l:
        if 'location' not in e or 'format' not in e or 'active_region' not in e:
            continue
        if len(e['active_region'])==0 or not e['active_region'][0]['label']:
            continue
	f = Path(dest + os.path.basename(loc))
	if f.is_file():
	    if os.path.getsize(f) == os.path.getsize(loc):
	        continue
	    print("ERROR: " + loc + " already exists in " + dest + " but the sizes do not match.")
	    quit()
        loc = e['location']
        copyfile(loc, os.path.join(dest, os.path.basename(loc)))

