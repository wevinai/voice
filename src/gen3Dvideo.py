'''
Description: 
Usage:
    python view3D.py <pickle file which holds X/Y/Y_names information>
'''
import settings
import sys
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import cPickle as pickle
from mpl_toolkits.mplot3d import Axes3D, axes3d

if len(sys.argv) < 3:
    print('Usage: python gen3Dvideo.py <X_Y.pkl> <label1> <label2> ...')
    print('    Or python gen3Dvideo.py <X_Y.pkl> all')
    quit()

f = open(sys.argv[1], 'r')
d = pickle.load(f)
X, Y = d['X'], d['Y']
#print('X.shape={} Y.shape={}'.format(X.shape, Y.shape))
assert X.ndim==2 and Y.ndim==1 and X.shape[0]==Y.shape[0] and X.shape[1] == 3
fig = plt.figure()
ax = Axes3D(fig)
colors = ['r', 'b', 'g', 'y', 'k', 'm', 'c', 'w']
shapes = ['o', '^', 'x']
if sys.argv[2] == 'all':
    labels = settings.all_labels
else:
    labels = sys.argv[2:]
output_file = '_'.join(labels) + '.mp4'

Y_names = np.empty((len(settings.all_labels)), dtype='S10')
for l, idx in settings.all_labels.iteritems():
    Y_names[idx] = l
label_id = []
for l in labels:
    assert l in settings.all_labels
    label_id.append(settings.all_labels[l])
label_id.sort()

def init():
    sel = 0
    for l in labels:
        mask = (Y == settings.all_labels[l])
        ax.scatter(X[mask,0], X[mask,1], X[mask,2], c=colors[sel%len(colors)], marker=shapes[sel/len(colors)], s=10)
        sel += 1
    plt.legend(Y_names[label_id], loc='best')
    ax.set_xlabel('1st PCA')
    ax.set_ylabel('2nd PCA')
    ax.set_zlabel('3rd PCA')
    return fig,

def animate(i):
    ax.view_init(elev=10, azim=i)
    return fig,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=360, interval=20, blit=True)
anim.save(output_file, fps=30, extra_args=['-vcodec', 'libx264'])

