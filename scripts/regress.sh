#!/bin/bash

# 1st argument is the file name of the combined merge
# 2nd & 3rd argument decide

function prompt {
    echo
    echo $1
    read answer
}

proj_dir=${VOICE_HOME}
data_dir_l="/hdd/mlrom/Data/animal_voice/audio /hdd/mlrom/Data/animal_voice/aaron/aaron_audio /hdd/mlrom/Data/animal_voice/vincent/20190226 /hdd/mlrom/Data/animal_voice/vincent/20190303 /hdd/mlrom/Data/animal_voice/weilin/85Catsounds /hdd/mlrom/Data/animal_voice/weilin/First14audios /hdd/mlrom/Data/animal_voice/weilin/41CatSneezes /hdd/mlrom/Data/animal_voice/downloads/freesound/meow"
echo "$filelist1"
prompt 'Check audio integrity? (yes/no)'
if [ $answer == 'yes' -o $answer == 'y' -o $answer == 'Yes' ]
then
    for f in $data_dir_l
    do
        echo "---- Run scr_check_aduio.py on $f"
        python $VOICE_HOME/src/scr_check_audio.py $f
    done
fi



prompt 'Check JSON integrity? (yes/no)'
if [ $answer == 'yes' -o $answer == 'y' -o $answer == 'Yes' ]
then
    json_files=()
    for f in $VOICE_HOME/data/*2019*.json
    do
        echo "---- Run scr_check_json on $f"
        python $VOICE_HOME/src/scr_check_json.py $f
        json_files[${#json_files[@]}]=$f
    done
fi

prompt 'Merge all the Json files'
echo "---- Merge the following JSON files:"
echo "     ${json_files[@]}"
python $VOICE_HOME/src/scr_merge_json.py $VOICE_HOME/data/all.json ${json_files[@]}

prompt 'Preprocess Audio data'
echo "---- Run preprocess to generate MFCC frequence vectors"
python $VOICE_HOME/src/preprocess_data.py $VOICE_HOME/data/all.json

#bigfile=/home/weilin/Desktop/AllCombinedAudios

#for file1 in $filelist1
#    do
#        python /hdd/projects/yuan/voice/src/scr_merge_json.py merge.json $bigfile /hdd/projects/yuan/voice/data/$file1
#        $bigfile=merge.json
#        rm merge.json
#    done

declare -a all_labels=('purring' 'attention' 'sneeze' 'hiss' 'scream' 'happy' 'complain' 'growl' 'unknown')
echo "${#all_labels[@]}"
DATE=`date +%y%m%d`
mkdir /hdd/mlrom/Data/animal_voice/data/3D.20$DATE

for i in "${#all_labels[@]}"-1; do
    for j in "${#all_labels[@]}"-i-1; do
        python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl all_labels[i] all_labels[j]
    done
done

