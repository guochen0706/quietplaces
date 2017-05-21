# TODO: Chen - crack open the file and add watson features.
import pickle
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

# Reading data back


fileObject = open('data/aggregated_api_data.json', 'r')
# load the object from the file into var b
results_in = pickle.load(fileObject)



# print '====  AGGREGATED DATA ======'
# for datum in data:
#     print datum

dataframe = json_normalize(results_in)
print dataframe.head()

# Do some work and augment the data...

results = []

outfile = open('data/aggregated_api_data_watson_enriched.json', 'w')
pickle.dump(results, outfile)
outfile.close()