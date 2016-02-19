from backgroundSubtraction import background_subtraction
from backgroundSubtraction import plot_summary
from backgroundSubtraction import save_output
from backgroundSubtraction import segmentation_FA
from backgroundSubtraction import segmentation_snap

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

import math
import matplotlib.pyplot as plt
import numpy as np

from skimage.draw import ellipse
from skimage.measure import label, regionprops
from skimage.transform import rotate
import pandas as pd

#script needs to take in image and return measurements of properites: focal adhesion area
#fluoresence intensity FAs, Fluoresence intensity SNAP tag at FAs (mean or median?)
#normalized FAs
#number of FA per cell
# total FA area per cell, total FA area normalized to cell area
#
#fn ="Snap-2019-Image Export-01_c1_ORG.tif"
#radius = 2
#height = 0.65
#minSize1 = 20
#minSize2 = 200
#
#path = "/Users/southk/dataAnalysis/Focal Adhesion Analysis/output/"
#
#backSub = background_subtraction(fn, radius, height)
#plot_summary(backSub, fn, path)
#save_output(backSub, fn, path)
#mask = segmentation_FA(backSub, fn, path, minSize1)
#image = backSub['hdome']
#
#fn_snap= "Snap-2019-Image Export-01_c2_ORG.tif"
#backSub_snap = background_subtraction(fn_snap, 2, 0.85)
#plot_summary(backSub_snap, fn_snap, path)
#save_output(backSub_snap, fn_snap, path)
#image_snap = backSub_snap['hdome']
#mask2 = segmentation_snap(backSub_snap, fn_snap, path, minSize2)

def label_image(mask):
    #clean up binary image
    bw = opening(mask, square(2))

    #remove artifacts connected to image border
    cleared = bw.copy()
    clear_border(cleared)

    #label image regions
    labeled_image = label(cleared)
    borders = np.logical_xor(bw, cleared)
    labeled_image[borders] = -1
    return labeled_image

def label_image_roi(mask, roi_mask):
    #clean up binary image
    bw = opening(mask, square(2))
    roi = dilation(roi_mask,square(6))
    
    #remove artifacts connected to image border
    cleared = bw.copy()
    clear_border(cleared)
    mask_image = roi.copy()
    masked = np.logical_and(mask_image, cleared)

    #label image regions
    labeled_image = label(masked)
    borders = np.logical_xor(bw, cleared)
    labeled_image[borders] = -1
    return labeled_image    

def measure_features(labeled_image, image, filename, path):    
    
    image_label_overlay = label2rgb(labeled_image, image=image)

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(image_label_overlay)

    for region in regionprops(labeled_image):   
    #draw rectangle around segmented adhesions
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

    #plt.show()
    plt.savefig(path+'labeled'+filename[:-4]+'.png', format='png')
    regions = regionprops(labeled_image, intensity_image = image)

    #properites data frame set up
    properties = []
    columns = ('x', 'y', 'Intensity', 'radius', 'area')
    indices = []
    min_radius = 0
    max_radius = 600

    for props in regions:
        #add properites to data frame
        radius = (props.area / np.pi)**0.5
        if (min_radius  < radius < max_radius):
            properties.append([props.centroid[0],
                            props.centroid[1],
                            props.mean_intensity,
                            radius,
                            props.area])
            indices.append(props.label)

    if not len(indices):
        all_props = pd.DataFrame([], index=[])
    indices = pd.Index(indices, name='label')
    properties = pd.DataFrame(properties, index=indices, columns=columns)
    properties['Intensity'] /= image.max()
    
    plt.close('all')
    return properties


def measure_features_roi(labeled_image, mask2, image, filename, path):    
    #clean up binary image
    roi = closing(mask2,square(2))

    #remove artifacts connected to image border
    mask_image = roi.copy()
    masked = np.logical_and(mask_image, cleared)

    #label image regions
    label_image = label(masked)
    image_label_overlay = label2rgb(label_image, image=image)
    
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(image_label_overlay)

    for region in regionprops(label_image):   
    #draw rectangle around segmented adhesions
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

    #plt.show()
    plt.savefig(path+'labeled'+filename[:-4]+'.png', format='png')
    regions = regionprops(label_image, intensity_image = image)

    #properites data frame set up
    properties = []
    columns = ('x', 'y', 'Intensity', 'radius', 'area')
    indices = []
    min_radius = 0
    max_radius = 600

    for props in regions:
        #add properites to data frame
        radius = (props.area / np.pi)**0.5
        if (min_radius  < radius < max_radius):
            properties.append([props.centroid[0],
                            props.centroid[1],
                            props.mean_intensity,
                            radius,
                            props.area])
            indices.append(props.label)

    if not len(indices):
        all_props = pd.DataFrame([], index=[])
    indices = pd.Index(indices, name='label')
    properties = pd.DataFrame(properties, index=indices, columns=columns)
    properties['Intensity'] /= image.max()
    
    plt.close('all')
    return properties
#
#labeled_FA = label_image(mask)
#labeled_FA_SNAP = label_image_roi(mask, mask2)
#output_FA = measure_features(labeled_FA, image, fn, path)
#output_FA_SNAP= measure_features(labeled_FA_SNAP, image, fn, path)
#output_SNAP = measure_features_roi(mask, mask2, image_snap, fn_snap, path)

#plt.imshow(output_SNAP)
#plt.show()