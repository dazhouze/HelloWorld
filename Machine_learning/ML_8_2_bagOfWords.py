#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import os

def preprocessor(text):
	text = re.sub('<[^>]*>', '', text)
	enoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
	text = (re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', ''))
	return text

def tokenizer(text):
	return text.split()

if __name__ == '__main__':
	from sklearn.feature_extraction.text import CountVectorizer
	count = CountVectorizer()
	docs = np.array(['The sun is shining', 'The weather is sweet', 'The sun is shining and the weather is sweet, and one and one is two'])
	bag = count.fit_transform(docs)
	print(count.vocabulary_)
	print(docs)
	print(bag.toarray())
	from sklearn.feature_extraction.text import TfidfTransformer
	tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)
	np.set_printoptions(precision=2)
	print(tfidf.fit_transform(count.fit_transform(docs)).toarray())
