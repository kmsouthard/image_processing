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

import skimage.io as io
#io.use_plugin('tifffile')

def background_subtraction(filename, radius, height):
    #load the image
    image = img_as_float(io.imread(filename))
    #apply median filter with given radius
    image = median_filter(image, 2)
    seed = np.copy(image) - height
    mask = image
    dilated = reconstruction(seed, mask, method='dilation')
    hdome = image - dilated

    #background subtracted image is now known as hdome

    #line plot through image, dilated image, background subtracted image
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(10, 5))

    yslice = 197

    ax1.plot(mask[yslice], '0.5', label='mask')
    ax1.plot(seed[yslice], 'k', label='seed')
    ax1.plot(dilated[yslice], 'r', label='dilated')
    ax1.set_ylim(-0.2, 1.2)
    ax1.set_title('image slice')
    ax1.set_xticks([])
    ax1.legend()

    ax2.imshow(dilated, vmin=image.min(), vmax=image.max())
    ax2.axhline(yslice, color='r', alpha=0.4)
    ax2.set_title('dilated')
    ax2.axis('off')

    ax3.imshow(hdome)
    ax3.axhline(yslice, color='r', alpha=0.4)
    ax3.set_title('image - dilated')
    ax3.axis('off')

    fig.tight_layout()
    #save summary image
    plt.savefig('foo.png', format='png')

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(hdome, cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('paxcillin-mcherry')
    plt.savefig('bar.png')

    plt.close('all')

    io.use_plugin('freeimage')
    im = hdome
    im = exposure.rescale_intensity(im, out_range='float')
    im = img_as_uint(im)

    io.imsave('test_16bit.tif', im)
    return
   
#filename ="Snap-2066-Image Export-01_c1_ORG.tif"
#radius = 2
#height = 0.90

#background_subraction(filename, radius, height)