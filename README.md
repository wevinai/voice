# README for all the contents within this project

Notes:
1. Project directory structure explanation:
   - All the data should locate at /hdd/mlrom/Data/animal_voice/ where audio files in 
     /hdd/mlrom/Data/animal_voice/audio and video files in /hdd/mlrom/Data/animal_voice/video
   - All code/human-written stuff are checked into GitHub and should locates at ~/work/voice
     In your home directory
   - voice/src includes source code for our AI code as well support scripts/code
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
   - Revert a uncomitted file change: git checkout file_name
   - Check previous checkin information: git log file_name
   - Find difference with older version: git diff <commit_version_id> file_name

4. Python programming rules:
   - Indent is 4 spaces
   - We use single quote for strings!
   - all file/function/variable names should be self explanatory, if using multiple words, separate with "_",
     for example, a function cutwindows should be "cut_windows"
   - Use whitespace to separate code into segments for readability
   - Add comments for each segments
   - For each function, write comments to explain input/output functionality, their shapes
   - At important function place, write assertions to check coming-in and going-out requirements
   - After downloading audio/video, MUST do the following steps to check its integrity:
       - Run 'python src/scr_check_audio.py <directory>'. If <directory is not specify, 
         it will check default directory
       - Run 'python src/scr_check_json.py <your json file>'.

   - Before check your changes to repository, MUST do the following steps:
       - git pull and merge your changes with others
       - Run regression using src/scr_check_code.py (to be done)
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
          "location": "/hdd/mlrom/Data/animal_voice/downloads/freesound/meow/110011__tuberatanka__cat-meow.wav",
          "website": "http://freesound.org/people/tuberatanka/sounds/110011/download/110011__tuberatanka__cat-meow.wav",
          "species": "cat",
          "race": "",
          "gender": "male",
          "purpose": "purring",
          "format" : "audio",
          "age" : "juvenile"
          "active_region": [
            {
              "start": 0.194,
              "end": 1.18,
              "label": "hungry"
            }
          ]
        },
     Note that "location", "format" and "active_region" must exist! Refer to data/example.json.
   - Use audacity to calculate "start"/"end" field in "active_region", verify the label is correct!
     This is most important step
   - Run our scr_check_json.py script to verify if the changes are valid
        python ./src/scr_check_json.py

   - Check in the changes into repository. Note that you MUST pull first before check in.
     You may need to do a merge.

2. How to use audacity to analyze audio?
   - At command line, run "audacity" to start a GUI to run
   - Select "Make a copy" optino without changing original audio
   - Load a wav/mp3/aiff file

3. How to download and organize the audio/video?
   - Download from freesound.org:
         python scripts/scraper_freesound.py
     This script download all the audio files from freesound.org whose label don't include a bunch of 
     keywords, and search by keyword "meow".
   - Download videos from youtube using youtube-dl in command line
         youtube-dl <youtube_page_address>
     e.g.,
         youtube-dl https://www.youtube.com/watch?v=Fzn_AKN67oI

4. How to find difference between two json file?
   - Use the new script scr_notin.py
         python scr_notin.py 1.json 2.json
     It will return all the entries in 1.json which are not in 2.json!

