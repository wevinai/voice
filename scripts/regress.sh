#!/bin/bash

echo Check audio integrity
python ../src/scr_check_audio.py

echo Check JSON integrity
python ../src/scr_check_json.py ../data/data.json

echo Merge human written JSON files
python ../src/scr_merge_json.py t.json /hdd/mlrom/Data/animal_voice/audio/dataP1.json /hdd/mlrom/Data/animal_voice/audio/dataP2.json
