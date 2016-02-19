import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import os
import fnmatch

path = '/Users/southk/Desktop/Dll4 activation 5uM DAPT'

pattern = '*.xls'

frame = pd.DataFrame()


read_excel('path_to_file.xls', sheetname='Sheet1')

for (path, dirs, files) in os.walk(path):
    for filename in fnmatch.filter(files, pattern):
        df = pd.read_xls(filename,index_col=None, header=0)
        list_.append(df)

frame = pd.concat(list_)