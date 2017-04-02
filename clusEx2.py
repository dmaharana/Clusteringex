#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 22:15:55 2017

@author: titu
"""
import os
import nltk.stem
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


class StemmedTfidfVectorizer(TfidfVectorizer):
      def build_analyzer(self):
          analyzer = super(TfidfVectorizer, self).build_analyzer()
          english_stemmer = nltk.stem.SnowballStemmer('english')
          return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

DIRtrain = '/home/titu/Documents/pyworkspace/Clusteringex/20news-bydate-train'
DIRtest = '/home/titu/Documents/pyworkspace/Clusteringex/20news-bydate-test'
groups = ['comp.graphics', 'comp.os.ms-windows.misc',
'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware',
'comp.windows.x', 'sci.space']

train_data = []
test_data = []
for category in groups:
    DIR = os.path.join(DIRtrain, category)
    train_data += [open(os.path.join(DIR, f), 'r', encoding='utf-8', errors='ignore').read() for f in os.listdir(DIR)]

    '''
    DIR = os.path.join(DIRtest, category)
    test_data += [open(os.path.join(DIR, f), 'r', encoding='utf-8', errors='ignore').read() for f in os.listdir(DIR)]

print(len(train_data), len(test_data))
'''
vectorizer = StemmedTfidfVectorizer(min_df=10, max_df=0.5,
stop_words='english', decode_error='ignore')
vectorized = vectorizer.fit_transform(train_data)
num_samples, num_features = vectorized.shape
print("#samples: %d, #features: %d" % (num_samples,num_features))

num_clusters = 50

km = KMeans(n_clusters=num_clusters, init='random', n_init=1,
verbose=1, random_state=3)
km.fit(vectorized)
print(km.labels_)
print(km.labels_.shape)