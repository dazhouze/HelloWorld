#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class Perceptron(object):
    '''Rerceptron classifier.

    Parameters
    ----------
    eta: float
        Learing rate (between 0.0 and 1.0)
    n_iter: int
        Passes over the traing dataset.

    Attributes
    ----------
    __w : 1d-array
        Weights after fitting.
    __errors: list
        Number of misclassifiation in every epoch.
    '''
    def __init__(self, eta=0.01, n_iter=10):
        self.__eta = eta
        self.__n_iter = n_iter

    '''
    def get_eta(self):
        return self.__eta

    def get_n_iter(self):
        return self.__n_iter
    '''

    def fit(self, X, y):
        '''Fit training data.

        Parameters
        ----------
        X: {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number
            of samples and n_feature is the number of features.
        y: array-like, shape = [n_samples]
            Target values.

        Returns
        ----------
        self: object
        '''
        self.__w = np.zeros(1 + X.shape[1]) # weigth number is features + 1
        self.__errors = []

        for i in range(0, self.__n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.__eta * (target - self.predict(xi))
                self.__w[1:] += update * xi
                self.__w[0] += update
                errors += int(update != 0.0)
            self.__errors.append(errors)
        return self

    def net_input(self, X):
        '''Calculate net input.'''
        return np.dot(X, self.__w[1:]) + self.__w[0]
    
    def predict(self, X):
        '''Return class label after unit step.'''
        return np.where(self.__net_input(X) >= 0.0, 1, -1)
