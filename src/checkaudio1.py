#os(operating system) used to find directory
import os
import librosa

#uses librosa library to check is can load the files

path = '/hdd/mlrom/Data/animal_voice/audio/'

files = os.listdir(path)

for name in files:
    y, sr = librosa.load(path + name)
    print(name, y.shape, sr)

print len(files)

