#!/usr/bin/env python

"""backgroundSubtraction.py: imports tiff image and performs:
1) smoothing
2) background subtraction (regional maxima)
to isolate bright objects on a dark background
converts image to float (0.0 to 1)
input: image, median filter radius
output: summary figure of background subtraction, background subtracted image
"""

__author__      = "Kaden Southard"
__copyright__   = "Copyright 2015, Planet Earth"

import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import median_filter 
from skimage import io, exposure, img_as_uint, img_as_float
from skimage.morphology import reconstruction
from skimage.filters import threshold_otsu

import skimage.io as io
#io.use_plugin('tifffile')

#fn ="Snap-2066-Image Export-01_c1_ORG.tif"
#radius = 2
#height = 0.8

def background_subtraction(filename, radius, height):
    #load the image
    image = img_as_float(io.imread(filename))
    #apply median filter with given radius
    image = median_filter(image, radius)
    seed = np.copy(image) - height
    mask = image
    dilated = reconstruction(seed, mask, method='dilation')
    hdome = image - dilated
    
    return {'hdome': hdome, 'mask': mask, 'dilated': dilated, 'seed': seed}    

def plot_summary(im_dict, filename, path):
    #line plot through image, dilated image, background subtracted image
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(10, 5))

    yslice = 197

    ax1.plot(im_dict['mask'][yslice], '0.5', label='mask')
    ax1.plot(im_dict['seed'][yslice], 'k', label='seed')
    ax1.plot(im_dict['dilated'][yslice], 'r', label='dilated')
    ax1.set_ylim(-0.2, 1.2)
    ax1.set_title('image slice')
    ax1.set_xticks([])
    ax1.legend()

    ax2.imshow(im_dict['dilated'], vmin=im_dict['mask'].min(), vmax=im_dict['mask'].max())
    ax2.axhline(yslice, color='r', alpha=0.4)
    ax2.set_title('dilated')
    ax2.axis('off')
    
    ax3.imshow(im_dict['hdome'])
    ax3.axhline(yslice, color='r', alpha=0.4)
    ax3.set_title('image - dilated')
    ax3.axis('off')
    
    fig.tight_layout()
    #save summary image
    plt.savefig(path+'summary'+filename[:-4]+'.png', format='png')
    plt.close()
    return

def save_output(im_dict, filename, path):
    io.use_plugin('freeimage')
    im = im_dict['hdome']
    im = exposure.rescale_intensity(im, out_range='float')
    im = img_as_uint(im)
    io.imsave(path+'output'+filename[:-4]+'.png', im)
    return
    
def segmentation(im_dict, filename, path):
    io.use_plugin('freeimage')
    thresh = threshold_otsu(im_dict['hdome'])
    binary = im_dict['hdome'] > thresh
    io.imsave(path+'binary'+filename[:-4]+'.png', binary)
    return

#bs=  background_subtraction(fn, radius, height)
#plot_summary(bs, fn)
#save_output(bs, fn)
  
#filename ="Snap-2066-Image Export-01_c1_ORG.tif"
#radius = 2
#height = 0.90

#background_subraction(filename, radius, height)