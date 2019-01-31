from __future__ import division
import numpy as np
import cPickle as pickle
import pandas as pd
import librosa
import math
import os
import json

global DATA_CTRL_FILE
global DEST_DIR

def preprocess_data(**kwargs):
    """Create mfcc matrix dataset for all files
    INPUT
        fft_win: fft window width in ms when calculating mfcc (default: 25)
        fft_hop: fft slide in ms when calculating mfcc (default: 10)

    More args customizabl in the subfuction windowcut
        dur: slice width of a time series signal in second (default: 1)
        discard_short: discard the time series data if it's shorter than slice width you want (default: True).
    """
    duration = kwargs['dur']
    fft_win = kwargs['fft_win']
    fft_hop = kwargs['fft_hop']
    n_mfcc = kwargs['n_mfcc']


    subdir = '_'.join(['dur'+str(duration).replace('.','p'),
                       'win'+str(fft_win).replace('.','p'),
                       'hop'+str(fft_hop).replace('.','p'), 'mfcc'+str(n_mfcc)])
    DEST_DIR = os.path.join(os.getcwd(), 'data', subdir)

    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    with open(DATA_CTRL_FILE, 'r') as f:
        dcf = json.load(f)
        ext = '.npy'
        for audio in dcf:
            assert 'format' in audio, 'Unknown "format" in {}'.format(audio)
            if audio['format'] != 'audio':
                continue
            assert 'location' in audio, 'Missing "location" in {}'.format(audio)
            assert 'active_region' in audio, 'Missing "active_region" in {}'.format(audio)
            if len(audio['active_region']) == 0:
                print 'Warning: active_region is empty in {}'.format(audio)
                continue
            audio_file = audio['location']
            try:
                y, sr = librosa.load(audio_file)
            except:
                print 'librosa failed on file {}'.format(audio_file)
                quit()
            k = 0
            y_norm = y/(abs(y).max())
            n_fft = int(round(fft_win/1000 * sr))
            hop_length = int(round(fft_hop/1000 * sr))
            for ar in audio['active_region']:
                i, j = int(ar['start']*sr), int(ar['end']*sr)
                if j - i <= duration * sr:
                    y_seg = cut_window(y=y_norm, frm=i, to=j, sr=sr, dur=duration, discard_short=kwargs['discard_short'])
                    savename = '_'.join([audio_file.basename().split('.')[0], 'k'+str(k)])
                    save_mfcc(save_to=os.path.join(DEST_DIR, savename+ext), y=y_seg, sr=sr, n_mfcc=n_mfcc,
                              n_fft=n_fft, hop_length=hop_length)
                else:
                    m=0
                    cut = lambda x: int((2*x+1)*duration*sr/2)
                    # old ill-performance code
                    #slices = filter(None, map(lambda n: (int(i+cut(n)-cut(0)),int(i+cut(n)+cut(0))) 
                    #                          if i+cut(n)<j else None, range(int(math.ceil(duration*sr)))))
                    slices = filter(None, map(lambda n: (i+cut(n)-cut(0), i+cut(n)+cut(0)) if i+cut(n)<j else None,
                                              range(int(math.ceil(len(y)/sr)))))
                    for ii, jj in slices:
                        y_seg = cut_window(y=y_norm, frm=ii, to=jj, sr=sr, dur=duration, discard_short = kwargs['discard_short'])
                        savename = '_'.join([os.path.basename(audio_file).split('.')[0],'k'+str(k)+'_'+'m'+str(m)])
                        # print DEST_DIR+savename+ext
                        save_mfcc(save_to=os.path.join(DEST_DIR, savename+ext), y=y_seg, sr=sr, n_mfcc=n_mfcc, 
                                  n_fft = n_fft, hop_length = hop_length)
                        m+=1
                k+=1
        print 'Done'

def save_mfcc(save_to, y, sr, n_mfcc,  **kwargs):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, **kwargs)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
    # Note: although a test showed not much difference, by eye, it seems rescaling each is better.
    #rescale each matrix
    # FIXME
    res = np.array([rescale(mfcc[1:]), rescale(mfcc_delta[1:]), rescale(mfcc_delta2[1:])])
    # FIXME
    #rescale all at once (deltas will be squeezed since mfcc has larger scales)
    #res = rescale(np.array([mfcc[1:],mfcc_delta[1:],mfcc_delta2[1:]]))
    np.save(save_to, res)

def cut_window(y, frm, to, dur=1, sr=22050, discard_short=True):
    """ Returns a slice of y with a specified width
    Parameters:
        y:   audio data in timescale using sampling rate of sr! shape =(n)
        frm: left of active region
        to:  right of active region
        dur: width of window in second
        discard_short: if the data is not enough, what do we do?
    Return:
    """
    if dur*sr < len(y):
        left = (frm + to - dur * sr)/2
        right = left + dur * sr
        if left<0:
            left = 0
            right = round(dur*sr)
        elif right>len(y):
            right = len(y)
            left = right -  round(dur*sr)
        return y[int(left):int(right)]
    else: 
        if discard_short:
            #discard data if total length is smaller than duration we want
            return None
        else: 
            #padd with zeros at the end
            return np.array(np.append(y,np.zeros(round(dur*sr)-len(y))))

def rescale(m):
    #rescale by global max of absolute values
    offset = m.min()
    scale = m.max()-m.min()
    return (m-offset)/scale



if __name__ =='__main__':

    DATA_CTRL_FILE = './data/example.json'
    preprocess_data(dur=1, discard_short = False, fft_win=50, fft_hop=25, n_mfcc=13)

