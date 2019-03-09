'''
Description: Given a list of JSON files, it will:
    1. Check each JSON file's integrity:
        a) Check if each file follows JSON format by loading them;
        b) Check if there are conflicts between JSON files or within JSON files;
        c) Check human mark's correctness;
    2. Merge them by
        a) Ignore those files which are not marked;
        b) Output a unified JSON file by including all valid entries
    Usage:
        python scr_merge_json.py <output.json> <input1.json> <input2.json> ...
Author: Yuan
'''
from __future__ import print_function
import sys
import json
import settings
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def print_active_region(ar, last, f):
    print('      {', file=f)
    print('        "start": {},'.format(ar['start']), file=f)
    print('        "end": {},'.format(ar['end']), file=f)
    print('        "label": "{}"'.format(ar['label']), file=f)
    if last:
        print('      }', file=ojf)
    else:
        print('      },', file=ojf)

def print_entry(e, last, f):
    print('  {', file=ojf)
    print('    "location": "{}",'.format(e['location']), file=f)
    if 'website' in e:
        print('    "website": "{}",'.format(e['website']), file=f)
    else:
        print('    "website": "",', file=f)
    if 'description' in e:
        print('    "description": "{}",'.format(e['description']), file=f)
    else:
        print('    "description": "",', file=f)
    if 'species' in e:
        print('    "species: ": "{}",'.format(e['species']), file=f)
    else:
        print('    "species: ": "",', file=f)
    if 'race' in e:
        print('    "race": "{}",'.format(e['race']), file=f)
    else:
        print('    "race": "",', file=f)
    if 'gender' in e:
        print('    "gender": "{}",'.format(e['gender']), file=f)
    else:
        print('    "gender": "",', file=f)
    print('    "format": "{}",'.format(e['format']), file=f)
    print('    "active_region": [', file=f)
    lar = None
    assert e['active_region'] != 0
    for ar in e['active_region']:
        if lar is not None:
            print_active_region(lar, False, f)
        lar = ar
    print_active_region(lar, True, f)
    print('    ]', file=f)
    if last:
        print('  }', file=f)
    else:
        print('  },', file=f)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: merge_json.py <output_file_name> <input_json1> <input_json2> ...")
    else:
        output_json_file = sys.argv[1]
        audio_dict = {}
        for jf in sys.argv[2:]:
            if jf == output_json_file:
                print('ERROR: Output file cannot be the same as input file {}'.format(jf))
            with open(jf, 'r') as jfp:
                try:
                    l = json.load(jfp)
                except Exception as e:
                    print('ERROR: JSON file {} has syntax errors at {}'.format(jf, e))
                    quit()
            for e in l:
                if 'location' not in e or not e['location']:
                    print('ERROR: "location: field missing in {}'.format(e))
                    quit()
                if 'active_region' not in e or not e['active_region']:
                    print('ERROR: "active_region" field missing in {}'.format(e))
                    quit()
                if 'format' not in e or not e['format']:
                    print('ERROR: "format" field missing in {}'.format(e))
                    quit()
    
                if len(e['active_region']) == 1 and not ('label' in e['active_region'][0] and e['active_region'][0]['label']):
                    # this entry is not labeled yet, ignore them
                    continue
    
                # sort active region data
                e['active_region'].sort(key=lambda ar: ar['start'])
                efilename = e['location'].split('/')[-1]
                # print (e['active_region']['label'])
		for x in e['active_region']:
		    if x['label'] not in settings.all_labels:
		    	for y in settings.all_labels:
			    if y in x['label']:
				x['label'] = y
                if efilename not in audio_dict:
                    audio_dict[efilename] = e
                else: # conflicted entry found, needs further check
                    e1 = audio_dict[efilename]
                    if e['location'] != e1['location'] or e['format'] != e1['format'] or \
                       len(e['active_region']) != len(e1['active_region']):
                        print('ERROR: conflict entry found: filename is {}'.format(efilename))
                    el = [ar['label'] for ar in e['active_region']]
                    e1l = [ar['label'] for ar in e['active_region']]
                    if el != e1l:
                        print('ERROR: Label inconsistent for conflict entries in {}'. format(efilename))
        # Now, audio_dict holds all valid entries, let's output them
        assert len(audio_dict) != 0
        with open(output_json_file, 'w') as ojf:
            print('[', file=ojf)
            lef, le = '', None
            for ef, e in sorted(audio_dict.iteritems()):
                if lef:
                    print_entry(le, False, ojf)
                lef, le = ef, e
            print_entry(le, True, ojf)
            print(']', file=ojf)
        print('There are {} entries after merge'.format(len(audio_dict)))

