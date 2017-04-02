#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 00:20:35 2017

@author: titu
"""

import os
import nltk.stem
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import defaultdict

class StemmedTfidfVectorizer(TfidfVectorizer):
      def build_analyzer(self):
          analyzer = super(TfidfVectorizer, self).build_analyzer()
          english_stemmer = nltk.stem.SnowballStemmer('english')
          return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

DIR = '/home/titu/Documents/pyworkspace/data/clusteringex'
posts = [open(os.path.join(DIR, f)).read() for f in os.listdir(DIR)]

vectorizer = StemmedTfidfVectorizer(min_df=1, stop_words='english', decode_error='ignore')


vectorized = vectorizer.fit_transform(posts)
num_samples, num_features = vectorized.shape

print(vectorizer.get_feature_names())
print(vectorized.toarray().transpose())
print(vectorized.shape)


print("#samples: %d, #features: %d" % (num_samples,num_features))

num_clusters = 3

km = KMeans(n_clusters=num_clusters, init='random', n_init=1, verbose=1, random_state=3)
km.fit(vectorized)
print(km.labels_)
print(km.labels_.shape)


postClustIdx = defaultdict(list)

for idx in range(km.labels_.shape[0]):
    postClustIdx[int(km.labels_[idx])].append([posts[idx]])

for clustId in postClustIdx:
    print('Cluster: {}, Text: {}'.format(clustId, postClustIdx[clustId]))