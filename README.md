# README for all the contents within this project

Notes:
1. Project directory structure explanation:
   - All the data should locate at /hdd/mlrom/Data/animal_voice/ where audio files in 
     /hdd/mlrom/Data/animal_voice/audio and video files in /hdd/mlrom/Data/animal_voice/video
   - All code/human-written stuff are checked into GitHub and should locates at ~/work/voice
     In your home directory
   - voice/scripts includes code/scripts to check if everything is smooth
   - voice/src includes source code for our AI code
   - voice/data includes data related information, temporary data, etc
   - voice/tryout includes the code which you can play around using Jupyter, etc
   - voice/lessons includes a number of tutorial/material to learn Python/Numpy/Eclipse/Github

2. Useful Linux commands 
   - Goto your own home directory: cd or cd ~
   - Goto a particular directory: cd <directory>, e.g. cd ~/work/voice    # ~ refers to home directory
   - Goto parent directory: cd ..
   - Remove a file/directory: rm <filename>
   - Create a new directory under current directory: mkdir <directory_name>

3. Useful GitHub commands
   - Get a repository: git clone <http://...>
   - Check current changes: git status
   - Pull from repository: git pull
   - Add a file to repository: git add <directory/filename>
   - Commit a change: git commit -m"what changed message"
   - Push committed changes to GitHub: git push

4. Python programming rules:
   - Indent is 4 spaces
   - all file/function/variable names should be self explanatory, if using multiple words, separate with "_",
     for example, a function cutwindows should be "cut_windows"
   - Use whitespace to separate code into segments for readability
   - Add comments for each segments
   - For each function, write comments to explain input/output functionality, their shapes
   - At important function place, write assertions to check coming-in and going-out requirements
   - After downloading audio/video, MUST do the following steps to check its integrity:
       - Run scripts/check_audio_integrity.py
       - Run scripts/checkjson.py (to be done)

   - Before check your changes to repository, MUST do the following steps:
       - git pull and merge your changes with others
       - Run regression using scripts/check_code_integrity.py (to be done)
       - If regression passes, check in your change!

5. Issues on editing a Json file?
   - Is [], {} in pairs?
   - Is the key to the dictionary consistent?
   - Is list separated by a comma and finish with empty note?


HowTo:
1. How to add an audio/video file into our system?
   - Before deciding to check in, please verify
        a) is animal's intention clear?
        b) is the voice quality good enough to recognize?
   - Add the file into either audio or video directory located at
        /hdd/mlrom/Data/animal_voice/audio OR
        /hdd/mlrom/Data/animal_voice/video
   - In project directory .../voice/data/data.json, add an entry look like the following:
        {
          "location": "/hdd/mlrom/Data/animal_voice/audio/Felis_silvestris_f_domestica_DIG0013_04_short.mp3",
          "species": "cat",
          "race": "",
          "gender": "male",
          "purpose": "purring",
          "format" : "audio",
          "age" : "juvenile"
          "active_region": [
            {
              "start": 0.146,
              "end": 1.389,
              "label": "screaming"
            }
          ]
        },
     Note that "location", "format" and "active_region" must exist! Refer to data/example.json.
   - Use audacity to calculate "start"/"end" field in "active_region", verify the label is correct!
     This is most important step
   - Run our checkjson.py script to verify if the changes are valid
        python ./src/checkjson.py

   - Check in the changes into repository. Note that you MUST pull first before check in.
     You may need to do a merge.

2. How to use audacity to analyze audio?
   - At command line, run "audacity" to start a GUI to run
   - Select "Make a copy" optino without changing original audio
   - Load a wav/mp3/aiff file


