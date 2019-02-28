'''
Description: List all entries in 1.json which are not listed in 2.json
    Usage is
        python scr_notin.py 1.json 2.json
Author: Yuan
'''
from __future__ import print_function
import sys
import json
import settings
import os
from sets import Set

def find_notin(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        try:
            l1 = json.load(f1)
        except Exception as ex:
            print('ERROR: JSON file {} has syntax erros {}'.format(file1, ex))
            quit()
        try:
            l2 = json.load(f2)
        except Exception as ex:
            print('ERROR: JSON file {} has syntax erros {}'.format(file2, ex))
            quit()
        wavf = {os.path.basename(e['location']) for e in l2}
        print('Entries in {} which is not in {}'.format(file1, file2))
        for e in l1:
            if os.path.basename(e['location']) not in wavf:
                print('  {}'.format(e['location']))

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print('Usage: python scr_notin.py <1.json> <2.json>')
        quit()
    if not os.path.isfile(sys.argv[1]):
        print('ERROR: JSON file {} does not exist'.format(sys.argv[1]))
    if not os.path.isfile(sys.argv[2]):
        print('ERROR: JSON file {} does not exist'.format(sys.argv[2]))

    find_notin(sys.argv[1], sys.argv[2])
