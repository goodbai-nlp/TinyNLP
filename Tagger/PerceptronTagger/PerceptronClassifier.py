#!/usr/bin/env python
# encoding: utf-8
"""
@version: V1.2
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: assignment2.py
@time: 16-7-7 下午8:44
"""
from __future__ import print_function
from copy import copy
import time

class PerceptronClassifier(object):
    # The perceptron classifier
    def __init__(self, max_iter=10, training_data=None, devel_data=None):
        '''
        Parameters
        ----------
        max_iter: int
            The max number of iteration
        training_data: list
            The training data
        devel_data: list
            The development data, to determine the best iteration.
        '''
        self.max_iter = max_iter
        self.learnRate = 1
        if training_data is not None:
            self.fit(training_data, devel_data)

    def fit(self, training_data, devel_data=None):
        '''
        Estimate the parameters for perceptron model. For multi-class perceptron, parameters can be
        treated as a T \times D matrix W, where T is the number of labels and D is the number of
        features.
        '''
        # feature_alphabet is a mapping from feature string to it's dimension in the feature space,
        # e.g. feature_alphabet['U1=I']=3, which means 'U1=I' is in the third column of W
        #
        # W = [[ . . 1 . . .],
        #      ...
        #      [ . . 1 . . .]]
        #            ^
        #            |
        #         'U1=I'
        self.feature_alphabet = {'None': 0}
        self.label_alphabet = {}

        # Extract features, build the feature_alphabet, label_alphabet and training instance pairs.
        # Each instance consist a tuple (X, Y) where X is the mapped features (list(int)), and Y is
        # the index of the corresponding label.
        instances = []
        for words, tags in training_data:
            L = len(words)
            prev = '<s>'
            for i in range(L):
                # Your code here, extract features and give it into X, convert POStag to index and
                # give it to Y
                X = self.extract_features(words, i, prev)
                Y = len(self.label_alphabet) if tags[i] not in self.label_alphabet.keys() else self.label_alphabet[tags[i]]
                instances.append((X, Y))
                if tags[i] not in self.label_alphabet.keys():
                    self.label_alphabet[tags[i]] = len(self.label_alphabet)
                prev = tags[i]

        # Build a mapping from index to label string to recover POStags.
        self.labels = [-1 for k in self.label_alphabet]
        for k in self.label_alphabet:
            self.labels[self.label_alphabet[k]] = k

        self.D, self.T = len(self.feature_alphabet), len(self.label_alphabet)
        print('number of features : %d' % self.D)
        print('number of labels: %d' % self.T)

        # Allocate the weight matrix W
        self.W = [[0 for j in range(self.D)] for i in range(self.T)]
        self.best_W = copy(self.W)
        best_acc = 0

        for it in range(self.max_iter):
            # The training part,
            n_errors = 0
            print('training iteration #%d' % it)
            for X, Y in instances:
                # Your code here, ake a prediction and give it to Z
                Z = self._predict(X)

                if Z != Y:
                    # print '初始预测：', Z, self._score(X, Z), 'Y的分数', self._score(X, Y)
                    # print self.W[Y]
                    tmp = self._score(X,Y)
                    # Your code here. If the predict is incorrect, perform the perceptron update

                    n_errors += 1
                    for x in X:
                        self.W[Y][x] =self.W[Y][x] + 1*self.learnRate
                # The perceptron update part.
                    for i in range(self.T):
                        if self._score(X, i) >= tmp and i!=Y:
                            for x in X:
                                self.W[i][x] = self.W[i][x] - 1 * self.learnRate
                    # print '调整后：',self._predict(X),'正确：',Y,'Y的分数',self._score(X,Y)
            print('training error %d' % n_errors)

            if devel_data is not None:
                # Test accuracy on the development set if provided.
                n_corr, n_total = 0, 0
                for words, tags in devel_data:
                    prev = '<s>'
                    for i in range(len(words)):
                        Z = self.predict(words, i, prev)
                        Y = self.label_alphabet[tags[i]]
                        if Z == Y:
                            n_corr += 1
                        n_total += 1
                        prev = self.labels[Z]
                print('accuracy: %f' % (float(n_corr) / n_total))
                # print 'W0',self.W[10][:100]
                if best_acc < float(n_corr) / n_total:
                    # If this round is better than before, save it.
                    best_acc = float(n_corr) / n_total
                    self.best_W = copy(self.W)

        if self.best_W is None:
            self.best_W = copy(self.W)

    def extract_features(self, words, i, prev_tag=None, add=True):
        '''
        Extract features from words and prev POS tag, if `add` is True, also insert the feature
        string to the feature_alphabet.

        Parameters
        ----------
        words: list(str)
            The words list
        i: int
            The position
        prev_tag: str
            Previous POS tag
        add: bool
            If true, insert the feature to feature_alphabet.

        Return
        ------
        mapped_features: list(int)
            The list of hashed features.
        '''
        L = len(words)
        context = ['<s>' if i - 2 < 0 else words[i - 2],
                   '<s>' if i - 1 < 0 else words[i - 1],
                   words[i],
                   '<e>' if i + 1 >= L else words[i + 1],
                   '<e>' if i + 2 >= L else words[i + 1]]
        raw_features = ['U1=%s' % context[0],
                        'U2=%s' % context[1],
                        'U3=%s' % context[2],
                        'U4=%s' % context[3],
                        'U5=%s' % context[4],
                        'U1,2=%s/%s' % (context[0], context[1]),
                        'U2,3=%s/%s' % (context[1], context[2]),  # Your code here, extract the bigram raw feature,
                        'U3,4=%s/%s' % (context[2], context[3]), # Your code here, extract the bigram raw feature,
                        'U4,5=%s/%s' % (context[3], context[4]),  # Your code here, extract the bigram raw feature,
                        ]

        if prev_tag is not None:
            raw_features.append('B=%s' % prev_tag)

        mapped_features = []
        for f in raw_features:
            if add and (f not in self.feature_alphabet):
                # Your code here, insert the feature string to the feature_alphabet.
                index = len(self.feature_alphabet)
                self.feature_alphabet[f] = index
            # Your code here, map the string feature to index.
            # for item in self.feature_alphabet.values():
            #     mapped_features[self.feature_alphabet[item]] = 1
            if f in self.feature_alphabet:
                mapped_features.append(self.feature_alphabet[f])
        return mapped_features

    def _score(self, features, t):
        '''
        Calcuate score from the given features and label t

        Parameters
        ----------
        features: list(int)
            The hashed features
        t: int
            The index of label

        Return
        ------
        s: int
            The score
        '''
        # Your code here, compute the score.
        s=0.0
        for x in features:
            s += self.W[t][x]
        return s

    def _predict(self, features):
        '''
        Calcuate score from the given features and label t

        Parameters
        ----------
        features: list(int)
            The hashed features
        t: int
            The index of label

        Return
        ------
        best_y: int
            The highest scored label's index
        '''
        pred_scores = [self._score(features, y) for y in range(self.T)]
        best_score, best_y = -1e5, -1
        # Your code here, find the highest scored class from pred_scores
        # best_score  = pred_scores[0]
        # best_y  = 0
        for index,value in enumerate(pred_scores):
            if value > best_score:
                best_score = value
                best_y = index

        # print 'best:',best_score,best_y
        # print max([math.fabs(sc - 10) for sc in pred_scores])
        return best_y

    def predict(self, words, i, prev_tag=None):
        '''
        Make prediction on list of words

        Parameters
        ----------
        words: list(str)
            The words list
        i: int
            The position
        prev_tag: str
            Previous POS tag

        Return
        ------
        y: int
            The predicted label's index
        '''
        X = self.extract_features(words, i, prev_tag, False)
        y = self._predict(X)
        return y


def greedy_search(words, classifier):
    '''
    Perform greedy search on the classifier.

    Parameters
    ----------
    words: list(str)
        The word list
    classifier: PerceptronClassifier
        The classifier object.
    '''
    prev = '<s>'
    ret = []
    for i in range(len(words)):
        # Your code here, implement the greedy search,
        label = classifier.predict(words,i,prev)
        ret.append(classifier.labels[label])
        prev = classifier.labels[label]
    return ret

from dataset import read_dataset
print (time.strftime('%Y-%m-%d %H:%M:%S'))
train_dataset = read_dataset('./penn.train.pos.gz')
devel_dataset = read_dataset('./penn.devel.pos.gz')

print('%d is training sentences.' % len(train_dataset))
print('%d is development sentences.' % len(devel_dataset))

perceptron = PerceptronClassifier(max_iter=1, training_data=train_dataset, devel_data=devel_dataset)

print('========================TEST CASE1==========================')
n_corr, n_total = 0, 0
for devel_data in devel_dataset:
    devel_data_x, devel_data_y = devel_data
    pred_y = greedy_search(devel_data_x, perceptron)
    for pred_tag, corr_tag in zip(pred_y, devel_data_y):
        if pred_tag == corr_tag:
            n_corr += 1
        n_total += 1
print("accuracy: %f" % (float(n_corr)/ n_total))

print('========================TEST CASE2==========================')

print (greedy_search(['HMM', 'is', 'a', 'widely', 'used', 'model', '.'], perceptron))
print (greedy_search(['I', 'like', 'cat', ',', 'but', 'I', 'hate', 'eating', 'fish', '.'], perceptron))

print('========================TEST CASE3==========================')
test_dataset = read_dataset('./penn.test.pos.blind.gz')

fpo=open('./penn.test.perceptron.pos.out', 'w')

for test_data_x, test_data_y in test_dataset:
    pred_y = greedy_search(test_data_x, perceptron)
    print(" ".join(y for y in pred_y), file=fpo)
fpo.close()
print('Mission complete!')
print (time.strftime('%Y-%m-%d %H:%M:%S'))