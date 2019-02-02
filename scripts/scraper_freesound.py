'''
This file is standalone executable to download and rough label on cat's audio downloaded from freesound
It uses the following packages:
    requests: access http
    bs4.BeautifulSoup: parse html
    webdriver: use "chromedriver" to download audio files
'''
from __future__ import print_function
from bs4 import BeautifulSoup 
import requests
import cPickle as pickle
from selenium import webdriver
import os
import subprocess
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

global USER_NAME
global PASSWORD
#global FIREFOX_USER_PF =  os.getenv('FIREFOX_USER_PF_FREESOUND') #path to a special user preference setting of firefox browser (to download media files without asking agreement)
global CHROME_WEBDRIVER
global DOWNLOAD_TO

def get_links(keyword): 
    '''
    Given a search keyword, this function scrape a link list in freesound.org, filters out 
    irrelevant ones using filter_file function
    Input: string (keyword to search on freesound.org)
    Output: list (of download links)
    '''
    #1. Get html pages from freesound.org
    mainpage = 'http://freesound.org/search/?q='+keyword
    s = requests.Session()
    res = s.get(mainpage)
    cookies = dict(res.cookies)
    r = s.get(mainpage, cookies=cookies)
    soup = BeautifulSoup(r.text,'html.parser')
    # there are more than one page returned, lastpage is the page# possible
    lastpg = int(soup.find('li',attrs={'class':'last-page'}).find('a').text)
    download_links=[]
    block_words = blockwords(keyword)
    # 2. Go thru each page to extract link, if they pass blockword check, record them in a list
    for page in range(lastpg):
        pageurl = mainpage+'&page='+str(page+1)+'#sound'
        r_i = s.get(pageurl, cookies=cookies)
        soup_i = BeautifulSoup(r_i.text, 'html.parser')
        listings = soup_i.findAll('div',attrs={'class':'sound_title'})
        k = 0
        for l in listings:
            title = l.find('a', attrs={'class':'title'}).text
            descr = l.find('p', attrs={'class':'description'}).text
            tags = ' '.join(l.find('ul', attrs={'class':'tags'}).text.split())
            text = title + ' / ' + descr + ' / ' + tags
            if sum(map(lambda x: x in text.lower(), block_words)) != 0:
                continue
            # good, find download link and collect them
            r_j = s.get('http://freesound.org'+l.find('a',attrs={'class':'title'})['href'])
            soup_j = BeautifulSoup(r_j.text, 'html.parser')
            download_links.append(('http://freesound.org'+soup_j.find('div',attrs={'id':'download'}).find('a')['href'], text))
            k += 1
        print('{}/{} files collected from page {}'.format(k, len(listings), page))
    print('Total {} links found'.format(len(download_links)))
    return download_links

def blockwords(key): #returns a list of block words for the search keyword
    if key == 'meow':
        # This list is used temporarily to filter some files irrelevant (or poorly tagged) for my search term 'meow'.
        # User should use their own filter (or none) that fits their purpose.
        fake = ['human','my voice','speed','loop','synth','transform','alter','distort','stereo',
                'instrument','doppler','mix','simulate','ring','tone','electric','effect','imitated',
                'manipulate','imitating','fake','speak']
        othernoise = ['background','dog','bark','child','people','scratch','ambient','ambience','city',
                      'car','eating','feeding','rain','water','clap','jungle','bird']
        stupid = ['mom','nya','silly','crazy','wife','mystery','school','paw','me meowing','me making',
                  'play','box','creepy','iphone','compilation','video','shadow','ailien','space']
        ambiguity = ['purr','hiss','heat','wildcat','fight','squeal','squeak','nervous','scream',
                     'irritated','fear','growl','howl']
    return fake + othernoise + stupid + ambiguity

def filter_file(listings, blocklist):
    rightlinks=[]
    for item in listings:
        title = item.find('a', attrs={'class':'title'}).text #title
        description = item.find('p', attrs={'class':'description'}).text
        tags = ' '.join(item.find('ul', attrs={'class':'tags'}).text.split())
        all_texts = title +' '+ description +' '+ tags
        if sum(map(lambda x: x in all_texts.lower(), blocklist)) == 0:
            # No words in the blocklist, then we keep it
            rightlinks.append('http://freesound.org'+item.find('a',attrs={'class':'title'})['href'])
    return rightlinks

def testlogin(browser=None): #testing loging in selenium+firefox and selenium+chrome. Firefox needs cumtom profile setup for auto-download
    if browser == 'chrome':
        #Chrome downloads without asking.
        driver = webdriver.Chrome(CHROME_WEBDRIVER)
    else:
        #Use default firefox browser (empty preference)
        driver = webdriver.Firefox()
    loginpg = 'http://freesound.org/home/login/?next=/'
    driver.get(loginpg)
    user = driver.find_element_by_name('username')
    user.click()
    user.send_keys(USER_NAME)
    pwrd = driver.find_element_by_name('password')
    pwrd.click()
    pwrd.send_keys(PASSWORD)
    driver.find_element_by_xpath("//input[@value='login'][@type='submit']").click()
    return driver

def download(download_links, tag): 
    '''
    Download audio file contents (log-in required) using selenium+chromedriver
    '''
    download_dir = os.path.join(DOWNLOAD_TO, tag)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    ## chrome browser launch
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : download_dir}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=CHROME_WEBDRIVER, chrome_options=chromeOptions)
    ## freesound.org log in
    loginpg = 'http://freesound.org/home/login/?next=/'
    driver.get(loginpg)
    user = driver.find_element_by_name('username')
    user.click()
    user.send_keys(USER_NAME)
    pwrd = driver.find_element_by_name('password')
    pwrd.click()
    pwrd.send_keys(PASSWORD)
    driver.find_element_by_xpath("//input[@value='login'][@type='submit']").click()
    with open(os.path.join(download_dir, 'data.json'), 'w') as jf:
        print('[', file=jf)
        i=0
        last_link, last_text = '', ''
        for link, text in download_links:
            driver.get(link)
            if i != 0:
                print_json(jf, False, last_link, last_text, download_dir)
            i+=1
            last_link, last_text = link, text
        print_json(jf, True, last_link, last_text, download_dir)
        print('{} files downloaded'.format(i))
        print(']', file=jf)

    # sleep for 60 seconds to wait for all downloads to finish. this step is important!
    time.sleep(60)

def print_json(f, last, link, desc, download_dir, formats='audio', species='cat'):
    filename = link.split('/')[-1]
    print('  {', file=f)
    print('    "location": "{}",'.format(os.path.join(download_dir,filename)), file=f)
    print('    "website": "{}",'.format(link), file=f)
    print('    "description": "{}",'.format(desc), file=f)
    print('    "species: ": "{}",'.format(species), file=f)
    print('    "race": "",', file=f)
    print('    "gender": "",', file=f)
    print('    "format": "{}",'.format(formats), file=f)
    print('    "active_region": [', file=f)
    print('      {', file=f)
    print('        "start": 0,', file=f)
    print('        "end": 0,', file=f)
    print('        "label": ""', file=f)
    print('      }', file=f)
    print('    ]', file=f)
    if last:
        print('  }', file=f)
    else:
        print('  },', file=f)

def rename(directory,tag): #rename audio files and save the name change log as pickle
    fileslist = os.listdir(directory)
    newfileslist=map(lambda i: tag+ '_' + str(i) + '.' + fileslist[i].split('.')[1],range(len(fileslist)))
    log = zip(fileslist,newfileslist)
    with open( 'renamed_'+tag+'.pkl', "w" ) as f:
        pickle.dump(log, f)
    print(directory)
    for old, new in log:
        os.rename(directory+'/'+old,directory+'/'+new)
    print('rename done')

def convert2wav(directory): # convert non-.wav audio files to .wav files using ffmpeg
    audioformats = ['mp3','flac','ogg','aiff','aif']
    fileslist = os.listdir(directory)
    bashCommandlist = filter(None,map(lambda name: 'ffmpeg -i '+ directory + '/'+ name + ' -ar 22050 -ac 1 '+ directory+'/'+ name.split('.')[0]+'.wav' if str(name.split('.')[1]) in audioformats else None, fileslist))
    for command in bashCommandlist:
        subprocess.check_output(['bash','-c', command])
    print('.wav convert done')

def movewavfiles(subdirectory): #move all .wav files into a subfolder named wav.
    # example: movewavfiles('data/freesound/test')
    cwd = os.getcwd()
    if not os.path.isdir(subdirectory+'/wav'):
        os.makedirs(subdirectory+'/wav')
    command = 'mv '+cwd+'/'+subdirectory+'/*.wav '+cwd+'/'+subdirectory+'/wav/'
    print(command)
    subprocess.check_output(['bash','-c', command])
    print('wav files moved')
    print('current directory: ', os.getcwd())

if __name__ == '__main__':

    USER_NAME = 'wevinai'
    PASSWORD = 'wevinai0'
    CHROME_WEBDRIVER = '/usr/bin/chromedriver'
    DOWNLOAD_TO = '/hdd/mlrom/Data/animal_voice/downloads/freesound/'

    links = get_links('meow')
    download(links,'meow')

