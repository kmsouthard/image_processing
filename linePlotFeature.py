from backgroundSubtraction import background_subtraction
from backgroundSubtraction import plot_summary
from backgroundSubtraction import save_output
from backgroundSubtraction import segmentation_FA
from backgroundSubtraction import segmentation_snap
from measureProperties import label_image, label_image_roi

from decimal import Decimal
from functools import partial

import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, opening, square, watershed, ball, dilation
from skimage.measure import regionprops, profile_line
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

def linePlot(labeled_image, image):    
    
    regions = regionprops(labeled_image, intensity_image = image)

    #line plots data frame set up
    line_plots = pd.DataFrame()
    
    for props in regions:
        y0, x0 = props.centroid
        orientation = props.orientation
        x1 = x0 - math.sin(orientation) * props.minor_axis_length
        y1 = y0 - math.cos(orientation) * props.minor_axis_length
        x2 = x0 + math.sin(orientation) * props.minor_axis_length
        y2 = y0 + math.cos(orientation) * props.minor_axis_length
        
        line = profile_line(image, (y1, x1), (y2,x2))
        line_len = len(line)
        indx = range(line_len)
        indx = np.array(indx) / float(line_len-1)
        indx = indx.round(2)
        temp = pd.Series(line, index = indx)
        temp_df = temp.to_frame(name = 'Intensity')
        temp_df.loc[:,'label'] = pd.Series(([props.label]*line_len), index = temp_df.index)
        line_plots = line_plots.append(temp_df)
        
    line_plots['Intensity'] /= image.max()
    
    return line_plots


fn ="Snap-2019-Image Export-01_c1_ORG.tif"
radius = 2
height = 0.65
minSize1 = 20
minSize2 = 200

path = "/Users/southk/dataAnalysis/Focal Adhesion Analysis/output/"

backSub = background_subtraction(fn, radius, height)
plot_summary(backSub, fn, path)
save_output(backSub, fn, path)
mask = segmentation_FA(backSub, fn, path, minSize1)
image = backSub['hdome']

fn_snap= "Snap-2019-Image Export-01_c2_ORG.tif"
backSub_snap = background_subtraction(fn_snap, 2, 0.85)
plot_summary(backSub_snap, fn_snap, path)
save_output(backSub_snap, fn_snap, path)
image_snap = backSub_snap['hdome']
mask2 = segmentation_snap(backSub_snap, fn_snap, path, minSize2)

labeled_FA = label_image(mask)
labeled_FA_SNAP = label_image_roi(mask, mask2)
output_FA = linePlot(labeled_FA, image)
output_FA_SNAP= linePlot(labeled_FA_SNAP, image)

