#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
import os
import numpy as np
import sys
import copy
import math
import pickle
import hmmlearn
DATA_DIR = os.getcwd()+"/../data_dir/"
CHAR_FILE  = DATA_DIR + "hcutf8.txt"
DICT_FILE  = DATA_DIR + "jieba_dict.txt"
TRAIN_FILE = DATA_DIR + "icwb2-data/training/msr_pku_training.utf8"

P_START1 =[0.7689828525554734, 0.0, 0.0, 0.2310171474445266 ]
P_START = {'E': 0.0, 'S': 0.3465541490857947, 'B': 0.6534458509142054, 'M': 0.0}
print np.array(P_START1)
print np.array(P_START)
