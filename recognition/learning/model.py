"""
This module provides different models to predict chords. These
models use single frame vectors as features, predicting a chord
for a frame from a vector of features.

"""
import itertools

import numpy as np
import sklearn.svm
import sklearn.linear_model
import sklearn.lda
import sklearn.hmm
import pickle

class SKModel(object):
    def __init__(self, skclass, **params):
        """
        Initializes scikit learn model with given parameters.

        """
        self.skmodel = skclass(**params)

    def fit(self, frames, labels, **kwargs):
        """
        Fits the model to data.

        """
        self.skmodel.fit(frames, labels, **kwargs)

    def predict(self, frames):
        """
        Predicts outputs for model.

        """
        return self.skmodel.predict(frames)

    def score(self, frames, labels):
        """
        Returns mean accuracy of predictions on frames.

        """
        return self.skmodel.score(frames, labels)

    def save(self, name):
        """
        Pickle dumps the model

        """
        pickle.dump(self, open("./trainedModels/" + name, "w+"));

class SVM(SKModel):
    """
    Usage Example: SVM(C=1, gamma = 0)

    """
    def __init__(self, **params):
        super(SVM, self).__init__(sklearn.svm.SVC, **params)

class Softmax(SKModel):
    """
    Usage Example: Softmax(tol=0.01)

    """
    def __init__(self, **params):
        super(Softmax, self).__init__(sklearn.linear_model.LogisticRegression,
                                      **params)
    def probs(self, frames):
        """
        Returns the probability of the sample for each class in the model
        [n_samples, n_classes]

        """
        return self.skmodel.predict_proba(frames) 

class LDA(SKModel):
    """
    Gaussian.

    """
    def __init__(self, **params):
        super(LDA, self).__init__(sklearn.lda.LDA, **params)

    def probs(self, frames):
        return self.skmodel.predict_proba(frames)

    def get_means(self):
        return self.skmodel.means_

    def get_covar(self):
        return self.skmodel.covariance_

class HMMGaussian(SKModel):
    """
    HMM Gaussian Model

    """
    def __init__(self, model = None, **params):
        if model is None:
            model = LDA()
        self.model = model

    def fit(self, frames, labels):
        # train LDA for means, covariance.
        self.model.fit(frames, labels, store_covariance = True)
        means = self.model.get_means()
        #force this to be a diagonal matrix later
        covar = self.model.get_covar()
        #covar = np.tied(covar, np.identity(covar.shape[0]))
        n_components = len(np.unique(labels))
        #transmat = np.zeros([n_components, n_components]) + 1.0/n_components
        transmat = np.identity(n_components);
        params = {'n_components' : n_components,
                  'startprob' : [1.0/n_components] * n_components,
                  'transmat' : transmat,
                  'covariance_type': 'tied',
                  'algorithm': 'viterbi',
                  #'means_prior': means,
                  #'covars_prior': list(itertools.repeat(covar, n_components)),
                  'params' : ''
        }
        self.skmodel = sklearn.hmm.GaussianHMM(**params)
        # set means, covariances
        self.skmodel.means_ = means
        #print means
        #full - 96.6
        #self.skmodel.covars_ = np.array(list(itertools.repeat(covar, n_components)))
        #tied - 96.6
        self.skmodel.covars_ = covar
        #diag 94.9
        #self.skmodel.covars_ = np.array([np.diag(covar)]* n_components)
        #spherical - 91.5
        #self.skmodel.covars_ = (np.ones(n_components) * np.mean(np.diag(covar))).reshape(-1, 1)
