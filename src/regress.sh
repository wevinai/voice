#!/bin/bash

# 1st argument is the file name of the combined merge
# 2nd & 3rd argument decide

filelist1=`ls /hdd/projects/yuan/voice/data/`
echo "$filelist1"
echo Check audio integrity
#python /hdd/projects/yuan/voice/src/scr_check_audio.py


echo Check JSON integrity
#python /hdd/projects/yuan/voice/src/scr_check_json.py Combined-190-audios.json
#for file1 in $filelist1
#    do
#        python /hdd/projects/yuan/voice/src/scr_check_json.py /hdd/projects/yuan/voice/data/$file1 
#    done

echo Merge human written JSON files
#python /hdd/projects/yuan/voice/src/scr_merge_json.py t.json /hdd/mlrom/Data/animal_voice/audio/dataP1.json /hdd/mlrom/Data/animal_voice/audio/dataP2.json
#python /hdd/projects/yuan/voice/src/scr_merge_json.py $1 $2 $3

bigfile=/home/weilin/Desktop/AllCombinedAudios

for file1 in $filelist1
    do
        python /hdd/projects/yuan/voice/src/scr_merge_json.py merge.json $bigfile /hdd/projects/yuan/voice/data/$file1
        $bigfile=merge.json
        rm merge.json
    done
        
