# -*- coding: utf-8 -*-
'''
Description: This file defines global constants/variables for all scripts/software
Author: Yuan
'''
from __future__ import print_function
#from sets import Set

# Sets
old_labels = {'hungry':0, 'happy':1, 'upset':2, 'annoy':3, 'angry':4, 'complain':5, 'comfortable':6, 'pain':7, 'attention':8, 
              'beg':9, 'sick':10, 'scared':11}
old_labels_20190320 = {'purring':0, 'attention':1, 'sneeze':2, 'hiss':3, 'scream':4, 'happy':5, 'complain':6, 'growl':7, 'unknown':8}
#all_labels = {'purring':0, 'attention':1, 'sneeze':2, 'hiss':3, 'scream':4, 'happy':5, 'complain':6, 'growl':7, 'unknown':8}

# The following cat vocal types are defined by Susanne Schötz from http://vr.humlab.lu.se/projects/meowsic/catvoc.html
# except that we add "sneeze" when cats are sick! Please also refers to Wikipedia for further information:
# https://en.wikipedia.org/wiki/Cat_communication
all_labels = {
              'chatter': 0,  # chirp/prey-directed sound, a hunting instinct where cats copy the calls of their prey
                             # HuntingMind
              'growl':   1,  # a guttural low-pitched sound of long duration produced during a slow steady 
                             # exhalation, [grrr..] with a vocalic [rrr...] or rhotic [ʌ], occasionally 
                             # beginning with an [m]. Used to signal danger or to warn or scare off an opponent,
                             # often intertwined with howls/moans/yowls and hisses.
                             # Warning
              'hiss':    2,  # involuntary reactions to when a cat is surprised by an (apparent) enemy
                             # old_labels_20190320.hiss
              'howl':    3,  # long and repeated vocalic warning signals produced by gradually opening the mouth 
                             # wider and closing it again. During a threatening situation, they are often merged 
                             # or combined with by growls in long sequences with slowly varying tone (melody) and 
                             # intensity!
                             # old_labels_20190320.{attention, complain} may be some scream
              'meow':    4,  # can be assertive, plaintive, friendly, bold, welcoming, attention soliciting, 
                             # demanding, or complaining, sad, or even be silent
                             # old_labels_20190320.{attention, happy, complain}
              'purring': 5,  # low-pitched regular sound when cat is content, hungry, stressed, in pain, 
                             # gives birth or is dying, produced by mouth closed!
                             # old_labels_20190320.purring
              'scream':  6,  # snarl, scream, cry, and pain shriek
                             # old_labels_20190320.scream
              'sneeze':  7,  # similar to human sneeze when cat is sick
                             # old_labels_20190320.sneeze
              'trill':   8,  # a short and often soft meow rolled on the tongue, produced by mouth closed, usually
                             # high pitched. Trill is an effort to get you to pay attention to her or as a way 
                             # to get you to check out something she deems important. Chirrups and squeaky little 
                             # trills might also happen when a cat is excited and happy.
              'call':    9,  # Mating call/mating cry, long sequences of meow-like sounds, sometimes similar to 
                             # howling and/or the cries of human infants, usually in spring during mating season.
                             # new label sound
              'unknown':10,  # sound that we are not sure, need further investigation
              'mew':    41,  # a high-pitched meow with [i], [ɪ] or [e] quality; kittens may use it to 
                                  # solicit attention from their mother, and adult cats may use it when they 
                                  # are sad or in distress or when they signal submissiveness 
              'squeak': 42,  # raspy nasal high-pitched mew-like call
              'moan':   43,  # with [o] or [u] vowel, often when sad or demanding
              'miaow' : 44   # combination of vowels resulting in the characteristic [iau] sequence, 
                             # often used in cat-human communication to solicit food or to pass an obstacle 
                             # (e.g. a closed door or window) Adult cats mainly meow to humans, and seldom 
                             # to other cats, so adult meow could be a post-domestication extension of 
                             # mewing by kittens
                             #
                             # short merow/mew (mew/miaow): standard greeting. "hello!"
                             # Multiple meows/mews (mew/miaow): Excited greeting. "Great to see u!"
                             # Mid-pitch meow (miaow?): Plea for sth. "I'd like to eat."
                             # Drawn-out mrrrrooow (?): Demand for sth. "Open the door now!"
                             # Low-pitch mrrrroooowwww (moan) : complaint of a wrong u have done.
                             # High-pitch RRRROWW! (squeak): Anger or pain.
}

# tuples
all_formats = ('.wav', '.mp3', '.aiff', '.aif', '.au', '.flac', '.m4a', '.mp4', '.webm', '.mkv')

data_dir = '/hdd/mlrom/Data/animal_voice'
