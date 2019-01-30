'''
Description: This file uses librosa to load audio files to check its integrity
Author: Vincent/Weilin
'''
#os(operating system) used to find directory
import os
import librosa

#uses librosa library to check is can load the files

path = '/hdd/mlrom/Data/animal_voice/audio/'

files = os.listdir(path)

for name in files:
    y, sr = librosa.load(path + name)
    print(name, y.shape, sr)

print "# of audio files=", len(files)

