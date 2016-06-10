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
