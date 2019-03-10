'''
Description: Analyze uses generated features from preprocess_data.py (MFCC coefficients), 
    assuming all data is stored in subdirectories of settings.data_dir, and the file name 
    should include the label information
Usage:
    python analyze_data.py -d <which_run_directory> <-v #> <-m pca/tsne> <-a video_filename>
'''
import settings
import sys
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import mglearn
import cPickle as pickle
from mpl_toolkits.mplot3d import Axes3D, axes3d

def show(X, Y, Y_names, labels, dim=2):
    if dim == 2:
        label_id = []
        mask = np.zeros(Y.shape, dtype=bool)
        if len(labels) == 0:
            label_id = range(len(settings.all_labels))
            mask = np.ones(Y.shape, dtype=bool)
        else:
            for l in labels:
                idx = settings.all_labels[l]
                mask = np.logical_or(mask, Y==idx)
                label_id.append(idx)
            label_id.sort()

        # show in 2D
        plt.figure(figsize=(8,8))
        mglearn.discrete_scatter(X[mask,0], X[mask,1], Y[mask])
        plt.legend(Y_names[label_id], loc='best')
        plt.gca().set_aspect('equal')
        plt.xlabel('1st PCA')
        plt.ylabel('2nd PCA')
        plt.show()
    else:
        figure = plt.figure()
        ax = Axes3D(figure, elev=-152, azim=-26)
        colors = ['r', 'b', 'g']
        shapes = ['o', '^', 'x']
        sel = 0
        for l in labels:
            mask = Y == settings.all_labels[l]
            ax.scatter(X[mask,0], X[mask,1], X[mask,2], c=colors[sel%3], marker=shapes[sel//3], 
                       cmap=mglearn.cm2, s=60)
            sel += 1
        ax.set_xlabel('1st PC')
        ax.set_ylabel('2nd PC')
        ax.set_zlabel('3rd PC')
        plt.show()

def analyze(data_dir, view_dim=2, method='pca', output=''):
    files = os.listdir(data_dir)
    label_count = {}
    X, Y = np.empty((0, 12, 41)), np.empty((0))
    Y_names = np.empty((len(settings.all_labels)), dtype='S10')
    for l, idx in settings.all_labels.iteritems():
        Y_names[idx] = l
    for f in files:
        if not f.endswith('.npy'):
            continue
        fname_ext = os.path.basename(f).split('____')
        assert fname_ext[1] in settings.all_labels, 'Label is not seen: {}'.format(f)
        if fname_ext[1] not in label_count:
            label_count[fname_ext[1]] = 1
        else:
            label_count[fname_ext[1]] += 1
        f_ = os.path.join(data_dir, f)
        x = np.load(f_)
        assert x.shape==(3, 12, 41), 'shape is incorrect ({}) in file {}'.format(x.shape, f)
        # We only consider the first row now!
        X = np.concatenate((X, x[[0]]))
        Y = np.concatenate((Y, [settings.all_labels[fname_ext[1]]]))

    # Basic statistics
    print('Statistics on labels:')
    for l in settings.all_labels:
        if l not in label_count:
            print('    Label ({}): 0'.format(l))
        else:
            print('    Label ({}): {}'.format(l, label_count[l]))

    if method == 'pca':
        # Use PCA dimension reduction to see data difference
        X_ = X.reshape(X.shape[0], X.shape[1]*X.shape[2])
        pca = PCA(n_components=view_dim)
        pca.fit(X_)
        X_twst = pca.transform(X_)
    elif method == 'tsne':
        X_ = X.reshape(X.shape[0], X.shape[1]*X.shape[2])
        tsne = TSNE(n_components=view_dim, verbose=1, perplexity=40, n_iter=300)
        X_twst = tsne.fit_transform(X_)
    else:
        print('ERROR: Analysis method is not supported')
        quit()
    assert X_twst.shape == (X.shape[0], view_dim)

    # Dump data for other investigation
    if output:
        result = {
            'X': X_twst,
            'Y': Y,
        }
        with open(output, 'wb') as f:
            pickle.dump(result, f)
    else:
        show(X_twst, Y, Y_names, [], dim=view_dim)
        #show(X_twst, Y, Y_names, ['happy', 'hiss'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['happy', 'scream'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['happy', 'sneeze'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['happy', 'complain'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['scream', 'hiss'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['attention', 'happy'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['attention', 'hiss'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['attention', 'scream'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['attention', 'sneeze'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['scream', 'sneeze'], dim=view_dim)
        #show(X_twst, Y, Y_names, ['scream', 'complain'], dim=view_dim)

if __name__ =='__main__':
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--data_dir', help='Directory which holds *.npy under {}'.format(settings.data_dir),
                        default='', dest='dir')
    parser.add_argument('-v', '--view_dim', help='Reduce-to dimension',
                        default=2, dest='dim')
    parser.add_argument('-m', '--method', help='Reduction method (only supports pca/tsne)',
                        default='pca', dest='method')
    parser.add_argument('-o', '--output', help='Instead to showing, we output data for future use',
                        default='', dest='output')
    args = parser.parse_args()
    if args.dir:
        my_dir = os.path.join(settings.data_dir, args.dir)
    if not os.path.isdir(my_dir):
        print('ERROR: Data directory is incorect: {}'.format(my_dir))
    analyze(my_dir, view_dim=int(args.dim), method=args.method, output=args.output)

