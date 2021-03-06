#!usr/bin/env python
#coding:utf-8

'''
Paper: Prem Gopalan, Francisco J.R. Ruiz, et al. Bayesian Non-parameter Poisson Factorization for Recommendation Systems
github: https://github.com/premgopalan/hgaprec/tree/master/src

Author: Haidong Zhang
Date: April 16, 2016
'''

from GraphicalRecommender import Recommender
import numpy as np
from numpy import log, sqrt
from scipy.sparse import dok_matrix
from util import normalize
from util import Logger

THRESHOLD = 1e-30

class BNPoissMF(Recommender):
    def __init__(self, trainMatrix, testMatrix, configHandler):
        Recommender.__init__(trainMatrix, testMatrix, configHandler)
        self.logger = Logger('BNPoissMF.log')


    def initModel(self):
        ''' Read the model parameters, and get some common values.
        '''
        self.numUsers, self.numItems = self.trainMatrix.shape()
        self.prediction = dok_matrix((self.numUsers, self.numItems))
        self.MAX_Iterations = int(self.configHandler.getParameter('BPoissMF', 'MAX_Iterations'))
        self.numFactors = int(self.configHandler.getParameter('BPoissMF', 'numFactors'))
        self.threshold = float(self.configHandler.getParameter('BPoissMF', 'threshold'))

        # Get the Parameters
        self.user_alpha = float(self.configHandler.getParameter('BPoissMF', 'user_alpha'))
        self.user_c = float(self.configHandler.getParameter('BPoissMF', 'user_c'))

        self.item_a = float(self.configHandler.getParameter('BPoissMF', 'item_a'))
        self.item_b = float(self.configHandler.getParameter('BPoissMF', 'item_b'))

        # The model parameters for users
        self.gamma0 = np.zeros(self.numUsers)
        self.gamma1 = np.zeros(self.numUsers)
        self.s = np.zeros(self.numUsers)
        self.nu = np.zeros((self.numUsers, self.numFactors))
        self.theta = np.zeros((self.numUsers, self.numFactors))

        # The model parameters for stick proportions
        self.tau = np.zeros((self.numUsers, self.numFactors))

        # The model parameters for item weights
        self.lambda0 = np.zeros((self.numItems, self.numFactors))
        self.lambda1 = np.zeros((self.numItems, self.numFactors))
        self.beta = np.zeros((self.numItems, self.numFactors))

        self.z = np.zeros((self.numUsers, self.numItems))

        self.pi = np.zeros((self.numUsers, self.numItems))
        self.logPi = np.zeros((self.numUsers, self.numItems))


    def buildModels(self):
        pass

    def initUserScalingParameters(self):
        ''' initial equations for the user scaling parameters gamma_u0 and gamma_u1

        '''




    def initStickProportions(self):
        ''' The update equations for the stick proportions tau_uk can be obtained by taking the derivative of the objective function with respect to tau_uk

        '''
        self.nu = 0.001 * np.random.random((self.numUsers, self.numFactors))


    def computePi(self):
        ''' Equation (10)

        '''



    def initItemWeights(self):
        pass

    def updateUserScalingParameters(self):
        pass

    def updateStickProportions(self):
        pass

    def updateItemWeights(self):
        pass

    def calculateConjugacy(self):
        pass

    def GammaPoisson(self):
        pass

    def solveQuadratic(self, a, b, c):
        '''
        '''
        s1 = (-b + sqrt(b*b - 4*a*c)) / (2*a)
        s2 = (-b - sqrt(b*b - 4*a*c)) / (2*a)

        if s1 > .0 and s1 <= 1.0 and s2 > .0 and s2 <= 1.0:
            self.logger.error('s1 %f and s2 %f are out of range in solve_quadratic()' % (s1, s2))
            self.logger.error('a = %.5f, b = %.5f, c = %.5f\n' % (a, b, c))

            if s1 < s2:
                return s1 + THRESHOLD
            else:
                return s2 + THRESHOLD

        if s1 > .0 and s1 <= 1.0:
            return s1

        if s2 > .0 and s1 <= 1.0:
            return s2

        if np.abs(s1 - .0) < THRESHOLD:
            return THRESHOLD

        if np.abs(1.0 - s1) < THRESHOLD:
            return 1.0 - THRESHOLD

        if np.abs(s2 - .0) < THRESHOLD:
            return THRESHOLD

        if np.abs(s2 - 1.0) < THRESHOLD:
            return 1.0 - THRESHOLD

        self.logger.error('WARNING: s1 %.10f and s2 %.10f are out of range in solve_quadratic()' % (s1, s2))
        return s1

if __name__ == '__main__':
    bnprec = BNPoissMF()