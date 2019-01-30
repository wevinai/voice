'''
Description: check data.json integrity
Author: Yuan
'''
import json
with open('./data/data.json', 'r') as f:
    try:
        l = json.load(f)
    except:
        print('data.json has syntax errors')
        quit()
    for e in l:
        if 'location' not in e:
            print 'location missing in {}'.format(e)
            quit()
        if 'active_region' not in e:
            print '"active_region" missing in {}'.format(e)
            quit()
        if 'format' not in e:
            print 'format missing in {}'.format(e)
            quit()
