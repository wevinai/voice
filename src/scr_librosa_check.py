import os
import librosa
import sys

if len(sys.argv) != 2:
    print('Usage: python scr.find_missing.py <audio file>')
    quit()


files = os.listdir(sys.argv[1])
for name in files:
    y, sr = librosa.load(path + name)
    print(name, y.shape, sr)

print len(files)
