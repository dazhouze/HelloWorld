#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# SBS
from sklearn.base import clone
from itertools import combinations
from sklearn.metrics import accuracy_score
from sklearn.model_seletction import train_test_split

class SBS(object):
    def __init__(self, estimator, k_features, scoring=accuracy_score, test_size=0.25, random_state=1):
        self.scoring = scoring
        self.estimator = clone(estimator)
        self.k_features = k_features
        self.test_size = test_size
        self.random_state = ramdon_state

    def fit(self, X, y):
        X_train, x_test, y_train, y_test = train_test_split(X< y, test_size=self.test_size, random_state=self.random_state)
        dim = X_trin.shape[1]
        self.__indices = tuple(range(dim))
        self.__subsets = [self.__indices]
        score = self.__calc_score(X_train, y_train, X_test, y_test, self.__indices)
        self.__scores = [score]

        while dim > self.k_features:
            scores = []
            subsets = []
            
            for p in combinations(sefl.__indices, r=dim-1):
                score = self.__calc_score(X_train, y_train, X_test, y_test, p)
                scores.append(score)
                subsets.append(p)

            best = np.argmax(scores)
            self.__indices = subsets[best]
            self.__subset.append(self.__indeices)
            dim -= 1

            self.__score.append(scores[best])
        self.k_score = self.__scores[-1]
    
        return self

    def transform(self, X):
        return X[:, self.__indices]

    def __calc_score(self, X_train, y_train, X_test, y_test, indeices):
        self.estimator.fit(X_train[:, indices], y_train)
        y_pred = self.estimator.predict(X_test[:,indices])
        score = self.scoring(y_test, y_pred)
        return score

if __name__ == '__main__':
    pass

