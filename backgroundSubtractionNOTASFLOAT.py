#!/usr/bin/env python

"""backgroundSubtraction.py: imports tiff image and performs:
1) smoothing
2) background subtraction (regional maxima)
to isolate bright objects on a dark background
converts image to float (0.0 to 1)
input: tiff image, median filter radius
output: summary figure of background subtraction, background subtracted image
"""

__author__      = "Kaden Southard"
__copyright__   = "Copyright 2015, Planet Earth"

import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io

from scipy.ndimage import median_filter 
from skimage import img_as_float
from skimage.morphology import reconstruction

io.use_plugin('tifffile')

#load the image
image = io.imread('/Users/southk/dataAnalysis/Focal Adhesion Analysis/2014.6 pax with all processed/RAW/NICD/Snap-2138-Image Export-08/Snap-2138-Image Export-08_c1_ORG.tif')

#apply median filter with given radius
#radius set to 2 for testing
image = median_filter(image, 2)

#h = 1
#seed = np.copy(image) - h
seed = np.copy(image)
seed[1:-1, 1:-1] = image.min()

mask = image
dilated = reconstruction(seed, mask, method='dilation')
hdome = image - dilated

#background subtracted image is now known as hdome

#write the background subtracted image to file?

fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(10, 5))

yslice = 197

ax1.plot(mask[yslice], '0.5', label='mask')
ax1.plot(seed[yslice], 'k', label='seed')
ax1.plot(dilated[yslice], 'r', label='dilated')
ax1.set_ylim(-0.2, 2)
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
plt.savefig('foo.png')

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(hdome, cmap=plt.cm.gray)
ax.axis('off')
ax.set_title('paxcillin-mcherry')
plt.savefig('bar.png')

plt.imsave('out.tif', hdome, cmap=plt.cm.gray)

#fft_mag = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(hdome)))

#visual = numpy.log(fft_mag)
#visual = (visual - visual.min()) / (visual.max() - visual.min())
#result = hdome.fromarray((visual * 255).astype(numpy.uint8))
#result.save('out.tiff')

from skimage.filters import threshold_adaptive
thresh = threshold_out(hdome, 41, 10)
binary = hdome > thresh

fig, ax = plt.subplots(figsize = (10, 10))
ax.imshow(binary, cmap=plt.cm.gray, interpolation = 'nearest')

from skimage import morphology
cleaned = morphology.remove_small_objects(binary, 10)

fig, ax = plt.subplots(figsize=(4, 3))
ax.imshow(cleaned, cmap=plt.cm.gray, interpolation='nearest')
ax.axis('off')
ax.set_title('Removing small objects')
plt.show()