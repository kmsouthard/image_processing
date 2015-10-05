import os
import fnmatch
from backgroundSubtraction import background_subtraction
from backgroundSubtraction import plot_summary
from backgroundSubtraction import save_output
from backgroundSubtraction import segmentation_FA
from backgroundSubtraction import segmentation_snap

path = '/Users/southk/dataAnalysis/Focal Adhesion Analysis/2014.6 pax with all processed/RAW'

#process channel 1 (paxcillin) background subtraction
#save background subtracted image
#perform segmentation on image
#return binary image (as bool)

pattern = '*c1_ORG.tif'
radius = 2
height = 0.6
i = 0
minSize = 15

for (path, dirs, files) in os.walk(path):
    i += 1
    for filename in fnmatch.filter(files, pattern):
        print filename
        backSub = background_subtraction(os.path.join(path, filename), radius, height)
        plot_summary(backSub, filename, path)
        save_output(backSub, filename, path)
        mask = segmentation_FA(backSub, filename, path, minSize)
    if i > 10:
        break    


#process channel 2 (SNAP lableing) background subtraction
#save background subtracted image
#perform segmentation on image
#return binary image (as bool)

path = '/Users/southk/dataAnalysis/Focal Adhesion Analysis/2014.6 pax with all processed/RAW'

pattern = '*c2_ORG.tif'
radius = 2
height = 0.95
i = 0
minSize = 200

for (path, dirs, files) in os.walk(path):
    i += 1
    for filename in fnmatch.filter(files, pattern):
        print filename
        backSub = background_subtraction(os.path.join(path, filename), radius, height)
        plot_summary(backSub, filename, path)
        save_output(backSub, filename, path)
        mask = segmentation_snap(backSub, filename, path, minSize)
    if i > 10:
        break    