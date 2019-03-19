
from __future__ import print_function
import os
import sys
import json
#import settings

jf = sys.argv[1]
with open(jf, 'r') as f:
    l = json.load(f)
    total_audio, total_seg, total_time = 0, 0, 0
    aud, seg, length, pitch = {}, {}, {}, {}
    found_dict = {}
    for e in l:
        if 'location' in e:
	    total_audio += 1
	for x in found_dict:
	    found_dict[x] = False
	for ar in e['active_region']:
	    total_seg += 1
	    total_time += ar['end'] - ar['start']
	    if ar['label'] not in aud:
		aud[ar['label']] = 0
	    if ar['label'] not in seg:
		seg[ar['label']] = 0
	    if ar['label'] not in length:
		length[ar['label']] = 0
	    if ar['label'] not in pitch:
		pitch[ar['label']] = 0
	    seg[ar['label']] += 1
	    length[ar['label']] += ar['end'] - ar['start']
	    if ar['label'] not in found_dict or found_dict[ar['label']] == False:
		aud[ar['label']] += 1
		found_dict[ar['label']] = True
print("Total audios : {}".format(total_audio))
print("Total segments : {}".format(total_seg))
print("Total length : {}".format(total_time))
for i, j in found_dict.items():
    print("Label '{}':".format(i))
    print("Number of audios: {}".format(aud[i]))
    print("Number of segments: {}".format(seg[i]))
    print("Total length: {}".format(length[i]))
