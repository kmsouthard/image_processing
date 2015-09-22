import os
import fnmatch
from backgroundSubtraction import background_subtraction
from backgroundSubtraction import plot_summary
from backgroundSubtraction import save_output
from backgroundSubtraction import segmentation

path = '/Users/southk/dataAnalysis/Focal Adhesion Analysis/2014.6 pax with all processed/RAW'

#process channel 1 (paxcillin)

pattern = '*c1_ORG.tif'
radius = 2
height = 0.75
i = 0

for (path, dirs, files) in os.walk(path):
    i += 1
    for filename in fnmatch.filter(files, pattern):
        print filename
        backSub = background_subtraction(os.path.join(path, filename), radius, height)
        plot_summary(backSub, filename, path)
        save_output(backSub, filename, path)
        #segmentation(backSub, filename, path)
    if i > 2:
        break    
