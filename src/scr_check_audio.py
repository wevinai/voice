'''
Description: This file uses librosa to check audio files locating at a given directory.
    If the directory is not given, default is the known directory.  Usage is
        python scr_check_audio.py <audio_directory> ...
Author: Vincent/Weilin
'''
#os(operating system) used to find directory
from __future__ import print_function
import os
import sys
import librosa
import settings

#uses librosa library to check is can load the files

if len(sys.argv) == 1:
    dirs  = ['/hdd/mlrom/Data/animal_voice/audio/']
else:
    dirs = sys.argv[1:]

for dir0 in dirs:
    files = os.listdir(dir0)
    for name in files:
        if name.lower().endswith('.json'):
            continue
        if name.lower().endswith(settings.all_formats):
            try:
                y, sr = librosa.load(os.path.join(dir0, name))
            except Exception as ex:
                print('ERROR: fail to load {} - {}'.format(name, ex))
                quit()
            print('{}: data.shape={} sample_rate={}'.format(name, y.shape, sr))
        else:
            print('WARN: file format is not recognized: {}'.format(name))
    print("# of audio files in {} = {}".format(dir0, len(files)))

