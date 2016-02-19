import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import pims
import trackpy as tp
from trackpy.utils import fit_powerlaw

import os
import fnmatch

mpl.rc('figure',  figsize=(10, 6))
mpl.rc('image', cmap='gray')


path = '/Users/southk/Desktop/dEGF movies/140620'

pattern = '*.tif'
radius = 11
threshold = 100
minMass = 10000
memory = 3
maxTravel = 5 

meanMass = 150000
meanSize = 2.6

i= 0

for (path, dirs, files) in os.walk(path):
    for filename in fnmatch.filter(files, pattern):
        print filename
        i += 1
        frames = pims.TiffStack(os.path.join(path, filename), as_grey = True)
        #locate particles
        particles = tp.batch(frames[1:600], radius, minMass, threshold)
        #link particles in trajectories
        tracks = tp.link_df(particles, maxTravel, memory)
        #filter out short trajectories
        t1 = tp.filter_stubs(tracks, 20)
        print 'Before:', tracks['particle'].nunique()
        print 'After:', t1['particle'].nunique()
        
        #filter based on mean trajectory apperence
        condition = lambda x: (x['mass'].mean() > 150000) & (x['size'].mean() < 2.6)
        t2 = tp.filter(t1, condition)  # a wrapper for pandas' filter that works around a bug in v 0.12
        print 'Before:', t1['particle'].nunique()
        print 'After:', t2['particle'].nunique()
        
        #filter based on diagonal size of trajectory
        t3 = t2.groupby('particle').filter(lambda x: tp.diagonal_size(x) > 5)
        print 'Before:', t2['particle'].nunique()
        print 'After:', t3['particle'].nunique()
        t3.to_csv(path+'traj'+filename[:-4]+'.csv')
        
        #save for MTracker compatability
        cols = ['x', 'y', 'signal','mass', 'size', 'frame', 'particle', 'ecc', 'ep']
        t4 = t3[cols]
        t4.to_csv(path+'traj'+filename[:-4]+'dat', sep = '\t', index = False)
        
        
        #plot trajectories
        ax = plt.axes().set_aspect('equal')
        tp.plot_traj(t3)
        plt.savefig(path+'traj'+filename[:-4]+'.png', format='png')
        plt.close('all')
        
        #plot individual MSDs
        im = tp.imsd(t3, 0.133, 20)  # microns per pixel = 100/133., frames per second = 50
        im.to_csv(path+'iMSD'+filename[:-4]+'.csv')
        
        im.plot(loglog=True, style='k-', alpha=0.1, legend=False)  # black lines, semitransparent, no legend
        plt.gca().set_ylabel(r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]');
        plt.savefig(path+'imMSD'+filename[:-4]+'.png', format='png')
        plt.close('all')
        
        #plot ensemble MSD
        em = tp.emsd(t3, 0.133, 20, max_lagtime = 8)
        ax = em.plot(loglog=True, style='o')
        ax.set(ylabel=r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]', xlabel='lag time $t$')
        ax.set(ylim=(1e-2, 2))
        plt.savefig(path+'emMSD'+filename[:-4]+'.png', format='png')
        plt.close('all')
        
        fit = fit_powerlaw(em, plot = False)
        fit.to_csv(path+'eMSDfit'+filename[:-4]+'.csv') 
        
        
        
        