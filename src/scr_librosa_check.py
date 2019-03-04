import os
import librosa
import sys

if len(sys.argv)! = 1:
    print('Usage: python scr.find_missing.py <json_file.json> <directory of audios>')
    quit()


files = os.listdir(sys.argv[1])
for name in files:
    y, sr = librosa.load(path + name)
    print(name, y.shape, sr)

print len(files)
