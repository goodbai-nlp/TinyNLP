#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: config.py
@time: 16-9-1 上午10:48
"""

import os

BASE_PATH = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])


class Config(object):
    PKU_TRAIN = os.path.join(BASE_PATH, 'data/icwb2-data/training/pku_training.utf8')
    MSR_TRAIN = os.path.join(BASE_PATH,'data/icwb2-data/training/msr_training.utf8')
    PKU_TEST = os.path.join(BASE_PATH,'data/icwb2-data/testing/pku_test.utf8')
    MSR_TEST = os.path.join(BASE_PATH,'data/icwb2-data/testing/msr_test.utf8')
    PKU_VOCAB = os.path.join(BASE_PATH,'data/icwb2-data/gold/pku_training_words.utf8')
    MSR_VOCAB = os.path.join(BASE_PATH,'data/icwb2-data/gold/msr_training_words.utf8')
    PKU_ANS = os.path.join(BASE_PATH,'data/icwb2-data/gold/pku_test_gold.utf8')
    MSR_ANS = os.path.join(BASE_PATH,'data/icwb2-data/gold/msr_test_gold.utf8')
    