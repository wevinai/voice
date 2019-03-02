'''
Description: Analyze generated MFCC data from preprocess_data.py. Assuming all data is stored in subdirectories 
    of settings.data_dir, and the file name should include the label information
Usage:
    python analyze_data.py <which_run_directory>
'''
import settings
import sys
import os
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import mglearn
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


def analyze(data_dir):
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

    X_ = X.reshape(X.shape[0], X.shape[1]*X.shape[2])
    pca = PCA(n_components=3)
    pca.fit(X_)
    X_pca = pca.transform(X_)
    assert X_pca.shape == (X.shape[0], 3)

    #show(X_pca, Y, Y_names, ['happy', 'upset'], dim=2)
    #show(X_pca, Y, Y_names, ['happy', 'angry'], dim=2)
    show(X_pca, Y, Y_names, [], dim=2)
    show(X_pca, Y, Y_names, ['happy', 'upset'], dim=2)
    show(X_pca, Y, Y_names, ['happy', 'scared'], dim=2)
    show(X_pca, Y, Y_names, ['happy', 'pain'], dim=2)
    show(X_pca, Y, Y_names, ['happy', 'complain'], dim=2)
    show(X_pca, Y, Y_names, ['happy', 'annoy'], dim=2)
    show(X_pca, Y, Y_names, ['attention', 'hungry'], dim=2)
    show(X_pca, Y, Y_names, ['attention', 'beg'], dim=2)
    show(X_pca, Y, Y_names, ['happy', 'beg'], dim=2)

    #for (label, cnt) in label_count.iteritems():
    #     print('Label ({}): {}'.format(label, cnt))
    for l in settings.all_labels:
        if l not in label_count:
            print('Label ({}): 0'.format(l))
        else:
            print('Label ({}): {}'.format(l, label_count[l]))

if __name__ =='__main__':
    if len(sys.argv) != 2:
        print('Usage: python analyze_data.py <run_dir_under_settings.data_dir>')
    my_dir = os.path.join(settings.data_dir, sys.argv[1])
    if not os.path.isdir(my_dir):
        print('ERROR: Data directory is incorect: {}'.format(my_dir))
    analyze(my_dir)
