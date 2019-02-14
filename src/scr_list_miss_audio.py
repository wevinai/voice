'''
Description: Report those audio files in audio_dir which are not listed in given data.json.
    This script facilitates labeling process.
    Usage is
        python scr_list_miss_audio.py data.json audio_dir
Author: Vincent
'''
from __future__ import print_function
import sys
import json
import settings
import os

if len(sys.argv)!=3:
    print('Usage: python scr_list_miss_audio.py <json_file.json> <directory_of_audios>')
    quit()
if not os.path.isfile(sys.argv[1]):
    print('ERROR: JSON file {} does not exist'.format(sys.argv[1]))
if not os.path.isdir(sys.argv[2]):
    print('ERROR: Audio directory {} does not exist'.format(sys.argv[2]))

with open(sys.argv[1], 'r') as f:
    l = json.load(f)
    print('A list of audio files which are not labeled in given json file:')
    for filename in os.listdir(sys.argv[2]):
        if filename.endswith('.wav') or filename.endswith('.mp3') or filename.endswith('.aiff') or \
           filename.endswith('.m4a') or filename.endswith('.flac'):
            found = False
            for js in l:
                if os.path.basename(js['location'])==filename:
                    found = True
                    break
            if found == False:
                print ('  {}'.format(filename))
