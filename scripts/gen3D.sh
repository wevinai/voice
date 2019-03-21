#!/bin/bash

python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl purring attention
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl purring sneeze
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl purring hiss
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl purring scream
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl purring happy
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl purring complain
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl purring growl

python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl attention sneeze
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl attention hiss
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl attention scream
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl attention happy
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl attention complain
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl attention growl

python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl sneeze hiss
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl sneeze scream
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl sneeze happy
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl sneeze complain
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl sneeze growl

python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl hiss scream
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl hiss happy
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl hiss complain
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl hiss growl

python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl scream happy
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl scream complain
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl scream growl

python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl happy
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl happy complain
python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl happy growl

python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl complain growl

python /hdd/projects/yuan/voice/src/gen3Dvideo.py ./feature.pkl all
