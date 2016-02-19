import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path ='/Users/southk/dataAnalysis/Focal Adhesion Analysis/2014.6 pax with all processed/RAW/SG4' # use your path
allFiles = glob.glob(path + "/*snap_linePlots.csv")
frame = pd.DataFrame()
list_ = []
count = 0

for file_ in allFiles:
    df = pd.read_csv(file_,index_col= 0, header=0)
    df.loc[:, 'cell'] = pd.Series(([count]* len(df.index)), index = df.index)
    list_.append(df)
    count += 1
frame = pd.concat(list_)

#group by index
grouped = frame.groupby(level = 0)

#mean intensity at each index (x) value with stats
meanI = grouped['Intensity'].agg([np.mean, np.std, len])
meanI.index.names = ['x']

meanI.to_csv(path+'concatSnap.csv')