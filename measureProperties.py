from backgroundSubtraction import background_subtraction
from backgroundSubtraction import plot_summary
from backgroundSubtraction import save_output
from backgroundSubtraction import segmentation_FA

import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, opening, square, watershed, ball, dilation
from skimage.measure import regionprops
from skimage.color import label2rgb

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage.morphology import watershed
from skimage.feature import peak_local_max

fn ="Snap-2237-Image Export-04_c1_ORG.tif"
radius = 2
height = 0.7
minSize = 20

path = "/Users/southk/dataAnalysis/Focal Adhesion Analysis/output/"

backSub = background_subtraction(fn, radius, height)
plot_summary(backSub, fn, path)
save_output(backSub, fn, path)
image = segmentation_FA(backSub, fn, path, minSize)

#clean up binary image
bw = closing(image, square(2))

#remove artifacts connected to image border
cleared = bw.copy()
clear_border(cleared)

#label image regions
#distance = ndi.distance_transform_edt(cleared)
#
#local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((4, 4)),
#                            labels=cleared)
#markers = ndi.label(local_maxi)[0]
#labels = watershed(-distance, markers, mask=cleared)
#
label_image = label(cleared)
borders = np.logical_xor(bw, cleared)
label_image[borders] = -1
image_label_overlay = label2rgb(label_image, image=image)

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
ax.imshow(image_label_overlay)

for region in regionprops(label_image):
    # skip small images
    if region.area < 10:
       continue
    
    #draw rectangle around segmented coins
    minr, minc, maxr, maxc = region.bbox
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

plt.show()

regions = regionprops(label_image, intensity_image = backSub['hdome'])

fig, ax = plt.subplots()
ax.imshow(image, cmap=plt.cm.gray)

import math
import matplotlib.pyplot as plt
import numpy as np

from skimage.draw import ellipse
from skimage.measure import label, regionprops
from skimage.transform import rotate
import pandas as pd

#properites data frame set up
properties = []
columns = ('x', 'y', 'Intensity', 'radius', 'area')
indices = []
min_radius = 0
max_radius = 600

for props in regions:
    #plot regions
    y0, x0 = props.centroid
    orientation = props.orientation
    x1 = x0 + math.cos(orientation) * 0.5 * props.major_axis_length
    y1 = y0 - math.sin(orientation) * 0.5 * props.major_axis_length
    x2 = x0 - math.sin(orientation) * 0.5 * props.minor_axis_length
    y2 = y0 - math.cos(orientation) * 0.5 * props.minor_axis_length

    ax.plot((x0, x1), (y0, y1), '-r', linewidth=2.5)
    ax.plot((x0, x2), (y0, y2), '-r', linewidth=2.5)
    ax.plot(x0, y0, '.g', markersize=15)

    minr, minc, maxr, maxc = props.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax.plot(bx, by, '-b', linewidth=2.5)
    
    #add properites to data frame
    radius = (props.area / np.pi)**0.5
    if (min_radius  < radius < max_radius):
        properties.append([props.centroid[0],
                            props.centroid[1],
                            props.mean_intensity*props.area,
                            radius,
                            props.area])
        indices.append(props.label)
if not len(indices):
    all_props = pd.DataFrame([], index=[])
indices = pd.Index(indices, name='label')
properties = pd.DataFrame(properties, index=indices, columns=columns)
properties['Intensity'] /= properties['Intensity'].max()

ax.axis((0, 484, 511, 0))
plt.show()