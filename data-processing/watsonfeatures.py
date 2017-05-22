# TODO: Chen - crack open the file and add watson features.
import pickle
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation
from watson_developer_cloud import ToneAnalyzerV3
import json
import matplotlib.pyplot as plt
from watson_developer_cloud import WatsonException

# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

# Reading data back

fileObject = open('data/aggregated_api_data_keyword_filtered_reviews.pkl', 'r')
# load the object from the file into var b
results_in = pickle.load(fileObject)

# print '====  AGGREGATED DATA ======'
# for datum in data:
#     print datum

df = json_normalize(results_in)
df['total_noise_words']=[0,2,1,1,3,0,2,0,0,0,2,2,2,5,0,0,1,0,0,0,2,0,2,0,1,0] #This is calculated from your output which are cumulative numbers


def calculate_emotion_score(dict):
    total = dict['anger']+dict['sadness']+dict['digust']+dict['fear'] # Remove Joy from emotions
    emotion_score = dict['anger']/total*0.4+dict['sadness']/total*0.3+dict['digust']/total*0.2+dict['fear']/total*0.1
    return emotion_score


fileObject = open('data/aggregated_api_data_all_reviews.pkl', 'r')
# load the object from the file into var b
results_in = pickle.load(fileObject)

# print '====  AGGREGATED DATA ======'
# for datum in data:
#     print datum

df = json_normalize(results_in)
df['total_noise_words']=[0,2,1,1,3,0,2,0,0,0,2,2,2,5,0,0,1,0,0,0,2,0,2,0,1,0]

#print df.columns.to_series().groupby(df.dtypes).groups





# Do some work and augment the data...
# Put all the reviews from google and fs in a dictionary 
# The dict looks like: {'hotel1': ['review1', 'review2', ...], 'hotel2': [...], ...}
dict = {}
hotels = df['name']
for i in range(df.shape[0]):
    google_reviews=df.ix[i,:]['all_google_reviews']
    fs_reviews=df.ix[i,:]['fs_reviews_to_check']
    data = {} 
    data['reviews']=[]
    if len(google_reviews)>0:
        for j in google_reviews:
            data['reviews'].append(j['text'])
    if len(fs_reviews)>0:
        for j in fs_reviews:
            data['reviews'].append(j)
    dict[hotels[i]]=data


tone_analyzer = ToneAnalyzerV3(username="92bc6426-b874-4f43-85ea-206dff3d9f22", 
                               password="s4RmTq2XEkyP", 
                               version='2016-05-19')

# Use tone analyzer to catch tones of reviews for each hotel
# For each hotel, find average score of each tone from all the reviews for that hotel  
avg_tones = []
for key in dict.keys():
    avg_tone = []
    anger = []
    digust = []
    fear = []
    joy = []
    sadness = []
    for text in dict[key]['reviews']:
        try:
            tone = tone_analyzer.tone(text)['document_tone']['tone_categories'][0]
            anger.append(tone['tones'][0]['score'])
            digust.append(tone['tones'][1]['score'])
            fear.append(tone['tones'][2]['score'])
            joy.append(tone['tones'][3]['score'])
            sadness.append(tone['tones'][4]['score'])
        except WatsonException:
            avg_tone = {'anger':0, 'digust':0, 'fear':0, 'joy':0, 'sadness': 0}
    avg_tone = {'anger': np.mean(anger), 'digust':np.mean(digust), 'fear':np.mean(fear), 'joy':np.mean(joy), 'sadness': np.mean(sadness)}
    print avg_tone 
    avg_tones.append(avg_tone)
	

#avg_tones=pd.DataFrame(avg_tones)
#avg_tones.set_index = df.name
#avg_tones.to_csv('avg_tones.csv')	


# Calculate the noisy score using the formula: 
# noisy_score = [1 - 1 / (1 + emotion_score*count_of_noise_words)] * 100
scores = []
for i in range(df.shape[0]):
    noise_word_count=df.ix[i,'total_noise_words']
    if noise_word_count>0:
        emotion=calculate_noise_score(avg_tones[i])
        param = emotion*noise_word_count
        score = 100 * (1-1/(1+param))
        scores.append(score)
    if noise_word_count==0:
        scores.append(0)
df['scores'] = scores


# Output the data
df = df.to_dict('records')
outfile = open('data/aggregated_api_data_watson_enriched.pkl', 'w')
pickle.dump(df, outfile)
outfile.close()