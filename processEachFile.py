import os
import fnmatch
from backgroundSubtraction import background_subtraction
from backgroundSubtraction import plot_summary
from backgroundSubtraction import save_output
from backgroundSubtraction import segmentation_FA
from backgroundSubtraction import segmentation_snap
from measureProperties import measure_features, label_image, label_image_roi
from linePlotFeature import linePlot
import pandas as pd

path = '/Users/southk/dataAnalysis/Focal Adhesion Analysis/2014.6 pax with all processed/RAW'

#process channel 1 (paxcillin) background subtraction
#save background subtracted image
#perform segmentation on image
#return binary image (as bool)

pattern1 = '*c1_ORG.tif'
pattern2 = '*c2_ORG.tif'
radius1 = 2
height1 = 0.6
radius2 = 2
height2 = 0.95
i = 0
minSize1 = 15
minSize2 = 200

for (path, dirs, files) in os.walk(path):
    i += 1
    for filename in fnmatch.filter(files, pattern1):
        print filename
        backSub = background_subtraction(os.path.join(path, filename), radius1, height1)
        plot_summary(backSub, filename, path)
        save_output(backSub, filename, path)
        mask = segmentation_FA(backSub, filename, path, minSize1)
        image_FA = backSub['hdome']
        labeled_image_FA = label_image(mask) 
        #props_FA = measure_features(labeled_image_FA, image_FA, filename, path)
        #props_FA.to_csv(path+'FA_props'+filename[:-4]+'.csv')
    for filename in fnmatch.filter(files, pattern2):
        print filename
        backSub = background_subtraction(os.path.join(path, filename), radius2, height2)
        plot_summary(backSub, filename, path)
        save_output(backSub, filename, path)
        image_SNAP = backSub['hdome']
        mask2 = segmentation_snap(backSub, filename, path, minSize2)
        labeled_image2= label_image_roi(mask, mask2)
        props_FA = measure_features(labeled_image2, image_FA, filename, path)
        props_snap = measure_features(labeled_image2, image_SNAP, filename, path)
        props_FA.to_csv(path+'FA_props.csv')
        props_snap.to_csv(path+'snap_props'+'.csv')
        linePlots_FA = linePlot(labeled_image2, image_FA)
        linePlots_SNAP = linePlot(labeled_image2,  image_SNAP)
        linePlots_FA.to_csv(path+'FA_linePlots.csv')
        linePlots_SNAP.to_csv(path+'snap_linePlots.csv')
    #if i > 10:
    #    break    


#process channel 2 (SNAP lableing) background subtraction
#save background subtracted image
#perform segmentation on image
#return binary image (as bool)

#path = '/Users/southk/dataAnalysis/Focal Adhesion Analysis/2014.6 pax with all processed/RAW'
#
#pattern = '*c2_ORG.tif'
#radius = 2
#height = 0.95
#i = 0
#minSize = 200
#
#for (path, dirs, files) in os.walk(path):
#    i += 1
#    for filename in fnmatch.filter(files, pattern):
#        print filename
#        backSub = background_subtraction(os.path.join(path, filename), radius, height)
#        plot_summary(backSub, filename, path)
#        save_output(backSub, filename, path)
#        mask = segmentation_snap(backSub, filename, path, minSize)
#    if i > 10:
#        break    