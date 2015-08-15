import os
import fnmatch
from backgroundSubtraction import background_subtraction

path = '/Users/southk/dataAnalysis/Focal Adhesion Analysis/2014.6 pax with all processed/RAW'

#process channel 1 (paxcillin)
i = 0
pattern = '*c1_ORG.tif'
radius = 2
height = 0.9
for (path, dirs, files) in os.walk(path):
    for filename in fnmatch.filter(files, pattern):
        print filename
        background_subtraction(os.path.join(path, filename), radius, height)
        i += 1
    if i > 4:
        break
